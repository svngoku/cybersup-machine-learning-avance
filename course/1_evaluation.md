# Jour 1 · Évaluer et régulariser

## Évaluer et régulariser
Kind: section
> Lundi 21 septembre · Construire une comparaison fiable
Notes: Objectif du jour : définir une cible, choisir un découpage cohérent et créer une baseline reproductible. Faire relier toute amélioration de score à une hypothèse vérifiable. Terminer la journée avec TP01 et un protocole écrit que le binôme pourra réutiliser dans le projet final.

## Le problème avant l'algorithme
- Quelle décision sera prise, pour qui et à quel moment ?
- Quelle cible observe-t-on, avec quel délai et quelles erreurs de mesure ?
- Quelle population devra bénéficier du modèle une fois utilisé ?
> Écrire la décision, l'horizon et la métrique avant d'entraîner
Notes: Activité de 10 minutes : chaque binôme formule la campagne d'appels en une phrase. Exemple : classer les clients éligibles avant le premier appel de la campagne. Demander ce qui changerait pour une prédiction après l'appel. Reprendre le cycle CRISP-DM comme un aller-retour entre compréhension métier, données, préparation, modélisation, évaluation et usage.
Sources: R38

## Le contrat des données du fil rouge
Table: data
Notes: Le site UCI présente plusieurs versions qu'il faut distinguer. Nous utilisons le fichier additionnel de 4 119 lignes, un sous-échantillon aléatoire de la version complète de 41 188 lignes. La page générale affiche aussi des chiffres d'une autre version : ne pas les mélanger. La colonne duration est exclue pour une décision antérieure à l'appel. L'empreinte SHA-256 vérifie la copie distribuée.
Sources: R32

## Trois familles de fuites
- Fuite de cible : une variable encode directement ou indirectement le résultat.
- Fuite de prétraitement : une moyenne, une sélection ou un encodage utilise le test.
- Fuite de structure : le même client, document ou futur se retrouve des deux côtés.
> Une variable disponible dans le fichier n'est pas forcément disponible à la décision
Notes: Proposer trois cas : duration après l'appel, normalisation sur tout le fichier, plusieurs transactions du même client dans train et test. Demander de classer les cas. Expliquer qu'une excellente performance peut constituer un signal d'alarme. Une pipeline protège contre certaines fuites d'apprentissage, mais ne décide pas à notre place si une variable est légitime.
Sources: R02, R32

## Entraînement, validation et test
- Entraînement : ajuster les paramètres du modèle et les transformations.
- Validation : choisir la famille, les hyperparamètres et le seuil.
- Test final : estimer la performance d'une procédure désormais figée.
> Regarder souvent le test revient à l'utiliser pour choisir
Notes: Distinguer jeu de validation explicite et plis de validation croisée. Le test est un contrat organisationnel, pas un simple nom de variable. Dans TP01, X_test existe mais n'est jamais scoré. Les recherches, ablations et choix de seuil appartiennent au développement. Un nouveau choix après le test réclame une nouvelle évaluation indépendante.
Sources: R03

## Choisir le bon découpage
Table: splits
Notes: Faire expliquer l'unité statistique : ligne, personne, machine ou période. La stratification ne résout ni la dépendance par groupes ni les fuites temporelles. Un gap peut être nécessaire si les fenêtres de features et de labels se chevauchent. Sur notre sous-échantillon aléatoire sans identifiant personne, reconnaître explicitement l'impossibilité de garantir une évaluation par personnes et périodes disjointes.
Sources: R03

## La pipeline apprend dans chaque pli
- fit : apprendre l'imputation, les catégories, le scaling et le modèle sur le train du pli.
- transform / predict : appliquer ces paramètres au pli de validation.
- La sélection de variables et le sampling font aussi partie de cette procédure.
> ColumnTransformer traite les colonnes ; Pipeline relie les étapes
Notes: Faire dessiner au tableau les frontières de la CV. Les données de validation peuvent traverser transform, jamais fit. Prévoir handle_unknown pour les nouvelles catégories. Dans une imblearn.Pipeline, le rééchantillonnage n'est réalisé qu'à l'ajustement. Montrer les paramètres de la pipeline avec get_params sans exécuter d'optimisation exhaustive.
Sources: R02, R18

## La matrice de confusion se lit avec un coût
Table: confusion
> 1 000 observations : 60 vrais positifs et 90 faux positifs
Notes: Exemple original : 100 positifs et 900 négatifs. La précision vaut 60/150 = 0,40. Le rappel vaut 60/100 = 0,60. L'accuracy vaut 870/1000 = 0,87. Le F1 vaut 2×0,4×0,6/(0,4+0,6) = 0,48. Demander aux étudiants quel chiffre regarder si les 150 alertes dépassent la capacité quotidienne d'analyse.
Sources: R04, R39

## Le piège de l'accuracy
- Avec 99 % de négatifs, prédire toujours « négatif » donne 99 % d'accuracy.
- Le rappel de la classe positive reste pourtant nul.
- Comparer à DummyClassifier et rapporter les effectifs de chaque classe.
> La métrique dépend de la décision, pas de ce qui donne le plus grand nombre
Notes: Exemple construit, sans lien avec le taux de souscription UCI. Demander si balanced accuracy résout tous les problèmes : non, elle moyenne les rappels des classes mais ne représente pas le coût métier. En multiclasse, distinguer macro, micro et moyenne pondérée. Les rares classes peuvent disparaître dans une moyenne dominée par la majorité.
Sources: R04

## ROC : ordonner les positifs et les négatifs
Chart: roc
- Chaque point correspond à un seuil.
- Axe horizontal : FP / négatifs.
- Axe vertical : VP / positifs.
Notes: Le graphique vient d'une expérimentation synthétique reproductible. L'AUC-ROC évalue le classement, pas le coût ni la calibration. À prévalence rare, un faible taux de faux positifs peut encore produire beaucoup d'alertes. Demander de convertir un FPR de 1% en nombre d'alertes parmi 100 000 négatifs.
Sources: R04

## Précision-rappel : regarder les alertes utiles
Chart: pr
- Précision : VP / (VP + FP).
- Rappel : VP / (VP + FN).
- La référence dépend de la prévalence.
Notes: Le modèle et les observations sont identiques à la diapositive ROC. La précision varie avec la prévalence, donc deux jeux de tests ayant des prévalences différentes ne se comparent pas naïvement. Average precision résume des incréments de rappel pondérés par la précision. Ne pas appeler automatiquement ce nombre aire trapézoïdale PR. Les notebooks utilisent average_precision_score.
Sources: R04

## Évaluer une régression
Equation: MAE = moyenne |y − ŷ|     RMSE = √ moyenne (y − ŷ)²
- MAE conserve une lecture en unités de la cible.
- RMSE pénalise davantage les grandes erreurs.
- R² peut être négatif sur des données nouvelles.
Notes: Faire calculer MAE et RMSE pour des résidus 1, 1 et 10. MAE=4 et RMSE=√34≈5,83. Discuter les valeurs extrêmes avant de les supprimer. Un R² négatif signifie que le modèle est moins bon que la référence constante correspondant à la moyenne de l'échantillon évalué. La MAPE devient délicate avec des valeurs nulles ou proches de zéro.
Sources: R04

## Minimiser une perte avec une pénalité
Equation: θ* = argminθ [ (1/n) Σ ℓ(yi, fθ(xi)) + λ Ω(θ) ]
- La perte mesure une erreur sur l'entraînement.
- La pénalité exprime une préférence pour certaines solutions.
- La validation choisit la force de cette préférence.
Notes: Expliquer chaque symbole : n observations, θ paramètres, ℓ perte individuelle, Ω pénalité, λ force de régularisation. Pour la logistique, une probabilité très confiante et fausse est fortement pénalisée par la log-loss. La perte optimisée peut différer de la métrique finale, par exemple log-loss pour apprendre et AP pour comparer le classement.
Sources: R05

## Biais et variance
Chart: bias
- Biais : erreur systématique liée à la famille de modèles.
- Variance : sensibilité aux données d'entraînement.
- Bruit : part irréductible du problème.
Notes: La décomposition montrée concerne la perte quadratique avec les hypothèses usuelles et une moyenne sur des jeux d'entraînement. Ce n'est pas une décomposition universelle de toute métrique. Les valeurs sont schématiques, pas mesurées. Faire prédire l'effet d'un arbre plus profond et celui d'une moyenne d'arbres.
Sources: R08

## Courbes d'apprentissage
Chart: learning
- Grand écart train/validation : examiner la variance.
- Scores tous deux faibles : examiner biais, features et labels.
- La courbe aide à juger l'intérêt de données supplémentaires.
Notes: Courbes construites pour l'enseignement. Elles ne promettent pas que doubler le volume améliore toujours le modèle. Les courbes réelles ont une incertitude et dépendent du protocole de découpage. Demander quelle action tester lorsque le train est excellent et la validation mauvaise : régulariser, réduire la complexité, vérifier les fuites et enrichir les données pertinentes.
Sources: R08

## L1 et L2 n'ont pas le même effet
Chart: regularization
- L2 réduit progressivement les coefficients.
- L1 peut annuler certains coefficients.
- Le scaling modifie le sens d'une pénalité sur les poids.
Notes: L'exemple représente un seul coefficient avec une normalisation fixée de la perte. La valeur exacte de λ n'est pas transférable entre bibliothèques sans vérifier leurs conventions. En présence de variables corrélées, Lasso peut choisir une variable parmi plusieurs alternatives. Ne pas interpréter cette sélection comme une preuve d'absence d'intérêt des autres.
Sources: R05

## Elastic Net et choix de régularisation
Equation: Ω(w) = α ||w||₁ + (1 − α) ||w||²₂ / 2
- Le mélange associe parcimonie et stabilité de la pénalisation.
- Choisir l'intensité et le mélange dans la validation.
- Dans LogisticRegression, un C plus petit renforce la régularisation.
Notes: Les conventions de paramétrage changent selon les estimateurs : l'α de cette formule est un taux de mélange, pas nécessairement le paramètre alpha d'une classe Python. Faire lire la signature de l'estimateur avant de programmer. Conserver le centrage et la standardisation dans les plis. Une variable catégorielle encodée reste un groupe de colonnes à interpréter ensemble.
Sources: R05

## SVM : marge et noyaux
- La marge sépare les classes en limitant certaines erreurs.
- C règle le compromis entre violations de marge et régularisation.
- Le noyau RBF introduit une portée locale contrôlée par gamma.
> Standardiser puis régler C et gamma sur une échelle logarithmique
Notes: Une marge est une distance à une frontière dans l'espace des features. Gamma élevé peut produire des frontières très locales et fragiles. Le noyau permet de travailler implicitement dans un espace transformé sans créer explicitement toutes ses coordonnées. Un score de décision SVM n'est pas directement une probabilité. La calibration et le coût de calcul doivent être considérés séparément.
Sources: R06

## TP01 : établir la baseline
- Livrer une pipeline de prétraitement et une comparaison à DummyClassifier.
- Comparer quatre valeurs de C avec les mêmes plis et la même métrique.
- Rédiger les risques de fuite et les limites du découpage.
> 120 minutes · notebooks/etudiants/01_evaluation.ipynb
Notes: Commencer par TP00 si l'environnement n'a pas été préparé. Débrief attendu : les résultats sont des estimations conditionnelles au protocole. Ne pas exiger un score fixe selon la machine. Évaluer la justification des choix et l'absence d'accès au test. Les permutations de cible sont un outil de diagnostic, pas un remplacement d'un protocole de test statistique correctement défini.
Sources: R02, R03

## Quiz J1 : défendre son protocole
- Peut-on standardiser tout le fichier avant une CV ?
- Quel split choisir si un client possède dix lignes ?
- Que signifie une AP supérieure avec un Brier moins bon ?
> Répondre seul, comparer en binôme, puis justifier
Notes: Réponses : non, apprendre les statistiques sur chaque train de pli ; découper par client pour l'objectif de généralisation à de nouveaux clients ; meilleur classement possible mais probabilités moins fidèles. Demander un contre-exemple concret à chaque réponse. Les corrigés détaillés et questions supplémentaires figurent dans evaluation/CORRIGES_QUIZ.md.
Sources: R02, R03, R16

## Les acquis du jour 1
Kind: summary
- Une cible et un instant de décision explicites.
- Une pipeline validée avec un découpage justifié.
- Une baseline, des métriques adaptées et un test final préservé.
> Demain : améliorer le modèle sans dégrader la qualité de la comparaison
Notes: Faire déposer au binôme son protocole en une page : définition de la cible, unité d'observation, variables interdites, découpage et métriques. Ce document sera audité lors du projet final. Demander un point encore confus pour orienter la reprise du lendemain.
