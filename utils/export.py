"""
utils/export.py
Handles data export to multiple formats (TXT, JSON, CSV, PDF).
"""

import json
import csv
import io
from typing import List, Dict, Any, Union

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

def export_to_txt(history: List[Dict[str, Any]]) -> str:
    """Exports history to a human-readable text block."""
    output = []
    output.append("=== UNIVERSAL ENCODER & DECODER TOOLKIT HISTORY ===")
    output.append(f"Total Operations: {len(history)}")
    output.append("-" * 50)
    for idx, item in enumerate(history, 1):
        output.append(f"[{idx}] Timestamp: {item['timestamp']}")
        output.append(f"    Operation: {item['operation']}")
        output.append(f"    Format: {item['format']}")
        output.append(f"    Input Snippet: {item['input']}")
        output.append(f"    Output Snippet: {item['output']}")
        output.append("-" * 50)
    return "\n".join(output)

def export_to_json(history: List[Dict[str, Any]]) -> str:
    """Exports history as formatted JSON."""
    return json.dumps(history, indent=4)

def export_to_csv(history: List[Dict[str, Any]]) -> str:
    """Exports history as a CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    # Write header
    writer.writerow(["Timestamp", "Operation", "Format", "Input Length", "Output Length", "Input Snippet", "Output Snippet"])
    # Write rows
    for item in history:
        writer.writerow([
            item["timestamp"],
            item["operation"],
            item["format"],
            item["input_len"],
            item["output_len"],
            item["input"],
            item["output"]
        ])
    return output.getvalue()

def export_to_pdf(history: List[Dict[str, Any]]) -> bytes:
    """
    Exports history as a PDF file.
    If fpdf2 is not available, falls back to a plain text representation converted to bytes.
    """
    if not FPDF_AVAILABLE:
        # Fallback to text encoded as bytes
        txt_content = export_to_txt(history)
        return txt_content.encode("utf-8")
        
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Universal Encoder & Decoder Toolkit History", ln=True, align="C")
        pdf.ln(10)
        
        pdf.set_font("Helvetica", "", 10)
        for idx, item in enumerate(history, 1):
            if pdf.get_y() > 250:
                pdf.add_page()
            
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 6, f"#{idx} - {item['operation']} ({item['format']}) - {item['timestamp']}", ln=True)
            
            pdf.set_font("Helvetica", "", 9)
            # PDF text cells need cleaning of characters outside Latin-1
            cleaned_input = str(item['input']).encode('latin-1', 'replace').decode('latin-1')
            cleaned_output = str(item['output']).encode('latin-1', 'replace').decode('latin-1')
            
            pdf.multi_cell(0, 5, f"Input: {cleaned_input}")
            pdf.multi_cell(0, 5, f"Output: {cleaned_output}")
            pdf.cell(0, 4, "-" * 80, ln=True)
            pdf.ln(2)
            
        return pdf.output()
    except Exception as e:
        # Graceful fallback on error
        txt_content = f"PDF compilation failed: {str(e)}\n\n" + export_to_txt(history)
        return txt_content.encode("utf-8")
