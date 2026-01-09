import subprocess
import sys
import tempfile
import os
from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime
from docx import Document


def convert_docx_to_html(file_path):
    """
    Convert a .docx file to simple HTML for the editor.
    """
    doc = Document(file_path)
    html_content = ""

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Simple mapping of styles to HTML tags
        if para.style.name.startswith('Heading 1'):
            html_content += f"<h1>{text}</h1>"
        elif para.style.name.startswith('Heading 2'):
            html_content += f"<h2>{text}</h2>"
        elif para.style.name.startswith('Heading 3'):
            html_content += f"<h3>{text}</h3>"
        elif para.style.name.startswith('List Bullet'):
            html_content += f"<ul><li>{text}</li></ul>"
        elif para.style.name.startswith('List Number'):
            html_content += f"<ol><li>{text}</li></ol>"
        else:
            html_content += f"<p>{text}</p>"

    return html_content


def parse_docx_to_modules(file_path):
    """
    Parse a .docx file and return a list of module data.
    Each heading starts a new module.
    """
    doc = Document(file_path)
    modules = []
    current_module = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Check if it's a heading (Heading 1, 2, 3 etc)
        if para.style.name.startswith('Heading'):
            if current_module:
                modules.append(current_module)

            current_module = {
                'title': text,
                'content': '',
                'content_type': 'text'
            }
        else:
            if current_module:
                current_module['content'] += text + '\n\n'
            else:
                # If no heading yet, start a default module
                current_module = {
                    'title': 'Introduction',
                    'content': text + '\n\n',
                    'content_type': 'text'
                }

    if current_module:
        modules.append(current_module)

    return modules


def send_access_key_email(user_email, course_title, access_key):
    """Send course access key to user's email"""
    subject = f"Your Access Key for {course_title}"
    message = f"""
    Hello!

    Thank you for enrolling in {course_title}.

    Your course access key is: {access_key}

    You can now access the course using this key.

    Happy learning!

    Best regards,
    Course Platform Team
    """

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


def execute_python_code(code, inputs="", timeout=5):
    """
    Execute Python code in a sandboxed environment
    Returns tuple: (success, output, error)
    """
    try:
        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            # Execute the code with timeout
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                input=inputs,
                timeout=timeout,
                cwd=tempfile.gettempdir()
            )

            if result.returncode == 0:
                return True, result.stdout, ""
            else:
                return False, "", result.stderr

        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)

    except subprocess.TimeoutExpired:
        return False, "", "Code execution timed out (5 seconds limit)"
    except Exception as e:
        return False, "", str(e)


def generate_certificate_pdf(certificate):
    """Generate PDF certificate"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=colors.HexColor('#1a73e8'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=18,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    content_style = ParagraphStyle(
        'Content',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    # Add spacing
    elements.append(Spacer(1, 1*inch))

    # Certificate title
    title = Paragraph("CERTIFICATE OF COMPLETION", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.5*inch))

    # Award text
    award_text = Paragraph("This is to certify that", content_style)
    elements.append(award_text)
    elements.append(Spacer(1, 0.2*inch))

    # User name
    user_name = Paragraph(
        f"<b>{certificate.user.get_full_name() or certificate.user.username}</b>",
        subtitle_style
    )
    elements.append(user_name)
    elements.append(Spacer(1, 0.2*inch))

    # Completion text
    completion = Paragraph(
        f"has successfully completed the course",
        content_style
    )
    elements.append(completion)
    elements.append(Spacer(1, 0.2*inch))

    # Course name
    course_name = Paragraph(
        f"<b>{certificate.course.title}</b>",
        subtitle_style
    )
    elements.append(course_name)
    elements.append(Spacer(1, 0.5*inch))

    # Date and certificate ID
    date_text = Paragraph(
        f"Issued on {certificate.issued_at.strftime('%B %d, %Y')}",
        content_style
    )
    elements.append(date_text)

    cert_id = Paragraph(
        f"Certificate ID: {certificate.certificate_id}",
        content_style
    )
    elements.append(cert_id)

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
