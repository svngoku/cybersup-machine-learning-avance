# Guide formateur · Machine Learning Avancé

**Chrys Fé-Marty NIONGOLO · Cybersup · 21–25 septembre 2026 · 35 h**

Ce guide reprend les intentions, calculs et débriefs des notes du PowerPoint. Les réponses des quiz et les corrigés des notebooks sont destinés au formateur. Voir le programme pour les durées et la différenciation.

## Diapositive 1 · Machine Learning Avancé

Accueillir les participants. Formation Cybersup en présentiel à Paris, du 21 au 25 septembre 2026, niveau M2 Data / IA, 35 heures pédagogiques. Faire annoncer à chacun un problème rencontré avec un modèle. Les temps de pause sont exclus des 35 heures. Le QR code mène au dépôt privé ; distribuer les notebooks par archive si les accès GitHub ne sont pas encore ouverts.

## Diapositive 2 · Votre formateur

Le lien LinkedIn a été fourni par le formateur. Aucune expérience, certification ni biographie supplémentaire n'est affirmée. Inviter les participants à préciser leur maîtrise de Python, des statistiques et de scikit-learn. Présenter le fonctionnement des échanges en présentiel.

## Diapositive 3 · Programme de la semaine

Présenter les cinq journées. Les notions d'évaluation sont reprises dans tous les TP. Le projet final utilise des compétences accumulées pendant la semaine. Les corrections sont dans un dossier réservé à l'animation ; les notebooks étudiants contiennent les exemples guidés et les espaces d'exercice.

## Diapositive 4 · Six compétences à démontrer

Les trois premières compétences reprennent la fiche de formation. Les trois suivantes, interprétabilité, évaluation fiable et reproductibilité/mise en production, complètent les objectifs masqués dans la fiche et ont été validées par le formateur. Il s'agit d'une préparation à la mise en production, pas d'un déploiement réel ni d'une certification de conformité.

## Diapositive 5 · Prérequis et diagnostic

Faire répondre au diagnostic de evaluation/QUIZ.md sans noter. Distinguer une difficulté de code d'une difficulté de raisonnement. Prévoir la ressource R33 pour la remédiation. Les mathématiques sont utilisées pour comprendre un mécanisme, puis reliées à une expérimentation.

À retenir : Diagnostic de 10 minutes puis groupes de travail complémentaires

Références : [R01](https://www.statlearning.com/), [R33](https://inria.github.io/scikit-learn-mooc/)

## Diapositive 6 · Le rythme des cinq journées

Le détail minute par minute figure dans docs/PROGRAMME_35H.md. Les créneaux totalisent 420 minutes par jour. Les TP longs incluent recherche, essais, rédaction et débrief, pas seulement l'exécution des cellules. Adapter le nombre d'extensions au diagnostic sans supprimer le projet ni le débrief.

À retenir : Chaque jour : 7 heures pédagogiques, pauses exclues

## Diapositive 7 · Le fil rouge : prioriser des appels

La question métier précède le choix d'algorithme. La cible historique est la souscription, pas un bénéfice ni un effet du traitement. Le gain incrémental d'une campagne demanderait une expérimentation ou une méthode causale appropriée. Les coûts FP/FN utilisés dans le cours sont des unités pédagogiques choisies explicitement.

À retenir : Un score de propension n'est pas l'effet causal d'un appel

Références : [R32](https://archive.ics.uci.edu/dataset/222/bank+marketing), R39 (support local)

## Diapositive 8 · Nos ressources de travail

Ouvrir le README avec les étudiants. Exécuter uv sync --frozen avant la formation, puis uv run jupyter lab. Sans uv, installer les dépendances depuis requirements.txt dans un environnement Python 3.12. Les corrections ne sont pas protégées par le simple nom d'un dossier : fournir une archive étudiante si l'on veut les masquer.

À retenir : CPU suffisant ; données des TP disponibles hors ligne après installation

## Diapositive 9 · Ce que nous reprenons des supports de 2020

Les supports de Julie Hor sont cités avec les pages PDF dans resources/PROVENANCE.md. Ne pas distribuer les PDF originaux sans autorisation. Corriger deux raccourcis : le coefficient de Pearson est invariant aux changements positifs d'unité, et il n'existe pas de règle universelle imposant 30 observations par feuille d'arbre.

À retenir : Exemples et illustrations du cours reconstruits et attribués

Références : R38 (support local), R39 (support local)

## Diapositive 10 · Évaluer et régulariser

Objectif du jour : définir une cible, choisir un découpage cohérent et créer une baseline reproductible. Faire relier toute amélioration de score à une hypothèse vérifiable. Terminer la journée avec TP01 et un protocole écrit que le binôme pourra réutiliser dans le projet final.

À retenir : Lundi 21 septembre · Construire une comparaison fiable

## Diapositive 11 · Le problème avant l'algorithme

Activité de 10 minutes : chaque binôme formule la campagne d'appels en une phrase. Exemple : classer les clients éligibles avant le premier appel de la campagne. Demander ce qui changerait pour une prédiction après l'appel. Reprendre le cycle CRISP-DM comme un aller-retour entre compréhension métier, données, préparation, modélisation, évaluation et usage.

À retenir : Écrire la décision, l'horizon et la métrique avant d'entraîner

Références : R38 (support local)

## Diapositive 12 · Le contrat des données du fil rouge

Le site UCI présente plusieurs versions qu'il faut distinguer. Nous utilisons le fichier additionnel de 4 119 lignes, un sous-échantillon aléatoire de la version complète de 41 188 lignes. La page générale affiche aussi des chiffres d'une autre version : ne pas les mélanger. La colonne duration est exclue pour une décision antérieure à l'appel. L'empreinte SHA-256 vérifie la copie distribuée.

Références : [R32](https://archive.ics.uci.edu/dataset/222/bank+marketing)

## Diapositive 13 · Trois familles de fuites

Proposer trois cas : duration après l'appel, normalisation sur tout le fichier, plusieurs transactions du même client dans train et test. Demander de classer les cas. Expliquer qu'une excellente performance peut constituer un signal d'alarme. Une pipeline protège contre certaines fuites d'apprentissage, mais ne décide pas à notre place si une variable est légitime.

À retenir : Une variable disponible dans le fichier n'est pas forcément disponible à la décision

Références : [R02](https://scikit-learn.org/stable/common_pitfalls.html), [R32](https://archive.ics.uci.edu/dataset/222/bank+marketing)

## Diapositive 14 · Entraînement, validation et test

Distinguer jeu de validation explicite et plis de validation croisée. Le test est un contrat organisationnel, pas un simple nom de variable. Dans TP01, X_test existe mais n'est jamais scoré. Les recherches, ablations et choix de seuil appartiennent au développement. Un nouveau choix après le test réclame une nouvelle évaluation indépendante.

À retenir : Regarder souvent le test revient à l'utiliser pour choisir

Références : [R03](https://scikit-learn.org/stable/modules/cross_validation.html)

## Diapositive 15 · Choisir le bon découpage

Faire expliquer l'unité statistique : ligne, personne, machine ou période. La stratification ne résout ni la dépendance par groupes ni les fuites temporelles. Un gap peut être nécessaire si les fenêtres de features et de labels se chevauchent. Sur notre sous-échantillon aléatoire sans identifiant personne, reconnaître explicitement l'impossibilité de garantir une évaluation par personnes et périodes disjointes.

Références : [R03](https://scikit-learn.org/stable/modules/cross_validation.html)

## Diapositive 16 · La pipeline apprend dans chaque pli

Faire dessiner au tableau les frontières de la CV. Les données de validation peuvent traverser transform, jamais fit. Prévoir handle_unknown pour les nouvelles catégories. Dans une imblearn.Pipeline, le rééchantillonnage n'est réalisé qu'à l'ajustement. Montrer les paramètres de la pipeline avec get_params sans exécuter d'optimisation exhaustive.

À retenir : ColumnTransformer traite les colonnes ; Pipeline relie les étapes

Références : [R02](https://scikit-learn.org/stable/common_pitfalls.html), [R18](https://scikit-learn.org/stable/modules/preprocessing.html)

## Diapositive 17 · La matrice de confusion se lit avec un coût

Exemple original : 100 positifs et 900 négatifs. La précision vaut 60/150 = 0,40. Le rappel vaut 60/100 = 0,60. L'accuracy vaut 870/1000 = 0,87. Le F1 vaut 2×0,4×0,6/(0,4+0,6) = 0,48. Demander aux étudiants quel chiffre regarder si les 150 alertes dépassent la capacité quotidienne d'analyse.

À retenir : 1 000 observations : 60 vrais positifs et 90 faux positifs

Références : [R04](https://scikit-learn.org/stable/modules/model_evaluation.html), R39 (support local)

## Diapositive 18 · Le piège de l'accuracy

Exemple construit, sans lien avec le taux de souscription UCI. Demander si balanced accuracy résout tous les problèmes : non, elle moyenne les rappels des classes mais ne représente pas le coût métier. En multiclasse, distinguer macro, micro et moyenne pondérée. Les rares classes peuvent disparaître dans une moyenne dominée par la majorité.

À retenir : La métrique dépend de la décision, pas de ce qui donne le plus grand nombre

Références : [R04](https://scikit-learn.org/stable/modules/model_evaluation.html)

## Diapositive 19 · ROC : ordonner les positifs et les négatifs

Le graphique vient d'une expérimentation synthétique reproductible. L'AUC-ROC évalue le classement, pas le coût ni la calibration. À prévalence rare, un faible taux de faux positifs peut encore produire beaucoup d'alertes. Demander de convertir un FPR de 1% en nombre d'alertes parmi 100 000 négatifs.

Références : [R04](https://scikit-learn.org/stable/modules/model_evaluation.html)

## Diapositive 20 · Précision-rappel : regarder les alertes utiles

Le modèle et les observations sont identiques à la diapositive ROC. La précision varie avec la prévalence, donc deux jeux de tests ayant des prévalences différentes ne se comparent pas naïvement. Average precision résume des incréments de rappel pondérés par la précision. Ne pas appeler automatiquement ce nombre aire trapézoïdale PR. Les notebooks utilisent average_precision_score.

Références : [R04](https://scikit-learn.org/stable/modules/model_evaluation.html)

## Diapositive 21 · Évaluer une régression

Faire calculer MAE et RMSE pour des résidus 1, 1 et 10. MAE=4 et RMSE=√34≈5,83. Discuter les valeurs extrêmes avant de les supprimer. Un R² négatif signifie que le modèle est moins bon que la référence constante correspondant à la moyenne de l'échantillon évalué. La MAPE devient délicate avec des valeurs nulles ou proches de zéro.

Références : [R04](https://scikit-learn.org/stable/modules/model_evaluation.html)

## Diapositive 22 · Minimiser une perte avec une pénalité

Expliquer chaque symbole : n observations, θ paramètres, ℓ perte individuelle, Ω pénalité, λ force de régularisation. Pour la logistique, une probabilité très confiante et fausse est fortement pénalisée par la log-loss. La perte optimisée peut différer de la métrique finale, par exemple log-loss pour apprendre et AP pour comparer le classement.

Références : [R05](https://scikit-learn.org/stable/modules/linear_model.html)

## Diapositive 23 · Biais et variance

La décomposition montrée concerne la perte quadratique avec les hypothèses usuelles et une moyenne sur des jeux d'entraînement. Ce n'est pas une décomposition universelle de toute métrique. Les valeurs sont schématiques, pas mesurées. Faire prédire l'effet d'un arbre plus profond et celui d'une moyenne d'arbres.

Références : [R08](https://scikit-learn.org/stable/auto_examples/ensemble/plot_bias_variance.html)

## Diapositive 24 · Courbes d'apprentissage

Courbes construites pour l'enseignement. Elles ne promettent pas que doubler le volume améliore toujours le modèle. Les courbes réelles ont une incertitude et dépendent du protocole de découpage. Demander quelle action tester lorsque le train est excellent et la validation mauvaise : régulariser, réduire la complexité, vérifier les fuites et enrichir les données pertinentes.

Références : [R08](https://scikit-learn.org/stable/auto_examples/ensemble/plot_bias_variance.html)

## Diapositive 25 · L1 et L2 n'ont pas le même effet

L'exemple représente un seul coefficient avec une normalisation fixée de la perte. La valeur exacte de λ n'est pas transférable entre bibliothèques sans vérifier leurs conventions. En présence de variables corrélées, Lasso peut choisir une variable parmi plusieurs alternatives. Ne pas interpréter cette sélection comme une preuve d'absence d'intérêt des autres.

Références : [R05](https://scikit-learn.org/stable/modules/linear_model.html)

## Diapositive 26 · Elastic Net et choix de régularisation

Les conventions de paramétrage changent selon les estimateurs : l'α de cette formule est un taux de mélange, pas nécessairement le paramètre alpha d'une classe Python. Faire lire la signature de l'estimateur avant de programmer. Conserver le centrage et la standardisation dans les plis. Une variable catégorielle encodée reste un groupe de colonnes à interpréter ensemble.

Références : [R05](https://scikit-learn.org/stable/modules/linear_model.html)

## Diapositive 27 · SVM : marge et noyaux

Une marge est une distance à une frontière dans l'espace des features. Gamma élevé peut produire des frontières très locales et fragiles. Le noyau permet de travailler implicitement dans un espace transformé sans créer explicitement toutes ses coordonnées. Un score de décision SVM n'est pas directement une probabilité. La calibration et le coût de calcul doivent être considérés séparément.

À retenir : Standardiser puis régler C et gamma sur une échelle logarithmique

Références : [R06](https://scikit-learn.org/stable/modules/svm.html)

## Diapositive 28 · TP01 : établir la baseline

Commencer par TP00 si l'environnement n'a pas été préparé. Débrief attendu : les résultats sont des estimations conditionnelles au protocole. Ne pas exiger un score fixe selon la machine. Évaluer la justification des choix et l'absence d'accès au test. Les permutations de cible sont un outil de diagnostic, pas un remplacement d'un protocole de test statistique correctement défini.

À retenir : 120 minutes · notebooks/etudiants/01_evaluation.ipynb

Références : [R02](https://scikit-learn.org/stable/common_pitfalls.html), [R03](https://scikit-learn.org/stable/modules/cross_validation.html)

## Diapositive 29 · Quiz J1 : défendre son protocole

Réponses : non, apprendre les statistiques sur chaque train de pli ; découper par client pour l'objectif de généralisation à de nouveaux clients ; meilleur classement possible mais probabilités moins fidèles. Demander un contre-exemple concret à chaque réponse. Les corrigés détaillés et questions supplémentaires figurent dans evaluation/CORRIGES_QUIZ.md.

À retenir : Répondre seul, comparer en binôme, puis justifier

Références : [R02](https://scikit-learn.org/stable/common_pitfalls.html), [R03](https://scikit-learn.org/stable/modules/cross_validation.html), [R16](https://scikit-learn.org/stable/modules/calibration.html)

## Diapositive 30 · Les acquis du jour 1

Faire déposer au binôme son protocole en une page : définition de la cible, unité d'observation, variables interdites, découpage et métriques. Ce document sera audité lors du projet final. Demander un point encore confus pour orienter la reprise du lendemain.

À retenir : Demain : améliorer le modèle sans dégrader la qualité de la comparaison

## Diapositive 31 · Ensembles et optimisation

Reprendre deux questions du jour 1 puis annoncer le fil : comprendre un arbre, diversifier les erreurs, corriger les résidus et choisir un budget de recherche. TP02 compare des familles sur une régression synthétique. TP03 évalue la procédure d'optimisation avec une boucle externe.

À retenir : Mardi 22 septembre · Comparer performance, stabilité et coût

## Diapositive 32 · Un arbre partitionne l'espace

Dessiner au tableau un exemple original : âge supérieur à 40 puis nombre de contacts antérieurs. Les seuils numériques ne constituent pas une recommandation bancaire. Un arbre apprend de manière gloutonne : il choisit la meilleure division disponible selon son critère, puis poursuit récursivement. Demander ce qu'il se passe lorsqu'une seule observation change près d'un seuil.

À retenir : Une règle lisible peut appartenir à un arbre globalement instable

Références : [R40](https://scikit-learn.org/stable/modules/tree.html), R39 (support local)

## Diapositive 33 · Calculer un gain de Gini

Faire calculer Gini = 1 − Σk pk². Dans le parent, p=0,4, donc Gini=1−0,16−0,36=0,48. Le gain est la différence entre l'impureté du parent et la moyenne pondérée des enfants. La division ici est informative mais n'isole pas parfaitement les classes. Gini mesure une impureté de classes, pas une précision hors échantillon.

Références : [R40](https://scikit-learn.org/stable/modules/tree.html)

## Diapositive 34 · Contrôler la complexité d'un arbre

Mettre en perspective le support de 2020 qui mentionne un ordre de grandeur de 30 observations. Ce n'est pas une contrainte mathématique universelle. Un minimum utile dépend du bruit, de la prévalence et du volume. Pour le pruning, expliquer la pénalité sur le nombre de feuilles et la séquence de sous-arbres. Choisir la pénalité uniquement dans les données de développement.

À retenir : Les seuils se valident ; aucune taille minimale universelle de feuille

Références : [R40](https://scikit-learn.org/stable/modules/tree.html), R39 (support local)

## Diapositive 35 · Bagging : moyenner des modèles instables

Un échantillon bootstrap de taille n contient des répétitions et n'inclut pas toutes les observations d'origine. La probabilité limite qu'une observation soit absente vaut environ e^-1, soit 36,8%. Cette propriété explique les observations out-of-bag. La moyenne réduit surtout la variance si les erreurs ne sont pas parfaitement corrélées. La classification utilise des votes ou une moyenne de probabilités selon la méthode.

À retenir : Le bénéfice dépend autant de la diversité que du nombre d'estimateurs

Références : [R07](https://scikit-learn.org/stable/modules/ensemble.html), [R08](https://scikit-learn.org/stable/auto_examples/ensemble/plot_bias_variance.html)

## Diapositive 36 · Pourquoi la corrélation limite le gain

Sous une variance identique σ² et une corrélation commune ρ, Var(moyenne)=σ²[ρ+(1−ρ)/M]. Dériver au tableau la somme des M variances et des M(M−1) covariances divisée par M². Pour M infini, la limite vaut ρσ². Ce modèle simplifié illustre un mécanisme, il ne décrit pas exactement toute forêt entraînée.

Références : [R08](https://scikit-learn.org/stable/auto_examples/ensemble/plot_bias_variance.html)

## Diapositive 37 · Random Forest : diversifier les divisions

Baisser max_features peut réduire la corrélation mais dégrader chaque arbre. Une forêt profonde n'est pas équivalente à un boosting peu profond. Les importances fondées sur la diminution d'impureté peuvent favoriser certaines variables, notamment à forte cardinalité. Réserver la discussion de l'interprétation à la permutation sur validation du jour 5.

À retenir : Comparer la force des arbres et la corrélation de leurs erreurs

Références : [R07](https://scikit-learn.org/stable/modules/ensemble.html)

## Diapositive 38 · Out-of-bag : utile avec ses limites

L'absence d'une ligne dans un bootstrap ne garantit pas l'absence d'autres lignes du même client. Un prétraitement appris hors de la forêt sur toutes les données peut également limiter l'interprétation. Ne pas régler indéfiniment sur l'OOB puis présenter ce score comme une mesure finale indépendante. Pour ce cours, la CV reste le protocole commun de comparaison.

À retenir : OOB ne remplace pas un test cohérent avec l'usage futur

Références : [R07](https://scikit-learn.org/stable/modules/ensemble.html), [R03](https://scikit-learn.org/stable/modules/cross_validation.html)

## Diapositive 39 · Boosting : corriger progressivement le modèle

Pour la perte quadratique, la direction à apprendre correspond aux résidus. Pour d'autres pertes, il s'agit du gradient négatif de la perte par rapport à la prédiction. Le boosting est séquentiel : l'étape suivante dépend des précédentes. Ne pas le décrire comme une simple moyenne d'arbres indépendants. Le nombre d'étapes et le learning rate doivent être réglés ensemble.

Références : [R11](https://xgboost.readthedocs.io/en/stable/tutorials/model.html)

## Diapositive 40 · Une itération de boosting à la main

Exemple original avec une variable ordonnée x=(1,2,3) et y=(2,3,7). F0 est la moyenne 4. Un arbre à une division, entre x=2 et x=3, ajuste les résidus : −1,5 et +3. Avec η=0,5, F1=(3,25,3,25,5,5). Faire calculer la nouvelle erreur quadratique et comparer à F0. La même logique de résidu ne s'applique telle quelle qu'à certaines pertes.

À retenir : La souche prédit −1,5 pour les deux premiers points et +3 pour le troisième

Références : [R11](https://xgboost.readthedocs.io/en/stable/tutorials/model.html)

## Diapositive 41 · Le gradient généralise le résidu

Relier cette étape à la descente de gradient connue des étudiants, mais dans un espace de fonctions. Pour une régression avec demi-perte quadratique, le gradient négatif est y−F(x). Avec une perte logistique et un score brut, le gradient est lié à y−p. Éviter de confondre le score brut, la probabilité après fonction logistique et la classe après seuillage.

Références : [R11](https://xgboost.readthedocs.io/en/stable/tutorials/model.html)

## Diapositive 42 · Quand arrêter le boosting ?

Courbes réellement calculées sur un problème Friedman synthétique. Un minimum peu marqué invite à considérer la variabilité, pas à choisir une itération à la décimale près. Early stopping constitue une sélection d'hyperparamètre : les données utilisées pour arrêter sont des données de validation. Un jeu temporel demande une validation d'arrêt qui respecte lui aussi le temps.

Références : [R07](https://scikit-learn.org/stable/modules/ensemble.html), [R09](https://scikit-learn.org/stable/modules/grid_search.html)

## Diapositive 43 · Boosting par histogrammes

Expliquer le compromis résolution/coût sans promettre une accélération universelle. HistGradientBoosting est disponible dans scikit-learn et suffit au socle des TP. Son comportement sur valeurs manquantes et catégories dépend des entrées et de la version. Notre pipeline générique prépare explicitement les colonnes pour rendre la comparaison transparente, même lorsqu'un autre pipeline natif serait possible.

À retenir : Un gain de calcul permet davantage d'expériences, pas un protocole moins strict

Références : [R07](https://scikit-learn.org/stable/modules/ensemble.html), [R12](https://lightgbm.readthedocs.io/en/stable/Features.html)

## Diapositive 44 · Quatre implémentations à connaître

Présenter ce tableau comme des choix d'implémentation, pas un classement de performance. Les paramètres qui portent le même nom ne sont pas toujours strictement comparables. XGBoost expose des mécanismes de régularisation et une optimisation du second ordre. LightGBM est notamment connu pour sa croissance par feuille. CatBoost propose un traitement spécialisé des catégories et de l'ordered boosting. Les trois bibliothèques sont des extensions, pas des dépendances indispensables cette semaine.

Références : [R11](https://xgboost.readthedocs.io/en/stable/tutorials/model.html), [R12](https://lightgbm.readthedocs.io/en/stable/Features.html), [R13](https://catboost.ai/docs/en/concepts/algorithm-main-stages)

## Diapositive 45 · Voting et stacking

Expliquer pourquoi un méta-modèle recevant des prédictions d'entraînement trop parfaites apprend un signal trompeur. StackingRegressor produit des prédictions hors pli pour cette phase. Si l'on évalue le stacking dans une boucle externe, ses propres ajustements doivent rester dans le train externe. Discuter la complexité opérationnelle d'un ensemble de nombreuses familles.

À retenir : Prédictions hors pli pour le méta-modèle, test final pour l'ensemble

Références : [R07](https://scikit-learn.org/stable/modules/ensemble.html)

## Diapositive 46 · TP02 : comparer les ensembles

La source synthétique permet de connaître les variables informatives sans télécharger un nouveau jeu. Demander de conserver tous les résultats, y compris les essais moins bons. Le temps d'ajustement dépend du matériel. Une extension stacking est proposée si les objectifs centraux sont atteints. Le débrief compare les mécanismes, pas seulement le classement des chiffres.

À retenir : 90 minutes · notebooks/etudiants/02_ensembles.ipynb

Références : [R07](https://scikit-learn.org/stable/modules/ensemble.html)

## Diapositive 47 · Définir un espace d'hyperparamètres

Exercice court : proposer un espace pour un boosting avec 4 valeurs de learning rate, 5 capacités d'arbre et 6 nombres d'itérations. La grille contient déjà 120 configurations, donc 360 ajustements pour une CV à trois plis, avant refit. Certains paramètres interagissent fortement. Conserver la même règle d'arrêt et le même budget pour comparer les méthodes de recherche.

À retenir : Écrire le budget d'essais avant de lancer la recherche

Références : [R09](https://scikit-learn.org/stable/modules/grid_search.html)

## Diapositive 48 · Grille, recherche aléatoire et TPE

TPE est une méthode d'optimisation séquentielle fondée sur un modèle des bonnes et moins bonnes régions. Elle n'est pas magique et a besoin d'un budget approprié. Sur huit essais, la phase initiale aléatoire compte beaucoup ; le TP fixe quatre essais initiaux. Le pruning évite de terminer certaines expériences peu prometteuses si des mesures intermédiaires comparables sont disponibles.

À retenir : Le meilleur score interne est un résultat de sélection

Références : [R09](https://scikit-learn.org/stable/modules/grid_search.html), [R10](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/003_efficient_optimization_algorithms.html)

## Diapositive 49 · Validation croisée imbriquée

Faire dessiner trois plis externes et trois plis internes dans un train externe. Pour chaque pli externe, la recherche repart de zéro. Si l'on sélectionne ensuite une nouvelle méthode en regardant tous les scores externes, ces scores participent à un nouveau niveau de sélection. Un test final séparé reste utile pour une décision finale importante.

À retenir : La boucle externe évalue une méthode de travail, pas un unique modèle final

Références : [R03](https://scikit-learn.org/stable/modules/cross_validation.html), [R09](https://scikit-learn.org/stable/modules/grid_search.html)

## Diapositive 50 · L'optimisation a un coût mesurable

Faire calculer le coût avant exécution. Ce total correspond au TP03 pour une recherche RandomizedSearchCV avec refit. Distinguer nombre d'ajustements et temps : deux familles peuvent avoir des coûts très différents. Les threads BLAS et n_jobs peuvent se multiplier ; on limite ici le parallélisme. Archiver le budget avec les scores.

Références : [R09](https://scikit-learn.org/stable/modules/grid_search.html)

## Diapositive 51 · Interpréter une petite différence

Ne pas calculer un intervalle de confiance naïf en traitant des plis recouvrants comme des échantillons indépendants. Les variations d'entraînement, de population et d'étiquetage doivent être distinguées. Un bootstrap du test suppose lui aussi une unité de rééchantillonnage adaptée, par exemple le client, et ne mesure pas toutes les sources d'incertitude du réentraînement.

À retenir : Les scores de plis corrélés ne sont pas des répétitions indépendantes

Références : [R03](https://scikit-learn.org/stable/modules/cross_validation.html)

## Diapositive 52 · TP03 : optimiser avec un budget fixé

Le TP utilise une logistique et des données synthétiques pour que le coût reste léger et que le protocole soit visible. L'objectif n'est pas de gagner un concours d'AP. Demander aux étudiants d'annoter quelles observations sont visibles à chaque étape. Les résultats aléatoires doivent être enregistrés, pas relancés jusqu'à obtenir une préférence attendue.

À retenir : 90 minutes · notebooks/etudiants/03_optimisation.ipynb

Références : [R09](https://scikit-learn.org/stable/modules/grid_search.html), [R10](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/003_efficient_optimization_algorithms.html)

## Diapositive 53 · Quiz J2 : mécanismes et protocole

Réponses : leurs erreurs sont corrélées, donc la variance ne s'annule pas ; un estimateur de la direction de correction, souvent le gradient négatif ; le maximum a été sélectionné parmi plusieurs scores bruités. Ajouter que la boucle externe réduit le biais de sélection lorsqu'elle encapsule bien toute la procédure.

À retenir : Donner une justification avant de citer une bibliothèque

Références : [R08](https://scikit-learn.org/stable/auto_examples/ensemble/plot_bias_variance.html), [R11](https://xgboost.readthedocs.io/en/stable/tutorials/model.html), [R09](https://scikit-learn.org/stable/modules/grid_search.html)

## Diapositive 54 · Les acquis du jour 2

Faire formuler un cas où la forêt constitue un choix raisonnable et un autre où un boosting est à expérimenter. Refuser une réponse universelle. Vérifier que les binômes ont conservé les graines, les budgets et les scores de tous les plis.

À retenir : Demain : transformer une probabilité en décision dans un problème déséquilibré

## Diapositive 55 · Déséquilibre et features

Reprise du protocole puis raisonnement par coûts. La matinée distingue apprendre, calibrer et décider. L'après-midi relie les variables à l'instant de décision et aux ablations. L'atelier features complète TP04 avec un cahier de travail, un corrigé méthodologique et des critères de comparaison.

À retenir : Mercredi 23 septembre · Relier données, probabilités et décisions

## Diapositive 56 · Trois décisions différentes

Une transformation monotone peut préserver le classement tout en modifiant la calibration. Un changement de seuil modifie précision et rappel mais ne réentraîne pas le modèle. Demander si un algorithme avec le meilleur ROC-AUC est nécessairement le meilleur choix pour un centre d'appels limité à 100 contacts par jour. La réponse dépend du segment de la courbe et de la décision.

À retenir : Améliorer l'une de ces étapes n'améliore pas automatiquement les autres

Références : [R16](https://scikit-learn.org/stable/modules/calibration.html), [R17](https://scikit-learn.org/stable/modules/classification_threshold.html)

## Diapositive 57 · Donner un coût aux erreurs

L'exemple du TP fixe CFP=1 et CFN=5 en unités pédagogiques. Ne pas présenter ces valeurs comme des euros ni une mesure de bénéfice réel. Les coûts des décisions correctes sont ici supposés nuls. En cas d'utilités positives, de contraintes ou de coûts individuels, écrire une fonction d'utilité plus complète.

Références : [R17](https://scikit-learn.org/stable/modules/classification_threshold.html)

## Diapositive 58 · Le seuil doit être choisi sur validation

La courbe est calculée sur une validation synthétique. Les points d'une grille de seuils donnent un aperçu ; le TP examine toutes les probabilités uniques pour minimiser le coût empirique. Un minimum sur un petit échantillon peut être instable. Faire discuter les seuils voisins et une contrainte de rappel minimal plutôt qu'un seuil présenté avec une précision injustifiée.

Références : [R17](https://scikit-learn.org/stable/modules/classification_threshold.html)

## Diapositive 59 · Un seuil théorique sous hypothèses

Comparer l'espérance de perte d'une décision positive CFP(1−p) et d'une décision négative CFN p. Déduire la formule. Ce résultat n'est pas une règle universelle : prévalence changée, calibration imparfaite, coûts variables et capacité limitée demandent une adaptation. Le seuil empirique du TP peut différer de 1/6 pour ces raisons et à cause de la variabilité d'échantillonnage.

Références : [R17](https://scikit-learn.org/stable/modules/classification_threshold.html)

## Diapositive 60 · Fβ et rappel sous contrainte

Faire calculer F2 à précision 0,4 et rappel 0,6 : 5×0,24/(4×0,4+0,6)=1,2/2,2≈0,545. Fβ encode un compromis abstrait, pas forcément un coût métier. Sur validation, une contrainte peut être satisfaite par hasard avec peu de positifs. Le volume et l'incertitude doivent accompagner le résultat.

Références : [R04](https://scikit-learn.org/stable/modules/model_evaluation.html)

## Diapositive 61 · Cinq leviers contre le déséquilibre

Partir d'une baseline et d'une métrique adaptée avant de sampler. Le déséquilibre ne rend pas chaque jeu de données automatiquement difficile : le chevauchement des classes, le bruit et le nombre absolu de positifs comptent aussi. Ne pas changer la prévalence du test pour rendre les métriques plus favorables. Comparer chaque levier sur le même jeu de validation représentatif.

Références : [R14](https://imbalanced-learn.org/stable/common_pitfalls.html), [R17](https://scikit-learn.org/stable/modules/classification_threshold.html)

## Diapositive 62 · Pondérer la fonction de perte

Expliquer que la pondération déplace l'objectif d'apprentissage. L'option balanced utilise les fréquences de classes selon la convention de l'estimateur, mais ne connaît pas les coûts réels de la campagne. Pondérer et baisser le seuil simultanément sans protocole peut doubler un effet recherché. Comparer les effets avec des ablations contrôlées.

Références : [R14](https://imbalanced-learn.org/stable/common_pitfalls.html), [R16](https://scikit-learn.org/stable/modules/calibration.html)

## Diapositive 63 · SMOTE : interpoler dans la classe minoritaire

Exemple original au tableau : xi=(2,4), voisin=(6,8), u=0,25 donne (3,5). Faire examiner les unités et la standardisation avant de mesurer les distances. SMOTE n'ajoute pas de nouvelle information observée et peut amplifier des labels erronés. Près d'une frontière, l'interpolation peut traverser une zone de l'autre classe. Le nombre de voisins doit être compatible avec les effectifs des plis.

Références : [R15](https://www.jair.org/index.php/jair/article/view/10302)

## Diapositive 64 · Où placer le rééchantillonnage ?

Contre-exemple : fabriquer les points SMOTE sur tout le fichier puis lancer une CV permet à des points très voisins de se retrouver des deux côtés. Le score devient artificiellement favorable et la distribution de validation n'est plus celle d'usage. Avec des catégories, comparer SMOTENC à la pondération. Une interpolation des colonnes one-hot peut créer des catégories fractionnaires sans sens.

À retenir : Utiliser imblearn.Pipeline pour encapsuler cette procédure

Références : [R14](https://imbalanced-learn.org/stable/common_pitfalls.html), [R15](https://www.jair.org/index.php/jair/article/view/10302)

## Diapositive 65 · Lire une courbe de calibration

Le graphique est schématique. La courbe observée p² correspond à de la surconfiance pour p dans ]0,1[. En pratique, choisir les bins et montrer leurs effectifs. Une bonne calibration globale peut masquer une mauvaise calibration dans un sous-groupe. Le Brier évalue la qualité des probabilités mais n'isole pas à lui seul toute la calibration.

Références : [R16](https://scikit-learn.org/stable/modules/calibration.html)

## Diapositive 66 · Apprendre une calibration sans fuite

Décrire le rôle de la CV interne dans CalibratedClassifierCV. Le train sert à produire des prédictions hors pli pour calibrer. Un autre jeu de validation sert ensuite à choisir le seuil. Le test estime la procédure une fois ces choix figés. Sur peu de positifs, une calibration flexible risque d'être instable. Ne pas annoncer une calibration meilleure sans la mesurer.

À retenir : CalibratedClassifierCV puis validation du seuil

Références : [R16](https://scikit-learn.org/stable/modules/calibration.html)

## Diapositive 67 · Concevoir des variables utiles

Une feature résume une hypothèse sur le problème. Décrire son nom, son unité, sa formule, sa fenêtre temporelle et son instant de disponibilité. Une interaction utile à une régression peut être déjà capturée par un arbre. La valeur ajoutée se mesure par une ablation conservant le même protocole. Les variables dérivées de données sensibles ou de proxys exigent une réflexion explicite sur l'usage.

Références : [R18](https://scikit-learn.org/stable/modules/preprocessing.html), [R41](https://scikit-learn.org/stable/modules/feature_selection.html)

## Diapositive 68 · Valeurs manquantes et catégories inconnues

Le loader remplace explicitement unknown par une valeur manquante. La branche numérique impute la médiane et ajoute un indicateur. La branche catégorielle impute la modalité fréquente, choix de baseline à discuter. Une autre stratégie conserverait une catégorie manquante explicite. Documenter ces choix et mesurer leur effet. Pour pdays, le code 999 doit être compris à partir du dictionnaire UCI.

À retenir : L'imputation est une hypothèse, pas une restauration de la vérité

Références : [R18](https://scikit-learn.org/stable/modules/preprocessing.html), [R32](https://archive.ics.uci.edu/dataset/222/bank+marketing)

## Diapositive 69 · Target encoding et cross-fitting

La formule illustre un lissage simple, pas tous les détails de TargetEncoder. Une catégorie presque unique peut révéler le label si le calcul est naïf. Le cross-fitting calcule l'encodage de chaque observation à partir d'autres plis. Dans scikit-learn, fit_transform et fit suivi de transform n'ont donc pas le même comportement d'entraînement. Pour des groupes ou du temps, auditer aussi les sous-plis internes de l'encodeur.

Références : [R19](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.TargetEncoder.html)

## Diapositive 70 · Ratios, interactions et variables temporelles

Exemples : fréquence de contacts sur 30 jours, ancienneté, interaction entre catégorie et nombre d'interactions. La somme d'événements doit être calculée point-in-time. Décrire un test manuel sur une ligne : la feature aurait-elle pu être produite le jour de la décision ? L'atelier features traite pdays=999 et compare une transformation documentée au pipeline de base.

À retenir : Une agrégation correcte dans le passé peut devenir une fuite si elle inclut le futur

Références : [R18](https://scikit-learn.org/stable/modules/preprocessing.html), [R32](https://archive.ics.uci.edu/dataset/222/bank+marketing)

## Diapositive 71 · Sélection de variables et ablation

Choisir des variables sur tout le jeu en regardant leur lien à y constitue une fuite même si l'on applique ensuite une CV au modèle. Avec des variables corrélées, retirer une seule colonne peut masquer une dépendance de groupe. Préférer des ablations interprétables et un budget défini. Consigner les essais pour ne pas transformer la validation en concours sans fin.

À retenir : La sélection supervisée fait partie de l'entraînement

Références : [R41](https://scikit-learn.org/stable/modules/feature_selection.html), [R25](https://scikit-learn.org/stable/modules/permutation_importance.html)

## Diapositive 72 · Corrélation : deux précisions utiles

Complément critique au support de méthodologie de 2020. Corr(X,aY+b)=Corr(X,Y) si a>0, et le signe est inversé si a<0. La covariance dépend en revanche des unités. Demander aux étudiants pourquoi passer des euros aux centimes change une distance euclidienne brute mais pas le coefficient de corrélation. Ces distinctions évitent de justifier le scaling par une raison erronée.

À retenir : Ne pas confondre covariance, corrélation et distance

Références : R39 (support local), [R18](https://scikit-learn.org/stable/modules/preprocessing.html)

## Diapositive 73 · TP04 : une décision validée

Exiger une séparation écrite des trois étapes : apprendre, calibrer, décider. Ne pas accepter une optimisation du seuil sur test. Demander la matrice de confusion avec effectifs, pas seulement un score. Le coût de validation peut être inférieur au coût de test ; c'est précisément la raison de garder un test indépendant.

À retenir : 120 minutes · notebooks/etudiants/04_desequilibre.ipynb

Références : [R14](https://imbalanced-learn.org/stable/common_pitfalls.html), [R16](https://scikit-learn.org/stable/modules/calibration.html), [R17](https://scikit-learn.org/stable/modules/classification_threshold.html)

## Diapositive 74 · Atelier : auditer et enrichir les features

Le livrable est un tableau de contrat et une analyse expérimentale argumentée. L'extension target encoding exige un cross-fitting compatible avec le split. Le corrigé méthodologique donne les attentes sans prétendre qu'une feature améliore systématiquement un modèle. Le score moyen est secondaire à la bonne définition des variables et à l'absence de fuite.

À retenir : 60 minutes · docs/ATELIER_FEATURES.md

Références : [R19](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.TargetEncoder.html), [R32](https://archive.ics.uci.edu/dataset/222/bank+marketing)

## Diapositive 75 · Quiz J3 : expliquer les compromis

Réponses : non, le seuil dépend des coûts et contraintes ; le test doit représenter la distribution d'usage et l'équilibrer change notamment la précision ; un encodage supervisé naïf peut mémoriser la cible et ne pas généraliser aux catégories rares ou nouvelles. Faire proposer une vérification concrète pour chacun de ces risques.

À retenir : Une réponse correcte doit préciser la population et le protocole

Références : [R14](https://imbalanced-learn.org/stable/common_pitfalls.html), [R17](https://scikit-learn.org/stable/modules/classification_threshold.html), [R19](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.TargetEncoder.html)

## Diapositive 76 · Les acquis du jour 3

Demander une seule recommandation d'action par binôme, avec métrique, seuil, volume attendu et limite. La réponse « SMOTE marche mieux » est insuffisante si elle n'indique pas la métrique, les données et le budget. Reprendre le protocole du projet final pour y ajouter le contrat de features.

À retenir : Demain : découvrir une structure quand la cible n'est pas donnée

## Diapositive 77 · Clustering et anomalies

L'objectif est de relier une partition à une représentation, une distance et une hypothèse. Insister sur le fait que l'absence de cible n'élimine pas le besoin d'évaluation. TP05 compare les mêmes points avec plusieurs méthodes, puis discute la stabilité et l'utilité. Les anomalies sont une extension vers la détection et le triage.

À retenir : Jeudi 24 septembre · Explorer une structure sans inventer une vérité

## Diapositive 78 · Un cluster dépend de la représentation

Faire décrire deux segmentations plausibles d'une population de clients : comportement d'achat ou contraintes de contact. Des variables et unités différentes conduisent à des partitions différentes. Les numéros de clusters sont arbitraires : le groupe 0 n'est pas intrinsèquement inférieur au groupe 1. Les étiquettes métier viennent après l'examen des profils.

À retenir : Un identifiant de cluster est un résultat d'algorithme, pas une classe naturelle

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html)

## Diapositive 79 · Distances et échelles

Exemple : revenu en euros et âge en années. Passer le revenu en centimes multiplie sa contribution à la distance euclidienne au carré. Standardiser peut équilibrer les contributions mais aussi donner du poids au bruit. Les données mixtes ne se traitent pas sans réflexion par une simple distance euclidienne sur un encodage one-hot. Demander quelles ressemblances le problème cherche réellement à représenter.

À retenir : Standardiser selon le sens métier, pas par automatisme

Références : [R18](https://scikit-learn.org/stable/modules/preprocessing.html), [R20](https://scikit-learn.org/stable/modules/clustering.html)

## Diapositive 80 · PCA : projeter en conservant de la variance

La SVD donne une formulation stable : les colonnes de V sont des directions de l'espace des features. La PCA centre les données, mais le scaling préalable dépend des unités et de l'objectif. La cible n'intervient pas : une direction de faible variance peut être très prédictive. Dans un pipeline supervisé, ajuster la PCA uniquement sur le train de chaque pli.

Références : [R22](https://scikit-learn.org/stable/modules/decomposition.html)

## Diapositive 81 · Lire la variance expliquée

Spectre construit pour un calcul au tableau, pas extrait d'un benchmark. Faire additionner les pourcentages et expliquer ce que l'on conserve. Un seuil de 90% est une convention de compression, pas une garantie de classification ni de clustering. Vérifier la stabilité et le sens des composantes, et comparer le résultat avec l'espace initial lorsque c'est raisonnable.

Références : [R22](https://scikit-learn.org/stable/modules/decomposition.html)

## Diapositive 82 · K-means : minimiser l'inertie

Décomposer la fonction objectif et expliquer pourquoi la moyenne minimise une somme de distances euclidiennes au carré. Une initialisation différente peut mener à une autre solution locale. k-means++ choisit des centres initiaux espacés, sans garantir le minimum global. Fixer explicitement n_init dans les exemples pour contrôler le nombre de redémarrages.

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html)

## Diapositive 83 · Une itération de K-means

Les centres initiaux sont 0 et 10. L'affectation place 1 et 2 dans A, 8 et 9 dans B. L'inertie initiale est 1²+2²+2²+1²=10. Après mise à jour, quatre écarts de 0,5 donnent 1. Le prochain tour conserve les affectations. Faire varier les centres initiaux pour discuter les minima locaux et les groupes vides.

À retenir : Points 1, 2, 8, 9 : les deux moyennes sont 1,5 et 8,5

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html)

## Diapositive 84 · Une géométrie que K-means représente mal

Les points sont des données synthétiques originales produites avec make_moons et la graine 42. Les couleurs montrent les groupes prédits, pas les classes de génération. Demander aux étudiants de proposer une notion de voisinage plutôt qu'une notion de centre. La comparaison suivante utilisera exactement les mêmes points et échelles.

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html)

## Diapositive 85 · L'inertie ne choisit pas K à votre place

La courbe est mesurée sur les mêmes lunes synthétiques. Un coude peut refléter une approximation géométrique plutôt que des classes naturelles. Ne pas choisir K à partir d'un seul critère puis annoncer une découverte. Demander comment le nombre de groupes s'articule avec le nombre d'actions réellement possibles dans une équipe.

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html)

## Diapositive 86 · Silhouette : séparation et compacité

La silhouette est définie lorsqu'il existe au moins deux groupes et pas un groupe par observation. Elle favorise certaines géométries compactes selon la distance choisie. Pour une méthode avec bruit, calculer la silhouette hors bruit et publier aussi la proportion exclue. Une bonne silhouette après exclusion de presque tous les points peut être peu utile.

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html)

## Diapositive 87 · GMM : une appartenance probabiliste

Contrairement à une affectation dure, la responsabilité représente une probabilité de composante conditionnelle au modèle. Elle n'est pas une probabilité de catégorie métier correcte. Comparer covariance sphérique, diagonale et complète : la flexibilité augmente le nombre de paramètres et le risque d'estimation fragile. Une régularisation des covariances évite certaines singularités numériques.

Références : [R21](https://scikit-learn.org/stable/modules/mixture.html)

## Diapositive 88 · EM : alterner deux problèmes plus simples

Ne pas dire que l'étape E prédit des labels vrais. Elle calcule des poids latents dans le modèle courant. BIC/AIC comparent ajustement et complexité dans leur cadre d'hypothèses. Les scores ne prouvent pas qu'un mélange gaussien est une bonne description métier. Tester plusieurs initialisations et inspecter les composantes minuscules ou dégénérées.

À retenir : EM peut converger vers un optimum local

Références : [R21](https://scikit-learn.org/stable/modules/mixture.html)

## Diapositive 89 · Classification hiérarchique agglomérative

Comparer single linkage, qui peut produire un effet de chaîne, et complete linkage, sensible au diamètre maximal. La hauteur de fusion dépend du linkage et n'a pas un sens universel. Un dendrogramme sur des milliers de points devient illisible. Les structures de distances et la mémoire limitent souvent l'usage direct sur un très grand volume.

À retenir : Ward s'appuie sur la variance et une géométrie euclidienne

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html)

## Diapositive 90 · DBSCAN : relier les régions denses

Distinguer points cœur, frontière et bruit. Le min_samples de scikit-learn compte le point lui-même. Un point frontière peut avoir une affectation dépendant de l'ordre dans certains cas. DBSCAN n'impose pas K, mais cela ne signifie pas qu'il n'a pas de paramètres à choisir. Un eps unique peut mal représenter des densités très différentes.

À retenir : Densité et distance dépendent de l'échelle des variables

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html)

## Diapositive 91 · Les mêmes lunes avec DBSCAN

Les points et leur standardisation sont exactement ceux du graphique K-means. Seul l'algorithme change. Cette réussite synthétique ne prouve pas une supériorité générale de DBSCAN. Discuter sa sensibilité au bruit, aux densités variables et à la dimension. Faire anticiper le résultat pour un eps très grand, puis très petit.

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html)

## Diapositive 92 · HDBSCAN : examiner plusieurs échelles

Le TP utilise sklearn.cluster.HDBSCAN. Le package externe hdbscan n'a pas exactement la même convention pour min_samples : éviter de copier des valeurs sans lire la documentation. Le résultat reste sensible à la représentation et aux hypothèses de densité. Un groupe persistant ne reçoit pas automatiquement un sens métier ni une justification causale.

À retenir : Vérifier la convention de min_samples selon l'implémentation

Références : [R23](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html)

## Diapositive 93 · Comparer les familles de clustering

Demander aux binômes de choisir deux méthodes pour une population compacte, puis deux méthodes pour des groupes non convexes. Ils doivent justifier ce qu'ils considèrent comme une distance légitime. Certains estimateurs n'ont pas de méthode predict pour de nouveaux points : anticiper comment la segmentation sera utilisée après l'analyse.

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html), [R21](https://scikit-learn.org/stable/modules/mixture.html), [R23](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html)

## Diapositive 94 · Évaluer sans labels

L'ARI compare deux partitions en tenant compte de l'accord attendu au hasard, avec des correspondances de numéros de groupes inutiles. Pour des partitions issues de sous-échantillons différents, comparer les observations communes ou utiliser une procédure d'affectation cohérente. Un score interne élevé n'est pas une garantie de pertinence. Ne pas utiliser les labels synthétiques pour régler puis pour annoncer une évaluation indépendante.

À retenir : Stabilité, séparation et utilité répondent à des questions différentes

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html)

## Diapositive 95 · Projections : explorer avec prudence

Montrer que la projection peut rapprocher ou éloigner des observations autrement qu'une lecture naïve ne le suggère. Ne pas interpréter automatiquement la taille d'un îlot ou les distances entre tous les groupes. UMAP peut être mentionné comme prolongement, sans en faire un socle obligatoire. Toujours revenir aux variables, aux voisins et à une validation dans l'espace pertinent.

À retenir : Un joli nuage 2D ne démontre pas le nombre de clusters

Références : [R22](https://scikit-learn.org/stable/modules/decomposition.html), [R42](https://scikit-learn.org/stable/modules/manifold.html)

## Diapositive 96 · Anomalie, nouveauté et classe rare

Présenter Isolation Forest, qui isole les points par des divisions aléatoires, et LOF, qui compare une densité locale à celle des voisins. Pour LOF, le mode novelty change l'usage sur de nouvelles données. Une forte anomalie n'est pas une preuve de fraude ni d'incident. Prévoir le volume de triage, les faux positifs et le délai de retour de labels.

À retenir : Un score d'anomalie doit être relié à une procédure de vérification

Références : [R24](https://scikit-learn.org/stable/modules/outlier_detection.html)

## Diapositive 97 · TP05 : expliquer une partition

Le temps comprend les trois exercices centraux et une analyse rédigée des profils. L'extension Ward est facultative si le groupe doit revenir sur PCA. Donner la priorité aux comparaisons contrôlées et à l'argumentation. Exiger qu'aucune conclusion métier soit tirée de simples numéros de clusters.

À retenir : 150 minutes · notebooks/etudiants/05_clustering.ipynb

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html), [R21](https://scikit-learn.org/stable/modules/mixture.html)

## Diapositive 98 · Quiz J4 : reconnaître les hypothèses

Réponses : non, l'inertie décroît avec la flexibilité ; non, il faut examiner les points exclus et l'objectif ; non, PCA ne voit pas la cible. Demander à chacun un exemple qui contredit une intuition trop simple. Reprendre les schémas du jour pour rattacher chaque réponse à une hypothèse.

Références : [R20](https://scikit-learn.org/stable/modules/clustering.html), [R22](https://scikit-learn.org/stable/modules/decomposition.html)

## Diapositive 99 · Les acquis du jour 4

Faire rédiger une fiche de segmentation : variables, transformations, distance, paramètres, profils, stabilité et limites. Cette fiche permet d'évaluer une analyse non supervisée même sans chiffre unique de performance. Elle peut servir d'extension au projet final, sans remplacer la classification demandée.

À retenir : Demain : expliquer, documenter et défendre le modèle final

## Diapositive 100 · Interpréter et restituer

Les concepts du jour complètent le projet. Commencer par distinguer explication, performance et causalité. Le socle est permutation, PDP/ICE, split-conformal et model card. La veille récente est une lecture critique, sans installation lourde ni promesse de supériorité. Le temps de projet reste protégé.

À retenir : Vendredi 25 septembre · Défendre une décision avec ses limites

## Diapositive 101 · Trois niveaux d'explication

Exemple : une variable liée à une situation sociale peut être très prédictive sans constituer une action pertinente ou acceptable. Les explications dépendent d'un modèle, de données de référence et d'une méthode. Ne pas utiliser l'existence d'un graphique explicatif comme preuve de qualité ou d'absence de biais. Vérifier d'abord que le modèle prédit de façon utile.

À retenir : Une explication prédictive ne répond pas automatiquement à une question causale

Références : [R25](https://scikit-learn.org/stable/modules/permutation_importance.html), [R27](https://papers.nips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html)

## Diapositive 102 · Importance par permutation

Le graphique est réellement calculé sur la régression synthétique Friedman du cours. Les cinq premières variables portent le signal par construction. L'importance dépend de la métrique et du modèle. Une importance négative faible peut refléter du bruit d'estimation ou une variable qui nuit à la prédiction. Si ce diagnostic sert à modifier le modèle, conserver encore un test final indépendant.

Références : [R25](https://scikit-learn.org/stable/modules/permutation_importance.html)

## Diapositive 103 · Variables corrélées : une explication ambiguë

Faire imaginer deux copies presque identiques d'une variable informative. Si l'une est permutée, le modèle peut utiliser l'autre. Les méthodes d'attribution conditionnelle et marginale ne posent pas la même question. Documenter la méthode choisie et les dépendances plutôt que présenter un classement de variables comme une vérité intrinsèque des données.

À retenir : Une faible importance individuelle ne signifie pas « variable inutile »

Références : [R25](https://scikit-learn.org/stable/modules/permutation_importance.html), [R27](https://papers.nips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html)

## Diapositive 104 · PDP et ICE

Le TP trace les deux premiers facteurs d'un problème Friedman connu. Le PDP peut masquer des interactions car il moyenne des effets différents. Une ICE ne prouve pas l'effet d'une intervention : elle décrit la réponse du modèle lorsque l'on modifie artificiellement une entrée. Discuter la couverture du domaine et la présence de peu d'observations dans certaines zones.

À retenir : Lire l'échelle de sortie et l'espace dans lequel les observations sont plausibles

Références : [R26](https://scikit-learn.org/stable/modules/partial_dependence.html)

## Diapositive 105 · SHAP : répartir une différence de prédiction

Décrire les valeurs de Shapley comme la moyenne pondérée de contributions marginales sur les ordres possibles des variables. L'additivité est une propriété de la représentation, pas une preuve causale. Selon l'explainer et la configuration, les valeurs peuvent s'additionner en score brut ou log-odds plutôt qu'en probabilité. Toujours vérifier l'échelle. L'installation SHAP reste facultative cette semaine.

Références : [R27](https://papers.nips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html), [R28](https://shap.readthedocs.io/en/latest/)

## Diapositive 106 · Un calcul de Shapley à deux variables

Exemple original fondé sur un jeu de coalition arbitraire mais cohérent. La contribution de A vaut 4 lorsqu'elle arrive avant B et 8 lorsqu'elle arrive après B ; la moyenne vaut 6. Pour B : 2 puis 6, moyenne 4. L'interaction de 4 est répartie équitablement. Les nombres ne sont pas une explication d'un modèle bancaire réel.

À retenir : φA = ½ [(14−10) + (20−12)] = 6 ; φB = 4

Références : [R27](https://papers.nips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html)

## Diapositive 107 · Une prédiction ponctuelle laisse une incertitude

Distinguer un intervalle de prédiction pour une nouvelle observation d'un intervalle de confiance sur un paramètre ou une moyenne. Le TP montre une méthode conforme simple. Il ne fournit ni une garantie conditionnelle pour toute personne ni une protection automatique contre tous les changements de distribution.

À retenir : Un intervalle large peut être honnête mais peu utile pour décider

Références : [R29](https://arxiv.org/abs/2107.07511)

## Diapositive 108 · Split-conformal : trois ensembles séparés

Les scores sont ordonnés et le rang est indexé à partir de 1. Si k dépasse ncal, on prend un intervalle infini dans la formulation conservatrice. Pour ncal=200 et alpha=0,1, k=181. La correction fini-échantillon compte. Les hypothèses portent notamment sur l'échangeabilité des scores de calibration et de la nouvelle observation, et sur la séparation des données d'ajustement.

Références : [R29](https://arxiv.org/abs/2107.07511)

## Diapositive 109 · Lire les intervalles conformes

Le graphique montre un extrait trié des prédictions d'un test synthétique. Le TP calcule la couverture sur tout le test et par deux sous-groupes. La garantie conforme ne promet pas 90% pour chaque segment ni après une dérive temporelle. Ne pas régler le niveau ou le modèle en regardant ce même test puis conserver la qualification de test final.

Références : [R29](https://arxiv.org/abs/2107.07511)

## Diapositive 110 · Évaluer des segments

Les segments doivent répondre à des questions d'usage et être définis avec prudence. Les différences observées peuvent venir de composition, de qualité de labels, de prévalence ou d'un comportement du modèle. Aucun indicateur isolé ne certifie l'équité. Le support donne une méthode de diagnostic et de documentation, pas un avis juridique ni une autorisation de décision automatisée.

À retenir : Une moyenne satisfaisante peut masquer un échec local

Références : [R30](https://arxiv.org/abs/1810.03993), [R16](https://scikit-learn.org/stable/modules/calibration.html)

## Diapositive 111 · Préparer un modèle à être utilisé

Montrer le manifeste créé dans le projet et expliquer ce qui manque pour une production : contrat d'API, tests de données, supervision, gestion des accès, validation métier et processus de maintenance. Le projet vérifie seulement la relecture d'un artefact local. Un fichier joblib/pickle non fiable peut exécuter du code ; n'ouvrir que des artefacts de confiance. Les versions compatibles doivent être documentées.

À retenir : Une bonne notebook n'est pas encore un service exploité

Références : [R31](https://scikit-learn.org/stable/model_persistence.html), [R30](https://arxiv.org/abs/1810.03993)

## Diapositive 112 · Trois dérives à distinguer

Distinguer une défaillance de schéma, un changement de distribution des entrées P(X), un changement de prévalence P(y) et une évolution de la relation P(y|X). Certains labels arrivent tard, donc des indicateurs sans labels sont nécessaires mais insuffisants. Définir des seuils d'action avec une période de référence et un responsable. Le réentraînement automatique n'est pas la seule réponse possible.

Références : [R30](https://arxiv.org/abs/1810.03993)

## Diapositive 113 · Une distribution différente n'est qu'un signal

Distributions construites, pas données de production. Demander deux explications possibles : saisonnalité attendue et changement de collecte. Une dérive statistiquement détectable peut être sans impact opérationnel, tandis qu'une baisse de performance peut survenir sans forte variation des marges de X. Les indicateurs doivent être reliés à une investigation et à une décision.

Références : [R30](https://arxiv.org/abs/1810.03993)

## Diapositive 114 · La model card rend les limites visibles

Utiliser evaluation/MODEL_CARD.md. Exiger au minimum les limites réelles du fil rouge : données historiques, disponibilité temporelle à auditer, contacts répétés sans identifiant personne et absence de preuve d'effet causal. Un bon rapport peut recommander de ne pas déployer. L'évaluation porte sur la qualité du raisonnement et la traçabilité, pas sur une promesse de performance.

À retenir : Écrire ce que le modèle ne permet pas de conclure

Références : [R30](https://arxiv.org/abs/1810.03993), [R32](https://archive.ics.uci.edu/dataset/222/bank+marketing)

## Diapositive 115 · TP06 : expliquer et quantifier

Quatre sous-ensembles sont explicités : train, diagnostic, calibration conforme et test. Le jeu diagnostic ne doit pas devenir un substitut du test final. La calibration conforme est distincte de la calibration probabiliste du jour 3. Demander aux étudiants de dire à voix haute de laquelle ils parlent.

À retenir : 90 minutes · notebooks/etudiants/06_interpretation.ipynb

Références : [R25](https://scikit-learn.org/stable/modules/permutation_importance.html), [R26](https://scikit-learn.org/stable/modules/partial_dependence.html), [R29](https://arxiv.org/abs/2107.07511)

## Diapositive 116 · Veille au 19 septembre 2026

La version 1.9.1 est documentée en septembre 2026. Les TP figent les versions dans uv.lock plutôt que dépendre d'un site stable évolutif. Présenter TabArena comme un benchmark vivant : les rangs varient avec les réglages, le budget et les jeux. Aucune supériorité universelle ni mesure de vitesse locale n'est affirmée dans ce cours.

À retenir : La nouveauté ne dispense pas d'une baseline ni d'un test adapté

Références : [R34](https://scikit-learn.org/stable/whats_new/v1.9.html), [R36](https://arxiv.org/abs/2506.16791)

## Diapositive 117 · TabPFN : publication et annonce récente

L'article Nature 2025 étudie notamment des jeux jusqu'à 10 000 observations et 500 variables ; ne pas transposer ces limites au modèle annoncé en 2026. Le rapport 3.5 est une source primaire de l'éditeur, récente de quatre jours lors de la préparation. Ses affirmations ne sont pas reprises comme un résultat reproduit ici. Le cours n'exige ni compte payant, ni GPU, ni transmission des données à une API.

À retenir : Une annonce de l'éditeur et une validation indépendante n'ont pas le même statut

Références : [R35](https://www.nature.com/articles/s41586-024-08328-6), [R37](https://priorlabs.ai/technical-reports/tabpfn-3-5)

## Diapositive 118 · Lire un benchmark de façon critique

Activité de lecture critique : ouvrir R36 et R37, relever une information sur les budgets et une limite du protocole. Vérifier la date, le statut de publication, les jeux et l'accès au code. Un benchmark est une preuve située, pas une vérité sur tous les problèmes tabulaires. Proposer un protocole de comparaison avec le pipeline du cours sans lancer un service externe.

À retenir : Une moyenne ou un rang ne remplace pas une expérience sur notre problème

Références : [R36](https://arxiv.org/abs/2506.16791), [R37](https://priorlabs.ai/technical-reports/tabpfn-3-5)

## Diapositive 119 · Projet final : prioriser une campagne

Consignes détaillées dans evaluation/PROJET.md. Fournir les fichiers étudiants sans les corrections si nécessaire. Un bonus clustering peut décrire les profils mais ne doit pas remplacer la tâche supervisée. Aucun seuil de score absolu n'est imposé. La cible historique ne permet pas de conclure au bénéfice incrémental d'une campagne.

À retenir : 180 minutes · binôme · notebook, manifeste, model card et restitution

Références : [R32](https://archive.ics.uci.edu/dataset/222/bank+marketing), [R30](https://arxiv.org/abs/1810.03993)

## Diapositive 120 · Une évaluation sur des preuves

Barème pédagogique proposé sur 20, à articuler avec les modalités officielles de l'école. Une fuite non corrigée met à zéro le critère protocole ; elle doit aussi être signalée comme invalidant les conclusions de performance. Ne pas sanctionner un résultat moins élevé si le protocole est honnête et la conclusion solide. Les critères détaillés figurent dans evaluation/PROJET.md.

## Diapositive 121 · Soutenance : cinq minutes pour décider

Proposition pour huit binômes au maximum : cinq minutes par binôme puis cinq minutes de synthèse collective. Pour un groupe plus grand, remplacer une partie des échanges par des posters et une évaluation croisée structurée. Le temps total de formation reste inchangé. Prévoir une question individuelle pour s'assurer de la compréhension de chaque membre.

À retenir : Répondre avec un résultat, son protocole et une limite concrète

## Diapositive 122 · Quiz final : raisonner sur un cas nouveau

Utiliser le questionnaire complet et son corrigé séparé dans evaluation/. Le quiz final dure 30 minutes. Les réponses doivent exposer un raisonnement et non recopier un nom d'algorithme. Le projet et le quiz donnent deux vues complémentaires de la maîtrise. Leurs poids éventuels dans une note officielle restent ceux de l'école.

À retenir : Identifier l'hypothèse rompue, proposer une vérification et une correction

## Diapositive 123 · Ressources : apprendre et pratiquer

Parcours de consolidation : choisir une faiblesse du diagnostic, faire une activité du MOOC et reproduire un exemple de documentation en changeant une seule hypothèse. Le livre et les ressources sont en anglais pour une large part ; les explications et exercices du cours restent en français.

À retenir : Liens complets dans les notes et resources/RESSOURCES.md

Références : [R01](https://www.statlearning.com/), [R33](https://inria.github.io/scikit-learn-mooc/), [R02](https://scikit-learn.org/stable/common_pitfalls.html)

## Diapositive 124 · Ressources : articles et veille

Les ressources sont accessibles à la lecture sans abonnement. Un texte gratuit n'est pas nécessairement libre de redistribution ; les liens sont préférés aux copies. Le dépôt conserve auteur, titre, date et rôle pédagogique pour chaque source. Les deux supports de 2020 sont référencés séparément avec leurs pages d'origine.

Références : [R15](https://www.jair.org/index.php/jair/article/view/10302), [R27](https://papers.nips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html), [R29](https://arxiv.org/abs/2107.07511), [R30](https://arxiv.org/abs/1810.03993), [R35](https://www.nature.com/articles/s41586-024-08328-6), [R36](https://arxiv.org/abs/2506.16791), [R37](https://priorlabs.ai/technical-reports/tabpfn-3-5)

## Diapositive 125 · Ce que vous savez maintenant défendre

Revenir aux six objectifs et demander à chaque participant une preuve issue de son travail. Recueillir une question restant ouverte. Donner une action après formation : reproduire le protocole sur un problème autorisé, puis documenter les différences de population, de coût et de disponibilité des données.

À retenir : Le livrable est une décision justifiée, accompagnée de preuves reproductibles

## Diapositive 126 · Merci

Remercier le groupe. Formateur : Chrys Fé-Marty NIONGOLO. Le lien cliquable mène au dépôt GitHub privé des ressources. Les droits d'accès sont nécessaires. Le dossier étudiant peut aussi être diffusé hors ligne par le formateur. Le profil LinkedIn est accessible depuis la diapositive formateur.
