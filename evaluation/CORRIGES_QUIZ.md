# Corrigés · Usage formateur

## Diagnostic

1. Classification : cible discrète, par exemple souscription oui/non. Régression : cible numérique, par exemple un montant.  
2. Estimer une procédure figée sur des observations qui n'ont participé à aucun choix.  
3. fit ajuste des paramètres ; predict applique le modèle appris. Les transformations ont aussi une phase fit.  
4. 99% d'accuracy et 0% de rappel positif.  
5. Non : confusion, causalité inverse et sélection sont notamment possibles.  
6. Pour donner un sens comparable aux distances et aux pénalités. Cela ne sert pas à rendre Pearson invariant aux unités : il l'est déjà pour une échelle positive.  
7. Paramètre : appris lors de fit. Hyperparamètre : choisi avant cet ajustement, souvent par validation.  
8. Adaptation à des particularités de l'entraînement qui ne se retrouvent pas dans de nouvelles observations.

## Jour 1

1. Non. Les statistiques de standardisation doivent être apprises dans chaque train de pli. Vérifier avec une pipeline.
2. Séparer par client si l'objectif est la généralisation à de nouveaux clients. Choisir GroupKFold ou une séparation par groupes appropriée ; si le futur est l'objectif, combiner cette réflexion avec le temps.
3. Non. AP évalue le classement, Brier la qualité des probabilités. Examiner une courbe de calibration sur validation.

## Jour 2

1. Leurs erreurs sont parfaitement corrélées. La moyenne reproduit la même erreur.
2. Une direction de correction de la prédiction courante, généralement le gradient négatif de la perte. Le résidu y−ŷ est le cas quadratique sous la convention usuelle.
3. Le maximum a été choisi parmi des estimations bruitées. Évaluer la recherche dans une boucle externe ou sur un jeu indépendant réservé.

## Jour 3

1. Non. Le seuil dépend des coûts et des contraintes. Sous coûts FP/FN fixes et décisions correctes sans coût, comparer CFP(1−p) et CFN p.
2. Cela change la distribution d'évaluation, notamment la prévalence et la précision. Conserver un test représentatif de l'usage.
3. L'encodage peut presque recopier le label. Utiliser lissage et cross-fitting, avec des sous-plis adaptés au problème.

## Jour 4

1. Non. L'inertie minimale ne peut qu'être réduite par une flexibilité accrue. Croiser avec stabilité et utilité.
2. Non. Publier le taux et le profil du bruit. Une méthode qui rejette la majorité des cas peut ne pas répondre au besoin.
3. Non. PCA maximise de la variance de X sans regarder y. Comparer la performance dans une pipeline si l'objectif est supervisé.

## Quiz final · Éléments de correction

1. **Fuite temporelle/cible.** La durée n'existe pas avant l'appel. Retirer la variable, auditer toute variable dérivée et réévaluer sans utiliser l'ancien test pour sélectionner.
2. **Split par patient.** Aucun patient commun entre train et validation/test pour ce scénario. Imputation, sélection et calibration dans le train de chaque pli. La stratification seule ne suffit pas.
3. **Baseline et métriques.** Demander matrice, rappel, précision, AP, prévalence, calibration et protocole. Comparer à la prédiction toujours négative.
4. **Biais de sélection.** CV imbriquée encapsulant toute la recherche ou jeu externe réservé. Documenter budget et variabilité ; ne pas traiter les plis corrélés comme des répétitions indépendantes.
5. **Contamination et prévalence altérée.** Les points synthétiques peuvent utiliser des futurs voisins du test et le test devient artificiellement équilibré. Split initial puis sampling dans chaque train de pli.
6. **Seuil 0,2.** 2/(2+8). Hypothèses : calibration sur la population d'usage, coûts fixes et aucun coût pour les prédictions correctes. Valider empiriquement si contraintes ou hypothèses diffèrent.
7. **Substitution.** Le modèle peut s'appuyer sur la copie ; une faible importance isolée n'établit pas l'inutilité. Permuter/ablater le groupe et examiner les corrélations.
8. **Couverture opérationnelle insuffisante.** La silhouette n'évalue que les points retenus si calculée hors bruit. Rapporter taille, profil, bruit et sens métier, puis tester stabilité et paramètres.
9. **Échangeabilité / distribution modifiée.** La garantie marginale repose sur le cadre de calibration. Ne pas annoncer une couverture individuelle, conditionnelle par groupe ou garantie sous toute dérive. Réexaminer données et calibration sur une période pertinente.
10. **Contrat et traçabilité.** Demander versions, environnement figé, données/empreintes, schéma, pipeline, paramètres, seuil, protocole, résultats et limites. Vérifier un rechargement fiable et des prédictions identiques, puis définir les preuves manquantes avant usage.

## Calculs guidés du diaporama

- Confusion : précision=0,40, rappel=0,60, accuracy=0,87, F1=0,48.
- Résidus 1,1,10 : MAE=4 et RMSE=√34≈5,83.
- Gini : parent 0,48, moyenne pondérée des enfants 0,40, gain 0,08.
- Boosting : F0=4, résidus=(-2,-1,3), souche=(-1,5,-1,5,3), η=0,5, F1=(3,25,3,25,5,5).
- Coût FP=1/FN=5 : seuil théorique 1/6 si les hypothèses du modèle de coût sont satisfaites.
- K-means 1D : centres 0 et 10, puis 1,5 et 8,5. Inertie 10 puis 1.
- Shapley : φA=6, φB=4, référence=10, prédiction=20.
- Conforme : ncal=200, alpha=0,1, rang=181 dans les scores ordonnés, index Python 180.
