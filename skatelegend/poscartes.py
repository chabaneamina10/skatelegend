import pygame

liste1=[]
liste2=[]
liste3=[]
liste4=[]
liste5=[]

pile1_rect = pygame.Rect(300, 10, 100, 170)
pile2_rect = pygame.Rect(900,10,100, 170)
pile1_rect4 = pygame.Rect(300, 300, 100, 170)
pile2_rect4 = pygame.Rect(500,300,100, 170)
button_rect=pygame.Rect(1000,600,80,50)
continuer_rect=pygame.Rect(1090,600,90,50)
exit_rect=pygame.Rect(1200,600,90,50)
casque_rect=pygame.Rect(900,600,90,50)
rouge_rect=pygame.Rect(900,570,70,20)
vert_rect=pygame.Rect(900,540,70,20)
jaune_rect=pygame.Rect(900,500,70,20)
bleu_rect=pygame.Rect(900,470,70,20)


def initmains():
    
    m1carte1=pygame.Rect(100,480,130,170)
    m1carte2=pygame.Rect(240,480,130,170)
    m1carte3=pygame.Rect(380,480,130,170)
    m1carte4=pygame.Rect(410,480,130,170)

    liste1.clear()
    liste1.append(m1carte1)
    liste1.append(m1carte2)
    liste1.append(m1carte3)
    liste1.append(m1carte4)

    
    return liste1





