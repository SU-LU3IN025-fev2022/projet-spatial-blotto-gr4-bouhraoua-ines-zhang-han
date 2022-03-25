# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random 
import numpy as np
import sys
from itertools import chain
from random import randrange

import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
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
    global player,game
    name = _boardname if _boardname is not None else 'blottoMap'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():
    journees = 10

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    
    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize
       
    print("lignes", nbLignes)
    print("colonnes", nbCols)
    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    print("Trouvé ", nbPlayers, " militants")
    
       
           
    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in players]
    print ("Init states:", initStates)
    
    # on localise tous les secteurs d'interet (les votants)
    # sur le layer ramassable
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    
        
    # on localise tous les murs
    # sur le layer obstacle
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    print ("Wall states:", wallStates)
    
    def legal_position(row,col):
        # une position legale est dans la carte et pas sur un mur
        return ((row,col) not in wallStates) and row>=0 and row<nbLignes and col>=0 and col<nbCols
    
    
    
        """ SEMAINE 1
    #-------------------------------
    # Attributaion aleatoire des fioles 
    #-------------------------------
    
    objectifs = []
    for k in range(nbPlayers):

        objectifs.append(random.choice(goalStates))
        print("Objectif joueur", k, objectifs[k])

    nbratab=[]*len(goalStates)
    nbrbtab=[]*len(goalStates)
    nbrtotal = [0]*len(goalStates)
    """

    # SEMAINE 2
    #-------------------------------
    # Attributaion aleatoire
    #-------------------------------
    nbratab=[]*len(goalStates)
    nbrbtab=[]*len(goalStates)
    nbrtotal = [0]*len(goalStates)
    posPlayers = initStates
    
    strgk = [([2, 2, 2, 2, 1],0.3),([3, 1, 1, 1, 1],0.2),([2, 1, 2, 1, 1],0.1),([0, 3, 1, 3, 0],0.3),([2, 0, 3, 0, 2],0.1)]


    def strategieAleatoire(nbPlayers,nbElec):
        tab= [0]*5
        for i in range(nbPlayers//2):
            tab[randrange(nbElec)] += 1

        return tab



    def strategieTetu (journe):
        tab=[]
        tmp = strategieAleatoire(nbPlayers,len(goalStates))
        for i in range(journees):
            tab.append(tmp)
        
        return tab
    
    def strategieStochastique (strgk):
      acc = 0
      k = random.uniform(0, 1)
      for i in range (len(strgk)):
          strat,p = strgk[i]
          acc = acc+p
          if (acc >= k):
              return strat









    def deplacementSansBudget(posiPlayers,strgA,strgB,goalStates):
        cpt= 0
        for n in range(len(strgA)):
            (row,col)=goalStates[n]
            for j in range(strgA[n]):
                print("cpt",cpt,n)
                posiPlayers[cpt]= goalStates[n]
                players[j].set_rowcol(row,col)
                print(posiPlayers[cpt])
                
                cpt+=1
                

        for t in range(len(strgB)):
            (row,col)=goalStates[t]
            for r in range(strgA[t]):
                print("cpt",cpt,t)
                posiPlayers[cpt]= goalStates[t]
                players[r].set_rowcol(row,col)
                print(posiPlayers[cpt])
                cpt+=1
                print("cpt",cpt,t)
        print(posiPlayers)
               
    

    def calculGain(strgA,strgB):
        nbrA= 0
        nbrB=0
        for m in range(len(strgA)):
            if ( strgA[m] > strgB[m]):
                nbrA+=1
            elif (strgA[m]<strgB[m]):
                nbrB+=1
        print("nbr A :", nbrA, " nbr B:", nbrB)
        if (nbrA > nbrB):
            print("A a gangé")
            return 1
        elif (nbrA < nbrB):
            print("B a gangé")
            return -1
        else:
            print("Egalisation")
            return 0


    def aleaF(journe):
        tab=[]
        for k in range (journe):
            tab.append(strategieAleatoire(nbPlayers,len(goalStates)))

        return tab

    """
    stratA = strategieTetu(journees)
    stratB = strategieTetu(journees)
    print("STRATEGIE TETU : ")
    """
    for jr in range(journees):
        print("Journee numéro:",jr)
        if (jr==0):
            strgA = strategieStochastique(strgk)
            strgB = strategieStochastique(strgk)
        elif (result == 1):
            strgB = tmpA
        elif (result == -1):
            strgA = tmpB
        
        tmpA = strgA
        tmpB = strgB
        print("STRATEGIE A : " , strgA)
        print("STRATEGIE B : " , strgB)
        deplacementSansBudget(posPlayers,strgA,strgB,goalStates)
        result = calculGain(strgA,strgB)
        


    """

    for j in range(len(goalStates)):
        nbra=0
        nbrb=0
        for i in range (len(objectifs)):
            if (goalStates[j] == objectifs[i]):
                if (i % 2) == 0:  
                    nbra+=1 
                    
                else:
                    nbrb+=1
                nbrtotal[j]+=1
        nbratab.append(nbra)
        nbrbtab.append(nbrb)
              

    voixa=0
    voixb=0

    for i in range(len(goalStates)):
        if (nbratab[i] > nbrbtab[i]):
            voixa +=1
        else:
            if(nbratab[i] < nbrbtab[i]):
                voixb +=1


    """
 

    
    #-------------------------------
    # Carte demo 
    # 2 joueurs 
    # Joueur 0: A*
    # Joueur 1: random walk
    #-------------------------------
    
    #-------------------------------
    # calcul A* pour le joueur 0
    #-------------------------------
    """
    path=[]
    
    g =np.ones((nbLignes,nbCols),dtype=bool)  # par defaut la matrice comprend des True  
    for w in wallStates:            # putting False for walls
        g[w]=False

    for j in range(nbPlayers):

        p = ProblemeGrid2D(initStates[j],objectifs[j],g,'manhattan')
        path.append(probleme.astar(p))
        print ("Chemin ", j+1 , " trouvé:", path)
    """
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    """
    cpt = 0      
    posPlayers = initStates

    for i in range(iterations):
        
        # on fait bouger chaque joueur séquentiellement
        for j in range(nbPlayers):
        # Joeur 0: suit son chemin trouve avec A* 
            if (initStates[j] != objectifs[j]):
                row,col = path[j][i]
                posPlayers[j]=(row,col)
                players[j].set_rowcol(row,col)
                print ("pos ", j, " :" , row,col)
                if (row,col) == objectifs[j]:
                    print("le joueur", j," a atteint son but!")
                    cpt += 1
                    if (cpt == nbPlayers):
                        break
            
   

    row,col = posPlayers[1]

    while True: # tant que pas legal on retire une position
        x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        next_row = row+x_inc
        next_col = col+y_inc
        if legal_position(next_row,next_col):
            break
        layers[1].set_rowcol(next_row,next_col)
        print ("pos 1:", next_row,next_col)
    
        col=next_col
        row=next_row
        posPlayers[1]=(row,col)
            
        if (row,col) == objectifs[1]:
            print("le joueur 1 a atteint son but!")
            break
            
    """
    


        
    # on passe a l'iteration suivante du jeu
    game.mainiteration(10)
    """
    print ("Les voix de a :", voixa)
    print ("Les voix de b :", voixb)

    if (voixa > voixb):
        print("Team a a gangé")
    else:
        if (voixa < voixb):
            print("Team b a gangé")
        else:
            print("Personne n'a gangé")
    """         
        
            
    
    pygame.quit()
    
    
    
    
    #-------------------------------
    
        
        
    
    
        
    
   

if __name__ == '__main__':
    main()
    


