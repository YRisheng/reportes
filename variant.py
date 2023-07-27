from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer,HRFlowable,KeepTogether
from reportlab.lib.units import cm
from reportlab.lib.colors import CMYKColor, PCMYKColor
from reportlab.platypus.tables import Table,TableStyle,colors,LongTable
from utility import notNull,toParagraph,toBold
import math
def add_variant(type,data,styles,elements):
  variant_summary(type,data,styles,elements)
  variant_other(type,data,styles,elements)
  variant_Interpretations(type,data,styles,elements)
  variant_Population(type,data,styles,elements)
  variant_Silico(type,data,styles,elements)
  variant_Conservation(type,data,styles,elements)
  variant_References(type,data,styles,elements)

#add sumary for one variant,check type of fiding and the sumary info.
def variant_summary(type,data,styles,elements):

    header= "&#8226 Summary "+data['findings'][1][0] + " ("+data['findings'][1][1]+")"

    match type:
        case 1:
            estilo_personalizado = ParagraphStyle(name='BoldRed',parent=styles['Normal'],fontName='Helvetica-Bold',textColor=colors.red,keepWithNext = True)
        case 2:
            estilo_personalizado = ParagraphStyle(name='boldOrange',parent=styles['Normal'],fontName='Helvetica-Bold',textColor=colors.orange,keepWithNext = True)
        case 3:
            estilo_personalizado = ParagraphStyle(name='boldOrange',parent=styles['Normal'],fontName='Helvetica-Bold',textColor=colors.greenyellow,keepWithNext = True)
    headerP = Paragraph(header, estilo_personalizado)
    elements.append(Spacer(1,0.3*cm))
    elements.append(headerP )

    linea = HRFlowable(width="100%", thickness=1, spaceBefore=10, spaceAfter=10)
    elements.append(linea)

    
    descripcion=""
    if(len(data['findings'][1][3])>0):
        descripcion +=data['findings'][1][3] + " variant"
    if(len(data['findings'][1][2])>0):
        descripcion +="of type "+data['findings'][1][3] 
    if (data['findings'][1][0].startswith('g')):
        descripcion += " in the intronic region of gene " 
    else:
        descripcion +=  " in the exonic region of gene " 
    descripcion += data['findings'][1][1] + " associated with the following phenotypes according to MedGen: "
    
    descripcionP = Paragraph(descripcion, styles["Normal"])
    elements.append(descripcionP)
    elements.append(Spacer(1,0.2*cm))

    custom_bullet_style = ParagraphStyle(
        name='CustomBulletStyle',
        parent=styles['BodyText'], 
    )
    for i in data['Summary']:
        texto= i
        textoParrafo = Paragraph(texto, custom_bullet_style,bulletText='    •',)
        elements.append(textoParrafo )

    elements.append(Spacer(1,0.3*cm))


#add othger name of the variant
def variant_other(type,data,styles,elements):
    header ="Other Names"
    estilo_personalizado = ParagraphStyle(name='Negrita',parent=styles['Normal'],fontName='Helvetica-Bold',textColor=colors.black)
    headerP = Paragraph(header, estilo_personalizado)
    elements.append(Spacer(1,0.3*cm))
    elements.append(headerP)
    elements.append(Spacer(1,0.3*cm))
    descripcion="This variant is also known as:"
    descripcionP = Paragraph(descripcion, styles["Normal"])
    elements.append(descripcionP)

    for i in data['Other']:
        texto= i
        textoParrafo = Paragraph(texto, styles["BodyText"],bulletText='    •')
        elements.append(textoParrafo )
    elements.append(Spacer(1,0.3*cm))


def variant_Interpretations(type,data,styles,elements):
    header ="Interpretations"
    estilo_personalizado = ParagraphStyle(name='Negrita',parent=styles['Normal'],fontName='Helvetica-Bold',textColor=colors.black,keepWithNext = True)
    header1 = Paragraph(header, estilo_personalizado)
    t=[]
    if(notNull(data['Interpretations'][1])):
        
        
        estilo_tabla = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#C4E3F3")),("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),('LINEBELOW', (0, 0), (-1, -1), 1, colors.grey)])
        
        var=[
            ["ClinVar","LOVD"],
            (
            Paragraph(data['Interpretations'][1][0], styles["Normal"]
                      )
            ,Paragraph(data['Interpretations'][1][1], styles["Normal"]
            )
            )
            ]

        t=LongTable( var,style=estilo_tabla,repeatRows=1)

        
    else:
        t = Paragraph("No interpretations found in ClinVar or LOVD.", styles['Normal'])
        
    
    elements.append(KeepTogether([header1,Spacer(1,0.3*cm),t]))
    elements.append(Spacer(1,0.3*cm))



def variant_Population(type,data,styles,elements):
  header ="Population Frequencies"
  estilo_personalizado = ParagraphStyle(name='Negrita',parent=styles['Normal'],fontName='Helvetica-Bold',textColor=colors.black)
  headerP = Paragraph(header, estilo_personalizado)
  elements.append(headerP )
  elements.append(Spacer(1,0.3*cm))
  vacio=True
  for i in data['Population'][1:][0]:
    if len(i) != 0:
      vacio=False


  if(vacio):
    header ="Variant absent from 1000 Genomes, ESP6500 and gnomAD."
    headerP = Paragraph(header, styles["Normal"])
    elements.append(Spacer(1,0.3*cm))
    elements.append(headerP )
  else:
    estilo_tabla = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#C4E3F3")),("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),('LINEBELOW', (0, 0), (-1, -1), 1, colors.grey)])

    t=Table(data['Population'],style=estilo_tabla,colWidths=18.5*cm/(len(data['Population'][1])))
    elements.append(t)




#comprobar si hay datos,
def variant_Silico(type,data,styles,elements):
  

  header ="In silico Predictions"
  estilo_personalizado = ParagraphStyle(name='Negrita',parent=styles['Normal'],fontName='Helvetica-Bold',textColor=colors.black)
  headerP = Paragraph(header, estilo_personalizado)
  elements.append(Spacer(1,0.3*cm))
  elements.append(headerP )
  predictors=data['inSilico'][0]
  types=toParagraph(data['inSilico'][1][0])
  values=toParagraph(data['inSilico'][1][1])
  
  if notNull(data['inSilico'][1][1]): # not null, else print no info
    maximo=max(predictors) #max protein function
    total=sum(predictors)#protein function
    texto=""
    if maximo == predictors[0]:
      texto=" algorithms have predicted that this variant will adverserly affect protein function."
    if maximo == predictors[1]:
      texto=" algorithms have predicted that this variant is unknown affect protein function."
    if maximo == predictors[2]:
      texto=" algorithms have predicted that this variant will not adverserly affect protein function."
    header = "<b>"+str(maximo)+"</b>"+" of "+"<b>"+str(total)+"</b>"+ texto
    headerP = Paragraph(header, styles["Normal"])
    elements.append(Spacer(1,0.3*cm))
    elements.append(headerP )

    tipo=["<font color=red>❤</font> Deletereous: ","? Unknown: ","<font color=green>❤</font> Tolerated "]
    for i in range(0,3):
      header=tipo[i]+str(predictors[i])+" predictors. "
      headerP = Paragraph(header, styles["Normal"],bulletText='•')
      elements.append(Spacer(1,0.3*cm))
      elements.append(headerP )

    elements.append(Spacer(1,0.3*cm))
    
    table_silico([types,values],styles,elements)


  else : #else print no info
    elements.append(Spacer(1,0.3*cm))
    texto ="No functional effect predictions have been found in the following in silico prediction tools: SIFT, PolyPhen2-HDIV, PolyPhen2-HVAR,LRT, MutationTaster, MutationAssessor, Provean, MetaSVM, MetaLR, MetaRNN, M-CAP, MutPred, MVP, MPC, PrimateAI, DEOGEN2,BayesDel AddAF, BayesDel NoAddAF, ClinPred, LIST-S2, Aloft, DANN, Fathmm, FATHMM KL Coding, and FATHMM XF Coding."
    textoP = Paragraph(texto, styles["Normal"])
    elements.append(textoP)
    elements.append(Spacer(1,0.3*cm))

#Comprobar en cada celda el color que tiene que tener.
def table_silico(data,styles,elements):
    dmgList=["Damaging","Deletereous","Disease causing","Known disease causing","High"]
    
    num_dato = len(data[1])
    num_colums=7
    num_table =math.ceil(num_dato/num_colums)
    column_width =math.ceil(18.5/num_colums)

    part_length = math.ceil(num_dato / num_table)


    parts = []
    for i in range(num_table):
      start = i * part_length
      end = (i + 1) * part_length
      part = data[0][start:end]
      part_labels = data[1][start:end]
      parts.append((part, part_labels))

    result = []
    for part, part_labels in parts:
      result.append([part, tuple(part_labels)])


    estilo_tabla = TableStyle([('LINEBELOW', (0, 0), (-1, -1), 1, colors.grey),('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#C4E3F3")),])
    tableTogether=[]
    for item in result:
      table = Table(item,style=estilo_tabla,colWidths=18.5*cm/(len(item[0])))
      # Recorrer los valores de la tabla
      tableTogether.append(Spacer(1,0.3*cm))
      tableTogether.append(table)
      
    # Recorrer los valores de la tabla
      for i, row in enumerate(table._cellvalues):
        for j, value in enumerate(row):
            # Acceder al valor de la celda
            # Aplicar lógica adicional según el valor de la celda
            if (value.getPlainText() in dmgList):
                table.setStyle(TableStyle([('BACKGROUND', (j, i), (j, i), colors.HexColor('#ffd6d6')),]))

            if (value.getPlainText() == "MutPred Score" ):
                input_string=table._cellvalues[i+1][j].getPlainText()
                if input_string.strip(): 
                    if  float(input_string) >= 0.74:
                        table.setStyle(TableStyle([('BACKGROUND', (j, i+1), (j, i+1), colors.HexColor('#ffd6d6')),]))
            if (value.getPlainText() == "MPC Score" ):
                input_string=table._cellvalues[i+1][j].getPlainText()
                if input_string.strip(): 
                    if  float(input_string) >= 0.74:
                        table.setStyle(TableStyle([('BACKGROUND', (j, i+1), (j, i+1), colors.HexColor('#ffd6d6')),]))
            if (value.getPlainText() == "MVP Score" ):
                input_string=table._cellvalues[i+1][j].getPlainText()
                if input_string.strip(): 
                    if  float(input_string) >= 0.74:
                        table.setStyle(TableStyle([('BACKGROUND', (j, i+1), (j, i+1), colors.HexColor('#ffd6d6')),]))
            if (value.getPlainText() == "DANN Score" ):
                input_string=table._cellvalues[i+1][j].getPlainText()
                if input_string.strip(): 
                    if  float(input_string) >= 0.74:
                        table.setStyle(TableStyle([('BACKGROUND', (j, i+1), (j, i+1), colors.HexColor('#ffd6d6')),]))
    elements.append(KeepTogether(tableTogether))
           


    estilo_leyenda = ParagraphStyle(
      name='Leyenda',
      parent=styles['Normal'],
      fontName='Helvetica-Oblique',
      fontSize=8,
      textColor='black'
    )
    texto ="Pathogenicity thresholds: MutPred >= 0.74 MVP >= 0.75 MPC >= 0.75 DANN >= 0.96"
    textoP = Paragraph(texto, estilo_leyenda)
    elements.append(Spacer(1,0.3*cm))
    elements.append(textoP )



def variant_Conservation(type,data,styles,elements): 
    header ="Conservation Predictions"
    estilo_personalizado = ParagraphStyle(name='Negrita',parent=styles['Normal'],fontName='Helvetica-Bold',textColor=colors.black)
    headerP = Paragraph(header, estilo_personalizado)
    elements.append(Spacer(1,0.3*cm))
    elements.append(headerP )
    var=data['Conservation']
    var_para=[toParagraph(data['Conservation'][0]),toParagraph(data['Conservation'][1])]
    if notNull(var[1]): #else print no info
        texto ="The affected sequence is predicted as conserved."
        textoP = Paragraph(texto, styles["Normal"])
        elements.append(Spacer(1,0.3*cm))
        elements.append(textoP )
        elements.append(Spacer(1,0.2*cm))

        estilo_tabla = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#C4E3F3")),('LINEBELOW', (0, 0), (-1, -1), 1, colors.grey)])
        t=LongTable(var_para,style=estilo_tabla,repeatRows=1,colWidths=18.5*cm/(len(var[0])))


        if(float(t._cellvalues[1][0].getPlainText()) > 7.2) :
            t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#ffd6d6')),
                ]))
        if(float(t._cellvalues[1][1].getPlainText()) > 7.2) :
            t.setStyle(TableStyle([
                    ('BACKGROUND', (1, 1), (1, 1), colors.HexColor('#ffd6d6')),
                ]))

        if(float(t._cellvalues[1][2].getPlainText()) >= 0.5) :
            t.setStyle(TableStyle([
                    ('BACKGROUND', (2, 1), (2, 1), colors.HexColor('#ffd6d6')),
                ]))
        if(float(t._cellvalues[1][3].getPlainText()) >= 0.5) :
            t.setStyle(TableStyle([
                    ('BACKGROUND', (3, 1), (3, 1), colors.HexColor('#ffd6d6')),
                ]))

        if(float(t._cellvalues[1][4].getPlainText()) >= 0) :
            t.setStyle(TableStyle([
                    ('BACKGROUND', (4, 1), (4, 1), colors.HexColor('#ffd6d6')),
                ]))

        elements.append(t)


        texto ="Conservation thresholds: PhyloP >= 7.2 PhastCons >= 0.5 GERP >= 0"
        textoP = Paragraph(texto, styles["Normal"])
        
        

    else :
        texto ="No sequence conservation predictions have been found in the following in silico prediction tools: PhyloP, PhasCons and GERP++."
        textoP = Paragraph(texto, styles["Normal"])
    elements.append(Spacer(1,0.3*cm))
    elements.append(textoP )



def variant_References(type,data,styles,elements):
  var=data['References']
  header ="References"
  estilo_personalizado = ParagraphStyle(name='Negrita',parent=styles['Normal'],fontName='Helvetica-Bold',textColor=colors.black)
  headerP = Paragraph(header, estilo_personalizado)
  elements.append(Spacer(1,0.3*cm))

  texto ='The variant has been referenced in the following publications (source'+ '<link href="' + 'https://candy.text-analytics.ch/Variomes/' + '">' + 'Variomes '+ '</link>' +'):'
  textoP = Paragraph(texto, styles["Normal"])
  elements.append(KeepTogether([headerP,Spacer(1,0.3*cm),textoP]))
  

  if(notNull(var[1])):
    estilo_tabla = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#C4E3F3")),("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),('LINEBELOW', (0, 0), (-1, -1), 1, colors.grey)])

    t=LongTable(var,style=estilo_tabla,repeatRows=1,colWidths=18.5*cm/(len(var[0])))
    elements.append(Spacer(1,0.3*cm))
    elements.append(t)
    elements.append(Spacer(1,0.3*cm))
  else:
    texto ='No data provided'
    textoP = Paragraph(texto, styles["Normal"])
    elements.append(textoP)