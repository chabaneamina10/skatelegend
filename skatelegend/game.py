from joueurs import j1,j2,j_pioche2,j_pioche1,piocherj,rejouer,visible,m1,m2,ajout_main,pioche1,pioche2,changement_joueurs
import pygame
from poscartes import pile1_rect,pile2_rect
from ui import afficher_cartesface
rouge=0
vert=0
bleu=0
jaune=0
cassé=0

#verification
def verifierj(j):
    if len(j)<=2:
        return True
    else:
        for i in range(len(j)):
            if j[i]["couleur"]=="rouge":
                rouge+=1
            elif j[i]["couleur"]=="bleu":
                bleu+=1
            elif j[i]["couleur"]=="jaune":
                jaune+=1
            else:
                vert+=1
            if j[i]["cassé"]==1:     
                cassé+=1
        if rouge>=3 or vert>=3 or jaune>=3 or bleu>=3  or cassé>=3:
            return False
        else:
            return True   

def partie(joueur,pioche,screen,event):
  
    if visible(joueur):
                    
                   
                    if pile1_rect.collidepoint(event.pos): 
                        afficher_cartesface(screen,pioche1)
                    if pile2_rect.collidepoint(event.pos):
                        afficher_cartesface(screen,pioche2)          
    elif piocherj(joueur):
            if joueur==j1:
                ajout_main(m1,pioche)
            else:
           
                 ajout_main(m2,pioche) 
                  
    #if rejouer(joueur):
    
        
          
   
def carte_avantvisible(pioche):
    
    carte=pioche[len(pioche)-1]
    return carte 
def  while_visible(pioche,carte):
    if pioche[len(pioche)-1]==carte:
        return True
    else:
        return False
         
         





            
        
    
        

