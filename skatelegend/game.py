# game_interface.py - Version avec interface pygame
import pygame
import random
import time
from cards import creation_pioches, liste_cartes, cartes_legendaires, creation_piocheleg, perfect_landing
from ai import JoueurStrategie
from ui import textescore, afficher_cartesleg, afficher_cartesjoueurs, afficher_mains, afficher_cartesbg1, afficher_cartesbg2, interface, draw_game_buttons, rec, draw_casque, couleurs, afficher_commentaires, joueur_chute, manche, textesmanche
from poscartes import pile1_rect, pile2_rect, button_rect, continuer_rect, casque_rect, rouge_rect, vert_rect, jaune_rect, bleu_rect, exit_rect
from joueurs import changement_joueurs
from sound import play_sound

# Dimensions
W, H = 1280, 720

# Variables globales
scores_totaux = {"j1": 0, "j2": 0, "j3": 0, "j4": 0, "j5": 0}
casques_disponibles = 6
casques_possedes = {"j1": 0, "j2": 0, "j3": 0, "j4": 0, "j5": 0}
cartes_leg_prises = {"j1": [], "j2": [], "j3": [], "j4": [], "j5": []}
defausse_globale = []

# Instances IA
_ia_instances = {}

def get_ia(joueur):
    if joueur not in _ia_instances:
        _ia_instances[joueur] = JoueurStrategie()
    return _ia_instances[joueur]

def get_pts(carte):
    return carte.get("récompense", 0)

def reconstruire_pioches(pioche1, pioche2, defausse):
    total_cartes = len(pioche1) + len(pioche2) + len(defausse)
    if total_cartes == 0:
        return [], [], []
    
    if not pioche1 and not pioche2 and defausse:
        nouvelle_pioche = defausse.copy()
        random.shuffle(nouvelle_pioche)
        milieu = len(nouvelle_pioche) // 2
        return nouvelle_pioche[:milieu], nouvelle_pioche[milieu:], []
    
    if not pioche1 and pioche2:
        milieu = len(pioche2) // 2
        return pioche2[:milieu], pioche2[milieu:], defausse
    
    if not pioche2 and pioche1:
        milieu = len(pioche1) // 2
        return pioche1[:milieu], pioche1[milieu:], defausse
    
    return pioche1, pioche2, defausse

def revalider_conditions_enchainement(enchainement):
    couleurs = {"rouge": 0, "vert": 0, "bleu": 0, "jaune": 0}
    nb_casse = 0
    
    for carte in enchainement:
        col = carte.get("couleur")
        if col in couleurs:
            couleurs[col] += 1
        if carte.get("cassé") == 1:
            nb_casse += 1
    
    for carte in enchainement:
        if not carte.get("est_legendaire", False):
            continue
        
        condition = carte.get("condition")
        carte["condition_validee"] = False
        
        if condition == "3 couleurs dif":
            nb_couleurs = sum(1 for v in couleurs.values() if v > 0)
            carte["condition_validee"] = nb_couleurs >= 3
        elif condition == "2 rouges":
            carte["condition_validee"] = couleurs["rouge"] >= 2
        elif condition == "1 jaune 1 verte":
            carte["condition_validee"] = couleurs["jaune"] >= 1 and couleurs["vert"] >= 1
        elif condition == "4 cartes":
            nb_couleurs = sum(1 for v in couleurs.values() if v > 0)
            carte["condition_validee"] = nb_couleurs >= 4
        elif condition == "5 cartes":
            nb_couleurs = sum(1 for v in couleurs.values() if v > 0)
            carte["condition_validee"] = nb_couleurs >= 5
        elif condition == "2 casse":
            carte["condition_validee"] = nb_casse >= 2
        elif condition == "2 couleurs id":
            carte["condition_validee"] = any(v >= 2 for v in couleurs.values())

def verifier_chute(enchainement, casque_actif=False, couleur_casque=None):
    couleurs = {"rouge": 0, "vert": 0, "bleu": 0, "jaune": 0}
    nb_casse = 0
    
    for carte in enchainement:
        col = carte.get("couleur")
        if col and col in couleurs:
            couleurs[col] += 1
        if carte.get("cassé") == 1:
            nb_casse += 1
    
    if casque_actif and couleur_casque in couleurs:
        couleurs[couleur_casque] = 0
    
    if any(v >= 3 for v in couleurs.values()) or nb_casse >= 3:
        return True
    return False

def defausser_enchainement(enchainement, defausse):
    while enchainement:
        carte = enchainement.pop()
        defausse.append(carte)

def score_enchainement(enchainement):
    total = 0
    for carte in enchainement:
        if carte.get("est_legendaire", False):
            if carte.get("condition_validee", False):
                total += carte.get("récompense", 0)
        else:
            total += carte.get("récompense", 0)
    return total

def prendre_carte_recompense(joueur, pile_recompense, mains, scores_totaux):
    global cartes_leg_prises
    
    if not pile_recompense:
        return False
    
    if pile_recompense[0].get("nom") == "perfect landing":
        carte = pile_recompense.pop(0)
        scores_totaux[joueur] += 5
        return True
    
    carte = pile_recompense.pop(0)
    carte_copy = carte.copy()
    carte_copy["est_legendaire"] = True
    carte_copy["condition_validee"] = False
    mains[joueur].append(carte_copy)
    cartes_leg_prises[joueur].append(carte_copy)
    return True

def construire_etat_ia(joueur, enchainement, main, casque_actuel, casques_reserve,
                       pioche1, pioche2, cartes_visibles, num_manche, scores_totaux):
    return {
        "id_manche": num_manche + 1,
        "moi": {
            "enchainement_actuel": enchainement.copy(),
            "main": main.copy(),
            "casque_actuel": casque_actuel,
            "casques_reserve": casques_reserve,
            "score_total": scores_totaux.get(joueur, 0),
        },
        "pioche": [
            cartes_visibles[1] if cartes_visibles[1] else (pioche1[-1] if pioche1 else None),
            cartes_visibles[2] if cartes_visibles[2] else (pioche2[-1] if pioche2 else None)
        ],
        "pioche1_liste": list(pioche1),
        "pioche2_liste": list(pioche2),
    }

def tour_ia(joueur, j, m, pioche1, pioche2, pile_recompense,
            ut_casque, stop, chute, couleur_casque,
            casques_joueurs, cartes_visibles, num_manche, scores_totaux, comment):
    
    ia = get_ia(joueur)
    
    etat = construire_etat_ia(joueur, j, m, 
                              couleur_casque.get(joueur) if ut_casque.get(joueur) else None,
                              casques_joueurs.get(joueur, 0),
                              pioche1, pioche2, cartes_visibles, num_manche, scores_totaux)
    
    # Décision stop
    if j and not ia.continuer_jouer(joueur, etat):
        stop[joueur] = True
        comment.append(f"IA {joueur[1]} s'arrête !")
        return "stop"
    
    # Décision casque
    if not ut_casque.get(joueur) and casques_joueurs.get(joueur, 0) > 0 and j:
        if ia.jouer_casque(joueur, etat):
            if j:
                derniere = j[-1]
                couleur = derniere.get("couleur")
                if couleur:
                    ut_casque[joueur] = True
                    couleur_casque[joueur] = couleur
                    casques_joueurs[joueur] -= 1
                    comment.append(f"IA {joueur[1]} utilise un casque sur {couleur}")
                    return "casque"
    
    # Choisir une action
    action = ia.jouer_carte(joueur, etat)
    
    if action is None:
        stop[joueur] = True
        comment.append(f"IA {joueur[1]} s'arrête")
        return "stop"
    
    # Jouer carte de la main
    if action[0] == 0:
        idx = action[1]
        if idx < len(m):
            carte = m.pop(idx)
            j.append(carte)
            comment.append(f"IA {joueur[1]} joue {carte['nom']}")
            return "joue", carte
    
    # Piocher
    elif action[0] == 1 and pioche1:
        carte = pioche1.pop()
        if cartes_visibles[1]:
            cartes_visibles[1] = None
            ia.oublier_pioche(1)
        j.append(carte)
        comment.append(f"IA {joueur[1]} pioche pioche 1 : {carte['nom']}")
        return "joue", carte
    
    elif action[0] == 2 and pioche2:
        carte = pioche2.pop()
        if cartes_visibles[2]:
            cartes_visibles[2] = None
            ia.oublier_pioche(2)
        j.append(carte)
        comment.append(f"IA {joueur[1]} pioche pioche 2 : {carte['nom']}")
        return "joue", carte
    
    stop[joueur] = True
    return "stop"

def input_visible_pygame(screen):
    font = pygame.font.SysFont("Arial", 24, bold=True)
    choix = None
    clock = pygame.time.Clock()
    
    while choix is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choix = 1
                elif event.key == pygame.K_2:
                    choix = 2
        
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        texte = font.render("Quelle pioche regarder ? Appuyez sur 1 ou 2", True, (255, 255, 255))
        screen.blit(texte, texte.get_rect(centerx=W//2, centery=H//2))
        
        pygame.display.flip()
        clock.tick(30)
    
    return choix

def input_piocher_pygame(screen):
    font = pygame.font.SysFont("Arial", 24, bold=True)
    choix = None
    clock = pygame.time.Clock()
    
    while choix is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choix = 1
                elif event.key == pygame.K_2:
                    choix = 2
        
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        texte = font.render("Piocher une carte ? Appuyez sur 1 ou 2", True, (255, 255, 255))
        screen.blit(texte, texte.get_rect(centerx=W//2, centery=H//2))
        
        pygame.display.flip()
        clock.tick(30)
    
    return choix

def afficher_choix_casque(screen):
    couleurs(screen, rouge_rect, vert_rect, jaune_rect, bleu_rect)

def lancer_partie_pygame(nbjoueurs, joueurs_ia, screen, background):
    global scores_totaux, casques_disponibles, casques_possedes, cartes_leg_prises, defausse_globale
    
    # Réinitialisation
    for k in scores_totaux:
        scores_totaux[k] = 0
    for k in casques_possedes:
        casques_possedes[k] = 0
    for k in cartes_leg_prises:
        cartes_leg_prises[k] = []
    casques_disponibles = 6
    defausse_globale = []
    _ia_instances.clear()
    
    # Création des pioches
    pioche1, pioche2 = creation_pioches(liste_cartes)
    pile_recompense, _ = creation_piocheleg(cartes_legendaires)

    for m in range(4):
        running = lancer_manche_pygame(m, nbjoueurs, pile_recompense, pioche1, pioche2, joueurs_ia, screen, background)
        if not running:
            return False
        
        if m < 3:
            # Afficher écran de fin de manche
            if nbjoueurs == 2:
                textes = textesmanche(scores_totaux["j1"], scores_totaux["j2"], 0, 0, 0, nbjoueurs)
                manche(screen, m, textes[0], textes[1], "", "", "", nbjoueurs)
            elif nbjoueurs == 3:
                textes = textesmanche(scores_totaux["j1"], scores_totaux["j2"], scores_totaux["j3"], 0, 0, nbjoueurs)
                manche(screen, m, textes[0], textes[1], textes[2], "", "", nbjoueurs)
            elif nbjoueurs == 4:
                textes = textesmanche(scores_totaux["j1"], scores_totaux["j2"], scores_totaux["j3"], scores_totaux["j4"], 0, nbjoueurs)
                manche(screen, m, textes[0], textes[1], textes[2], textes[3], "", nbjoueurs)
            else:
                textes = textesmanche(scores_totaux["j1"], scores_totaux["j2"], scores_totaux["j3"], scores_totaux["j4"], scores_totaux["j5"], nbjoueurs)
                manche(screen, m, textes[0], textes[1], textes[2], textes[3], textes[4], nbjoueurs)
    
    # Bonus casques
    for i in range(nbjoueurs):
        joueur = f"j{i+1}"
        bonus = casques_possedes.get(joueur, 0) * 2
        scores_totaux[joueur] += bonus
    
    return True

def lancer_manche_pygame(num_manche, nbjoueurs, pile_recompense, pioche1, pioche2, jai, screen, background):
    global casques_disponibles, casques_possedes, scores_totaux, cartes_leg_prises, defausse_globale
    attente_visible = False
    attente_piocher = False
    commentaires = []
    
    def ajout_comment(msg):
        commentaires.append(msg)
        if len(commentaires) > 20:
            commentaires.pop(0)
    
    ajout_comment(f"MANCHE {num_manche + 1}/4")
    
    # Initialisation
    enchainements = {f"j{i+1}": [] for i in range(nbjoueurs)}
    mains = {f"j{i+1}": [] for i in range(nbjoueurs)}
    a_chute = {f"j{i+1}": False for i in range(nbjoueurs)}
    a_stop = {f"j{i+1}": False for i in range(nbjoueurs)}
    casque_utilise_manche = {f"j{i+1}": False for i in range(nbjoueurs)}
    couleur_casque = {f"j{i+1}": None for i in range(nbjoueurs)}
    
    # Distribution initiale
    for i in range(nbjoueurs):
        joueur = f"j{i+1}"
        if pioche1:
            mains[joueur].append(pioche1.pop())
        elif pioche2:
            mains[joueur].append(pioche2.pop())

    # Ajout des légendaires gagnées
    for i in range(nbjoueurs):
        joueur = f"j{i+1}"
        for carte in cartes_leg_prises.get(joueur, []):
            mains[joueur].append(carte)
        cartes_leg_prises[joueur] = []

    joueur_actuel = "j1"
    joueur_fin_manche = None
    cartes_visibles = {1: None, 2: None}
    
    # Initialisation IA
    for joueur in jai:
        ia = get_ia(joueur)
        etat_init = construire_etat_ia(joueur, [], [], None, 0, pioche1, pioche2, cartes_visibles, num_manche, scores_totaux)
        ia.notifier_choix(joueur, None, None, etat_init)
    
    clock = pygame.time.Clock()
    
    # Boucle de jeu
    while True:
        # Vérifier reconstruction pioches
        if (not pioche1 or not pioche2) and (pioche1 or pioche2 or defausse_globale):
            pioche1, pioche2, defausse_globale = reconstruire_pioches(pioche1, pioche2, defausse_globale)
            cartes_visibles = {1: None, 2: None}
        
        # Vérifier fin de manche
        tous_finis = all(a_chute.get(j, False) or a_stop.get(j, False) for j in [f"j{i+1}" for i in range(nbjoueurs)])
        if tous_finis:
            break
        
        if a_chute.get(joueur_actuel, False) or a_stop.get(joueur_actuel, False):
            joueur_actuel = changement_joueurs(joueur_actuel, nbjoueurs)
            continue
        
        # Afficher l'interface
        scores_liste = [
            scores_totaux[f"j{i+1}"] + score_enchainement(enchainements[f"j{i+1}"])
            for i in range(nbjoueurs)
        ]
        
        if nbjoueurs == 2:
            textes_scores = textescore(scores_liste[0], scores_liste[1], 0, 0, 0, nbjoueurs)
            interface(screen, background, textes_scores[0], textes_scores[1], "", "", "", nbjoueurs)
        elif nbjoueurs == 3:
            textes_scores = textescore(scores_liste[0], scores_liste[1], scores_liste[2], 0, 0, nbjoueurs)
            interface(screen, background, textes_scores[0], textes_scores[1], textes_scores[2], "", "", nbjoueurs)
        elif nbjoueurs == 4:
            textes_scores = textescore(scores_liste[0], scores_liste[1], scores_liste[2], scores_liste[3], 0, nbjoueurs)
            interface(screen, background, textes_scores[0], textes_scores[1], textes_scores[2], textes_scores[3], "", nbjoueurs)
        else:
            textes_scores = textescore(scores_liste[0], scores_liste[1], scores_liste[2], scores_liste[3], scores_liste[4], nbjoueurs)
            interface(screen, background, textes_scores[0], textes_scores[1], textes_scores[2], textes_scores[3], textes_scores[4], nbjoueurs)
        
        # Afficher les zones
        rec(screen)
        draw_game_buttons(screen, button_rect, continuer_rect, exit_rect)
        
        if casques_possedes.get(joueur_actuel, 0) > 0:
            draw_casque(screen, casque_rect, casques_possedes.get(joueur_actuel, 0))
        if cartes_visibles[1]:
            screen.blit(cartes_visibles[1]["image"], (300, 10))
            afficher_cartesbg2(screen)
        else:    
            afficher_cartesbg1(screen)
        if  cartes_visibles[2]:
            screen.blit(cartes_visibles[2]["image"], (900, 10))
            afficher_cartesbg1(screen)
        else:
              afficher_cartesbg2(screen)   
        afficher_cartesleg(screen, pile_recompense[:3] if pile_recompense else [], perfect_landing)
        afficher_cartesjoueurs(screen, enchainements[joueur_actuel])
        afficher_mains(screen, mains[joueur_actuel])
        afficher_commentaires(screen, commentaires)
        
        pygame.display.flip()
        
        # TOUR IA
        if joueur_actuel in jai:
            pygame.time.wait(500)
            
            j = enchainements[joueur_actuel]
            m = mains[joueur_actuel]
            
            resultat = tour_ia(joueur_actuel, j, m, pioche1, pioche2, pile_recompense,
                               casque_utilise_manche, a_stop, a_chute, couleur_casque,
                               casques_possedes, cartes_visibles, num_manche, scores_totaux, commentaires)
            
            if isinstance(resultat, tuple) and resultat[0] == "joue":
                carte_jouee = resultat[1]
                revalider_conditions_enchainement(j)
                afficher_cartesjoueurs(screen, enchainements[joueur_actuel])
                afficher_mains(screen, mains[joueur_actuel])
                afficher_commentaires(screen, commentaires)
                pygame.display.flip()
                pygame.time.wait(1000) 
                if verifier_chute(j, casque_utilise_manche.get(joueur_actuel, False), couleur_casque.get(joueur_actuel)):
                    a_chute[joueur_actuel] = True
                    if casques_disponibles > 0:
                        casques_disponibles -= 1
                        casques_possedes[joueur_actuel] = casques_possedes.get(joueur_actuel, 0) + 1
                    ajout_comment(f"IA {joueur_actuel[1]} a CHUTÉ !")
                    defausser_enchainement(j, defausse_globale)
                    joueur_actuel = changement_joueurs(joueur_actuel, nbjoueurs)
                    continue
                
                if carte_jouee.get("rejouer", 0) > 0:
                    ajout_comment(f"REJOUER ! L'IA rejoue")
                    continue
                elif carte_jouee.get("visible", 0) == 1:
                    ia = get_ia(joueur_actuel)
                    choix = 1  # par défaut
                    if choix == 1 and pioche1:
                        ia.memoriser_pioche(1, pioche1[-1])
                        cartes_visibles[1] = pioche1[-1].copy()
                    elif choix == 2 and pioche2:
                        ia.memoriser_pioche(2, pioche2[-1])
                        cartes_visibles[2] = pioche2[-1].copy()
                elif carte_jouee.get("piocher", 0) == 1:
                    ia = get_ia(joueur_actuel)
                    etat = construire_etat_ia(joueur_actuel, j, m, couleur_casque.get(joueur_actuel),
                                              casques_possedes.get(joueur_actuel, 0),
                                              pioche1, pioche2, cartes_visibles, num_manche, scores_totaux)
                    action_pioche = ia.piocher_carte(joueur_actuel, etat)
                    choix = action_pioche[0]
                    if choix == 1 and pioche1:
                        carte = pioche1.pop()
                        if cartes_visibles[1]:
                            cartes_visibles[1] = None
                            ia.oublier_pioche(1)
                        m.append(carte)
                        ajout_comment(f"IA {joueur_actuel[1]} pioche (effet) : {carte['nom']}")
                    elif choix == 2 and pioche2:
                        carte = pioche2.pop()
                        if cartes_visibles[2]:
                            cartes_visibles[2] = None
                            ia.oublier_pioche(2)
                        m.append(carte)
                        ajout_comment(f"IA {joueur_actuel[1]} pioche (effet) : {carte['nom']}")
            
            elif resultat == "stop":
                a_stop[joueur_actuel] = True
                if all(a_stop.get(j, False) or a_chute.get(j, False) for j in [f"j{i+1}" for i in range(nbjoueurs)]):
                    joueur_fin_manche = joueur_actuel
            
            joueur_actuel = changement_joueurs(joueur_actuel, nbjoueurs)
            continue
        
        # TOUR HUMAIN
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                j = enchainements[joueur_actuel]
                m = mains[joueur_actuel]
                if attente_visible:
                        if pile1_rect.collidepoint(event.pos):
                            cartes_visibles[1] = pioche1[-1].copy() if pioche1 else None
                            attente_visible = False
                            continue
                        elif pile2_rect.collidepoint(event.pos):
                            cartes_visibles[2] = pioche2[-1].copy() if pioche2 else None
                            attente_visible = False
                            continue

                    # Gestion de l'attente PIOCHER
                if attente_piocher:
                    if pile1_rect.collidepoint(event.pos) and pioche1:
                        carte = pioche1.pop()
                        if cartes_visibles[1]:
                            cartes_visibles[1] = None
                        mains[joueur_actuel].append(carte)
                        ajout_comment(f"Joueur {joueur_actuel[1]} pioche (effet) : {carte['nom']}")
                        attente_piocher = False
                        continue
                            
                    elif pile2_rect.collidepoint(event.pos) and pioche2:
                        carte = pioche2.pop()
                        if cartes_visibles[2]:
                            cartes_visibles[2] = None
                        mains[joueur_actuel].append(carte)
                        ajout_comment(f"Joueur {joueur_actuel[1]} pioche (effet) : {carte['nom']}")
                        attente_piocher = False
                        continue    
                if exit_rect.collidepoint(event.pos):
                    return False
                    
                # Pioche 1
                if pile1_rect.collidepoint(event.pos) and not (a_stop[joueur_actuel] or a_chute[joueur_actuel]):
                    play_sound()
                    if pioche1:
                        carte = pioche1.pop()
                        if cartes_visibles[1]:
                            cartes_visibles[1] = None
                        j.append(carte)
                        ajout_comment(f"Joueur {joueur_actuel[1]} pioche pioche 1 : {carte['nom']}")
                        revalider_conditions_enchainement(j)
                        
                        if verifier_chute(j, casque_utilise_manche.get(joueur_actuel, False), couleur_casque.get(joueur_actuel)):
                            joueur_chute(screen, int(joueur_actuel[1]), joueur_actuel, j)
                            a_chute[joueur_actuel] = True
                            if casques_disponibles > 0:
                                casques_disponibles -= 1
                                casques_possedes[joueur_actuel] = casques_possedes.get(joueur_actuel, 0) + 1
                            ajout_comment(f"Joueur {joueur_actuel[1]} a CHUTÉ !")
                            defausser_enchainement(j, defausse_globale)
                            joueur_actuel = changement_joueurs(joueur_actuel, nbjoueurs)
                            continue
                        
                        if carte.get("rejouer", 0) > 0:
                            ajout_comment("REJOUER ! Rejoue immédiatement")
                            continue
                        if carte.get("visible", 0) == 1:
                            attente_visible=True
                            ajout_comment("Cliquez sur une pioche pour voir la carte")
                            continue
                        
                        elif carte.get("piocher", 0) == 1:
                            attente_piocher=True
                            ajout_comment(f"cliquer sur une pioche")
                            continue    
                # Pioche 2
                if pile2_rect.collidepoint(event.pos) and not (a_stop[joueur_actuel] or a_chute[joueur_actuel]):
                    play_sound()
                    if pioche2:
                        carte = pioche2.pop()
                        if cartes_visibles[2]:
                            cartes_visibles[2] = None
                        j.append(carte)
                        ajout_comment(f"Joueur {joueur_actuel[1]} pioche pioche 2 : {carte['nom']}")
                        revalider_conditions_enchainement(j)
                        
                        if verifier_chute(j, casque_utilise_manche.get(joueur_actuel, False), couleur_casque.get(joueur_actuel)):
                            joueur_chute(screen, int(joueur_actuel[1]), joueur_actuel, j)
                            a_chute[joueur_actuel] = True
                            if casques_disponibles > 0:
                                casques_disponibles -= 1
                                casques_possedes[joueur_actuel] = casques_possedes.get(joueur_actuel, 0) + 1
                            ajout_comment(f"Joueur {joueur_actuel[1]} a CHUTÉ !")
                            defausser_enchainement(j, defausse_globale)
                            joueur_actuel = changement_joueurs(joueur_actuel, nbjoueurs)
                            continue
                        
                        if carte.get("rejouer", 0) > 0:
                            ajout_comment("REJOUER ! Rejoue immédiatement")
                            continue
                        elif carte.get("visible", 0) == 1:
                            attente_visible=True
                            ajout_comment("Cliquez sur une pioche pour voir la carte")
                            continue
                        elif carte.get("piocher", 0) == 1:
                            attente_piocher=True
                            ajout_comment(f"cliquer sur une pioche")
                            continue
                          
                # Cartes de la main
                main_positions = [(100, 480), (220, 480), (340, 480), (460, 480)]
                for i, pos in enumerate(main_positions):
                    carte_rect = pygame.Rect(pos[0], pos[1], 90, 160)
                    if carte_rect.collidepoint(event.pos) and i < len(m) and not (a_stop[joueur_actuel] or a_chute[joueur_actuel]):
                        play_sound()
                        carte = m.pop(i)
                        j.append(carte)
                        ajout_comment(f"Joueur {joueur_actuel[1]} joue : {carte['nom']}")
                        revalider_conditions_enchainement(j)
                        
                        if verifier_chute(j, casque_utilise_manche.get(joueur_actuel, False), couleur_casque.get(joueur_actuel)):
                            joueur_chute(screen, int(joueur_actuel[1]), joueur_actuel, j)
                            a_chute[joueur_actuel] = True
                            if casques_disponibles > 0:
                                casques_disponibles -= 1
                                casques_possedes[joueur_actuel] = casques_possedes.get(joueur_actuel, 0) + 1
                            ajout_comment(f"Joueur {joueur_actuel[1]} a CHUTÉ !")
                            defausser_enchainement(j, defausse_globale)
                            joueur_actuel = changement_joueurs(joueur_actuel, nbjoueurs)
                            continue
                        
                        if carte.get("rejouer", 0) > 0:
                            ajout_comment("REJOUER ! Rejoue immédiatement")
                            continue
                        if carte.get("visible", 0) == 1:
                            attente_visible=True
                            ajout_comment("Cliquez sur une pioche pour voir la carte")
                            continue
                      
                            
                        elif carte.get("piocher", 0) == 1:
                            attente_piocher=True
                            ajout_comment("Cliquez sur une pioche pour la piocher")
                            continue
                     
                # Cartes légendaires
                leg_positions = [(490, 10), (565, 10), (640, 10)]
                for idx, pos in enumerate(leg_positions):
                    leg_rect = pygame.Rect(pos[0], pos[1], 90, 160)
                    if leg_rect.collidepoint(event.pos) and idx < len(pile_recompense) and not (a_stop[joueur_actuel] or a_chute[joueur_actuel]):
                        play_sound()
                        carte = pile_recompense.pop(idx).copy()
                        carte["est_legendaire"] = True
                        carte["condition_validee"] = False
                        j.append(carte)
                        ajout_comment(f"Joueur {joueur_actuel[1]} joue légendaire : {carte['nom']}")
                        revalider_conditions_enchainement(j)
                        
                        if verifier_chute(j, casque_utilise_manche.get(joueur_actuel, False), couleur_casque.get(joueur_actuel)):
                            joueur_chute(screen, int(joueur_actuel[1]), joueur_actuel, j)
                            a_chute[joueur_actuel] = True
                            if casques_disponibles > 0:
                                casques_disponibles -= 1
                                casques_possedes[joueur_actuel] = casques_possedes.get(joueur_actuel, 0) + 1
                            ajout_comment(f"Joueur {joueur_actuel[1]} a CHUTÉ !")
                            defausser_enchainement(j, defausse_globale)
                            joueur_actuel = changement_joueurs(joueur_actuel, nbjoueurs)
                            continue
        
                # Bouton STOP
                if button_rect.collidepoint(event.pos) and not (a_stop[joueur_actuel] or a_chute[joueur_actuel]):
                    a_stop[joueur_actuel] = True
                    ajout_comment(f"Joueur {joueur_actuel[1]} s'arrête !")
                    revalider_conditions_enchainement(j)
                    
                    autres_encore = [j for j in [f"j{i+1}" for i in range(nbjoueurs)]
                                     if j != joueur_actuel and not a_chute.get(j, False) and not a_stop.get(j, False)]
                    if not autres_encore:
                        joueur_fin_manche = joueur_actuel
                    
                    joueur_actuel = changement_joueurs(joueur_actuel, nbjoueurs)
                    continue
                
                # Bouton CONTINUER
                if continuer_rect.collidepoint(event.pos) and not (a_stop[joueur_actuel] or a_chute[joueur_actuel]):
                    joueur_actuel = changement_joueurs(joueur_actuel, nbjoueurs)
                    continue
                
                # Bouton CASQUE
                if casque_rect.collidepoint(event.pos) and casques_possedes.get(joueur_actuel, 0) > 0 and not (a_stop[joueur_actuel] or a_chute[joueur_actuel]) and j:
                    if not casque_utilise_manche[joueur_actuel]:
                        afficher_choix_casque(screen)
                        pygame.display.flip()
                        
                        attente_casque = True
                        couleur = None
                        while attente_casque:
                            for ev in pygame.event.get():
                                if ev.type == pygame.QUIT:
                                    return False
                                if ev.type == pygame.MOUSEBUTTONDOWN:
                                    if rouge_rect.collidepoint(ev.pos):
                                        couleur = "rouge"
                                        attente_casque = False
                                    elif vert_rect.collidepoint(ev.pos):
                                        couleur = "vert"
                                        attente_casque = False
                                    elif jaune_rect.collidepoint(ev.pos):
                                        couleur = "jaune"
                                        attente_casque = False
                                    elif bleu_rect.collidepoint(ev.pos):
                                        couleur = "bleu"
                                        attente_casque = False
                            
                            afficher_choix_casque(screen)
                            pygame.display.flip()
                            clock.tick(30)
                        
                        if couleur:
                            casque_utilise_manche[joueur_actuel] = True
                            couleur_casque[joueur_actuel] = couleur
                            casques_possedes[joueur_actuel] -= 1
                            ajout_comment(f"Joueur {joueur_actuel[1]} utilise un casque sur {couleur}")
                            joueur_actuel = changement_joueurs(joueur_actuel, nbjoueurs)
                            continue
    
    # Fin de manche - Calcul des points
    if not joueur_fin_manche:
        for joueur in [f"j{i+1}" for i in range(nbjoueurs)]:
            if not a_chute.get(joueur, False):
                joueur_fin_manche = joueur
                break
    
    if joueur_fin_manche and not a_chute.get(joueur_fin_manche, False):
        ajout_comment(f"{joueur_fin_manche} gagne une carte légendaire !")
        prendre_carte_recompense(joueur_fin_manche, pile_recompense, mains, scores_totaux)
    elif pile_recompense:
        carte_defaussee = pile_recompense.pop(0)
        ajout_comment(f"Carte légendaire défaussée : {carte_defaussee['nom']}")
    
    # Ajouter les points
    for joueur in [f"j{i+1}" for i in range(nbjoueurs)]:
        if not a_chute.get(joueur, True):
            revalider_conditions_enchainement(enchainements[joueur])
            points = score_enchainement(enchainements[joueur])
            scores_totaux[joueur] += points
            ajout_comment(f"{joueur} gagne {points} points")
    
    return True
