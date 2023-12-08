import requests
from bs4 import BeautifulSoup
import csv 
import os

#cette boucle gratte tous les éléments de les vingts pages de jumia article ordinateur portable.
#la liste URL_index_global sera remplis par les liens de tous éléments.
URL_index_global=[]
for j in range(20):
    page=requests.get(f"https://www.jumia.ma/pc-portables/?page={j+1}#catalog-listing")
    soup=BeautifulSoup(page.content,'lxml')
#cette liste des article contient tous les articles d'une page.
    articles_global=soup.find_all("article",{'class':'prd _fb col c-prd'}) 
# URL_index contient les URL des éléments de la page sélectionnée et chaque fois qu'on change de page, ce dernier sera mis à jour.
    URL_index=[]   
    for i in range(len(articles_global)):    
        URL_index.append(articles_global[i].find('a',{'class':'core'}).get('href'))
    for k in range(len(URL_index)):
#on ajoute le préfixe https://www.jumia.ma/ pour chaque lien
        URL_index[k]="https://www.jumia.ma"+URL_index[k] 
        URL_index_global.append(URL_index[k])
        
#comme ça notre list des liens des éléments est prêt pour le gratage
with open('LINKS2.txt', 'w') as file:
    for value in URL_index_global: 
        print(value)
        print("\n")        
        file.write(str(value))
        file.write("\n")
        
    