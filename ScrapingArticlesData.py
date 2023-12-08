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
    if (('mémoire' in attr_elements)  and (('vivre' in attr_elements) | ('vive' in attr_elements  )|('interne' in attr_elements)) and (len(attr_elements)==2)) | (('ram' in attr_elements) and ('emplacements' not in attr_elements)  )| (('memoire' in attr_elements )  and (('vivre' in attr_elements  ) |('vive' in attr_elements  )|('interne' in attr_elements))) |(('taille' in attr_elements)  and (('mémoire' in attr_elements))and (len(attr_elements)==2) )|(('ram' in attr_elements) and (len(attr_elements)==1) ):
        attr='RAM'
    for c in ('cpu','Processeur'):
        if ((c in attr_elements and len(attr_elements)==1)| ((c+'.') in attr_elements)):
            attr='TypeCPU'
    if (('disque' in attr_elements  and (('dure' in attr_elements) | ('dur' in attr_elements )) and len(attr_elements)==2) | ('memoire' in attr_elements )|(('stockage' in attr_elements) and ( (len(attr_elements))==1) ) | ('memoire' in attr_elements )  ):
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
def get_info(description,i):
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
        i = i + 1
        k = str(i)
        pairs = ['nom' + k, description]
    print(pairs)
#---------------les clés de dictionnaire qui continent les valeurs des attribut de chaque article doivent être passé  par process_att-------------
    key = preprocess_att(pairs[0])
    print(key)
    if key in ['MARK','RAM','typeRam','TypeCPU','GenerationCPU','GPU','STOCKAGE','TypeStockage','COULEUR','POIDS','ECRAN','PRIX','RATE'] : 
        attr_value.append(key)
        attr_value.append(pairs[1])
        
    return attr_value 


Linksfile = 'LINKS2.txt'
df = pd.DataFrame(columns=['MARK','RAM','typeRam','TypeCPU','GenerationCPU','GPU','STOCKAGE','TypeStockage','COULEUR','POIDS','ECRAN','PRIX','RATE'])





with open(Linksfile, 'r') as file:
    lines = file.readlines()
    
    for line in lines :
        article_info={}
        article_info['PRIX']=get_price(line)
        article_info['RATE']=get_rate(line)
        page = requests.get(line.strip())  
        soup = BeautifulSoup(page.content, 'lxml')
        titreArticle=soup.find("h1",{'class','-fs20 -pts -pbxs'})
        descriptionC = soup.find("div", {'class': 'markup -pam'})
        descriptionT = soup.find("ul",{'class':'-pvs -mvxs -phm -lsn'})
        
    
        if descriptionC:
            info_articles = descriptionC.find_all("li")
            i=0
            for li_tag in info_articles:
                text_content = li_tag.get_text(strip=True)
                print(text_content)
                info=[]
                try:
                    info=get_info(text_content,i)
                    if info:
                        article_info[info[0]]=info[1]
                except:
                    print()
#---------------Insertion des données collecté dans le dataFrame-----------------------------------------------------------------------------------
            df=df._append(article_info, ignore_index=True)
        if descriptionT:
            info_articles = descriptionT.find_all("li")
            i=0
            for li_tag in info_articles:
                attribut_tag=li_tag.find("span",{'class':'-b'})
                text_content = li_tag.get_text(strip=True)
                text_content+=attribut_tag.get_text(strip=True)
                print(text_content)
                info=[]
                try:
                    info=get_info(text_content,i)
                    if info:
                        article_info[info[0]]=info[1]
                except:
                    print()
            df=df._append(article_info, ignore_index=True)
        df.to_excel('output.xlsx', index=False)        


# print(df.to_string())
