#!/usr/bin/env python3
"""
Email Configuration Test Script

Use this script to test your email setup before running the main application.
"""

import os
import smtplib
import ssl
import sys
from email.mime.text import MIMEText
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError as e:
    print(f"✗ Missing dependency: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)


def test_email_config():
    """Test email configuration from .env file."""
    
    # Load .env file
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print("✗ .env file not found!")
        print(f"  Expected location: {env_file}")
        print("\nPlease create .env file with:")
        print("  SMTP_USER=your_email@gmail.com")
        print("  SMTP_PASSWORD=your_app_password")
        print("  SMTP_HOST=smtp.gmail.com")
        print("  SMTP_PORT=587")
        return False
    
    load_dotenv(env_file)
    
    # Get configuration
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    # Validate configuration
    if not smtp_user:
        print("✗ SMTP_USER not found in .env file")
        return False
    
    if not smtp_password:
        print("✗ SMTP_PASSWORD not found in .env file")
        return False
    
    print("="*60)
    print("Email Configuration Test")
    print("="*60)
    print(f"SMTP User: {smtp_user}")
    print(f"SMTP Host: {smtp_host}")
    print(f"SMTP Port: {smtp_port}")
    print("="*60)
    print("\nAttempting to send test email...")
    
    try:
        # Create email message
        msg = MIMEText(
            "This is a test email from the Database Query Tool.\n\n"
            "If you received this email, your configuration is working correctly!\n\n"
            "You can now use the main application to send database reports."
        )
        msg['Subject'] = "Test Email from Database Tool"
        msg['From'] = smtp_user
        msg['To'] = smtp_user
        
        print(f"   🔗 Connecting to SMTP server: {smtp_host}:{smtp_port}")
        
        # Connect to SMTP server
        if smtp_port == 465:
            # Port 465: Use SSL/TLS
            print(f"   Using SSL/TLS (port 465)...")
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, context=context)
        else:
            # Port 587: Use STARTTLS
            print(f"   Using STARTTLS (port {smtp_port})...")
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls(context=ssl.create_default_context())
        
        # Login
        print(f"   Authenticating...")
        server.login(smtp_user, smtp_password)
        
        # Send email
        print(f"   Sending test email...")
        server.send_message(msg, from_addr=smtp_user, to_addrs=[smtp_user])
        server.quit()
        
        print("✓ Test email sent successfully!")
        print(f"✓ Check your inbox: {smtp_user}")
        print("\nYour email configuration is working correctly!")
        return True
        
    except Exception as e:
        error_msg = str(e).lower()
        
        if "authentication" in error_msg or "invalid" in error_msg or "credentials" in error_msg:
            print(f"✗ Authentication failed: {e}")
            print("\nTroubleshooting:")
            print("  1. Make sure you're using an APP PASSWORD, not your regular password")
            print("  2. For Gmail: Enable 2-Step Verification and generate App Password")
            print("  3. For Outlook: Enable Two-Factor Authentication and generate App Password")
            print("  4. Remove spaces (Gmail) or dashes (Outlook) from app password")
            print("  5. See EMAIL_SETUP.md for detailed instructions")
            
        elif "connection" in error_msg or "refused" in error_msg:
            print(f"✗ Connection error: {e}")
            print("\nTroubleshooting:")
            print("  1. Check your internet connection")
            print(f"  2. Verify SMTP settings: {smtp_host}:{smtp_port}")
            print("  3. Check firewall settings")
            print("  4. Try from a different network")
            
        else:
            print(f"✗ Error: {e}")
            print("\nTroubleshooting:")
            print("  1. Check .env file has correct values")
            print("  2. Verify SMTP settings match your email provider")
            print("  3. See SETUP_GUIDE.md for complete documentation")
        
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Email Configuration Test")
    print("="*60)
    print()
    
    success = test_email_config()
    
    print()
    print("="*60)
    if success:
        print("✓ Test completed successfully!")
        sys.exit(0)
    else:
        print("✗ Test failed. Please fix the issues above.")
        print("\nFor help, see:")
        print("  - EMAIL_SETUP.md - Email setup guide")
        print("  - SETUP_GUIDE.md - Complete setup guide")
        sys.exit(1)

