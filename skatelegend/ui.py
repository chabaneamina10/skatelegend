import pygame
from cards import creation_pioches,liste_cartes,bg1,cartes_legendaires,creation_piocheleg,cl10,cas
from joueurs import j1,j2,pioche1,pioche2,distribution


piochelegp,piocheleg=creation_piocheleg(cartes_legendaires)
lenp1=len(pioche1)
lenp2=len(pioche2)

def afficher_cartesbg1(screen):
    screen.blit(bg1, (300,50))

def afficher_cartesbg2(screen):    
    screen.blit(bg1, (900,50))
    
def afficher_cartesface(screen,pioche):
    if pioche==pioche1:
        screen.blit(pioche[len(pioche)-1]["image"],(300,50))
    else:
        screen.blit(pioche[len(pioche)-1]["image"],(900,50))


def afficher_cartesleg(screen):
    screen.blit(piochelegp[0]["image"],(490,50))
    screen.blit(piochelegp[1]["image"],(565,50))
    screen.blit(piochelegp[2]["image"],(640,50))
    screen.blit(cl10,(715,50))


def afficher_cartesj1(screen):
    for i in range(len(j1)):
        screen.blit(j1[i]["image"],(100+i*40,400))
def afficher_cartesj2(screen,):
    for i in range(len(j2)):
        screen.blit(j2[i]["image"],(700+i*40,400))   
  

    

   
def afficher_cas(screen):
   
    screen.blit(cas,(490,310))
    screen.blit(cas,(550,310))
    screen.blit(cas,(610,310))
    screen.blit(cas,(670,310))
    screen.blit(cas,(730,310))
    screen.blit(cas,(790,310))
    


