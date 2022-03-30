# Rapport de projet

## Groupe 4
* ZHANG Han
* BOUHRAOUA Ines

## Description des choix importants d'implémentation

### Pour la semaine 1:

  - On a choisi de déclarer un tableau qui stock les objectifs aléatoirs pour les 14 militants et de les déplacer tous avec la méthode A*, ensuite on a déclaré 2 variables pour les voix de a et les voix de b pour déterminer le gagnant à la fin.

### Pour la semaine 2:

  - On a décidé d'implémenter un menu avec des choix pour que l'utilisateur fait entrer le nombre de journnées souhaités et les différentes stratégies jouées par les militants...
  - Les stratégies implémentées:
    - Stratégie Aléatoire: attribuer aléatoirement les militants aux agents
    - Stratégie Têtu: attribuer aléatoirement une décomposition qui va être jouer en boucle sans la changer pendant le reste de la partie
    - Stratégie Stochastique: on a définie un tableau avec des différentes décompositions des militants en jouant avec les nombres par exemple: paire,impaire,paire,impaire ... ou des palindromes 0,3,1,3,0 etc .. avec leurs probabilités pour qu'après la stratégie avec la probabilité la plus haute va être sélectionnée.
    - Stratégie Meilleure réponse:

## Description des résultats

### Pour la semaine 1:

  - À chaque exécution du jeu les 14 militants sélectionnent des agents au hasard et se déplacent vers ces derniers avec la méthode A* - Résultats corrects

### Pour la semaine 2:

  - Stratégie Aléatoire marche avec le même principe de la semaine 1 - Résultats corrects
  - Stratégie Têtu prend une stratégie aléatoire et la répète pendant le reste de la partie - Résultats corrects
  - Stratégie Stochastique choisit une stratégie avec la probabilité la plus haute parmis les stratégies prédéfinis - Résultats corrects
  - Stratégie Meilleure réponse
