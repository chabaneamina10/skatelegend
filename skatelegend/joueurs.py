from cards import creation_pioches,liste_cartes
import pygame
pioche1,pioche2=creation_pioches(liste_cartes)
j1=[]
j2=[]
m1=[]
m2=[]

def distribution():
    j1.append(pioche1[len(pioche1)-1])
    pioche1.pop()
    j2.append(pioche1[len(pioche1)-1])
    pioche1.pop()
    return j1,j2

taille_carte=(100,200)
for carte in j1:
    carte["image"]=pygame.transform.scale(carte["image"], taille_carte)
for carte in j2:
    carte["image"]=pygame.transform.scale(carte["image"], taille_carte)    
def j_pioche1(j):
    j.append(pioche1[len(pioche1)-1])
    pioche1.pop()
    return j

def j_pioche2(j):
    j.append(pioche2[len(pioche2)-1])
    pioche2.pop()
    return j
  
def piocherj(j):
    if j[len(j)-1]["piocher"]==1:
        return True
    else:
        return False    
def rejouer(j):
    if j[len(j)-1]["rejouer"]==1:
        return True
    else:
        return False
     
def visible(j):
    if j[len(j)-1]["visible"]==1:
        return True
    else:
        return False

def ajout_main(m:list,pioche:list):
    m.append(pioche[len(pioche)-1])
    pioche.pop()    

def changement_joueurs(joueur):
    if joueur=="j1":
        joueur="j2"
    else:
        joueur="j1"
    return joueur 
def quijoue(joueur):
    if joueur=="j1":
        return j1
    else:
        return j2       
 