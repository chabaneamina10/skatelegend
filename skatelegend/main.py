import pygame
from ui import afficher_cartesbg1,afficher_cartesbg2
from ui import afficher_cartesleg,afficher_cas,afficher_cartesj1,afficher_cartesj2,lenp1,lenp2,afficher_cartesface
from poscartes import pile1_rect,pile2_rect
from sound import play_sound
from joueurs import changement_joueurs,j_pioche2,j_pioche1,piocherj,rejouer,visible,m1,m2,ajout_main,pioche1,pioche2,quijoue,distribution

from game import partie,while_visible,carte_avantvisible
pygame.init()
screen=pygame.display.set_mode((1280,720),pygame.FULLSCREEN)
pygame.display.set_caption("skatelegend")
background=pygame.image.load("../assets/bg.jpg")      
running=True
joueur="j1"
cle="affichage"
vis=None
carte=None
distribution()
while running:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        
        if event.type==pygame.QUIT:
            running=False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            

            if cle=="affichage" :
                j=quijoue(joueur)
                
                
                if pile1_rect.collidepoint(event.pos):
                    pioche=pioche1
                    play_sound()
                    j_pioche1(j)
                    
                        

                if pile2_rect.collidepoint(event.pos):
                    pioche=pioche2
                    play_sound()
                    j_pioche2(j)
                    
              
                      
                if rejouer(j):
                    joueur=changement_joueurs(changement_joueurs(joueur))
                elif visible(j):
                    cle="visible"
                    
                else:                        
                    joueur=changement_joueurs(joueur) 
                    vis=None    
            elif cle=="visible":
                    if event.button==1:      
                        if pile1_rect.collidepoint(event.pos):
                            vis="p1"
                            cle="affichage"
                            carte=carte_avantvisible(pioche1)
                        elif pile2_rect.collidepoint(event.pos):
                            vis="p2" 
                            cle="affichage"
                            carte=carte_avantvisible(pioche2)
        
    
                     
    if vis=="p1" or while_visible(pioche1,carte):
        afficher_cartesbg2(screen)
        afficher_cartesface(screen,pioche1)
        

    elif vis=="p2" or while_visible(pioche2,carte):
        afficher_cartesbg1(screen)
        afficher_cartesface(screen,pioche2)
    else:
        afficher_cartesbg1(screen)
        afficher_cartesbg2(screen)
    afficher_cartesj1(screen)
    afficher_cartesj2(screen)  
    afficher_cartesleg(screen) 
    afficher_cas(screen)
    
    
    
    
    pygame.display.flip()
    
pygame.quit()    

       