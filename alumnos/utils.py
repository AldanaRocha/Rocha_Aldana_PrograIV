from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from datetime import datetime

def generar_pdf_alumno(alumno):
    """
    Genera un PDF con la información del alumno
    """
    buffer = io.BytesIO()
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Contenedor para los elementos del PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=12,
    )
    
    # Título
    title = Paragraph("INFORMACIÓN DEL ALUMNO", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Fecha de generación
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    fecha_text = Paragraph(f"<i>Generado el: {fecha_actual}</i>", normal_style)
    elements.append(fecha_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Datos personales
    heading_personal = Paragraph("Datos Personales", heading_style)
    elements.append(heading_personal)
    
    data_personal = [
        ['Campo', 'Información'],
        ['Nombre Completo:', alumno.nombre],
        ['DNI:', alumno.dni],
        ['Email:', alumno.email],
        ['Teléfono:', alumno.telefono],
    ]
    
    table_personal = Table(data_personal, colWidths=[2.5*inch, 4*inch])
    table_personal.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(table_personal)
    elements.append(Spacer(1, 0.3*inch))
    
    # Datos académicos
    heading_academico = Paragraph("Datos Académicos", heading_style)
    elements.append(heading_academico)
    
    data_academico = [
        ['Campo', 'Información'],
        ['Carrera:', alumno.carrera],
        ['Fecha de Ingreso:', alumno.fecha_ingreso.strftime("%d/%m/%Y")],
        ['Promedio:', f"{alumno.promedio}" if alumno.promedio else "No especificado"],
    ]
    
    table_academico = Table(data_academico, colWidths=[2.5*inch, 4*inch])
    table_academico.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(table_academico)
    elements.append(Spacer(1, 0.5*inch))
    
    # Pie de página
    footer = Paragraph(
        "<i>Este documento ha sido generado automáticamente por el Sistema de Gestión de Alumnos.</i>",
        normal_style
    )
    elements.append(footer)
    
    # Construir el PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer