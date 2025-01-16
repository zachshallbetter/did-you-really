from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
import os
import uuid


def create_tracking_layer(output_path, tracking_id):
    """Create a PDF layer with tracking elements."""
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Add visible marker for testing
    c.setFillColorRGB(0.8, 0.8, 0.8)  # Light gray
    c.setFont("Helvetica", 8)
    c.drawString(10, 10, f"Tracking ID: {tracking_id}")
    
    c.save()


def add_tracking_to_pdf(input_pdf_path, output_pdf_path=None):
    """Add tracking elements to an existing PDF."""
    if output_pdf_path is None:
        # Save in the current directory
        filename = os.path.basename(input_pdf_path)
        base, ext = os.path.splitext(filename)
        output_pdf_path = f"{base}_tracked{ext}"
    
    # Generate unique tracking ID
    tracking_id = str(uuid.uuid4())[:8]
    
    # Create temporary tracking layer
    temp_tracking_pdf = 'temp_tracking.pdf'
    create_tracking_layer(temp_tracking_pdf, tracking_id)
    
    try:
        # Open the original PDF
        original = PdfReader(input_pdf_path)
        tracking = PdfReader(temp_tracking_pdf)
        
        # Create PDF writer
        writer = PdfWriter()
        
        # Add tracking to each page
        for page in original.pages:
            # Merge tracking content with original page
            page.merge_page(tracking.pages[0])
            writer.add_page(page)
        
        # Add JavaScript action to the PDF that runs when opened
        writer.add_js(f"""
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'http://localhost:5001/track?id={tracking_id}', true);
        xhr.send();
        """)
        
        # Write the result
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"Created tracked PDF: {output_pdf_path}")
        print(f"Tracking ID: {tracking_id}")
        print("\nTest tracking with:")
        print(f"curl 'http://localhost:5001/track?id={tracking_id}'")
        
    finally:
        # Clean up
        if os.path.exists(temp_tracking_pdf):
            os.remove(temp_tracking_pdf)


if __name__ == '__main__':
    resume_path = os.path.expanduser(
        "~/Library/Mobile Documents/com~apple~CloudDocs/"
        "Professional/Zachary-Shallbetter-Resume.pdf"
    )
    add_tracking_to_pdf(resume_path) 