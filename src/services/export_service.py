"""Export service for Excel and PDF exports."""

from pathlib import Path

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle


class ExcelExportService:
    """Service for exporting DataFrames to Excel."""

    @staticmethod
    def export(df: pd.DataFrame, output_path: str) -> str:
        """Export DataFrame to Excel file.

        Args:
            df: pandas DataFrame to export
            output_path: Output Excel file path

        Returns:
            Path to created Excel file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        df.to_excel(output_path, index=False, engine="openpyxl")
        print(f"✓ Excel file created: {output_path}")

        return str(output_file.absolute())


class PDFExportService:
    """Service for exporting DataFrames to PDF."""

    @staticmethod
    def export(df: pd.DataFrame, output_path: str) -> str:
        """Export DataFrame to PDF file.

        Args:
            df: pandas DataFrame to export
            output_path: Output PDF file path

        Returns:
            Path to created PDF file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(output_path, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title = Paragraph("Database Report", styles['Title'])
        elements.append(title)
        elements.append(Paragraph("<br/>", styles['Normal']))

        data = [df.columns.tolist()]
        for _, row in df.iterrows():
            data.append([str(val) for val in row.values])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#4472C4'),
            ('TEXTCOLOR', (0, 0), (-1, 0), '#FFFFFF'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#F2F2F2'),
            ('GRID', (0, 0), (-1, -1), 1, '#000000'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), ['#FFFFFF', '#E8E8E8']),
        ]))

        elements.append(table)
        doc.build(elements)
        print(f"✓ PDF file created: {output_path}")

        return str(output_file.absolute())

