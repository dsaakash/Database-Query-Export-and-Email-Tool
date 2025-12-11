"""Email service for sending reports via SMTP."""

import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List

import pandas as pd

from src.services.export_service import ExcelExportService


class EmailService:
    """Service for sending emails with report attachments."""

    def __init__(
        self,
        smtp_user: str,
        smtp_password: str,
        smtp_host: str = "smtp.gmail.com",
        smtp_port: int = 587,
    ):
        """Initialize email service.

        Args:
            smtp_user: SMTP username (Gmail email)
            smtp_password: SMTP password (Gmail app password)
            smtp_host: SMTP server host
            smtp_port: SMTP server port
        """
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def _convert_to_html(self, df: pd.DataFrame) -> str:
        """Convert DataFrame to HTML table.

        Args:
            df: pandas DataFrame to convert

        Returns:
            HTML string with styled table
        """
        html_body = df.to_html(index=False, classes='table table-striped', table_id='data-table')
        
        styled_html = f"""
        <html>
        <head>
            <style>
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #4472C4;
                    color: white;
                    font-weight: bold;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                tr:hover {{
                    background-color: #e8e8e8;
                }}
            </style>
        </head>
        <body>
            <h2>Database Report</h2>
            {html_body}
        </body>
        </html>
        """
        return styled_html

    def send_email(
        self,
        df: pd.DataFrame,
        recipients: List[str],
        subject: str,
        excel_file: str,
        pdf_file: str = None,
        cc_recipients: List[str] = None,
    ) -> None:
        """Send email with HTML body and Excel/PDF attachments.

        Args:
            df: pandas DataFrame for HTML body
            recipients: List of recipient email addresses (TO)
            subject: Email subject
            excel_file: Path to Excel file attachment
            pdf_file: Optional path to PDF file attachment
            cc_recipients: Optional list of CC recipient email addresses

        Raises:
            RuntimeError: If email sending fails
        """
        if not recipients:
            raise ValueError("At least one recipient email is required")

        try:
            html_body = self._convert_to_html(df)

            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_user
            msg['To'] = ', '.join(recipients)
            
            if cc_recipients and len(cc_recipients) > 0:
                msg['Cc'] = ', '.join(cc_recipients)

            # Add HTML body
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)

            # Add attachments
            attachments = []
            if excel_file and Path(excel_file).exists():
                with open(excel_file, 'rb') as f:
                    excel_attachment = MIMEApplication(f.read())
                    excel_attachment.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=Path(excel_file).name
                    )
                    msg.attach(excel_attachment)
                    attachments.append(Path(excel_file).name)

            if pdf_file and Path(pdf_file).exists():
                with open(pdf_file, 'rb') as f:
                    pdf_attachment = MIMEApplication(f.read())
                    pdf_attachment.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=Path(pdf_file).name
                    )
                    msg.attach(pdf_attachment)
                    attachments.append(Path(pdf_file).name)

            # Prepare recipient list (TO + CC)
            all_recipients = recipients.copy()
            if cc_recipients:
                all_recipients.extend(cc_recipients)

            # Connect to SMTP server with proper SSL/TLS handling
            print(f"   🔗 Connecting to SMTP server: {self.smtp_host}:{self.smtp_port}")
            
            try:
                if self.smtp_port == 465:
                    # Port 465: Use SSL/TLS
                    print(f"   Using SSL/TLS (port 465)...")
                    # Create unverified context to handle certificate issues
                    context = ssl._create_unverified_context()
                    server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context)
                else:
                    # Port 587: Use STARTTLS
                    print(f"   Using STARTTLS (port {self.smtp_port})...")
                    server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                    # Create unverified context to handle certificate issues
                    context = ssl._create_unverified_context()
                    server.starttls(context=context)
                
                # Login
                print(f"   Authenticating...")
                server.login(self.smtp_user, self.smtp_password)
                
                # Send email
                print(f"   Sending email...")
                server.send_message(msg, from_addr=self.smtp_user, to_addrs=all_recipients)
                server.quit()
                
            except smtplib.SMTPException as smtp_error:
                error_msg = str(smtp_error).lower()
                # Try alternative port if SSL error
                if "ssl" in error_msg or "wrong_version_number" in error_msg or "tls" in error_msg:
                    print(f"   ⚠ SSL/TLS issue detected, trying alternative port...")
                    server.quit() if 'server' in locals() else None
                    
                    # Try alternative port
                    alt_port = 465 if self.smtp_port == 587 else 587
                    print(f"   Trying port {alt_port}...")
                    
                    try:
                        if alt_port == 465:
                            context = ssl._create_unverified_context()
                            server = smtplib.SMTP_SSL(self.smtp_host, alt_port, context=context)
                        else:
                            server = smtplib.SMTP(self.smtp_host, alt_port)
                            context = ssl._create_unverified_context()
                            server.starttls(context=context)
                        
                        server.login(self.smtp_user, self.smtp_password)
                        server.send_message(msg, from_addr=self.smtp_user, to_addrs=all_recipients)
                        server.quit()
                        print(f"   ✓ Successfully sent using port {alt_port}")
                    except Exception as alt_error:
                        raise RuntimeError(
                            f"Failed to send email after trying both ports {self.smtp_port} and {alt_port}.\n"
                            f"Please check your SMTP settings in .env file.\n"
                            f"Original error: {str(smtp_error)}\n"
                            f"Alternative error: {str(alt_error)}"
                        ) from alt_error
                else:
                    raise

            # Print success message
            print(f"✓ Email sent successfully to: {', '.join(recipients)}")
            if cc_recipients:
                print(f"  CC: {', '.join(cc_recipients)}")
            if attachments:
                print(f"  Attachments: {', '.join(attachments)}")

        except Exception as e:
            error_msg = str(e).lower()
            
            # Provide specific error messages for common issues
            if "wrong_version_number" in error_msg or "ssl" in error_msg:
                troubleshooting = f"""
✗ SSL/TLS Configuration Error

💡 Troubleshooting:
   1. For Gmail/Outlook with port 587:
      - Use STARTTLS (not SSL)
      - Verify SMTP_PORT=587 in .env
      
   2. For Gmail/Outlook with port 465:
      - Use SSL/TLS
      - Verify SMTP_PORT=465 in .env
      - Update .env: SMTP_PORT=465
      
   3. Common fixes:
      - Try port 587 with STARTTLS (default)
      - Or try port 465 with SSL
      - Check firewall/proxy settings
      - Verify SMTP credentials
      
   4. Update your .env file:
      For port 587 (STARTTLS): SMTP_PORT=587
      For port 465 (SSL): SMTP_PORT=465
"""
                raise RuntimeError(f"Failed to send email: SSL/TLS configuration error.\n{troubleshooting}\nOriginal error: {str(e)}") from e
            elif "authentication" in error_msg or "invalid" in error_msg:
                raise RuntimeError(f"Failed to send email: Authentication failed. Please check your SMTP_USER and SMTP_PASSWORD in .env file.\nOriginal error: {str(e)}") from e
            elif "connection" in error_msg or "refused" in error_msg:
                raise RuntimeError(f"Failed to send email: Connection failed. Check your internet connection and SMTP settings.\nOriginal error: {str(e)}") from e
            else:
                raise RuntimeError(f"Failed to send email: {str(e)}") from e

