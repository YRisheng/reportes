from utility import paragraph_Datos, toBold
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Paragraph, Spacer,PageBreak
from reportlab.lib.units import cm
from reportlab.platypus.tables import Table,TableStyle,colors


def createClosure(data,elements):
    styles=styles = getSampleStyleSheet()
    add_AditionalInfo(data,styles,elements)
    elements.append(Spacer(1,0.5*cm))
    add_Annex(data,styles,elements)

def add_AditionalInfo(data,styles,elements):
  
  header ="Aditional Info"
  head1=Paragraph(header,styles["Heading1"])
  elements.append(head1)
  elements.append(Spacer(1,0.3*cm))

  justified_style = ParagraphStyle(
    name=styles["Normal"].name,
    parent=styles["Normal"],
    alignment=TA_JUSTIFY  # Ajuste justificado
  )

  for i in data['info']:
    gen=toBold(i['gen'])
    desc=i['desc']
    sumary = Paragraph(gen+": "+desc, justified_style,bulletText='  •')
    elements.append(Spacer(1,0.3*cm))
    elements.append(sumary)


def add_Annex(data,styles,elements):
  annex=data["anexo"]
  header =annex["Header"]
  head1 = Paragraph(header, styles["Title"])
  elements.append(head1)
  elements.append(Spacer(1,0.3*cm))

  justified_style = ParagraphStyle(
    name=styles["Normal"].name,
    parent=styles["Normal"],
    alignment=TA_JUSTIFY  # Ajuste justificado
  )
  header1 ="<b>Reference Genome: </b> " + annex["Genome"]
  header1p = Paragraph(header1, justified_style)
  elements.append(header1p)
  elements.append(Spacer(1,0.3*cm))

  header2  ="<b>Sequencer libraries:</b>"   + annex["Sequencer"]
  header2p = Paragraph(header2, justified_style)
  elements.append(header2p)
  elements.append(Spacer(1,0.3*cm))

  header3 ="<b>Bioinformatic analysis:</b> " + annex["Analysis"]
  header3P = Paragraph(header3, justified_style)
  elements.append(header3P)
  elements.append(Spacer(1,0.3*cm))

  header4 ="<b>Sample quality:</b>"
  header4P =Paragraph(header4,justified_style)
  elements.append(header4P)
  for sample in annex["Sample"]:
    samplep =Paragraph(sample, justified_style,bulletText='  •')
    elements.append(samplep)
    elements.append(Spacer(1,0.1*cm))

  header5 ="<b>Databases:</b> "
  header5P =Paragraph(header5, justified_style)
  elements.append(header5P)
  for sample in annex["Database"]:
    samplep =Paragraph(sample, justified_style,bulletText='  •')
    elements.append(samplep)
    elements.append(Spacer(1,0.1*cm))

