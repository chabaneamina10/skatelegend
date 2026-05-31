"""
ai.py — IA avancée pour Skate Legend
Stratégie : lookahead 1-carte exact + heuristiques + mémoire + style adaptatif
"""
import random

# ─── Seuils de risque (probabilité de chute sur la PROCHAINE carte uniquement) ──
SEUIL_NORMAL   = 0.42   # > 42 % de chute sur la carte suivante → stop
SEUIL_PRUDENT  = 0.28   # style prudent
SEUIL_AGRESSIF = 0.62   # style agressif
MIN_CARTES     = 2       # Joue toujours au moins N cartes avant d'envisager le stop

# ─── Utilitaires ─────────────────────────────────────────────────────────────

def _pts(carte):
    return carte.get("recompense", 0)

def _compter(enchainement):
    """Retourne (dict_couleurs, nb_casse)."""
    coul = {"rouge": 0, "vert": 0, "bleu": 0, "jaune": 0}
    nb_c = 0
    for c in enchainement:
        col = c.get("couleur")
        if col in coul:
            coul[col] += 1
        if c.get("casse", 0) == 1:
            nb_c += 1
    return coul, nb_c

def _chute(enchainement, casque_couleur=None):
    """Vrai si l'enchainement provoque une chute."""
    coul, nb_c = _compter(enchainement)
    if casque_couleur:
        coul[casque_couleur] = 0
    return any(v >= 3 for v in coul.values()) or nb_c >= 3

def _sure(carte, enchainement, casque_couleur=None):
    return not _chute(enchainement + [carte], casque_couleur)

def _score(enchainement):
    total = 0
    for c in enchainement:
        if c.get("est_legendaire", False):
            if c.get("condition_validee", False):
                total += _pts(c)
        else:
            total += _pts(c)
    return total

def _proba_chute_next(enchainement, pioche1, pioche2, casque_couleur=None):
    """
    Probabilité EXACTE que la prochaine carte piochée cause une chute.
    Calcul sur toutes les cartes restantes (pas de sampling).
    """
    pool = list(pioche1) + list(pioche2)
    if not pool:
        return 1.0
    n_chute = sum(1 for c in pool if _chute(enchainement + [c], casque_couleur))
    return n_chute / len(pool)

# ─── Classe principale ────────────────────────────────────────────────────────

class JoueurStrategie:
    """
    IA avancée pour Skate Legend :
    - Ne s'arrête JAMAIS avant MIN_CARTES cartes dans l'enchainement
    - Décision stop basée sur la probabilité exacte de chute sur la prochaine carte
    - Style adaptatif selon la manche et l'écart de score
    - Mémoire des pioches vues (effet VISIBLE)
    - Choix de cartes prioritarisé : légendaire → nouvelle couleur → meilleure sûre
    """

    def __init__(self):
        self.premier_tour    = True
        self._pioche_connue  = {1: None, 2: None}
        self.style           = "normal"
        self._id_manche      = 0
        self._score_perso    = 0
        self._scores_adv     = {}

    # ── Début de manche ──────────────────────────────────────────────────────

    def notifier_choix(self, joueur_id, continuer, carte_jouee, etat_partie):
        """Signal de début de manche quand continuer=None et carte_jouee=None."""
        if continuer is None and carte_jouee is None:
            self.premier_tour   = True
            self._pioche_connue = {1: None, 2: None}
            if etat_partie:
                self._id_manche   = etat_partie.get("id_manche", 1)
                self._score_perso = etat_partie.get("moi", {}).get("score_total", 0)
                self._scores_adv  = etat_partie.get("scores_adversaires", {})
                self._ajuster_style()

    def _ajuster_style(self):
        m     = self._id_manche
        meill = max(self._scores_adv.values(), default=0)
        ecart = self._score_perso - meill
        if m <= 2:
            self.style = "normal"
        elif m == 3:
            self.style = "prudent" if ecart >= 8 else ("agressif" if ecart <= -8 else "normal")
        else:
            self.style = "prudent" if ecart >= 5 else ("agressif" if ecart <= -5 else "normal")
        print(f"  [IA] Style : {self.style.upper()} (manche {m}, écart {ecart:+d})")

    # ── Mémoire pioches ──────────────────────────────────────────────────────

    def memoriser_pioche(self, num, carte):
        self._pioche_connue[num] = carte.copy() if carte else None
        if carte:
            print(f"  [IA-MEM] Pioche {num} = {carte['nom']} ({carte.get('couleur') or '—'})")

    def oublier_pioche(self, num):
        self._pioche_connue[num] = None

    # ── Seuil selon le style ─────────────────────────────────────────────────

    def _seuil(self):
        if self.style == "prudent":
            return SEUIL_PRUDENT
        if self.style == "agressif":
            return SEUIL_AGRESSIF
        return SEUIL_NORMAL

    # ── DÉCISION : continuer ou stop ─────────────────────────────────────────

    def continuer_jouer(self, joueur_id, etat_partie):
        moi          = etat_partie["moi"]
        enc          = moi.get("enchainement_actuel", [])
        casq         = moi.get("casque_actuel")
        pioche1      = etat_partie.get("pioche1_liste", [])
        pioche2      = etat_partie.get("pioche2_liste", [])
        nb           = len(enc)
        score_act    = _score(enc)

        # Toujours jouer si enchainement vide
        if nb == 0:
            return True

        # Forcer le jeu jusqu'à MIN_CARTES (sauf risque structurel immédiat)
        coul, nb_c = _compter(enc)
        coul_eff = dict(coul)
        if casq:
            coul_eff[casq] = 0
        presentes = [v for v in coul_eff.values() if v > 0]

        # Règle dure : TOUTES les couleurs présentes sont à 2 + 2 cassés → danger total
        if presentes and all(v >= 2 for v in presentes) and nb_c >= 2:
            print(f"  [IA] Danger total (toutes couleurs à 2, {nb_c} cassés) → STOP")
            return False

        # Ne pas s'arrêter avant MIN_CARTES
        if nb < MIN_CARTES:
            return True

        # Probabilité exacte de chute sur la prochaine carte
        p = _proba_chute_next(enc, pioche1, pioche2, casq)
        seuil = self._seuil()
        print(f"  [IA] Score={score_act} | Chute_next={p:.0%} | Seuil={seuil:.0%} "
              f"| {nb} cartes")

        if p >= seuil:
            print(f"  [IA] Risque trop élevé → STOP")
            return False

        # Style prudent : si on a un bon score, ne pas risquer
        if self.style == "prudent" and score_act >= 5 and nb >= 3:
            print(f"  [IA] Score suffisant en mode prudent → STOP")
            return False

        return True

    # ── DÉCISION : casque ────────────────────────────────────────────────────

    def jouer_casque(self, joueur_id, etat_partie):
        moi     = etat_partie["moi"]
        enc     = moi.get("enchainement_actuel", [])
        reserve = moi.get("casques_reserve", 0)
        actuel  = moi.get("casque_actuel")
        p1      = etat_partie.get("pioche1_liste", [])
        p2      = etat_partie.get("pioche2_liste", [])

        if reserve == 0 or actuel is not None or len(enc) == 0:
            return False

        derniere = enc[-1]
        coul_d   = derniere.get("couleur")
        if not coul_d:
            return False

        coul, _ = _compter(enc)

        # Défensif : couleur à 2 → une 3e = chute
        if coul.get(coul_d, 0) >= 2:
            print(f"  [IA] Casque défensif sur '{coul_d}'")
            return True

        # Offensif : si proba de chute élevée et bon score
        score_act = _score(enc)
        if score_act >= 4 and len(enc) >= 3:
            p = _proba_chute_next(enc, p1, p2)
            if p >= 0.40:
                print(f"  [IA] Casque offensif (p_chute={p:.0%})")
                return True

        return False

    # ── DÉCISION : quelle carte/pioche jouer ─────────────────────────────────

    def jouer_carte(self, joueur_id, etat_partie):
        """
        Retourne (action, idx) :
          (0, idx) → jouer main[idx]
          (1, 0)   → piocher pioche 1
          (2, 0)   → piocher pioche 2
        """
        moi  = etat_partie["moi"]
        main = moi.get("main", [])
        enc  = moi.get("enchainement_actuel", [])
        casq = moi.get("casque_actuel")
        pip  = etat_partie.get("pioche", [None, None])

        if self.premier_tour:
            self.premier_tour = False
            # Au 1er tour, jouer une légendaire si dispo sinon piocher
            idx_l, _ = self._meilleure_legendaire(main, enc, casq)
            if idx_l is not None:
                return (0, idx_l)
            return (self._choisir_pioche(pip, enc, casq), 0)

        # Priorité 1 : légendaire avec condition remplie
        idx_l, _ = self._meilleure_legendaire(main, enc, casq)
        if idx_l is not None:
            return (0, idx_l)

        # Priorité 2 : carte de la main apportant une nouvelle couleur
        coul_enc, _ = _compter(enc)
        nb_coul = sum(1 for v in coul_enc.values() if v > 0)
        if nb_coul < 3:
            idx_d, _ = self._carte_couleur_nouvelle(main, enc, casq)
            if idx_d is not None:
                return (0, idx_d)

        # Priorité 3 : meilleure pioche sûre vs meilleure carte main sûre
        num_p         = self._choisir_pioche(pip, enc, casq)
        carte_pip     = pip[num_p - 1]
        pip_sure      = carte_pip is not None and _sure(carte_pip, enc, casq)
        idx_m, cm     = self._meilleure_carte_sure(main, enc, casq)

        if pip_sure:
            pts_pip = _pts(carte_pip)
            pts_m   = _pts(cm) if cm else -1
            if pts_pip >= pts_m:
                print(f"  [IA] Pioche {num_p} sûre et rentable ({pts_pip} pts)")
                return (num_p, 0)

        if idx_m is not None:
            print(f"  [IA] Carte main : {cm['nom']}")
            return (0, idx_m)

        # Priorité 4 : piocher
        choix = self._choisir_pioche(pip, enc, casq)
        print(f"  [IA] Pioche {choix} (fallback)")
        return (choix, 0)

    # ── EFFET PIOCHER ─────────────────────────────────────────────────────────

    def piocher_carte(self, joueur_id, etat_partie):
        moi  = etat_partie["moi"]
        enc  = moi.get("enchainement_actuel", [])
        casq = moi.get("casque_actuel")
        pip  = etat_partie.get("pioche", [None, None])
        choix = self._choisir_pioche(pip, enc, casq)
        print(f"  [IA] Effet PIOCHER → pioche {choix}")
        return (choix, 0)

    # ── EFFET VISIBLE ─────────────────────────────────────────────────────────

    def choisir_pioche_visible(self, joueur_id, etat_partie):
        pip = etat_partie.get("pioche", [None, None])
        # Regarder la pioche inconnue en priorité
        if self._pioche_connue[1] is None and pip[0] is None:
            return 1
        if self._pioche_connue[2] is None and pip[1] is None:
            return 2
        return 1

    # ── Helpers internes ──────────────────────────────────────────────────────

    def _choisir_pioche(self, pip, enc, casq):
        """Choisit la meilleure pioche (sûre + rentable, ou évite le danger connu)."""
        v = {
            1: pip[0] if pip[0] is not None else self._pioche_connue[1],
            2: pip[1] if pip[1] is not None else self._pioche_connue[2],
        }
        s1 = v[1] is not None and _sure(v[1], enc, casq)
        s2 = v[2] is not None and _sure(v[2], enc, casq)

        if s1 and s2:
            return 1 if _pts(v[1]) >= _pts(v[2]) else 2
        if s1:
            return 1
        if s2:
            return 2
        # Les deux connues et dangereuses → fuir vers l'inconnue
        if v[1] is not None and v[2] is None:
            return 2
        if v[2] is not None and v[1] is None:
            return 1
        return random.choice([1, 2])

    def _meilleure_legendaire(self, main, enc, casq):
        best = []
        for i, c in enumerate(main):
            if not c.get("est_legendaire", False):
                continue
            if not _sure(c, enc, casq):
                continue
            if self._condition_ok(c, enc):
                best.append((i, c, _pts(c)))
        if not best:
            return None, None
        best.sort(key=lambda x: x[2], reverse=True)
        i, c, _ = best[0]
        print(f"  [IA] Légendaire : {c['nom']} (condition OK, {_pts(c)} pts)")
        return i, c

    def _condition_ok(self, carte, enc):
        cond = carte.get("condition")
        if cond is None:
            return True
        test = enc + [carte]
        coul, nb_c = _compter(test)
        nb_dif = sum(1 for v in coul.values() if v > 0)
        if cond == "2 couleurs id":  return any(v >= 2 for v in coul.values())
        if cond == "2 rouges":       return coul["rouge"] >= 2
        if cond == "1 jaune 1 verte":return coul["jaune"] >= 1 and coul["vert"] >= 1
        if cond == "3 couleurs dif": return nb_dif >= 3
        if cond == "4 cartes":       return len(test) >= 4
        if cond == "5 cartes":       return len(test) >= 5
        if cond == "2 casse":        return nb_c >= 2
        return False

    def _carte_couleur_nouvelle(self, main, enc, casq):
        coul_enc, _ = _compter(enc)
        best = (None, None, -1)
        for i, c in enumerate(main):
            col = c.get("couleur")
            if col and coul_enc.get(col, 0) == 0 and _sure(c, enc, casq):
                p = _pts(c)
                if p > best[2]:
                    best = (i, c, p)
        return best[0], best[1]

    def _meilleure_carte_sure(self, main, enc, casq):
        best = (None, None, -999)
        coul_enc, _ = _compter(enc)
        for i, c in enumerate(main):
            if not _sure(c, enc, casq):
                continue
            score = _pts(c)
            col = c.get("couleur")
            if col and coul_enc.get(col, 0) == 0:
                score += 1.5
            if c.get("rejouer", 0) >= 1:
                score += 2.0
            if c.get("piocher", 0) >= 1:
                score += 1.0
            if c.get("casse", 0) == 1:
                score -= 0.5
            if score > best[2]:
                best = (i, c, score)
        return best[0], best[1]
