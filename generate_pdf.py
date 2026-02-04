import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_pdf():
    doc = SimpleDocTemplate("LearnHub_Installation_Guide.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=30,
        textColor=colors.HexColor("#1e40af")
    )
    
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontSize=18,
        spaceBefore=20,
        spaceAfter=12,
        textColor=colors.HexColor("#1e3a8a")
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=10
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leftIndent=20,
        rightIndent=20,
        backgroundColor=colors.HexColor("#f3f4f6"),
        borderPadding=5,
        spaceBefore=5,
        spaceAfter=5
    )

    elements = []

    # Title Page
    elements.append(Spacer(1, 100))
    elements.append(Paragraph("LearnHub", title_style))
    elements.append(Paragraph("Panduan Instalasi & Penggunaan Lengkap", ParagraphStyle('SubTitle', parent=title_style, fontSize=16, textColor=colors.grey)))
    elements.append(Spacer(1, 50))
    elements.append(Paragraph("Platform Management Pembelajaran (LMS) Modern berbasis Django", ParagraphStyle('Desc', parent=body_style, alignment=TA_CENTER)))
    elements.append(PageBreak())

    # Introduction
    elements.append(Paragraph("1. Pendahuluan", h2_style))
    elements.append(Paragraph(
        "LearnHub adalah platform Kursus Online (LMS) yang dirancang untuk memudahkan proses belajar mengajar secara digital. "
        "Sistem ini memiliki fitur manajemen modul, video pembelajaran, code execution (Python/JS), assessment/ujian otomatis, "
        "dan penerbitan sertifikat digital.", body_style))

    # Tech Stack
    elements.append(Paragraph("2. Teknologi (Tech Stack)", h2_style))
    tech_data = [
        ["Komponen", "Teknologi"],
        ["Backend", "Django 5.2.11+"],
        ["Database", "MySQL (Laragon)"],
        ["Python", "3.12 - 3.14.2+"],
        ["Modern UI", "Tailwind CSS & Django Unfold"],
        ["Laporan/Dokumen", "ReportLab (PDF Generation)"]
    ]
    t = Table(tech_data, colWidths=[150, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e40af")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(t)

    # Installation Steps
    elements.append(Paragraph("3. Langkah Instalasi", h2_style))
    
    steps = [
        ("A. Persiapan", "Pastikan Python 3.12+ dan Laragon sudah terinstall di komputer Anda."),
        ("B. Clone Repository", "git clone https://github.com/adrian-dev-art/learnhub.git"),
        ("C. Instal Dependensi", "Buka terminal di folder project dan jalankan:<br/><b>pip install -r requirements.txt</b>"),
        ("D. Setup Database", "Mulai Laragon, buka HeidiSQL, dan buat database bernama <b>gampangbelajar</b>."),
        ("E. Migrasi & Seed", "Jalankan perintah berikut secara berurutan:<br/>"
                             "1. python manage.py migrate<br/>"
                             "2. python manage.py seed")
    ]
    
    for title, desc in steps:
        elements.append(Paragraph(f"<b>{title}</b>", body_style))
        elements.append(Paragraph(desc, body_style))
        elements.append(Spacer(1, 5))

    # Credentials
    elements.append(Paragraph("4. Akun Default (Hasil Seeding)", h2_style))
    cred_data = [
        ["Peran", "Username", "Password"],
        ["Admin", "admin", "admin123"],
        ["Owner", "owner", "owner123"],
        ["Mentor", "mentor1", "password123"],
        ["Student", "student1", "password123"]
    ]
    t2 = Table(cred_data, colWidths=[100, 150, 150])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e40af")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(t2)

    # Note for Python 3.14
    elements.append(Paragraph("5. Catatan Khusus Python 3.14+", h2_style))
    elements.append(Paragraph(
        "Proyek ini menyertakan patch otomatis untuk kompatibilitas Python 3.14 di file <b>config/__init__.py</b>. "
        "Metode ini memungkinkan Django 5.2 tetap berjalan stabil meskipun Python 3.14 memiliki perubahan pada objek internal super().", body_style))

    # Footer
    elements.append(Spacer(1, 50))
    elements.append(Paragraph("Dicetak pada: 2026-02-04", ParagraphStyle('Footer', parent=body_style, alignment=TA_CENTER, fontSize=8, textColor=colors.grey)))

    doc.build(elements)
    print("PDF Generated: LearnHub_Installation_Guide.pdf")

if __name__ == "__main__":
    generate_pdf()
