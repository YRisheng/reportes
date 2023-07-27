import sys
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,KeepTogether
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm
from body import createBody
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from closure import createClosure
from header import firstPage
from dato import datos


def main(my_path="report.pdf",dato=datos):
  if len(sys.argv)>2:
    my_path=sys.argv[1]
  my_doc=SimpleDocTemplate(my_path,pagesize=A4)
  my_doc.leftMargin = 1*cm
  my_doc.rightMargin = 1*cm
  elements=[]
  elements.append(Spacer(1,8*cm)) #Espacio que ocupa el titulo y el logo
  createBody(dato,elements)
  createClosure(dato,elements)
  my_doc.build(elements,onFirstPage=firstPage) #general el pdf con el titulo y info en firstPage



if __name__ == '__main__':
    main()