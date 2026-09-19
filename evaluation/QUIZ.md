# Questions et quiz · Version étudiante

## Diagnostic d'entrée · 10 min, non noté

1. Distinguer classification et régression avec un exemple.
2. À quoi sert un jeu de test ?
3. Définir la différence entre fit et predict.
4. Un jeu contient 10 positifs et 990 négatifs. Quelle accuracy donne la prédiction constante « négatif » ?
5. Une corrélation permet-elle de conclure à une causalité ?
6. Pourquoi peut-on standardiser avant un SVM ?
7. Quelle différence entre paramètre et hyperparamètre ?
8. Que veut dire « surapprentissage » ?

## Quiz quotidiens · 3 questions à argumenter

### Jour 1

1. Peut-on standardiser tout le fichier avant une CV ?
2. Quel split choisir si un client possède dix lignes ?
3. Une AP supérieure et un Brier moins bon sont-ils contradictoires ?

### Jour 2

1. Pourquoi 1 000 arbres identiques ne réduisent-ils pas la variance ?
2. Qu'apprend une étape de gradient boosting ?
3. Pourquoi le meilleur score interne est-il optimiste ?

### Jour 3

1. Une bonne calibration impose-t-elle un seuil de 0,5 ?
2. Pourquoi ne pas équilibrer artificiellement le test ?
3. Quel risque pose un target encoding naïf d'une catégorie presque unique ?

### Jour 4

1. Une baisse d'inertie prouve-t-elle un meilleur choix de K ?
2. Une silhouette élevée suffit-elle avec 70% de bruit ?
3. Une composante PCA est-elle nécessairement utile pour prédire la cible ?

## Quiz final individuel · 30 min · Proposition de barème sur 20

Deux points par réponse : 1 pour l'explication correcte et 1 pour une vérification ou une action pertinente.

1. Le score augmente fortement après ajout de la durée d'un appel pour prédire avant l'appel. Identifier le problème et le corriger.
2. Plusieurs observations du même patient sont présentes. On souhaite généraliser à de nouveaux patients. Définir la séparation et son articulation avec les transformations.
3. Un modèle affiche 99% d'accuracy pour 1% de positifs. Quelles informations demander avant de le retenir ?
4. On lance 200 configurations et annonce leur meilleur score de CV comme performance future. Expliquer le biais et proposer une procédure.
5. On applique SMOTE puis on découpe train/test. Quelles sont les deux conséquences problématiques ?
6. Avec une probabilité calibrée et CFP=2, CFN=8, quel est le seuil théorique sous le modèle de coût simple ? Citer une hypothèse.
7. Une variable a peu d'importance par permutation mais une copie corrélée est présente. Comment interpréter et investiguer ?
8. Un clustering donne une bonne silhouette en classant 80% des lignes comme bruit. Pourquoi ce résultat peut-il être inutilisable ?
9. Un intervalle conforme calibré sur la population passée perd sa couverture après une dérive. Quelle hypothèse est en cause ? Quelle garantie ne faut-il pas annoncer ?
10. Un modèle et un fichier de poids sont livrés sans versions, schéma ni protocole. Qu'exiger pour une reproduction et une décision d'usage ?
