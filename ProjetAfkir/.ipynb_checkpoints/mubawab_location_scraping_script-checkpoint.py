# Les bibliothèques nécessaires
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import re

# Calcul de temps du collecte de données
start_time = time.time()
# les différentes villes
villes = ["agadir", "bouskoura", "casablanca", "dar-bouazza", "kénitra", "marrakech", "mohammedia", "rabat", "salé", "tanger"]
# les listes des attributs  
ville_column = []
prix = []
Type_de_bien = []
surface = []
nb_de_pieces = []
nb_de_chambre = []
nb_salles_de_bains = []
etat = []
age = []
quel_etage = []
Orientation = []
Jardin = []
Terrasse = []
Garage = []
Ascenseur = []
Piscine = []
Concierge = []
Meublé = []
Salon_Marocain = []
Salon_européen = []
Climatisation = []
Sécurité = []
Cuisine_équipée = []
Réfrigérateur = []
Four = []
TV = []
Machine_à_laver = []
Micro_ondes = []
Animaux_domestiques_autorisés = []
Type_de_sol = []
Cheminée = []
Antenne_parabolique = []

for ville in villes: 
    liens=[] # ou on vas stocker les liens vers les differentes annonces
    # C'est le site de location des appartements et des maisons!
    url = f"https://www.mubawab.ma/fr/ct/{ville}/immobilier-a-louer-all:sc:apartment-rent,house-rent:p:1"

    # page principale
    page = requests.get(url)
    src = page.content
    soup = BeautifulSoup(src, "xml")

    # Extraire le nombre de page des annonces de cette ville
    v_nb_de_pages = soup.find_all('p',{"class" : "fSize11 centered"})
    v1 = v_nb_de_pages[0].text.strip()
    match = re.search(r'(\d+)(?=\s*pages)', v1) # Extraire exactement le nombre de page en utilisant cet exp reg
    if match:
        nb_pages = int(match.group(1)) # convertir en int
    print(nb_pages)
    for k in range(1,nb_pages+1):
        page = requests.get(f"https://www.mubawab.ma/fr/ct/{ville}/immobilier-a-louer-all:sc:apartment-rent,house-rent:p:{k}")
        src = page.content
        soup = BeautifulSoup(src, "xml")
        var_de_annonce = soup.find_all('h2', {"class":"listingTit"})
        for i in range(len(var_de_annonce)):
          a_tag = var_de_annonce[i].find("a")
          if a_tag is not None: # vérifie que le lien existe vers les détails de l'annonce
              liens.append(a_tag.attrs["href"])
    print(len(liens))
    for i in range(len(liens)): # boucler pour chaque lien et extraire les données
          page = requests.get(liens[i]) # accèder au lien
          src = page.content
          soup = BeautifulSoup(src, "xml")
          # descp_de_maison = [p.text for p in soup.find_all('p')]
          v_prix = soup.find_all('h3', {"class":"orangeTit"})
          if v_prix:
              prix.append(v_prix[0].text.strip())
          else:
              prix.append('Nan')
          # type de bien
          v_type_de_bien = soup.find_all("div", {"class" : "col-8 vAlignM"})
          if len(v_type_de_bien) == 0:
              v_type_de_bien = 'Nan'
          else:
              v_type_de_bien = v_type_de_bien[0].text.strip()
          if 'Appartement' in v_type_de_bien:
              v_type_de_bien = 'Appartement'
          elif 'Maison' in v_type_de_bien:
              v_type_de_bien = 'Maison'
          else:
              v_type_de_bien = 'Nan'


          attributes = soup.select('div.mainInfoProp div.catNav span.tagProp')
          # Initializer tous les attributs par 'Nan'
          valeur_de_surface = valeur_de_nb_de_piecess = valeur_de_chambres = valeur_de_salle_de_bains = valeur_etat = valeur_age = valeur_de_etages = 'Nan'
          for attribute in attributes:
              test = attribute.text.strip().replace('\n', '').replace('\t', '')
              if 'm²' in test:
                  valeur_de_surface = test
              elif 'Pièce' in test:
                  valeur_de_nb_de_piecess = test
              elif 'Chambre' in test:
                  valeur_de_chambres = test
              elif 'bain' in test:
                  valeur_de_salle_de_bains = test
              elif 'Nouveau' in test or 'état' in test:
                  valeur_etat = test
              elif 'an' in test:
                  valeur_age = test
              elif 'étage' in test:
                  valeur_de_etages = test


          attributes2 = soup.find_all('span',{"class": "characIconText centered"})
          # Initializer tous les attributs par 'Non'
          valeur_de_orientation = valeur_de_jardin = valeur_de_terrasses = valeur_de_Garage = valeur_ascenceur = valeur_piscine = valeur_de_concierge = valeur_meuble = valeur_de_salon_marocain = valeur_de_salon_europeen = valeur_de_climatisation = valeur_securite = valeur_cuisine = valeur_de_equipee = valeur_de_refregirateur = valeur_de_four = veleur_de_tv = veleur_de_machine_a_laver = veleur_de_micro_ondes = valeur_de_animaux_domestiques_autorisé = valeur_de_type_de_sol = valuer_de_cheminee = valeur_de_antenne_parabolique = 'Non'

          for attribute in attributes2:
              test = attribute.text.strip()
              if 'Orientation' in test:
                  valeur_de_orientation = test.replace('\t','').replace("Orientation",'').replace(":",'')
              elif 'Jardin' in test:
                  valeur_de_jardin = 'Oui'
              elif 'Terrasse' in test:
                  valeur_de_terrasses = 'Oui'
              elif 'Garage' in test:
                  valeur_de_Garage = 'Oui'
              elif 'Ascenseur' in test:
                  valeur_ascenceur = 'Oui'
              elif 'Piscine' in test:
                  valeur_piscine = 'Oui'
              elif 'Concierge' in test:
                  valeur_de_concierge = 'Oui'
              elif 'Meublé' in test:
                  valeur_meuble = 'Oui'
              elif 'Salon Marocain' in test:
                  valeur_de_salon_marocain = 'Oui'
              elif 'Salon européen' in test:
                  valeur_de_salon_europeen = 'Oui'
              elif 'Climatisation' in test:
                  valeur_de_climatisation = 'Oui'
              elif 'Sécurité' in test:
                  valeur_securite = 'Oui'
              elif 'Cuisine' in test:
                  valeur_cuisine = 'Oui'
              elif 'équipée' in test:
                  valeur_de_equipee = 'Oui'
              elif 'Réfrigérateur' in test:
                  valeur_de_refregirateur = 'Oui'
              elif 'Four' in test:
                  valeur_de_four = 'Oui'
              elif 'TV' in test:
                  veleur_de_tv = 'Oui'
              elif ' Machine à laver' in test:
                  veleur_de_machine_a_laver = 'Oui'
              elif 'Micro-ondes' in test:
                  veleur_de_micro_ondes = 'Oui'
              elif 'Animaux domestiques autorisés' in test:
                  valeur_de_animaux_domestiques_autorisé = "Oui"
              elif 'Type du sol' in test:
                  valeur_de_type_de_sol = test.replace('Type du sol', '').replace('\t','').replace(':','')
              elif 'Cheminée' in test:
                  valuer_de_cheminee = 'Oui'
              if valeur_de_orientation == 'Non':
                  valeur_de_orientation = "Nan" # changer la valeur d'orintation par 'Nan' si elle est non
              if valeur_de_type_de_sol == 'Non':
                  valeur_de_type_de_sol = "Nan" # changer la valeur de type du sol par 'Nan' si elle est non


          # Ajouter les valeurs au listes des attributs
          surface.append(valeur_de_surface)
          nb_de_pieces.append(valeur_de_nb_de_piecess)
          nb_de_chambre.append(valeur_de_chambres)
          nb_salles_de_bains.append(valeur_de_salle_de_bains)
          etat.append(valeur_etat)
          age.append(valeur_age)
          quel_etage.append(valeur_de_etages)
          ville_column.append(ville)
          Orientation.append(valeur_de_orientation)
          Jardin.append(valeur_de_jardin)
          Terrasse.append(valeur_de_terrasses)
          Garage.append(valeur_de_Garage)
          Ascenseur.append(valeur_ascenceur)
          Piscine.append(valeur_piscine)
          Concierge.append(valeur_de_concierge)
          Meublé.append(valeur_meuble)
          Salon_Marocain.append(valeur_de_salon_marocain)
          Salon_européen.append(valeur_de_salon_europeen)
          Climatisation.append(valeur_de_climatisation)
          Sécurité.append(valeur_securite)
          Cuisine_équipée.append(valeur_cuisine)
          Réfrigérateur.append(valeur_de_refregirateur)
          Four.append(valeur_de_four)
          TV.append(veleur_de_tv)
          Machine_à_laver.append(veleur_de_machine_a_laver)
          Micro_ondes.append(veleur_de_micro_ondes)
          Animaux_domestiques_autorisés.append(valeur_de_animaux_domestiques_autorisé)
          Type_de_sol.append(valeur_de_type_de_sol)
          Type_de_bien.append(v_type_de_bien)
          Cheminée.append(valuer_de_cheminee)
          Antenne_parabolique.append(valeur_de_antenne_parabolique)
# Charger les données en fichier 'csv'
df = pd.DataFrame({
    'Ville': ville,
    'Prix': prix,
    'Type De Bien': Type_de_bien,
    'Surface': surface,
    'Nombre De Pièces': nb_de_pieces,
    'Nombre De Chambres': nb_de_chambre,
    'Nombre De Salles De Bain': nb_salles_de_bains,
    'Etat De Location': etat,
    'Age De Location': age,
    'Nombre D’Étages': quel_etage,
    'Orientation': Orientation,
    'Jardin': Jardin,
    'Terrasse': Terrasse,
    'Garage': Garage,
    'Ascenseur': Ascenseur,
    'Piscine': Piscine,
    'Concierge': Concierge,
    'Meublé': Meublé,
    'Salon Marocain': Salon_Marocain,
    'Salon européen': Salon_européen,
    'Climatisation': Climatisation,
    'Sécurité': Sécurité,
    'Cuisine équipée': Cuisine_équipée,
    'Réfrigérateur': Réfrigérateur,
    'Four': Four,
    'TV': TV,
    'Machine à laver': Machine_à_laver,
    'Micro-ondes': Micro_ondes,
    'Animaux domestiques autorisés': Animaux_domestiques_autorisés,
    'Type du sol': Type_de_sol,
    'Cheminée': Cheminée,
    'Antenne parabolique': Antenne_parabolique
})
df.to_csv('Mubawab_Rental_Data.csv', index=False)

print(f"Le temps total pour exécuter le code: {((time.time() - start_time)/60):.2f} minutes")
