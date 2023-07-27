from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import CMYKColor, PCMYKColor
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

def paragraph_Datos(dato):
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    bold_style = styles["Heading1"]
    # Crear una lista para almacenar los párrafos
    paragraph_list = []
    for item in dato:
      if isinstance(item, list):
          paragraph_list.append([element for element in item])
      else:
          paragraph_list.append(tuple(Paragraph(element,styles['Normal']) for element in item))
    return paragraph_list

def toParagraph(lista):
  styles = getSampleStyleSheet()
  res=[]
  for titulo in lista:
    res.append(Paragraph(titulo,styles["Normal"]))
  return res

def notNull(datos):
    if len(datos) == 0 or all(all(value == "" for value in row) for row in datos):
        return False
    else:
        return True


def toBold(lista):
  res=""
  for titulo in lista:
    res+=("<b>"+titulo+"</b>")
  return res

def get_image_aspect(path, width=1*cm):
    img = ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return [width,(width * aspect)]


def divideFidings(dato):
    significant_Findings= [['Variant Name', 'Gene', 'Variant Effect', 'Genotype', 'Result']]
    significant_Variant=[]
    uncertain_Findings= [['Variant Name', 'Gene', 'Variant Effect', 'Genotype', 'Result']]
    uncertain_Variant=[]
    other_Findings=[['Variant Name', 'Gene', 'Variant Effect', 'Genotype', 'Result']]
    other_Variant=[]
    
    
    for i in dato['variant'].keys():
      type=dato['variant'][i]['type']
      match type:
          case "Significant":
              significant_Findings.append(dato['variant'][i]['findings'][1])
              significant_Variant.append(dato['variant'][i]['findings'][1][0])
          case "Uncertain":
              uncertain_Findings.append(dato['variant'][i]['findings'][1])
              uncertain_Variant.append(dato['variant'][i]['findings'][1][0])
          case "Other":
              other_Findings.append(dato['variant'][i]['findings'][1])
              other_Variant.append(dato['variant'][i]['findings'][1][0])
    return[[significant_Findings,uncertain_Findings,other_Findings],[significant_Variant,uncertain_Variant,other_Variant]]

black = CMYKColor(0,0,0,1)
cyan = PCMYKColor(100,0,0,0)
grey=CMYKColor(0,0,0,0.404)