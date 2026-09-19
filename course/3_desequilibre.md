# Jour 3 · Déséquilibre et ingénierie de variables

## Déséquilibre et features
Kind: section
> Mercredi 23 septembre · Relier données, probabilités et décisions
Notes: Reprise du protocole puis raisonnement par coûts. La matinée distingue apprendre, calibrer et décider. L'après-midi relie les variables à l'instant de décision et aux ablations. L'atelier features complète TP04 avec un cahier de travail, un corrigé méthodologique et des critères de comparaison.

## Trois décisions différentes
- Apprendre un score qui classe les observations.
- Calibrer ce score pour estimer une probabilité.
- Choisir une règle d'action selon les coûts et la capacité.
> Améliorer l'une de ces étapes n'améliore pas automatiquement les autres
Notes: Une transformation monotone peut préserver le classement tout en modifiant la calibration. Un changement de seuil modifie précision et rappel mais ne réentraîne pas le modèle. Demander si un algorithme avec le meilleur ROC-AUC est nécessairement le meilleur choix pour un centre d'appels limité à 100 contacts par jour. La réponse dépend du segment de la courbe et de la décision.
Sources: R16, R17

## Donner un coût aux erreurs
Equation: Coût(t) = CFP × FP(t) + CFN × FN(t)
- Définir les coûts avec les personnes qui prennent la décision.
- Tester leur sensibilité plutôt que figer une valeur arbitraire.
- Distinguer coût moyen, nombre d'alertes et contraintes de capacité.
Notes: L'exemple du TP fixe CFP=1 et CFN=5 en unités pédagogiques. Ne pas présenter ces valeurs comme des euros ni une mesure de bénéfice réel. Les coûts des décisions correctes sont ici supposés nuls. En cas d'utilités positives, de contraintes ou de coûts individuels, écrire une fonction d'utilité plus complète.
Sources: R17

## Le seuil doit être choisi sur validation
Chart: threshold
- Un seuil bas augmente souvent rappel et volume d'alertes.
- Le minimum de coût dépend des coûts choisis.
- Le test final reste fermé pendant ce réglage.
Notes: La courbe est calculée sur une validation synthétique. Les points d'une grille de seuils donnent un aperçu ; le TP examine toutes les probabilités uniques pour minimiser le coût empirique. Un minimum sur un petit échantillon peut être instable. Faire discuter les seuils voisins et une contrainte de rappel minimal plutôt qu'un seuil présenté avec une précision injustifiée.
Sources: R17

## Un seuil théorique sous hypothèses
Equation: Agir si p(y=1|x) > CFP / (CFP + CFN)
- Hypothèse : probabilités calibrées pour la population d'usage.
- Hypothèse : deux coûts fixes et aucun coût pour les décisions correctes.
- Avec CFP=1 et CFN=5, le seuil théorique vaut 1/6.
Notes: Comparer l'espérance de perte d'une décision positive CFP(1−p) et d'une décision négative CFN p. Déduire la formule. Ce résultat n'est pas une règle universelle : prévalence changée, calibration imparfaite, coûts variables et capacité limitée demandent une adaptation. Le seuil empirique du TP peut différer de 1/6 pour ces raisons et à cause de la variabilité d'échantillonnage.
Sources: R17

## Fβ et rappel sous contrainte
Equation: Fβ = (1 + β²) × précision × rappel / (β² × précision + rappel)
- β > 1 donne plus de poids au rappel dans la moyenne harmonique.
- Un objectif « rappel maximal avec précision ≥ 60 % » est une autre règle.
- Toujours rapporter les effectifs et la capacité nécessaire.
Notes: Faire calculer F2 à précision 0,4 et rappel 0,6 : 5×0,24/(4×0,4+0,6)=1,2/2,2≈0,545. Fβ encode un compromis abstrait, pas forcément un coût métier. Sur validation, une contrainte peut être satisfaite par hasard avec peu de positifs. Le volume et l'incertitude doivent accompagner le résultat.
Sources: R04

## Cinq leviers contre le déséquilibre
Table: imbalance
Notes: Partir d'une baseline et d'une métrique adaptée avant de sampler. Le déséquilibre ne rend pas chaque jeu de données automatiquement difficile : le chevauchement des classes, le bruit et le nombre absolu de positifs comptent aussi. Ne pas changer la prévalence du test pour rendre les métriques plus favorables. Comparer chaque levier sur le même jeu de validation représentatif.
Sources: R14, R17

## Pondérer la fonction de perte
Equation: L = Σi wi ℓ(yi, f(xi))
- Les observations coûteuses ou minoritaires contribuent davantage à l'objectif.
- class_weight ne crée aucune observation supplémentaire.
- La probabilité produite peut nécessiter une recalibration.
Notes: Expliquer que la pondération déplace l'objectif d'apprentissage. L'option balanced utilise les fréquences de classes selon la convention de l'estimateur, mais ne connaît pas les coûts réels de la campagne. Pondérer et baisser le seuil simultanément sans protocole peut doubler un effet recherché. Comparer les effets avec des ablations contrôlées.
Sources: R14, R16

## SMOTE : interpoler dans la classe minoritaire
Equation: xnouveau = xi + u (xvoisin − xi), avec u ∈ [0,1]
- Choisir un voisin minoritaire selon une distance.
- Créer un point sur le segment qui relie deux observations.
- Vérifier que cette interpolation reste plausible.
Notes: Exemple original au tableau : xi=(2,4), voisin=(6,8), u=0,25 donne (3,5). Faire examiner les unités et la standardisation avant de mesurer les distances. SMOTE n'ajoute pas de nouvelle information observée et peut amplifier des labels erronés. Près d'une frontière, l'interpolation peut traverser une zone de l'autre classe. Le nombre de voisins doit être compatible avec les effectifs des plis.
Sources: R15

## Où placer le rééchantillonnage ?
- Réserver le test avant tout sampling.
- Dans chaque pli : apprendre le prétraitement et sampler uniquement le train.
- Évaluer sur la distribution naturelle du pli de validation.
> Utiliser imblearn.Pipeline pour encapsuler cette procédure
Notes: Contre-exemple : fabriquer les points SMOTE sur tout le fichier puis lancer une CV permet à des points très voisins de se retrouver des deux côtés. Le score devient artificiellement favorable et la distribution de validation n'est plus celle d'usage. Avec des catégories, comparer SMOTENC à la pondération. Une interpolation des colonnes one-hot peut créer des catégories fractionnaires sans sens.
Sources: R14, R15

## Lire une courbe de calibration
Chart: calibration
- Une probabilité annoncée de 0,8 doit correspondre à environ 80 % de positifs.
- La diagonale représente la calibration idéale.
- Les bins rares rendent l'estimation incertaine.
Notes: Le graphique est schématique. La courbe observée p² correspond à de la surconfiance pour p dans ]0,1[. En pratique, choisir les bins et montrer leurs effectifs. Une bonne calibration globale peut masquer une mauvaise calibration dans un sous-groupe. Le Brier évalue la qualité des probabilités mais n'isole pas à lui seul toute la calibration.
Sources: R16

## Apprendre une calibration sans fuite
- Sigmoïde : transformation paramétrique relativement simple.
- Isotone : transformation monotone plus flexible, exigeant assez de données.
- Les prédictions utilisées pour calibrer doivent venir de modèles qui n'ont pas vu ces labels.
> CalibratedClassifierCV puis validation du seuil
Notes: Décrire le rôle de la CV interne dans CalibratedClassifierCV. Le train sert à produire des prédictions hors pli pour calibrer. Un autre jeu de validation sert ensuite à choisir le seuil. Le test estime la procédure une fois ces choix figés. Sur peu de positifs, une calibration flexible risque d'être instable. Ne pas annoncer une calibration meilleure sans la mesurer.
Sources: R16

## Concevoir des variables utiles
Table: features
Notes: Une feature résume une hypothèse sur le problème. Décrire son nom, son unité, sa formule, sa fenêtre temporelle et son instant de disponibilité. Une interaction utile à une régression peut être déjà capturée par un arbre. La valeur ajoutée se mesure par une ablation conservant le même protocole. Les variables dérivées de données sensibles ou de proxys exigent une réflexion explicite sur l'usage.
Sources: R18, R41

## Valeurs manquantes et catégories inconnues
- L'absence d'une valeur peut elle-même contenir un signal.
- Distinguer « inconnu », « non applicable » et une vraie valeur nulle.
- Prévoir les catégories inédites au moment de prédire.
> L'imputation est une hypothèse, pas une restauration de la vérité
Notes: Le loader remplace explicitement unknown par une valeur manquante. La branche numérique impute la médiane et ajoute un indicateur. La branche catégorielle impute la modalité fréquente, choix de baseline à discuter. Une autre stratégie conserverait une catégorie manquante explicite. Documenter ces choix et mesurer leur effet. Pour pdays, le code 999 doit être compris à partir du dictionnaire UCI.
Sources: R18, R32

## Target encoding et cross-fitting
Equation: enc(c) = (nc × moyenne_c + m × moyenne_globale) / (nc + m)
- Résumer une catégorie avec une statistique de la cible et un lissage.
- Ne jamais calculer cette statistique à partir de sa propre cible sans contrôle.
- Produire l'encodage d'entraînement par sous-plis adaptés au problème.
Notes: La formule illustre un lissage simple, pas tous les détails de TargetEncoder. Une catégorie presque unique peut révéler le label si le calcul est naïf. Le cross-fitting calcule l'encodage de chaque observation à partir d'autres plis. Dans scikit-learn, fit_transform et fit suivi de transform n'ont donc pas le même comportement d'entraînement. Pour des groupes ou du temps, auditer aussi les sous-plis internes de l'encodeur.
Sources: R19

## Ratios, interactions et variables temporelles
- Ratio : protéger le dénominateur et documenter les unités.
- Interaction : exprimer une hypothèse entre deux facteurs.
- Fenêtre : ne retenir que les événements antérieurs à la décision.
> Une agrégation correcte dans le passé peut devenir une fuite si elle inclut le futur
Notes: Exemples : fréquence de contacts sur 30 jours, ancienneté, interaction entre catégorie et nombre d'interactions. La somme d'événements doit être calculée point-in-time. Décrire un test manuel sur une ligne : la feature aurait-elle pu être produite le jour de la décision ? L'atelier features traite pdays=999 et compare une transformation documentée au pipeline de base.
Sources: R18, R32

## Sélection de variables et ablation
- Filtre : sélectionner selon une statistique avant le modèle, dans les plis.
- Méthode embarquée : utiliser une pénalité ou le mécanisme du modèle.
- Ablation : retirer un groupe de variables puis réévaluer la procédure.
> La sélection supervisée fait partie de l'entraînement
Notes: Choisir des variables sur tout le jeu en regardant leur lien à y constitue une fuite même si l'on applique ensuite une CV au modèle. Avec des variables corrélées, retirer une seule colonne peut masquer une dépendance de groupe. Préférer des ablations interprétables et un budget défini. Consigner les essais pour ne pas transformer la validation en concours sans fin.
Sources: R41, R25

## Corrélation : deux précisions utiles
- Pearson mesure une association linéaire, pas une causalité.
- Un changement positif d'unité ne change pas Pearson.
- Standardiser reste utile pour les distances, les pénalités et certaines optimisations.
> Ne pas confondre covariance, corrélation et distance
Notes: Complément critique au support de méthodologie de 2020. Corr(X,aY+b)=Corr(X,Y) si a>0, et le signe est inversé si a<0. La covariance dépend en revanche des unités. Demander aux étudiants pourquoi passer des euros aux centimes change une distance euclidienne brute mais pas le coefficient de corrélation. Ces distinctions évitent de justifier le scaling par une raison erronée.
Sources: R39, R18

## TP04 : une décision validée
- Comparer modèle simple, poids de classes et SMOTE sur train.
- Calibrer, puis choisir le seuil sur validation avec les coûts fixés.
- Ouvrir le test une fois et commenter les résultats, même décevants.
> 120 minutes · notebooks/etudiants/04_desequilibre.ipynb
Notes: Exiger une séparation écrite des trois étapes : apprendre, calibrer, décider. Ne pas accepter une optimisation du seuil sur test. Demander la matrice de confusion avec effectifs, pas seulement un score. Le coût de validation peut être inférieur au coût de test ; c'est précisément la raison de garder un test indépendant.
Sources: R14, R16, R17

## Atelier : auditer et enrichir les features
- Examiner le dictionnaire UCI et l'instant de disponibilité de cinq variables.
- Proposer deux transformations, dont une pour la sentinelle pdays=999.
- Définir une ablation et le split permettant d'en mesurer l'intérêt.
> 60 minutes · docs/ATELIER_FEATURES.md
Notes: Le livrable est un tableau de contrat et une analyse expérimentale argumentée. L'extension target encoding exige un cross-fitting compatible avec le split. Le corrigé méthodologique donne les attentes sans prétendre qu'une feature améliore systématiquement un modèle. Le score moyen est secondaire à la bonne définition des variables et à l'absence de fuite.
Sources: R19, R32

## Quiz J3 : expliquer les compromis
- Une probabilité bien calibrée impose-t-elle un seuil de 0,5 ?
- Pourquoi ne pas équilibrer le test ?
- Pourquoi une variable catégorielle presque unique est-elle risquée ?
> Une réponse correcte doit préciser la population et le protocole
Notes: Réponses : non, le seuil dépend des coûts et contraintes ; le test doit représenter la distribution d'usage et l'équilibrer change notamment la précision ; un encodage supervisé naïf peut mémoriser la cible et ne pas généraliser aux catégories rares ou nouvelles. Faire proposer une vérification concrète pour chacun de ces risques.
Sources: R14, R17, R19

## Les acquis du jour 3
Kind: summary
- Des features disponibles à l'instant de décision et définies précisément.
- Une stratégie de classes rares comparée sans fuite.
- Une calibration et un seuil évalués dans le bon ordre.
> Demain : découvrir une structure quand la cible n'est pas donnée
Notes: Demander une seule recommandation d'action par binôme, avec métrique, seuil, volume attendu et limite. La réponse « SMOTE marche mieux » est insuffisante si elle n'indique pas la métrique, les données et le budget. Reprendre le protocole du projet final pour y ajouter le contrat de features.
