import re
def extract(description):
    AttrAndValue={}
    Mark_pattern=re.compile(r'(mod(é|è|e)le?)|(mar(k|que))')
    CPU_pattern=re.compile(r'(cpu|processeur).')
    RAM_pattern=re.compile(r'(ram)|(m(é|e)moire((vivre|vive|)?(interne)?(installé)?)).')
    
    StockageSSD_pattern=re.compile(r'(disque?dure?)|(m(e|é)moire)|(stockage?)|(capacité?(ssd|stockage)|(ssd))')
    StockageHDD_pattern=re.compile(r'(disque?dure?)|(m(e|é)moire)|(stockage?)|(capacité?(hdd|stockage)|(hdd))')
    GPU_pattern=re.compile(r'(gpu)|(((contr(o|ô)leure?)|carte?)graphique?)')
    Ecran_pattern=re.compile(r'(pouce?)|(taille?(d\'?)?(e|é)cran)|(display)|(\d{1,2}")')
    Poid_pattern=re.compile(r'poids?')
    Couleur_pattern=re.compile(r'couleur(e|s)?')
    
    textwithspaces=description.strip().lower()
    text=re.sub(r'\s+',"",textwithspaces)
    print(text)
    if (re.search(Mark_pattern,text)):
        valuei=re.sub(Mark_pattern,"",text)
        valuef=re.sub(r'(\d*|\W*|_)',"",valuei)
        AttrAndValue['MARK']=valuef
    elif(re.search(CPU_pattern,text)):
        cpu_generation_pattern=r'(\d{4,5}|\dth)'
        cpu_brand_pattern=r'(intel|amd)'
        cpu_modifier_pattern=r'i[3579]'
        if (re.search(cpu_brand_pattern,text)):
            AttrAndValue['CPU-Brand']=re.search(cpu_brand_pattern,text).group()
        elif(re.search(cpu_generation_pattern,text)):
            gen=re.search(cpu_generation_pattern,text)
            AttrAndValue['CPU-Generation']=(re.search(r'^\d',gen.group(1))).group(1)
        elif(re.search(cpu_modifier_pattern,text)):
            AttrAndValue['CPU-Modifier']=(re.search(cpu_modifier_pattern,text)).group(1)
    elif(re.search(RAM_pattern,text)):
        ramValue=re.search(r'\d{1,2}(g(b|o))?',text)
        ramType=re.search(r'(ddr(2|3|4))',text)
        AttrAndValue['RAM']=ramValue.group(1)
        if ramType:
            AttrAndValue['typeRam']=ramType.group(1)
    elif(re.search(StockageHDD_pattern,text)):
        FStockage=re.search(r'\d{1,5}(g(b|o)|t)?',text)
        if re.search(r't',FStockage.group()):
            stockage=re.search(r'\d+',FStockage.group())
            try:
                AttrAndValue['STOCKAGEHDD']=(int(stockage.group())*1000)
            except:
                print()
        if re.search(r'g(b|o)',FStockage.group()):
            stockage=re.search(r'\d+',FStockage.group())
            try:    
                AttrAndValue['STOCKAGEHDD']=int(stockage.group())
            except:
                print()
    elif(re.search(StockageSSD_pattern,text)):
        FStockage=re.search(r'\d{1,5}(g(b|o)|t)?',text)
        if re.search(r't',FStockage.group()):
            stockage=re.search(r'\d+',FStockage.group())
            try:
                AttrAndValue['STOCKAGEHDD']=(int(stockage.group())*1000)
            except:
                print()
        if re.search(r'g(b|o)',FStockage.group()):
            stockage=re.search(r'\d+',FStockage.group())
            try:
                AttrAndValue['STOCKAGESSD']=int(stockage.group())
            except:
                print()
    elif(re.search(GPU_pattern,text)):
        AttrAndValue['GPU']=re.sub(GPU_pattern,"",text)
    elif(re.search(Ecran_pattern,text)):
        try:
            EcranValue=re.search(r'(\d{1,2}("|pouce))|(\d*x?\d*cm)',text).group()
            AttrAndValue['ECRAN']=EcranValue 
        except:
            print()
    elif(re.search(Poid_pattern,text)):
        poidValue=re.sub(Poid_pattern,"",text)
        AttrAndValue['POIDS']=re.sub(r'\D*',"",poidValue)
    elif(re.search(Couleur_pattern,text)):
        CouleurValue=re.sub(Couleur_pattern,"",text)
        AttrAndValue['COULEUR']=re.sub(r'\d*|\W*',"",CouleurValue)
    
    return AttrAndValue
text=["""Nom     :       DELL Latitude E5440 2.3GHz i5-4300U 14\" 1366 x 768pixels 4G Noir

Type produit :  Notebooks

Marque :        DELL

Modèle de processeur :  i5-4300U

Fréquence du processeur Turbo :         2,9 GHz

Nombre de coeurs de processeurs  :  2

Fréquence du processeur  :   2,3 GHz

Séries de processeurs    :   Intel Core i5-5300 Mobile series

Mémoire interne   :   8 Go

Capacité totale de stockage      :   500 Go

Taille de l'écran           :    35,6 cm (14")

Résolution de l'écran   :    1366 x 768 pixels

Modèle d'adaptateur graphique à bord    Intel® HD Graphics 5500

Sorties de la carte graphique prises en charge  :  DisplayPort, Embedded DisplayPort (eDP), HDMI

Wifi    :  Oui

Ethernet/LAN   :        Oui

Nombre de port Ethernet LAN (RJ-45 )     :      1

Nombre de ports VGA (D-Sub) :   1

Quantité de ports HDMI   :      1

Combo casque / microphone Port  :  Oui

Quantité de ports de type A USB 3,0 (3,1 Gen 1)   :     3

SKU: DE014CL0DH5A6NAFAMZSKU

Gamme de produits: latitudeGamme de produits

Modèle: DELL Latitude E5450Modèle

Taille (Longueur x Largeur x Hauteur cm): 33.8 cm x 23.1 cm x 1.895 cmTaille (Longueur x Largeur x Hauteur cm)

Poids (kg): 1.81Poids (kg)

Couleur: noirCouleur

Matière principale: aluminumMatière principale

Processeur Intel Core i5-8350U (Quad-Core 1.7 GHz / 3.6 GHz Turbo - Cache 6 Mo)

8 Go de mémoire DDR4

Ecran de 13.3" anti-reflets avec résolution Full HD (1920 x 1080)

Technologie HP Sure View

Fonctionnement rapide avec un SSD  PCIe de 256 Go

Communication sans fil Wi-Fi AC + Bluetooth 4.2

Clavier rétroéclairé résistant aux éclaboussures

Webcam HD intégrée

2 ports USB 3.0 + 1 port USB 3.0 Type C

Sécurité : puce TPM 2.0 et lecteur d'empreinte digitale

Système audio Bang & Olufsen

Windows 10 Professionnel 64 bits

Remise à neuf

6 Mois de Garantie

SKU: HP017CL05NFPSNAFAMZSKU

Modèle: Hp EliteBook 830 G5Modèle

Taille (Longueur x Largeur x Hauteur cm): 33.8 x 23.7 x 1.89Taille (Longueur x Largeur x Hauteur cm)

Poids (kg): 1Poids (kg)

Couleur: argentCouleur

Type de boutique: Jumia MallType de boutique

CPU : AMD Ryzen™ 3 3250U

RAM : 8 GB DDR4 2400 MHz

Stockage : 512 Go SSD M.2 PCIe

Écran : 15,6″ Full-HD TN 1080 Pixels

Communication : Wi-Fi + Bluetooth

OS : FREDOS

Clavier: Azerty

Garantie constructeur 1 ans

SKU: LE018CL0MI09MNAFAMZSKU

Gamme de produits: .Gamme de produits

Modèle: ideapad 3 15ADA05Modèle

Taille (Longueur x Largeur x Hauteur cm): 25.3 x 36.2 x 19.9 cm (HxLxP)Taille (Longueur x Largeur x Hauteur cm)

Poids (kg): 1.9Poids (kg)

Couleur: GRISCouleur

Matière principale: metaliqueMatière principale

Dell Latitude 7280 i5 7ème génération

CPU:Intel Core i5  7300U/(7ème génération)

RAM:8 Go de Mémoire DDR4–2133, extensible à 32 Go.

Stockage:256Go SSD FORME M.2 2280 NOUVELLE TECHNOLOGIE .

Carte graphique:Intel HD 620 .

CAMERA:HD 720p intégré .

Connexion:WiFi 802.11 b/g/n/ac, Bluetooth® 4.2, Realtek Ethernet 10/100/1000

Ecran: 12.5" (16:9) Full HD antreflets-Rétroéclairage par LED.

Ecran tactile

Résolution:1920x1080 Pixels (FHD)

chargeur& batterie original autonomie 2h~3h.

clavier:rétroéclairé : Oui .

Haut-parleurs:stéréo, double tableau de microphone .

Lecteur d'empreinte digitale  :non en option.

Ports:3 USB 3.0/1 USB type C /HDMI/LAN/Prise combo/ casque/microphone/Socle/Lecteur de carte SD.

Poids :1.36 KG

Couleur produit :Noir

Remis à neuf

SKU: DE014CL0350CPNAFAMZSKU

Modèle: Latitude 7280Modèle

Poids (kg): 2Poids (kg)

Couleur: NoirCouleur

Processeur Intel Core i5-5200U (Dual-Core 1.9 GHz / 2.6 GHz Turbo - cache 3 Mo)

16 Go de mémoire DDR3L

Ecran de 14" avec résolution HD+ (1600 x 900)

Sortie mini DisplayPort, pour le raccordement à un écran HD

Disque dur de 500 HDD

Clavier "Thinkpad Precision" avec touches rétro-éclairées QWERTY

2 ports USB 3.0 (dont 1 avec fonction "always on" : toujours alimenté même si le PC est éteint)

Communication sans fil performante : Wi-Fi AC + Bluetooth 4.0

Haut-parleurs intégrés avec technologie Dolby Home Theater v

SKU: LE018CL15D8UENAFAMZSKU

Gamme de produits: professionnelGamme de produits

Modèle: T450Modèle

Pays de production: USAPays de production

Taille (Longueur x Largeur x Hauteur cm): Hauteur : 3,2 cm // Largeur : 33,8 cm // Profondeur : 23,2 cmTaille (Longueur x Largeur x Hauteur cm)

Poids (kg): 2Poids (kg)

Couleur: noirCouleur

Matière principale: carbonMatière principale

Type de boutique: Jumia Mall/FoodType de boutique

Remis à neuf

Processeur : Intel Xeon E-2176M (12 Cpus)

Clavier AZERTY

Mémoire vive (RAM) : 32 Go (extensible jusqu'à 128 Go)

Stockage : SSD de 512 Go

Carte graphique : NVIDIA Quadro P4200 avec 8 Go de mémoire vidéo

Écran : 17,3 pouces

Système d'exploitation : Windows 10 Pro

Connectivité : Wi-Fi, Bluetooth, USB-C, HDMI, Ethernet, lecteur de carte SD

Sécurité : Authentification d'empreintes digitales

SKU: LE018CL0JDUSQNAFAMZSKU

Modèle: P72Modèle

Taille (Longueur x Largeur x Hauteur cm): 41,6 x 28,1 x 2,59~3,1Taille (Longueur x Largeur x Hauteur cm)

Poids (kg): 3,4Poids (kg)

Couleur: NoirCouleur

Nom : HP EliteBook 850 G3 3.4GHz i7-6500U 14\" 1920 x 1080pixels Argent

Marque : HP

processeur :  Intel Core i7 6500U - 3.4 Ghz - 4 Threads

Capacité disque dur :  1TB SSD

Ram DDR4 32 Gb

Fréquence du processeur Turbo : 3,4 GHz

Type HD : Full HD

Modèle d'adaptateur graphique à bord Intel® HD Graphics 520

Microphone intégré :  Oui

Fabricant de haut-parleurs :  Bang & Olufsen

Nombre de haut-parleurs intégrés :  2

Caméra avant :  Oui

Standards wifi :  802.11a, 802.11ac, 802.11b, 802.11g

Bluetooth :  Oui

Version du Bluetooth :  4.2

Wifi :  Oui

Système d'exploitation :  Windows 10 Pro

Architecture du système d'exploitation :  64-bit

garantie : 6 MOIS

Remis a neuf

SKU: HP017CL0EH47YNAFAMZSKU

Gamme de produits: ProfGamme de produits

Modèle: 850 G3Modèle

Pays de production: USAPays de production

Poids (kg): 1.5Poids (kg)

Couleur: GRISCouleur

Matière principale: aluminiumMatière principale

Type de boutique: Jumia MallType de boutique

Model: Lenovo ThinkPad T440

État    :Remis a neuf

Taille de l'écran : 14p  de résolution

Processeur :Intel core i5_4200u (Dual-Core 1.6 GHz / 2.6 GHz Turbo - cache 3 Mo)

Ram : 4 Go DDR3

Disque dur : 500G HDD

Carte graphique : Intel® HD Graphics

Garantie :6 Mois

OS : Windows 10 Pro 64Bits

Clavierrétro éclairé.qwerty

Poids : 1.80 Kg

SKU: BR621CL02XHMKNAFAMZSKU

Gamme de produits: Pc Portable ProfessionalGamme de produits

Modèle: T440Modèle

Pays de production: USA, ChinaPays de production

Poids (kg): 1.8Poids (kg)

Couleur: noirCouleur

Matière principale: carbonMatière principale

Type de boutique: Jumia Mall/FoodType de boutique

DESIGN INCROYABLEMENT FIN – Le MacBook Air repensé est plus portable que jamais et ne pèse que 1,24 kg. Il est capable de tout et vous permet de travailler, de jouer ou de créer sans limite, et de partout.

BOOSTÉ PAR LA PUCE M2 – Une efficacité accrue grâce à un CPU 8 cœurs nouvelle génération, un GPU 8 cœurs et 8 Go de mémoire unifiée.

JUSQU’À 18 HEURES D’AUTONOMIE – La batterie vous accompagne tout au long de la journée – et une partie de la nuit – grâce aux performances énergétiques de 
la puce Apple M2.

GRAND ÉCRAN SPECTACULAIRE – L’écran Liquid Retina de 13,6 pouces offre plus de 500 nits de luminosité, une large gamme de couleurs P3 et la prise en charge d’un milliard de couleurs pour des images éclatantes et un niveau de détail impressionnant.

CAMÉRA ET AUDIO AVANCÉS – Une caméra FaceTime HD 1080p, un ensemble de trois micros et un système audio à quatre haut-parleurs avec audio spatial pour que 
tout soit clair, net, précis.

SKU: AP009CL0ACMO8NAFAMZSKU

Gamme de produits: Produits pour tous les âges et tous les sexes, Generation SilverGamme de produits

Modèle: MacBook Air avec puce M2 QWERTY EspagnolModèle

Pays de production: European UnionPays de production

Taille (Longueur x Largeur x Hauteur cm): 21,5 x 30,41 x 1,13Taille (Longueur x Largeur x Hauteur cm)

Poids (kg): 1.24Poids (kg)

Couleur: Space GreyCouleur

Matière principale: AluminiumMatière principale

Model :  Dell XPS 15 9520

Ecran : 15.6 FHD+ de résolution 1920 x 1200

Processeur : Intel® Core™ i7-12700H de 12e génération (cache de 24 Mo, 14 cœurs, 20 threads, jusqu’à 4,70 GHz Turbo)

RAM : 32Go DDR5, 4800 MHz on board

Disque dur : 1TB SSD  100% flash Extensible .

Clavier: Azerty rétroéclairé

OS : Windows 11 pro

Carte graphique : NVIDIA GeForce RTX 3050  4 Go GDDR6/Intel® Iris® Xe Graphics

Ports : 1 USB 3.2 Gen 2 Type-C™ (avec DisplayPort et PowerDelivery); 2 Thunderbolt™ 4 (USB Type-C™) avec DisplayPort et Power Delivery; 1 Prise combinée casque/microphone 3,5 mm

Dimensions (L x P x H) : 1.854 x 34.440 x 23.010 cm

Poids : 1,92kg

Garantie 24 mois Pro support.

Produit Neuf.

SKU: DE014CL1K6SRYNAFAMZSKU

Modèle: Dell xps 15 9520Modèle

Taille (Longueur x Largeur x Hauteur cm): 1.854 x 34.440 x 23.010Taille (Longueur x Largeur x Hauteur cm)

Poids (kg): 1.92Poids (kg)

Couleur: ArgentCouleur

CPU : Intel Core i7-8665U (8 éme Géneration)

(1,90 GHz up to 4,80 GHz,4C/8T, 8 Mo Cache)

RAM : 16 Go DDR4

SSD : 256 Go M.2

GPU : Intel UHD Graphics 620

Ecran : 13,3 Pouces Full HD (1920 x 1080) Tactile

Clavier : QWERTY"""]
text=text[0].split('\n')
for textt in text :
    print(textt)
    print(extract(textt))