import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def preprocess_att(discription) :
    attr_elements=discription.split(' ')
    print(attr_elements)
    for i in range(len(attr_elements)):
        attr_elements[i]=attr_elements[i].strip().lower()   
        
    print(attr_elements) 
    if ((('mémoire' in attr_elements)  and (('vivre' in attr_elements) | ('vive' in attr_elements  )|('interne' in attr_elements) |('RAM' in attr_elements))  and (len(attr_elements)==2)) | (('ram' in attr_elements) and ('emplacements' not in attr_elements)  )| (('memoire' in attr_elements )  and (('vivre' in attr_elements  ) |('vive' in attr_elements  )|('interne' in attr_elements))) |(('taille' in attr_elements)  and (('mémoire' in attr_elements))and (len(attr_elements)==2) )|(('ram' in attr_elements) and (len(attr_elements)==1))| (('Mémoire' and 'vive' and 'installée' )in attr_elements )):
        attr='RAM'
    for c in ('cpu','Processeur'):
        if ((c in attr_elements and len(attr_elements)==1)| ((c+'.') in attr_elements)):
            attr='CPU-Brand'
    if (('disque' in attr_elements  and (('dure' in attr_elements) | ('dur' in attr_elements )) and len(attr_elements)==2) | ('memoire' in attr_elements )|(('stockage' in attr_elements) and ( (len(attr_elements))==1) ) | ('memoire' in attr_elements )| ('Capacité'and 'SSD') in attr_elements  ):
        attr='STOCKAGE'
    if ((('contrôleur' in attr_elements)  and ('graphique' in attr_elements) and (len(attr_elements)==2)) | (('carte' in attr_elements )  and ('graphique' in attr_elements  ) and ( (len(attr_elements)==2))) | (('gpu' in attr_elements)and (len(attr_elements)==1) )):
        attr='GPU'
    if ((('pouce' in attr_elements) and (len(attr_elements)==1)) | (('taille' in attr_elements) and ('d''écran' in attr_elements ) and (len(attr_elements)==2))|(('display' in attr_elements) and (len(attr_elements)==1)) |(('écran' in attr_elements) and len(attr_elements)==1)):
        attr='ECRAN'
    if (('poids' in attr_elements)|('poid' in attr_elements)):
        attr='POIDS'
    for m in ['modèle','model','modele','modéle','marque']:
        if (( m in attr_elements) and (len(attr_elements)==1)):
            attr='MARK'
    if (('couleur' in attr_elements) and len(attr_elements)==1 ):
        attr='COULEUR'
    
    return attr
def get_mark(link):
    page = requests.get(link.strip())  
    soup = BeautifulSoup(page.content, 'lxml')
    try:
        mark = soup.find("h1", {'class': '-fs20 -pts -pbxs'})
        if mark is not None:
            return mark.get_text(strip=True).split(' ')[0]
    except:
        return None
def extract(description):
    AttrAndValue={}
    Mark_pattern=re.compile(r'(mar(k|que))')
    CPU_pattern=re.compile(r'(cpu|processeur|intel|ryzen)')
    RAM_pattern=re.compile(r'(ram)|(m(é|e)moire((vivre|vive|)?(interne)?(installé)?)).')
    StockageSSD_pattern = re.compile(r'(((disque?dure?)|(m(e|é)moire)|(stockage?)|(capacité?stockage))*\w*\W*ssd\w*\W*((disque?dure?)|(m(e|é)moire)|(stockage?)|(capacité?(ssd|stockage)))*)')
    StockageHDD_pattern = re.compile(r'(((disque?dure?)|(m(e|é)moire)|(stockage?)|(capacité?stockage))*\w*\W*(hdd|sata)\w*\W*((disque?dure?)|(m(e|é)moire)|(stockage?)|(capacité?(ssd|stockage)))*)')
    Stockage_pattern=re.compile(r'(disque?dure?)|(m(e|é)moire)|(stockage?)|(capacité?((hdd|sdd)|stockage)*|(hdd|sdd))')
    GPU_pattern=re.compile(r'(gpu)|(((contr(o|ô)leure?)|carte?)graphique?)')
    Ecran_pattern=re.compile(r'(pouce?)|(taille?(d\'?)?(e|é)cran)|(display)|(\d{1,2}")')
    Poid_pattern=re.compile(r'poids?')
    Couleur_pattern=re.compile(r'couleur(e|s)?')
    
    textwithspaces=description.strip().lower()
    text=re.sub(r'\s+',"",textwithspaces)
    
    if (re.search(Mark_pattern,text)):
        valuei=re.sub(Mark_pattern,"",textwithspaces)
        listmark=valuei.split(' ')
        for i in range(len(listmark)):
            listmark[i]=listmark[i].strip()
            listmark[i]=re.sub(r'-',"",listmark[i])
            listmark[i]=re.sub(r'\s',"",listmark[i])
            if (re.search(r'.?\w*.*?',listmark[i])):
                AttrAndValue['MARK']=re.sub(r'\W*',"",listmark[i])
            else:        
                print()
    elif(re.search(CPU_pattern,text)) and not(re.search(GPU_pattern,text)):
        CPU_patternn = r'((\d{4,6})|(\d{1,2}th)|(\d{1,2}(e|è|é)me)|(i\d-?\d{4,6}?))'
        cpu_brand_pattern = r'(intel|amd|ryzen)'
        cpu_modifier_pattern = r'i[3579]'
        if (re.search(CPU_patternn,text)):
            print(text)
            if re.search(cpu_brand_pattern, text):
                AttrAndValue['CPU_Brand'] = re.search(cpu_brand_pattern, text).group()
                print(AttrAndValue['CPU_Brand'])
                if AttrAndValue['CPU_Brand'] in ['amd', 'ryzen']:
                    CPU_serie = re.search(r'\d{4,5}(u|r|x)', text)
                    CPU_amd_gen=re.search(r'^\d{3}',CPU_serie.group(0))
                    AttrAndValue['CPU_Modifier'] = CPU_serie.group(0)[0]

                    if CPU_amd_gen.group(0)[1] in ['3', '4', '5', '6', '7', '8', '9']:
                        AttrAndValue['CPU_Generation'] = int(CPU_serie.group(0)[0])
                    else:
                        AttrAndValue['CPU_Generation'] = int(CPU_serie.group(0)[0:1])
                    if re.search(r'\dpro',text):
                        AttrAndValue['CPU_Modifier'] = re.search(r'\dpro',text).group(0)[0]
                elif AttrAndValue['CPU_Brand']=='intel':
                    CPU_intel=re.search(r'(i\d-?\d{4,6}?)', text)
                    generation = re.search(r'(\d{4,6})|(\d{1,2}th)|(\d{1,2}(e|è|é)me)', text)
                    
                    if generation.group(0)[0] in ['3', '4', '5', '6', '7', '8', '9']:
                        AttrAndValue['CPU_Generation'] = int(generation.group(0)[0])
                    else:
                        AttrAndValue['CPU_Generation'] = int(generation.group(0)[0:2])

                    if re.search(cpu_modifier_pattern, text):
                        AttrAndValue['CPU_Modifier'] = re.search(cpu_modifier_pattern, text).group().lower()


    elif(re.search(RAM_pattern,text) and not (re.search(r'(fr(é|e)quence)|(cache)',text))):
        ramType=re.search(r'(ddr(2|3|4))',text)
        textwithnoddr=re.sub(r'(ddr(2|3|4))',"",text)
        ramValue=re.search(r'\d{1,2}(g(b|o))',textwithnoddr)
        if ramValue:
            AttrAndValue['RAM']=ramValue.group(0)
        else:
            AttrAndValue['RAM']=re.search(r'\d{1,2}',text).group(0)
        if ramType:
            AttrAndValue['typeRam']=ramType.group(0)
        
    elif(re.search(StockageHDD_pattern,text)):
        FStockage=re.search(r'\d{1,5}(g(b|o)?|to?|\w?\W?(hdd|sata))?',text)
        if FStockage:
            stockageenTera=re.search(r'\d+to?',FStockage.group())
            if stockageenTera:
                stockageValeur=re.search(r'\d*',stockageenTera.group())
                try:
                    AttrAndValue['STOCKAGEHDD']=(int(stockageValeur.group(0))*1000)
                except:
                    print()
        
            stockagego=re.search(r'\d+g(b|o)?',FStockage.group())
            if stockagego:
                stockageValeur=re.search(r'\d*',stockagengiga.group())
                try:
                    AttrAndValue['STOCKAGEHDD']=int(stockageValeur.group(0))
                except:
                    print()
        
            
        AttrAndValue['TypeStockage']='hdd'     
    elif(re.search(StockageSSD_pattern,text)):
        print(text)
        FStockage=re.search(r'\d{1,5}(g(b|o)?|t|\w?\W?ssd)?',text)
        if FStockage:
            stockageenTera=re.search(r'\d+to?',FStockage.group())
            if stockageenTera:
                stockageValeur=re.search(r'\d*',stockageenTera.group())
                try:
                    AttrAndValue['STOCKAGESSD']=(int(stockageValeur.group(0))*1000)
                except:
                    print()
        
            stockagengiga=re.search(r'\d+g(b|o)?',FStockage.group())
            if stockagengiga:
                stockageValeur=re.search(r'\d*',stockagengiga.group())
                try:
                    AttrAndValue['STOCKAGESSD']=int(stockageValeur.group(0))
                except:
                    print()
            
        AttrAndValue['TypeStockage']='ssd'    
    elif(re.search(GPU_pattern,text)):
        AttrAndValue['GPU']=re.sub(GPU_pattern,"",textwithspaces)
    elif(re.search(Ecran_pattern,text)):
        try:
            EcranValue=re.search(r'(\d{1,2}("|pouce))|(\d*x?\d*cm)',text).group()
            AttrAndValue['ECRAN']=EcranValue 
        except:
            print()
    elif(re.search(Poid_pattern,text)):
        poidValue=re.sub(Poid_pattern,"",text)
        AttrAndValue['POIDS']=re.sub(r':*\(*[A-Za-z]*\):*',"",poidValue)
    elif(re.search(Couleur_pattern,text)):
        CouleurValue=re.sub(Couleur_pattern,"",text)
        AttrAndValue['COULEUR']=re.sub(r'\d*|\W*',"",CouleurValue)
    elif(re.search(Stockage_pattern,text)):
        
        FStockage=re.search(r'\d{1,5}(g(b|o)|t)?',text)
        if FStockage:
            stockageenTera=re.search(r'\d+to?',FStockage.group())
            if stockageenTera:
                stockageValeur=re.search(r'\d*',stockageenTera.group())
                try:
                    AttrAndValue['Stockage']=(int(stockageValeur.group(0))*1000)
                except:
                    print()
        
            stockagengiga=re.search(r'\d+g(b|o)?',FStockage.group())
            if stockagengiga:
                stockageValeur=re.search(r'\d*',stockagengiga.group())
                try:
                    AttrAndValue['Stockage']=int(stockageValeur.group(0))
                except:
                    print()
    return AttrAndValue       
def get_price(link):
    page = requests.get(link.strip())  
    soup = BeautifulSoup(page.content, 'lxml')
    try:
        prix = soup.find("span", {'class': '-b -ltr -tal -fs24 -prxs'})
        if prix is not None:
            return prix.get_text(strip=True)
    except:
        return None
def get_rate(link) :
    page = requests.get(link.strip())  
    soup = BeautifulSoup(page.content, 'lxml')
    try:
        rate = soup.find("div", {'class': 'stars _m _al'})
        if rate is not None :
            return rate.get_text(strip=True)
    except:
        return None
def get_info(description):
    attr_value = []
    pairs=[]
# --------------spliting sur les ':' si possible sinon on split sur des espaces '  ' ,sinon on divise pas -----------------------------------------------------
    if not pairs and re.search(r':', description):
        pairs = re.split(':', description)
        for i in range(len(pairs)):
            pairs[i] = pairs[i].strip()

    if not pairs and re.search(r'\s{2,}', description):
        pairs = re.split('  ', description)
        for i in range(len(pairs)):
            pairs[i] = pairs[i].strip()

    if not pairs and re.search(r'\t', description):
        pairs = re.split('\t', description)
        for i in range(len(pairs)):
            pairs[i] = pairs[i].strip()

    if not pairs:
        pairs = ['uknown :'+ description]
    
    if pairs[0]:
#---------------les clés de dictionnaire qui continent les valeurs des attribut de chaque article doivent être passé  par process_att-------------
        key = preprocess_att(pairs[0])
        print(key)
    if key in ['MARK','RAM','typeRam','CPU_Brand','Model','GenerationCPU','GPU','STOCKAGE','TypeStockage','COULEUR','POIDS','ECRAN','PRIX','RATE'] : 
        attr_value.append(key)
        attr_value.append(pairs[1])
        
    return attr_value 



Linksfile = 'LINKS2.txt'
df = pd.DataFrame(columns=['MARK','RAM','typeRam','CPU_Brand','CPU_Modifier','CPU_Generation','GPU','STOCKAGEHDD','STOCKAGESSD','TypeStockage','Stockage','COULEUR','POIDS','ECRAN','PRIX','RATE'])
MARK=[]
RAM=[]
typeRam=[]
CPU_Brand=[]
CPU_Modifier=[]
CPU_Generation=[]
GPU=[]
STOCKAGEHDD=[]
STOCKAGESSD=[]
Stockage=[]
TypeStockage=[]
COULEUR=[]
POIDS=[]
ECRAN=[]
PRIX=[]
RATE=[]




with open(Linksfile, 'r') as file:
    lines = file.readlines()
    i=0
    for line in lines:
        MARK.append(get_mark(line))
        RAM.append(None)
        typeRam.append(None)
        CPU_Brand.append(None)
        CPU_Modifier.append(None)
        CPU_Generation.append(None)
        GPU.append(None)
        STOCKAGEHDD.append(None)
        STOCKAGESSD.append(None)
        Stockage.append(None)
        TypeStockage.append(None)
        COULEUR.append(None)
        POIDS.append(None)
        ECRAN.append(None)
        PRIX.append(get_price(line))
        RATE.append(get_rate(line))

        article_info={}
        
        page = requests.get(line.strip())  
        soup = BeautifulSoup(page.content, 'lxml')
        titreArticle=soup.find("h1",{'class','-fs20 -pts -pbxs'})
        descriptionC = soup.find("div", {'class': 'markup -pam'})
        descriptionT = soup.find("ul",{'class':'-pvs -mvxs -phm -lsn'})
    
        if descriptionC:
            info_articles = descriptionC.find_all("li")
            
            for li_tag in info_articles:
                text_content = li_tag.get_text(strip=True)
                
                try:
                    article_info=extract(text_content)
                except:
                    print()
                for key, value in article_info.items():
                    if ((key=='MARK') and (MARK[i] is None)):
                        MARK[i]=value
                    elif key=='RAM' and (RAM[i] is None):
                        RAM[i]=value
                    elif key=='typeRam':
                        typeRam[i]=value
                    elif key=='CPU_Brand':
                        CPU_Brand[i]=value
                    elif key=='CPU_Modifier':
                        CPU_Modifier[i]=value
                    elif key=='CPU_Generation' and (CPU_Generation[i] is None):
                        CPU_Generation[i]=value
                    elif key=='GPU':
                        GPU[i]=value
                    elif key=='STOCKAGEHDD':
                        STOCKAGEHDD[i]=value
                    elif key=='STOCKAGESSD':
                        STOCKAGESSD[i]=value
                    elif key=='Stockage' and (Stockage[i] is None):
                        Stockage[i]=value
                    elif key=='TypeStockage':
                        TypeStockage[i]=value   
                    elif key=='COULEUR':
                        COULEUR[i]=value   
                    elif key=='POIDS':
                        POIDS[i]=value
                    elif key=='ECRAN':
                        ECRAN[i]=value
    #------------------------------------données collecté dans le dataFrame-----------------------------------------------------------------------------------
            
        if descriptionT:
            info_articles = descriptionT.find_all("li")
            for li_tag in info_articles:
                attribut_tag=li_tag.find("span",{'class':'-b'})
                text_content = li_tag.get_text(strip=True)
                text_content+=attribut_tag.get_text(strip=True)
                try:
                    article_info=extract(text_content)
                    
                except:
                    print()
            
                for key, value in article_info.items():
                    if((key=='MARK') ):
                        MARK[i]=value
                    elif key=='RAM' and (RAM[i] is None):
                        RAM[i]=value
                    elif key=='typeRam':
                        typeRam[i]=value
                    elif key=='CPU_Brand':
                        CPU_Brand[i]=value
                    elif key=='CPU_Modifier':
                        CPU_Modifier[i]=value
                    elif key=='CPU_Generation':
                        CPU_Generation[i]=value
                    elif key=='GPU':
                        GPU[i]=value
                    elif key=='STOCKAGEHDD':
                        STOCKAGEHDD[i]=value
                    elif key=='STOCKAGESSD':
                        STOCKAGESSD[i]=value 
                    elif key=='TypeStockage':
                        TypeStockage[i]=value  
                    elif key=='Stockage' and (Stockage[i] is None):
                        print('got into if of stockage')
                        Stockage[i]=value 
                    elif key=='COULEUR':
                        COULEUR[i]=value   
                    elif key=='POIDS':
                        POIDS[i]=value
                    elif key=='ECRAN':
                        ECRAN[i]=value
                        
        # Apply the function to the "ram" column
        i+=1
data_frame = pd.DataFrame({
    "MARK": MARK,
    "RAM": RAM,
    "typeRam": typeRam,
    "CPU_Brand": CPU_Brand,
    "CPU_Modifier": CPU_Modifier, 
    "CPU_Generation": CPU_Generation,
    "GPU": GPU,
    "STOCKAGEHDD": STOCKAGEHDD,
    "STOCKAGESSD": STOCKAGESSD,
    "TypeStockage": TypeStockage,
    "Stockage":Stockage,
    "COULEUR": COULEUR,
    "POIDS": POIDS,
    "ECRAN": ECRAN,
    "PRIX": PRIX,
    "RATE": RATE,
})
data_frame.to_csv("output1.csv", index=False)    