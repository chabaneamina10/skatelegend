import pygame
from cards import bg1,cas

def textescore(score1, score2, score3, score4, score5, nbjoueurs):
    font = pygame.font.SysFont("Gagalin", 15)
    texte1 = font.render(f"{score1} point(s)", True, (255, 255, 255))
    texte2 = font.render(f"{score2} point(s)", True, (255, 255, 255))
    texte3 = font.render(f"{score3} point(s)", True, (255, 255, 255))
    texte4 = font.render(f"{score4} point(s)", True, (255, 255, 255))
    texte5 = font.render(f"{score5} point(s)", True, (255, 255, 255))
    if nbjoueurs == 2:
        return texte1, texte2
    elif nbjoueurs == 3:
        return texte1, texte2, texte3
    elif nbjoueurs == 4:
        return texte1, texte2, texte3, texte4
    else:
        return texte1, texte2, texte3, texte4, texte5

def interface(screen, background, texte1, texte2, texte3, texte4, texte5, nbjoueurs):
    # Afficher le fond d'écran
    screen.blit(background, (0, 0))
    
    # Dimensions de la zone scores
    x, y = 20, 0
    largeur = 220
    hauteur = 40
    espacement = 48
    
    # Liste des textes à afficher
    textes = []
    if nbjoueurs >= 1:
        textes.append(("Joueur 1", texte1))
    if nbjoueurs >= 2:
        textes.append(("Joueur 2", texte2))
    if nbjoueurs >= 3:
        textes.append(("Joueur 3", texte3))
    if nbjoueurs >= 4:
        textes.append(("Joueur 4", texte4))
    if nbjoueurs >= 5:
        textes.append(("Joueur 5", texte5))
    
    for i, (nom, texte) in enumerate(textes):
        rect = pygame.Rect(x, y + i * espacement, largeur, hauteur)
        
        # Fond bleu foncé (comme rec)
        pygame.draw.rect(screen, (5, 8, 25), rect, width=0, border_radius=8)
        # Cadre bleu clair
        pygame.draw.rect(screen, (25, 45, 80), rect, width=2, border_radius=8)
        
        # Nom du joueur
        font_nom = pygame.font.SysFont("Arial", 14, bold=True)
        txt_nom = font_nom.render(nom, True, (200, 210, 240))
        screen.blit(txt_nom, (rect.x + 10, rect.y + 12))
        
        # Score
        screen.blit(texte, (rect.x + largeur - 80, rect.y + 12))

def manche(screen, p, text1, text2, text3, text4, text5, nbjoueurs):
    W, H = 1280, 720
    
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    
    font_title = pygame.font.SysFont("Arial Black", 42, bold=True)
    titre = f"MANCHE {p+1} - TERMINÉE"
    titre_render = font_title.render(titre, True, (255, 200, 50))
    screen.blit(titre_render, titre_render.get_rect(centerx=W // 2, y=150))
    
    pygame.draw.line(screen, (255, 200, 50), (W//2 - 200, 200), (W//2 + 200, 200), 2)
    
    font_name = pygame.font.SysFont("Arial", 24, bold=True)
    
    y_start = 260
    if nbjoueurs == 2:
        y_start = 280
    elif nbjoueurs == 3:
        y_start = 260
    elif nbjoueurs == 4:
        y_start = 230
    else:
        y_start = 200

    def draw_score_row(num, texte_score, y, color):
        row_rect = pygame.Rect(W//2 - 250, y - 15, 500, 45)
        pygame.draw.rect(screen, (30, 35, 55, 200), row_rect, border_radius=10)
        pygame.draw.rect(screen, color, row_rect, 2, border_radius=10)
        
        nom = font_name.render(f"Joueur {num}", True, (255, 255, 255))
        screen.blit(nom, (W//2 - 200, y))
        screen.blit(texte_score, (W//2 + 100, y))
    
    if nbjoueurs == 2:
        draw_score_row(1, text1, y_start, (255, 100, 100))
        draw_score_row(2, text2, y_start + 70, (100, 150, 255))
    elif nbjoueurs == 3:
        draw_score_row(1, text1, y_start, (255, 100, 100))
        draw_score_row(2, text2, y_start + 65, (100, 150, 255))
        draw_score_row(3, text3, y_start + 130, (100, 255, 100))
    elif nbjoueurs == 4:
        draw_score_row(1, text1, y_start, (255, 100, 100))
        draw_score_row(2, text2, y_start + 60, (100, 150, 255))
        draw_score_row(3, text3, y_start + 120, (100, 255, 100))
        draw_score_row(4, text4, y_start + 180, (255, 200, 100))
    else:
        draw_score_row(1, text1, y_start, (255, 100, 100))
        draw_score_row(2, text2, y_start + 60, (100, 150, 255))
        draw_score_row(3, text3, y_start + 120, (100, 255, 100))
        draw_score_row(4, text4, y_start + 180, (255, 200, 100))
        draw_score_row(5, text5, y_start + 250, (255, 128, 0))
    
    small = pygame.font.SysFont("Arial", 14)
    continuer = small.render("Appuyez sur une touche pour continuer...", True, (150, 160, 190))
    screen.blit(continuer, continuer.get_rect(centerx=W//2, y=H - 50))
    
    pygame.display.flip()
    pygame.time.wait(2500)

def afficher_cartesbg1(screen):
   
    screen.blit(bg1, (300, 10))
    

def afficher_cartesbg2(screen):
   
    screen.blit(bg1, (900, 10))
   

def afficher_cartesleg(screen, cartes_affichees, perfect_landing):
    
    positions = [490, 565, 640]
    for i, carte in enumerate(cartes_affichees[:3]):
        screen.blit(carte["image"], (positions[i], 10))
    # Afficher Perfect Landing
    screen.blit(perfect_landing["image"], (715, 10))

def afficher_cartesjoueurs(screen, j):
    for i in range(len(j)):
        screen.blit(j[i]["image"], (100 + i * 120, 270))

def afficher_cas(screen):
    positions = [490, 550, 610, 670, 730, 790]
    for pos in positions:
        screen.blit(cas, (pos, 200))

def afficher_mains(screen, m):
    if m:
        for i in range(len(m)):
            screen.blit(m[i]["image"], (100 + i * 120, 480))

def textesmanche(score1, score2, score3, score4, score5, nbjoueurs):
    font = pygame.font.SysFont("Gagalin", 27)
    texte1 = font.render(f"{score1} point(s)", True, (255, 255, 255))
    texte2 = font.render(f"{score2} point(s)", True, (255, 255, 255))
    texte3 = font.render(f"{score3} point(s)", True, (255, 255, 255))
    texte4 = font.render(f"{score4} point(s)", True, (255, 255, 255))
    texte5 = font.render(f"{score5} point(s)", True, (255, 255, 255))

    if nbjoueurs == 2:
        return texte1, texte2
    elif nbjoueurs == 3:
        return texte1, texte2, texte3
    elif nbjoueurs == 4:
        return texte1, texte2, texte3, texte4
    else:
        return texte1, texte2, texte3, texte4, texte5

def draw_game_buttons(screen, button_rect, continuer_rect, exit_rect):
    font = pygame.font.SysFont("Arial", 16)
    surf_stop = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
    surf_stop.fill((0, 0, 0, 150))
    screen.blit(surf_stop, button_rect)
    txt_stop = font.render("STOP", True, (255, 70, 70))
    screen.blit(txt_stop, txt_stop.get_rect(center=button_rect.center))
    
    surf_cont = pygame.Surface((continuer_rect.width, continuer_rect.height), pygame.SRCALPHA)
    surf_cont.fill((0, 0, 0, 150))
    screen.blit(surf_cont, continuer_rect)
    txt_cont = font.render("CONTINUER", True, (70, 255, 70))
    screen.blit(txt_cont, txt_cont.get_rect(center=continuer_rect.center))

    surf_exit = pygame.Surface((exit_rect.width, exit_rect.height), pygame.SRCALPHA)
    surf_exit.fill((0, 0, 0, 150))
    screen.blit(surf_exit, exit_rect)
    exit_txt = font.render("EXIT", True, (0, 100, 250))
    screen.blit(exit_txt, exit_txt.get_rect(center=exit_rect.center))
def draw_casque(screen, casque_rect, nb_casques):
    font = pygame.font.SysFont("Arial", 14)
    surf_casque = pygame.Surface((casque_rect.width, casque_rect.height), pygame.SRCALPHA)
    surf_casque.fill((0, 0, 0, 150))
    screen.blit(surf_casque, casque_rect)
    txt = font.render(f"CASQUE x{nb_casques}", True, (255, 180, 50))
    screen.blit(txt, txt.get_rect(center=casque_rect.center))
    
##design arr cartes

def rec(screen):
    w_combo = 980
    h_combo = 190
    w_main = 700
    h_main = 190
    x_combo = 90
    x_main = 90
    y_combo = 260
    y_main = 470
    pygame.draw.rect(screen, (5, 8, 25), (x_combo, y_combo, w_combo, h_combo), width=0, border_radius=12)
    pygame.draw.rect(screen, (25, 45, 80), (x_combo, y_combo, w_combo, h_combo), width=2, border_radius=12)
    font_title = pygame.font.SysFont("Arial", 16, bold=True)
    titre = font_title.render("ENCHAÎNEMENT", True, (60, 90, 130))
    screen.blit(titre, (x_combo + 15, y_combo - 20)) 
    pygame.draw.rect(screen, (5, 8, 25), (x_main, y_main, w_main, h_main), width=0, border_radius=12)
    pygame.draw.rect(screen, (25, 45, 80), (x_main, y_main, w_main, h_main), width=2, border_radius=12)
    titre_main = font_title.render("MAIN DU JOUEUR", True, (60, 90, 130))
    screen.blit(titre_main, (x_main + 15, y_main - 20))
def couleurs(screen, rouge_rect, vert_rect, jaune_rect, bleu_rect):
    font = pygame.font.SysFont("Arial", 16, bold=True)
    c1 = font.render("Rouge", True, (255, 0, 0))
    c2 = font.render("Vert", True, (0, 255, 0))
    c3 = font.render("Jaune", True, (255, 255, 0))
    c4 = font.render("Bleu", True, (0, 100, 255))
    pygame.draw.rect(screen, (200, 50, 50), rouge_rect)
    pygame.draw.rect(screen, (50, 200, 50), vert_rect)
    pygame.draw.rect(screen, (200, 200, 50), jaune_rect)
    pygame.draw.rect(screen, (50, 100, 200), bleu_rect)
    c1_rect = c1.get_rect(center=rouge_rect.center)
    c2_rect = c2.get_rect(center=vert_rect.center)
    c3_rect = c3.get_rect(center=jaune_rect.center)
    c4_rect = c4.get_rect(center=bleu_rect.center)
    screen.blit(c1, c1_rect)
    screen.blit(c2, c2_rect)
    screen.blit(c3, c3_rect)
    screen.blit(c4, c4_rect)


def afficher_commentaires(screen, commentaires):
    boite = pygame.Rect(1000, 10, 250, 180)
    pygame.draw.rect(screen, (5, 8, 25), boite, width=0, border_radius=12)
    pygame.draw.rect(screen, (25, 45, 80), boite, width=2, border_radius=12)
    # Titre
    font_title = pygame.font.SysFont("Arial", 14, bold=True)
    titre = font_title.render("ACTIONS", True, (60, 90, 130))
    screen.blit(titre, (boite.x + 10, boite.y + 5))
    pygame.draw.line(screen, (25, 45, 80), (boite.x + 10, boite.y + 22), (boite.x + boite.width - 10, boite.y + 22), 1)
    # Afficher les commentaires
    font_comment = pygame.font.SysFont("Arial", 11)
    y_offset = 32
    for comment in commentaires[-6:]:
        if len(comment) > 32:
            comment = comment[:29] + "..."
        
        # Couleurs des textes
        if "chute" in comment.lower():
            color = (255, 80, 80)      
        elif "stop" in comment.lower() or "arrêté" in comment.lower():
            color = (80, 255, 80)      
        elif "carte" in comment.lower():
            color = (255, 220, 80)   
        elif "casque" in comment.lower():
            color = (80, 180, 255)    
        elif "tour" in comment.lower():
            color = (255, 180, 80)     
        else:
            color = (160, 170, 200)    
        texte = font_comment.render(comment, True, color)
        screen.blit(texte, (boite.x + 8, boite.y + y_offset))
        y_offset += 18
def joueur_chute(screen,numj,joueur,j):
    afficher_cartesjoueurs(screen, j)  # Force le dessin de l'enchaînement
    pygame.display.flip()
    chute_msg = pygame.font.SysFont("Arial", 18, bold=True)
    numj=joueur[1]
    cmsg = chute_msg.render(f" OPS! JOUEUR {numj} A CHUTÉ ! +1 CASQUE", True, (255, 200, 50))
    screen.blit(cmsg, (1280//2 - cmsg.get_width()//2, 200))
    pygame.display.flip()
    pygame.time.wait(2000)
#####################################################################################
ASSETS_PATH = "../assets" 

W, H = 1280, 720
FPS = 60

S_MENU, S_CONFIG, S_GAME, S_RESULTS = "menu", "config", "game", "results"
def draw_button(surf, fonts, text, rect, color, hover=False, disabled=False, fkey="bold"):

    if disabled:
        pygame.draw.rect(surf, (60, 60, 60), rect, border_radius=10)
        txt = fonts[fkey].render(text, True, (180, 180, 180))
        surf.blit(txt, txt.get_rect(center=rect.center))
        return

    # Effet hover
    if hover:
        color = tuple(min(255, c + 30) for c in color)

    # Ombre du bouton
    shadow_rect = rect.move(4, 4)
    pygame.draw.rect(surf, (0, 0, 0), shadow_rect, border_radius=10)

    # Bouton principal
    pygame.draw.rect(surf, color, rect, border_radius=10)

    # Contour clair
    border = tuple(min(255, c + 50) for c in color)
    pygame.draw.rect(surf, border, rect, 2, border_radius=10)

    # Ombre du texte
    shadow = fonts[fkey].render(text, True, (0, 0, 0))
    surf.blit(shadow, shadow.get_rect(center=(rect.centerx + 2, rect.centery + 2)))

    # Texte principal
    txt = fonts[fkey].render(text, True, (255, 255, 255))
    surf.blit(txt, txt.get_rect(center=rect.center))
import random
import math
import sys
# Couleurs pour l'interface menu/config
C = {
    "bg": (12, 18, 30),
    "gold": (255, 200, 50),
    "white": (255, 255, 255),
    "text": (255, 255, 255),
    "text_dim": (210,220,240),
    "btn_go": (28,36,58),
    "btn_stop": (90,55,30),
    "btn_dark": (38, 52, 82),
    "btn_pile": (65, 125, 205),
    "btn_helmet": (235, 165, 25),
    "border": (50, 70, 110),
    "panel": (22, 32, 52),
    "panel2": (30, 44, 72),
    "rouge": (220, 55, 75),
    "bleu": (55, 140, 230),
    "vert": (75, 190, 75),
    "jaune": (240, 190, 35),
    "danger": (255, 65, 65),
    "warn": (255, 165, 35),
    "safe": (65, 215, 95),
    "shadow":(0,0,0),
}
#particules
class particules:
    def __init__(self):
        self.reset()
        self.y = random.randint(0, H)
    
    def reset(self):
        self.x = random.randint(0, W)
        self.y = -10
        self.vy = random.uniform(0.3, 1.8)
        self.vx = random.uniform(-0.4, 0.4)
        self.r = random.randint(2, 5)
        self.col = random.choice([C["rouge"], C["bleu"], C["vert"], C["jaune"], C["gold"]])
        self.alpha = random.randint(55, 155)
        self.life = random.randint(60, 220)
        self.age = 0
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        if self.age > self.life or self.y > H + 10:
            self.reset()
    
    def draw(self, surf):
        s = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
        a = int(self.alpha * max(0, 1 - self.age / self.life))
        pygame.draw.circle(s, (*self.col, a), (self.r, self.r), self.r)
        surf.blit(s, (int(self.x - self.r), int(self.y - self.r)))

PARTS = [particules() for _ in range(55)]



def init_fonts():
    pygame.font.init()
    return {
        "huge": pygame.font.SysFont("Arial Black", 52, bold=True),
        "title": pygame.font.SysFont("Arial", 34, bold=True),
        "head": pygame.font.SysFont("Arial", 22, bold=True),
        "medium": pygame.font.SysFont("Arial", 15),
        "bold": pygame.font.SysFont("Arial", 14, bold=True),
        "tiny": pygame.font.SysFont("Arial", 10),
    }

def rr(surf, color, rect, r=8, border=0, bcol=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if border and bcol:
        pygame.draw.rect(surf, bcol, rect, border, border_radius=r)

def rr_alpha(surf, color, alpha, rect, r=8):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), s.get_rect(), border_radius=r)
    surf.blit(s, rect.topleft)

def gradient_rect(surf, rect, top, bot):
    steps = max(rect.height, 1)
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        col = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        pygame.draw.line(surf, col, (rect.x, rect.y + i), (rect.x + rect.width - 1, rect.y + i))

def draw_text_shadow(surface, font, text, color, shadow_color, pos):
    # Ombre
    shadow = font.render(text, True, shadow_color)
    surface.blit(shadow, (pos[0] + 2, pos[1] + 2))

    # Texte principal
    txt = font.render(text, True, color)
    surface.blit(txt, pos)

def draw_panel(surf, rect, title=None, fonts=None):
    rr(surf, C["panel"], rect, r=12, border=2, bcol=C["border"])
    if title and fonts:
        t = fonts["bold"].render(title.upper(), True, C["gold"])
        surf.blit(t, (rect.x + 10, rect.y + 8))


class MenuScreen:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.btn_play = pygame.Rect(W // 2 - 130, H // 2 + 30, 260, 58)
        self.btn_quit = pygame.Rect(W // 2 - 130, H // 2 + 110, 260, 48)
        self.hp = self.hq = False
        self.t = 0
        try:
            self.menu_bg = pygame.image.load("../assets/skater6.jpg")  # Votre chemin
            self.menu_bg = pygame.transform.scale(self.menu_bg, (W, H))
        except:
            self.menu_bg = None
    def handle_event(self, ev):
        if ev.type == pygame.MOUSEMOTION:
            self.hp = self.btn_play.collidepoint(ev.pos)
            self.hq = self.btn_quit.collidepoint(ev.pos)
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.btn_play.collidepoint(ev.pos):
                return S_CONFIG
            if self.btn_quit.collidepoint(ev.pos):
                pygame.quit()
                sys.exit()
        return None

    def update(self):
     
        
        self.t += 1

        for p in PARTS:
            p.update()

    def draw(self):
        s = self.screen

        # Background
        if self.menu_bg:
            s.blit(self.menu_bg, (0, 0))
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))  # voile noir semi-transparent
            s.blit(overlay, (0, 0))

            # Voile sombre pour lisibilité
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 50))
            s.blit(overlay, (0, 0))

        else:
            gradient_rect(s, s.get_rect(), (14, 22, 38), C["bg"])

        # Lignes décoratives
        for i in range(7):
            yl = i * H // 6
            ls = pygame.Surface((W, 1), pygame.SRCALPHA)
            ls.fill((*C["border"], 20))
            s.blit(ls, (0, yl))

        # Animation titre
        pulse = 0.04 * math.sin(self.t * 0.04)

        # Textes principaux
        sk = self.fonts["huge"].render("SKATE", True, (180, 190, 210))
        lg = self.fonts["huge"].render("LEGEND", True, (255, 235, 240))

        # Ombres
        shadow_sk = self.fonts["huge"].render("SKATE", True, (0, 0, 0))
        shadow_lg = self.fonts["huge"].render("LEGEND", True, (0, 0, 0))

        # Surface du titre
        ts = pygame.Surface((600, 140), pygame.SRCALPHA)

        # Ombres
        ts.blit(shadow_sk, shadow_sk.get_rect(centerx=303, y=3))
        ts.blit(shadow_lg, shadow_lg.get_rect(centerx=303, y=65))

        # Textes
        ts.blit(sk, sk.get_rect(centerx=300, y=0))
        ts.blit(lg, lg.get_rect(centerx=300, y=62))

        # Animation zoom
        sc = pygame.transform.smoothscale(
            ts,
            (int(600 * (1 + pulse)), int(140 * (1 + pulse)))
        )

        s.blit(sc, sc.get_rect(centerx=W // 2, centery=H // 2 - 120))

        # Sous-titre
        sub = self.fonts["medium"].render(
            "Un jeu Rose Noire Edition  •  2–5 joueurs",
            True,
            (240, 240, 240)
        )

        s.blit(sub, sub.get_rect(centerx=W // 2, y=H // 2 - 30))

        # Boutons
        draw_button(
            s,
            self.fonts,
            "JOUER",
            self.btn_play,
            C["btn_go"],
            self.hp,
            fkey="head"
        )

        draw_button(
            s,
            self.fonts,
            "QUITTER",
            self.btn_quit,
            C["btn_stop"],
            self.hq
        )

        # Version
        ver = self.fonts["tiny"].render(
            "Skate Legend © Rose Noire",
            True,
            (220, 220, 220)
        )

        s.blit(ver, (10, H - 18))

class ConfigScreen:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.num = 2
        self.names = ["Joueur 1", "Joueur 2", "Joueur 3", "Joueur 4","Joueur 5"]
        self.human = [True, True, True, True,False]
        self.active = None
        self.btn_start = pygame.Rect(W // 2 - 140, H - 100, 280, 55)
        self.btn_back = pygame.Rect(20, 20, 100, 38)
        self.btn_minus = pygame.Rect(W // 2 - 90, 145, 42, 42)
        self.btn_plus = pygame.Rect(W // 2 + 48, 145, 42, 42)
        self.hs = self.hb = False

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEMOTION:
            self.hs = self.btn_start.collidepoint(ev.pos)
            self.hb = self.btn_back.collidepoint(ev.pos)
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.btn_back.collidepoint(ev.pos):
                return S_MENU
            if self.btn_start.collidepoint(ev.pos):
                return S_GAME
            if self.btn_minus.collidepoint(ev.pos) and self.num > 2:
                self.num -= 1
            if self.btn_plus.collidepoint(ev.pos) and self.num < 5:
                self.num += 1
            self.active = None
            for i in range(self.num):
                if self._fr(i).collidepoint(ev.pos):
                    self.active = i
                if self._tr(i).collidepoint(ev.pos):
                    self.human[i] = not self.human[i]
        if ev.type == pygame.KEYDOWN and self.active is not None:
            if ev.key == pygame.K_BACKSPACE:
                self.names[self.active] = self.names[self.active][:-1]
            elif ev.key in (pygame.K_RETURN, pygame.K_TAB):
                self.active = None
            elif len(self.names[self.active]) < 14:
                self.names[self.active] += ev.unicode
        return None

    def get_config(self):
        return self.names[:self.num], self.human[:self.num]

    def _fr(self, i):
        return pygame.Rect(W // 2 - 170, 228 + i * 78, 230, 40)

    def _tr(self, i):
        return pygame.Rect(W // 2 + 75, 230 + i * 78, 115, 36)

    def draw(self):
        s = self.screen
        gradient_rect(s, s.get_rect(), (14, 22, 38), C["bg"])
        t = self.fonts["title"].render("CONFIGURATION", True, C["gold"])
        s.blit(t, t.get_rect(centerx=W // 2, y=45))
        nt = self.fonts["bold"].render("Nombre de joueurs :", True, C["text"])
        s.blit(nt, nt.get_rect(centerx=W // 2, y=112))
        draw_button(s, self.fonts, "−", self.btn_minus, C["btn_dark"], fkey="head")
        draw_button(s, self.fonts, "+", self.btn_plus, C["btn_dark"], fkey="head")
        nb = self.fonts["title"].render(str(self.num), True, C["gold"])
        s.blit(nb, nb.get_rect(centerx=W // 2, centery=166))
        for i in range(self.num):
            y = 218 + i * 78
            lb = self.fonts["bold"].render(f"Joueur {i + 1} :", True, C["text_dim"])
            s.blit(lb, (W // 2 - 270, y + 11))
            fr = self._fr(i)
            act = (self.active == i)
            rr(s, C["panel2"], fr, r=8, border=2, bcol=C["gold"] if act else C["border"])
            ft = self.fonts["medium"].render(self.names[i], True, C["text"])
            s.blit(ft, (fr.x + 8, fr.y + 11))
            if act and (pygame.time.get_ticks() // 500) % 2 == 0:
                cx2 = fr.x + 8 + ft.get_width()
                pygame.draw.line(s, C["gold"], (cx2, fr.y + 6), (cx2, fr.y + 34), 2)
            tr = self._tr(i)
            col2 = C["btn_pile"] if self.human[i] else C["btn_dark"]
            draw_button(s, self.fonts, "HUMAIN" if self.human[i] else "IA", tr, col2)
        draw_button(s, self.fonts, "COMMENCER", self.btn_start, C["btn_go"], self.hs, fkey="head")
        draw_button(s, self.fonts, "Retour", self.btn_back, C["btn_dark"], self.hb)

class GameScreen:
    
    def __init__(self, screen, fonts, names, humans):
        self.screen = screen
        self.fonts = fonts
        self.names = names
        self.humans = humans
        self.nb_joueurs = len(names)
        
        # Charger le background de jeu (votre image)
        try:
            self.background = pygame.image.load("../assets/bl.jpg")
            self.background = pygame.transform.scale(self.background, (W, H))
        except:
            self.background = pygame.Surface((W, H))
            self.background.fill((20, 30, 50))
        
        self.running = True
        self.manche = 0

    def handle_event(self, ev):
        return None

    def update(self):
        pass

    def draw(self):
        pass

    # Ajoutez cette fonction dans GameScreen (vers ligne 170 environ)

    # Dans ui.py, remplace la méthode play de la classe GameScreen par :

    
    def play(self):
        from game import lancer_partie_pygame
        import game as gi
        
        # Réinitialiser l'état global du jeu
        gi.scores_totaux = {"j1": 0, "j2": 0, "j3": 0, "j4": 0, "j5": 0}
        gi.casques_disponibles = 6
        gi.casques_possedes = {"j1": 0, "j2": 0, "j3": 0, "j4": 0, "j5": 0}
        gi.cartes_leg_prises = {"j1": [], "j2": [], "j3": [], "j4": [], "j5": []}
        gi.defausse_globale = []
        gi._ia_instances.clear()
        
        # Créer l'ensemble des joueurs IA
        joueurs_ia = set()
        for i, is_human in enumerate(self.humans):
            if not is_human:
                joueurs_ia.add(f"j{i+1}")
        
        # Lancer la partie
        running = lancer_partie_pygame(self.nb_joueurs, joueurs_ia, self.screen, self.background)
        
        if not running:
            return S_MENU, None, None
        
        # Récupérer les scores finaux
        scores_liste = [(self.names[i], gi.scores_totaux[f"j{i+1}"]) for i in range(self.nb_joueurs)]
        scores_liste.sort(key=lambda x: x[1], reverse=True)
        vainqueur = scores_liste[0][0]
        
        return S_RESULTS, vainqueur, scores_liste
class ResultsScreen:
    def __init__(self, screen, fonts, vainqueur, scores):
        self.screen = screen
        self.fonts = fonts
        self.vainqueur = vainqueur  # Nom du vainqueur
        self.scores = scores  # Liste des scores [(nom, points), ...]
        self.btn_menu = pygame.Rect(W // 2 - 150, H - 90, 135, 52)
        self.btn_retry = pygame.Rect(W // 2 + 20, H - 90, 135, 52)
        self.t = 0

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.btn_menu.collidepoint(ev.pos):
                return S_MENU
            if self.btn_retry.collidepoint(ev.pos):
                return S_CONFIG
        return None
    def update(self):
        self.t += 1
        for p in PARTS:
            p.update()
    def draw(self):
        s = self.screen
        gradient_rect(s, s.get_rect(), (14, 22, 38), C["bg"])
        #for p in PARTS:
         #   p.draw(s)
        
        # Titre principal
        t = self.fonts["title"].render("FIN DE PARTIE ", True, C["gold"])
        s.blit(t, t.get_rect(centerx=W // 2, y=40))
        
        # Ligne décorative
        pygame.draw.line(s, C["gold"], (W//2 - 250, 90), (W//2 + 250, 90), 2)
        
        # Cadre du vainqueur
        winner_frame = pygame.Rect(W//2 - 250, 110, 500, 100)
        pygame.draw.rect(s, C["panel2"], winner_frame, border_radius=15)
        pygame.draw.rect(s, C["gold"], winner_frame, 3, border_radius=15)
        
        # Texte "VAINQUEUR"
        font_vainqueur = pygame.font.SysFont("Arial", 24, bold=True)
        vainqueur_titre = font_vainqueur.render("VAINQUEUR ", True, C["gold"])
        s.blit(vainqueur_titre, vainqueur_titre.get_rect(centerx=W//2, y=130))
        
        # Nom du vainqueur (grand et doré)
        font_nom = pygame.font.SysFont("Arial", 36, bold=True)
        nom_render = font_nom.render(self.vainqueur, True, C["gold"])
        s.blit(nom_render, nom_render.get_rect(centerx=W//2, y=170))
        
        # Tableau des scores
        score_frame = pygame.Rect(W//2 - 300, 230, 600, 350)
        pygame.draw.rect(s, C["panel"], score_frame, border_radius=15)
        pygame.draw.rect(s, C["border"], score_frame, 2, border_radius=15)
        
        # Titre du tableau
        score_titre = self.fonts["bold"].render("CLASSEMENT FINAL", True, C["gold"])
        s.blit(score_titre, score_titre.get_rect(centerx=W//2, y=245))
        
        # Ligne sous le titre
        pygame.draw.line(s, C["border"], (score_frame.x + 20, 270), (score_frame.x + score_frame.width - 20, 270), 1)
        
        # Afficher les scores
        font_nom_score = pygame.font.SysFont("Arial", 20)
        font_pts = pygame.font.SysFont("Arial", 20, bold=True)
        
        y_start = 290
        medailles = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        
        for i, (nom, points) in enumerate(self.scores):
            y = y_start + i * 50
            
            # Couleur selon le rang
            if i == 0:
                couleur = C["gold"]
                med = medailles[0]
            elif i == 1:
                couleur = (192, 192, 192)  # Argent
                med = medailles[1]
            elif i == 2:
                couleur = (205, 127, 50)   # Bronze
                med = medailles[2]
            else:
                couleur = C["text_dim"]
                med = medailles[i] if i < len(medailles) else f"{i+1}️⃣"
            
            # Médailles
            med_render = font_nom_score.render(med, True, couleur)
            s.blit(med_render, (score_frame.x + 30, y))
            
            # Nom du joueur
            nom_render = font_nom_score.render(nom, True, couleur)
            s.blit(nom_render, (score_frame.x + 80, y))
            
            # Points
            pts_render = font_pts.render(f"{points} pts", True, C["white"])
            s.blit(pts_render, (score_frame.x + score_frame.width - 100, y))
        
        # Boutons
        draw_button(s, self.fonts, "MENU", self.btn_menu, C["btn_dark"])
        draw_button(s, self.fonts, "REJOUER", self.btn_retry, C["btn_pile"])
