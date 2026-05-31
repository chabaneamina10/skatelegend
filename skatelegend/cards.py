import random
import pygame
cartes = (
    12*[{"nom": "manual"      , "couleur": "rouge", "récompense": 1, "piocher": 0, "rejouer": 0, "visible":0, "cassé":0, "condition":None}] +
    22*[{"nom": "no comply"   , "couleur": "rouge", "récompense": 1, "piocher": 1, "rejouer": 0, "visible":0, "cassé":0, "condition":None}] +
    2 *[{"nom": "no comply"   , "couleur": "rouge", "récompense": 1, "piocher": 0, "rejouer": 0, "visible":0, "cassé":1, "condition":None}] +
    16*[{"nom": "melon grab"  , "couleur": "bleu" , "récompense": 1, "piocher": 0, "rejouer": 0, "visible":0, "cassé":0, "condition":None}] +
    10*[{"nom": "handplant"   , "couleur": "bleu" , "récompense": 1, "piocher": 0, "rejouer": 0, "visible":1, "cassé":0, "condition":None}] +
    6 *[{"nom": "handplant"   , "couleur": "bleu" , "récompense": 1, "piocher": 0, "rejouer": 0, "visible":0, "cassé":1, "condition":None}] +
    10*[{"nom": "ollie"       , "couleur": "vert" , "récompense": 1, "piocher": 0, "rejouer": 0, "visible":0, "cassé":0, "condition":None}] +
    12*[{"nom": "pop shove-it", "couleur": "vert" , "récompense": 1, "piocher": 0, "rejouer": 1, "visible":0, "cassé":0, "condition":None}] +
    6 *[{"nom": "pop shove-it", "couleur": "vert" , "récompense": 1, "piocher": 0, "rejouer": 0, "visible":0, "cassé":1, "condition":None}] +
    12*[{"nom": "powerslide"  , "couleur": "jaune", "récompense": 2, "piocher": 0, "rejouer": 0, "visible":0, "cassé":1, "condition":None}] +
    12*[{"nom": "boardslide"  , "couleur": "jaune", "récompense": 1, "piocher": 0, "rejouer": 0, "visible":0, "cassé":0, "condition":None}]
)

cartes_legendaires = [
    {"nom": "1080°"        , "couleur": None   , "récompense": 4, "piocher": 0, "rejouer": 0, "visible":0, "cassé":0, "condition": "3 couleurs dif"},
    {"nom": "360°"         , "couleur": None   , "récompense": 4, "piocher": 0, "rejouer": 0, "visible":0, "cassé":0, "condition": "2 rouges"},
    {"nom": "900°"         , "couleur": None   , "récompense": 4, "piocher": 0, "rejouer": 0, "visible":0, "cassé":0, "condition": "1 jaune 1 verte"},
    {"nom": "180°"         , "couleur": None   , "récompense": 4, "piocher": 0, "rejouer": 0, "visible":0, "cassé":0, "condition": "4 couleurs"},
    {"nom": "720°"         , "couleur": None   , "récompense": 4, "piocher": 0, "rejouer": 0, "visible":0, "cassé":0, "condition": "5 couleurs"},
    {"nom": "air walk grab", "couleur": "bleu" , "récompense": 4, "piocher": 0, "rejouer": 0, "visible":1, "cassé":0, "condition": "2 skates cassés"},
    {"nom": "kick flip"    , "couleur": "vert" , "récompense": 5, "piocher": 0, "rejouer": 2, "visible":0, "cassé":0, "condition": None},
    {"nom": "casper slide" , "couleur": "jaune", "récompense": 4, "piocher": 0, "rejouer": 0, "visible":0, "cassé":1, "condition": "2 cartes même couleur"},
    {"nom": "hippy jump"   , "couleur": "rouge", "récompense": 2, "piocher": 2, "rejouer": 0, "visible":0, "cassé":0, "condition": None}

]
perfect_landing = {"nom": "perfect landing", "couleur": None, "récompense": 5, "piocher": 0, "rejouer": 0, "visible":0, "cassé":0, "condition": None}
liste_cartes=list(cartes)
carte1 = pygame.image.load("../assets/cartes/carte1.png")
carte2 = pygame.image.load("../assets/cartes/carte2.png")
carte3 = pygame.image.load("../assets/cartes/carte3.png")
carte4 = pygame.image.load("../assets/cartes/carte4.png")
carte5 = pygame.image.load("../assets/cartes/carte5.png")
carte6 = pygame.image.load("../assets/cartes/carte6.png")
carte7 = pygame.image.load("../assets/cartes/carte7.png")
carte8 = pygame.image.load("../assets/cartes/carte8.png")
carte9 = pygame.image.load("../assets/cartes/carte9.png")
carte10 = pygame.image.load("../assets/cartes/carte10.png")
carte11 = pygame.image.load("../assets/cartes/carte11.png")
cl1=pygame.image.load("../assets/carteleg/cl1.png")
cl3=pygame.image.load("../assets/carteleg/cl3.png")
cl2=pygame.image.load("../assets/carteleg/cl2.png")
cl4=pygame.image.load("../assets/carteleg/cl4.png")
cl5=pygame.image.load("../assets/carteleg/cl5.png")
cl6=pygame.image.load("../assets/carteleg/cl6.png")
cl7=pygame.image.load("../assets/carteleg/cl7.png")
cl8=pygame.image.load("../assets/carteleg/cl8.png")
cl9=pygame.image.load("../assets/carteleg/cl9.png")
cl10=pygame.image.load("../assets/carteleg/cl10.png")


bg = pygame.image.load("../assets/cartesbg/noskate.png")


for i in range(12):
    liste_cartes[i]["image"] = carte1

for i in range(12, 34):
    liste_cartes[i]["image"] = carte2

for i in range(34, 36):
    liste_cartes[i]["image"] = carte3

for i in range(36, 52):
    liste_cartes[i]["image"] = carte4

for i in range(52, 62):
    liste_cartes[i]["image"] = carte5

for i in range(62, 68):
    liste_cartes[i]["image"] = carte6

for i in range(68, 78):
    liste_cartes[i]["image"] = carte7

for i in range(78, 90):
    liste_cartes[i]["image"] = carte8

for i in range(90, 96):
    liste_cartes[i]["image"] = carte9

for i in range(96, 108):
    liste_cartes[i]["image"] = carte10

for i in range(108, 120):
    liste_cartes[i]["image"] = carte11

for i in range(len(liste_cartes)):
    liste_cartes[i]["bgimage"] = bg
#taille_carte = (130, 250)
taille_carte=(90,160)



for carte in liste_cartes:
    carte["image"] = pygame.transform.scale(carte["image"], taille_carte)
bg1=pygame.image.load("../assets/cartesbg/noskate.png")    
bg1=pygame.transform.scale(bg1, taille_carte)   
bg2= pygame.image.load("../assets/cartesbg/skate.png") 
bg2=pygame.transform.scale(bg2, taille_carte)   
def creation_pioches(liste_cartes):
    copie=liste_cartes
    random.shuffle(copie)
    milieu=len(copie)//2
    pioche1=copie[:milieu]
    pioche2=copie[milieu:]
    return pioche1,pioche2

def creation_piocheleg(cartes_legendaires):
    copie=cartes_legendaires
    random.shuffle(copie)
    pile_a_presenter=copie[:3]
    pile_reste=copie[3:]
    return pile_a_presenter,pile_reste

cartes_legendaires[0]["image"]=cl5
cartes_legendaires[1]["image"]=cl7
cartes_legendaires[2]["image"]=cl9
cartes_legendaires[3]["image"]=cl6
cartes_legendaires[4]["image"]=cl8
cartes_legendaires[5]["image"]=cl4
cartes_legendaires[6]["image"]=cl1
cartes_legendaires[7]["image"]=cl2
cartes_legendaires[8]["image"]=cl3
perfect_landing["image"]=cl10


for carte in cartes_legendaires:
    carte["image"] = pygame.transform.scale(carte["image"], taille_carte)
cl10=pygame.transform.scale(cl10, taille_carte)     
cas=pygame.image.load("../assets/cas.png") 
cas=pygame.transform.scale(cas,(50,50))  
perfect_landing["image"]=pygame.transform.scale(perfect_landing["image"],taille_carte)
