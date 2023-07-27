from reportlab.lib.units import cm
from utility import get_image_aspect,black,grey,cyan
from dato import Sample
def firstPage(c,doc):
  c.saveState()
  c.translate(1.0*cm,1.0*cm) #magen 1.8cm
  c.setFont("Times-Roman", 14)
  c.setStrokeColorRGB(0.1,0.8,0.1)
  c.setFillColorRGB(0,0,1) # font colour
  imageSize=get_image_aspect(r"C:\Users\KooRUi\MITSS\infromePDF\rsc\img.png",width=6.5*cm)
  c.drawImage(r"C:\Users\KooRUi\MITSS\infromePDF\rsc\img.png",12.5*cm,25*cm,width=imageSize[0],height=imageSize[1])

  c.setFont("Times-Roman", 18)
  c.setFillColor(black)
  c.drawString(0, 26.5*cm, "Genetic Study Results")
  c.setFont("Times-Roman", 14)
  c.setFillColor(grey)
  c.drawString(0, 26*cm, "Technical Report")
  X=Sample
  c.setLineWidth(1)
  c.setStrokeColor(grey)
  c.rect(0,19*cm,19*cm,5.5*cm)
  c.setFont("Helvetica-Bold", 10)
  c.setFillColor(black)
  c.drawString(1*cm, 24*cm, "Sample ID: "+X['SampleID'])
  c.drawString(1*cm, 23*cm, "Petitioner: "+X['Petitioner'])
  c.drawString(1*cm, 22*cm, "Hospital: "+X['Hospital'])

  c.drawString(5*cm, 24*cm, "Sample collection date: "+X['SampleDate'])
  c.drawString(5*cm, 23*cm, "BIONOS reception date: "+X['BIONOSDate'])
  c.drawString(5*cm, 22*cm, "UPV reception date: "+X['UPVDate'])
  c.drawString(5*cm, 21*cm, "Report date: "+X['ReportDate'])
  c.drawString(5*cm, 20*cm, "Last report update date: "+X['updateDate'])

  c.drawString(12*cm, 24*cm, "Diagnostic/reason: "+X['Diagnostic/reason'])
  c.drawString(12*cm, 23*cm, "Comments: "+X['Comments'])
  c.restoreState()