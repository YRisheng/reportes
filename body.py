from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Paragraph, Spacer,PageBreak
from reportlab.lib.units import cm
from reportlab.platypus.tables import Table,TableStyle,colors
from utility import divideFidings,paragraph_Datos,notNull
from variant import add_variant
#create the inicial table of each fiding
def fidings(type,dato,styles,elements):
  
  match type:
    case 1:
      header = "<font color='red'>!</font>"+" Significant Findings"
      style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.pink),("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),('LINEBELOW', (0, 0), (-1, -1), 1, colors.grey)])  # Establecer el color rosa para la primera fila
    case 2:
      header = "<font color='orange'>?</font>"+" Variants of Uncertain Significance"
      style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#C4E3F3")),("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),('LINEBELOW', (0, 0), (-1, -1), 1, colors.grey)])  # Establecer el color cyan para la primera fila
    case 3:
      header = "Other findings"
      style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#90EE90")),("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),('LINEBELOW', (0, 0), (-1, -1), 1, colors.grey)])  # Establecer el color verde para la primera fila
  head1 = Paragraph(header, styles['Heading1'])
  elements.append(head1)
  elements.append(Spacer(1,0.3*cm))
  
  if(type == 1):
    estilo_personalizado = ParagraphStyle(name='NegritaRoja',parent=styles['Normal'],fontName='Helvetica-Bold',textColor=colors.red)
    body1=  Paragraph("Genetic study in relatives is recommended according to clinical criteria.",estilo_personalizado)
    elements.append(body1)
    elements.append(Spacer(1,0.3*cm))

  if len(dato)>1:
      dato_table=paragraph_Datos(dato)
      table=Table(dato_table,repeatRows=1,colWidths=18.5*cm/(len(dato[0])))

      table.setStyle(style)
      elements.append(table)
      elements.append(Spacer(1,0.3*cm))

      estilo_leyenda = ParagraphStyle(
        name='Leyenda',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        textColor='gray'
      )
      leyenda1=  Paragraph("SNV: Single Nucleotide Variant <br/> (!): See Other Names section for alternative names of this variant",estilo_leyenda)
      elements.append(leyenda1)
      elements.append(Spacer(1,0.3*cm))
  else:
    text=  Paragraph("No variants have been found.",styles['Normal'])
    elements.append(text)
    elements.append(Spacer(1,0.3*cm))




#metod create each section of fidings
def createBody(dato,elements):
  styles = getSampleStyleSheet()
  styles["Normal"].leftMargin = 0
  styles["Normal"].rightMargin = 0
  styles["Normal"].alignment=TA_JUSTIFY
  findings=divideFidings(dato)
  fidings(1,findings[0][0],styles,elements)
  for i in findings[1][0]:
    add_variant(1,dato['variant'][i],styles,elements)

  elements.append(PageBreak())
  fidings(2,findings[0][1],styles,elements)

  for i in findings[1][1]:
    add_variant(2,dato['variant'][i],styles,elements)

  elements.append(PageBreak())
  fidings(3,findings[0][2],styles,elements)
  for i in findings[1][2]:
    add_variant(3,dato['variant'][i],styles,elements)