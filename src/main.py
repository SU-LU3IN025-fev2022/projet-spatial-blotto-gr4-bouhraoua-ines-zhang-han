# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals
from copy import deepcopy
from gettext import find

import random
import numpy as np
import sys
from itertools import chain
from random import randrange
import heapq

import pygame

from pySpriteWorld.gameclass import Game, check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme


# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----


# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()


def init(_boardname=None):
    global player, game
    name = _boardname if _boardname is not None else "blottoMap"
    game = Game("./Cartes/" + name + ".json", SpriteBuilder)
    game.O = Ontology(True, "SpriteSheet-32x32/tiny_spritesheet_ontology.csv")
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player


def main():
    journees = 10

    # for arg in sys.argv:
    iterations = 100  # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print("Iterations: ")
    print(iterations)

    init()

    # -------------------------------
    # Initialisation
    # -------------------------------

    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize

    print("lignes", nbLignes)
    print("colonnes", nbCols)

    players = [o for o in game.layers["joueur"]]
    nbPlayers = len(players)
    print("Trouvé ", nbPlayers, " militants")

    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in players]
    print("Init states:", initStates)

    # on localise tous les secteurs d'interet (les votants)
    # sur le layer ramassable
    goalStates = [o.get_rowcol() for o in game.layers["ramassable"]]
    print("Goal states:", goalStates)

    # on localise tous les murs
    # sur le layer obstacle
    wallStates = [w.get_rowcol() for w in game.layers["obstacle"]]
    print("Wall states:", wallStates)

    def legal_position(row, col):
        # une position legale est dans la carte et pas sur un mur
        return (
            ((row, col) not in wallStates)
            and row >= 0
            and row < nbLignes
            and col >= 0
            and col < nbCols
        )

    print("Semaine 1?\n 0->Non 1->Yes")
    s1 = input("please enter:")

    if int(s1) == 1:
        # -------------------------------
        # Attributaion aleatoire des fioles
        # -------------------------------

        objectifs = []
        for k in range(nbPlayers):
            objectifs.append(random.choice(goalStates))
            print("Objectif joueur", k, objectifs[k])

        nbratab = [] * len(goalStates)
        nbrbtab = [] * len(goalStates)
        nbrtotal = [0] * len(goalStates)

        for j in range(len(goalStates)):
            nbra = 0
            nbrb = 0
            for i in range(len(objectifs)):
                if goalStates[j] == objectifs[i]:
                    if (i % 2) == 0:
                        nbra += 1

                    else:
                        nbrb += 1

                    nbrtotal[j] += 1
            nbratab.append(nbra)
            nbrbtab.append(nbrb)

        print(nbratab)
        print(nbrbtab)

        voixa = 0
        voixb = 0

        for i in range(len(goalStates)):
            # print(i)
            if nbratab[i] > nbrbtab[i]:
                voixa += 1
            else:
                if nbratab[i] < nbrbtab[i]:
                    voixb += 1
        # -------------------------------
        # Carte demo
        # 2 joueurs
        # Joueur 0: A*
        # Joueur 1: random walk
        # -------------------------------

        # -------------------------------
        # calcul A* pour le joueur 0
        # -------------------------------
        path = []
        g = np.ones(
            (nbLignes, nbCols), dtype=bool
        )  # par defaut la matrice comprend des True
        for w in wallStates:  # putting False for walls
            g[w] = False
        for j in range(nbPlayers):
            p = ProblemeGrid2D(initStates[j], objectifs[j], g, "manhattan")
            path.append(probleme.astar(p))
        print("Chemin trouvé:", path)

        # -------------------------------
        # Boucle principale de déplacements
        # -------------------------------
        cp = 0
        posPlayers = initStates

        for i in range(iterations):
            # on fait bouger chaque joueur séquentiellement
            for h in range(nbPlayers):
                # Joeur 0: suit son chemin trouve avec A*
                if initStates[h] != objectifs[h]:
                    row, col = path[h][i]
                    posPlayers[h] = (row, col)
                    players[h].set_rowcol(row, col)
                    # print ("pos ", j, " :" , row,col)

                    if (row, col) == objectifs[h]:
                        print("le joueur", h, " a atteint son but!")
                        cp += 1
                        if cp == nbPlayers:
                            break
            if cp == nbPlayers:
                break

            # on passe a l'iteration suivante du jeu
            game.mainiteration()

        print("Les voix de a :", voixa)
        print("Les voix de b :", voixb)

        if voixa > voixb:
            print("Team a a gangé")
        else:
            if voixa < voixb:
                print("Team b a gangé")
            else:
                print("Personne n'a gangé")

        pygame.quit()
    else:
        print("\nil y a combien de jours?")
        jours = int(input("please enter:"))

        print("\nla strategie pour joueur 1:")
        print("0 : aleatoire")
        print("1 : tetu")
        print("2 : stochastique expert")
        print("3 : strategie meilleur reponse")
        print("4 : strategie fictious")
        strg1 = int(input("please enter:"))

        print("\nla strategie pour joueur 2:")
        print("0 : aleatoire")
        print("1 : tetu")
        print("2 : stochastique expert")
        print("3 : strategie meilleur reponse")
        print("4 : strategie fictious")
        strg2 = int(input("please enter:"))

        # SEMAINE 2
        # -------------------------------
        # Attributaion aleatoire
        # -------------------------------
        nbratab = [] * len(goalStates)
        nbrbtab = [] * len(goalStates)
        nbrtotal = [0] * len(goalStates)
        posPlayers = initStates

        strgk = [
            ([2, 2, 2, 2, 1], 0.3),
            ([3, 1, 1, 1, 1], 0.2),
            ([2, 1, 2, 1, 1], 0.1),
            ([0, 3, 1, 3, 0], 0.3),
            ([2, 0, 3, 0, 2], 0.1),
        ]

        def strategieAleatoire(nbPlayers, nbElec):
            tab = [0] * 5
            for i in range(nbPlayers // 2):
                tab[randrange(nbElec)] += 1

            return tab

        def strategieStochastique(strgk):
            acc = 0
            k = random.uniform(0, 1)
            for i in range(len(strgk)):
                strat, p = strgk[i]
                acc = acc + p
                if acc >= k:
                    random.shuffle(strat)
                    return strat

        def deplacementSansBudget(posiPlayers, strgA, strgB, goalStates):
            cpt = 0
            for n in range(len(strgA)):
                (row, col) = goalStates[n]
                for j in range(strgA[n]):
                    posiPlayers[cpt] = goalStates[n]
                    players[j].set_rowcol(row, col)
                    cpt += 1

            for t in range(len(strgB)):
                if cpt >= 14:
                    break
                (row, col) = goalStates[t]
                for r in range(strgA[t]):
                    if cpt >= 14:
                        break

                    posiPlayers[cpt] = goalStates[t]
                    players[r].set_rowcol(row, col)
                    cpt += 1

        def calculGain(strgA, strgB):
            nbrA = 0
            nbrB = 0
            for m in range(len(strgA)):
                if strgA[m] > strgB[m]:
                    nbrA += 1
                elif strgA[m] < strgB[m]:
                    nbrB += 1
            # print("nbr A :", nbrA, " nbr B:", nbrB)
            if nbrA > nbrB:
                # print("A a gangé")
                return 1
            elif nbrA < nbrB:
                # print("B a gangé")
                return -1
            else:
                # print("Egalisation")
                return 0

        def aleaF(journe):
            tab = []
            for k in range(journe):
                tab.append(strategieAleatoire(nbPlayers, len(goalStates)))

            return tab

        def findIndicePlusPetit(nb, lis):
            nl = []
            tmp = heapq.nsmallest(nb, lis)
            for i in range(len(lis)):
                if len(nl) == nb:
                    break
                if lis[i] in tmp:
                    nl.append(i)
            return nl

        def strategieMeilleure(strgAvant):
            nstrg = [0] * len(strgAvant)
            cpt = 0
            lis = findIndicePlusPetit(3, strgAvant)
            for i in lis:
                nstrg[i] = strgAvant[i] + 1
                cpt += strgAvant[i] + 1
            cpt = 7 - cpt
            nstrg[0] = nstrg[0] + cpt
            return nstrg

        tabSitu = [[1 / 2, 1 / 2, 2 / 3], [1 / 2, 1 / 2, 3 / 5], [1 / 3, 2 / 5, 1 / 2]]

        def findZero(stg):
            cpt = 0
            for i in stg:
                if i == 0:
                    cpt += 1

            if cpt > 2:
                return 2
            return cpt

        def noAlea(tota, nbChoix):
            lis = []
            for i in range(nbChoix):
                tmp = random.randint(0, tota - 1)
                while tmp in lis:
                    tmp = random.randint(0, tota - 1)
                lis.append(tmp)
            return lis

        def strGene(nbTrous, longu, nbPeople):
            nlis = [0] * longu
            avoidLis = noAlea(longu, nbTrous)
            for i in range(longu):
                if i in avoidLis:
                    continue
                nlis[i] = 1
            for i in range(nbPeople - longu + nbTrous):
                tmp = random.randint(0, longu - 1)
                while tmp in avoidLis:
                    tmp = random.randint(0, longu - 1)
                nlis[tmp] += 1

            return nlis

        def calculEs(lisPref):
            llen = sum(lisPref)

            lis = []
            for i in range(3):
                lis.append(0)
                for j in range(3):
                    lis[i] += lisPref[j] / llen * tabSitu[i][j]

            # print(lis)
            return lis.index(max(lis))

        def strgFictious(lisPref):
            return strGene(calculEs(lisPref), len(goalStates), nbPlayers // 2)

        print("\n\nStart:\n\n")
        aTotal = 0
        bTotal = 0

        # A instancier
        lisPa = [1, 2, 2]
        lisPb = [2, 0, 3]
        for jr in range(jours):
            if jr > 0:
                tmpAlis = deepcopy(strgA)
                tmpBlis = deepcopy(strgB)

            match strg1:
                case 0:
                    strgA = strategieAleatoire(nbPlayers, len(goalStates))
                case 1:
                    if jr == 0:
                        # strgA = [0, 0, 1, 1, 5]
                        strgA = strategieAleatoire(nbPlayers, len(goalStates))
                    else:
                        random.shuffle(strgA)
                case 2:
                    strgA = strategieStochastique(strgk)
                case 3:
                    if jr == 0:
                        strgA = strategieAleatoire(nbPlayers, len(goalStates))
                    else:
                        strgA = strategieMeilleure(tmpBlis)
                case 4:
                    strgA = strgFictious(lisPb)
                case _:
                    raise Exception("strategie not found")

            lisPa[findZero(strgA)] += 1

            match strg2:
                case 0:
                    strgB = strategieAleatoire(nbPlayers, len(goalStates))
                case 1:
                    if jr == 0:
                        strgB = strategieAleatoire(nbPlayers, len(goalStates))
                    else:
                        random.shuffle(strgB)
                case 2:
                    strgB = strategieStochastique(strgk)
                case 3:
                    if jr == 0:
                        strgB = strategieAleatoire(nbPlayers, len(goalStates))
                    else:
                        # print("**tmpAlis ", tmpAlis)
                        strgB = strategieMeilleure(tmpAlis)
                case 4:
                    strgB = strgFictious(lisPa)
                case _:
                    raise Exception("strategie not found")

            lisPb[findZero(strgB)] += 1

            deplacementSansBudget(posPlayers, strgA, strgB, goalStates)
            # print("strgA: ", strgA)
            # print("strgB: ", strgB)
            result = calculGain(strgA, strgB)
            # print("result: ", result)

            match result:
                case 1:
                    aTotal += 1
                case -1:
                    bTotal += 1

        print("\n\naTotal: ", aTotal)
        print("bTotal: ", bTotal)

        game.mainiteration(10)

        pygame.quit()

    # -------------------------------


if __name__ == "__main__":
    main()
