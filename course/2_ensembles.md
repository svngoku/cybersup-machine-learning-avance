# Jour 2 · Ensembles et optimisation

## Ensembles et optimisation
Kind: section
> Mardi 22 septembre · Comparer performance, stabilité et coût
Notes: Reprendre deux questions du jour 1 puis annoncer le fil : comprendre un arbre, diversifier les erreurs, corriger les résidus et choisir un budget de recherche. TP02 compare des familles sur une régression synthétique. TP03 évalue la procédure d'optimisation avec une boucle externe.

## Un arbre partitionne l'espace
- Une question sur une variable divise les observations en deux groupes.
- Chaque feuille produit une valeur ou une distribution de classes.
- Le choix local d'une division ne garantit pas le meilleur arbre global.
> Une règle lisible peut appartenir à un arbre globalement instable
Notes: Dessiner au tableau un exemple original : âge supérieur à 40 puis nombre de contacts antérieurs. Les seuils numériques ne constituent pas une recommandation bancaire. Un arbre apprend de manière gloutonne : il choisit la meilleure division disponible selon son critère, puis poursuit récursivement. Demander ce qu'il se passe lorsqu'une seule observation change près d'un seuil.
Sources: R40, R39

## Calculer un gain de Gini
Table: gini
Notes: Faire calculer Gini = 1 − Σk pk². Dans le parent, p=0,4, donc Gini=1−0,16−0,36=0,48. Le gain est la différence entre l'impureté du parent et la moyenne pondérée des enfants. La division ici est informative mais n'isole pas parfaitement les classes. Gini mesure une impureté de classes, pas une précision hors échantillon.
Sources: R40

## Contrôler la complexité d'un arbre
- max_depth limite la profondeur des interactions.
- min_samples_leaf évite des feuilles soutenues par trop peu d'observations.
- ccp_alpha pénalise la complexité lors de l'élagage.
> Les seuils se valident ; aucune taille minimale universelle de feuille
Notes: Mettre en perspective le support de 2020 qui mentionne un ordre de grandeur de 30 observations. Ce n'est pas une contrainte mathématique universelle. Un minimum utile dépend du bruit, de la prévalence et du volume. Pour le pruning, expliquer la pénalité sur le nombre de feuilles et la séquence de sous-arbres. Choisir la pénalité uniquement dans les données de développement.
Sources: R40, R39

## Bagging : moyenner des modèles instables
- Tirer plusieurs échantillons avec remise à partir du train.
- Ajuster un estimateur sur chaque échantillon bootstrap.
- Agréger les prédictions pour réduire une partie de la variance.
> Le bénéfice dépend autant de la diversité que du nombre d'estimateurs
Notes: Un échantillon bootstrap de taille n contient des répétitions et n'inclut pas toutes les observations d'origine. La probabilité limite qu'une observation soit absente vaut environ e^-1, soit 36,8%. Cette propriété explique les observations out-of-bag. La moyenne réduit surtout la variance si les erreurs ne sont pas parfaitement corrélées. La classification utilise des votes ou une moyenne de probabilités selon la méthode.
Sources: R07, R08

## Pourquoi la corrélation limite le gain
Chart: bagging
- Erreurs identiques : ajouter des arbres apporte peu.
- Erreurs diversifiées : la moyenne devient plus stable.
- Une variance résiduelle reste lorsque ρ est positif.
Notes: Sous une variance identique σ² et une corrélation commune ρ, Var(moyenne)=σ²[ρ+(1−ρ)/M]. Dériver au tableau la somme des M variances et des M(M−1) covariances divisée par M². Pour M infini, la limite vaut ρσ². Ce modèle simplifié illustre un mécanisme, il ne décrit pas exactement toute forêt entraînée.
Sources: R08

## Random Forest : diversifier les divisions
- Le bootstrap diversifie les lignes vues par chaque arbre.
- max_features diversifie les variables candidates à chaque division.
- n_estimators stabilise l'ensemble, au prix du calcul et du stockage.
> Comparer la force des arbres et la corrélation de leurs erreurs
Notes: Baisser max_features peut réduire la corrélation mais dégrader chaque arbre. Une forêt profonde n'est pas équivalente à un boosting peu profond. Les importances fondées sur la diminution d'impureté peuvent favoriser certaines variables, notamment à forte cardinalité. Réserver la discussion de l'interprétation à la permutation sur validation du jour 5.
Sources: R07

## Out-of-bag : utile avec ses limites
- Pour une observation, agréger les arbres qui ne l'ont pas utilisée.
- Obtenir une estimation interne sans découpage de validation supplémentaire.
- Vérifier que groupes, temps et prétraitements ne rendent pas l'estimation trompeuse.
> OOB ne remplace pas un test cohérent avec l'usage futur
Notes: L'absence d'une ligne dans un bootstrap ne garantit pas l'absence d'autres lignes du même client. Un prétraitement appris hors de la forêt sur toutes les données peut également limiter l'interprétation. Ne pas régler indéfiniment sur l'OOB puis présenter ce score comme une mesure finale indépendante. Pour ce cours, la CV reste le protocole commun de comparaison.
Sources: R07, R03

## Boosting : corriger progressivement le modèle
Equation: Fm(x) = Fm−1(x) + η hm(x)
- Fm−1 représente la prédiction courante.
- hm apprend une direction de correction.
- η règle l'amplitude de chaque nouvelle correction.
Notes: Pour la perte quadratique, la direction à apprendre correspond aux résidus. Pour d'autres pertes, il s'agit du gradient négatif de la perte par rapport à la prédiction. Le boosting est séquentiel : l'étape suivante dépend des précédentes. Ne pas le décrire comme une simple moyenne d'arbres indépendants. Le nombre d'étapes et le learning rate doivent être réglés ensemble.
Sources: R11

## Une itération de boosting à la main
Table: booststep
> La souche prédit −1,5 pour les deux premiers points et +3 pour le troisième
Notes: Exemple original avec une variable ordonnée x=(1,2,3) et y=(2,3,7). F0 est la moyenne 4. Un arbre à une division, entre x=2 et x=3, ajuste les résidus : −1,5 et +3. Avec η=0,5, F1=(3,25,3,25,5,5). Faire calculer la nouvelle erreur quadratique et comparer à F0. La même logique de résidu ne s'applique telle quelle qu'à certaines pertes.
Sources: R11

## Le gradient généralise le résidu
Equation: rim = − ∂ℓ(yi, F(xi)) / ∂F(xi) à l'étape m−1
- Ajuster un modèle faible sur cette direction de descente.
- Pour la log-loss, corriger une prédiction sur son échelle appropriée.
- Répéter en contrôlant la capacité et la taille des mises à jour.
Notes: Relier cette étape à la descente de gradient connue des étudiants, mais dans un espace de fonctions. Pour une régression avec demi-perte quadratique, le gradient négatif est y−F(x). Avec une perte logistique et un score brut, le gradient est lié à y−p. Éviter de confondre le score brut, la probabilité après fonction logistique et la classe après seuillage.
Sources: R11

## Quand arrêter le boosting ?
Chart: boosting
- Mesurer la RMSE sur une validation indépendante.
- Réduire la complexité ou arrêter si la validation cesse de progresser.
- Conserver un test indépendant de cette décision.
Notes: Courbes réellement calculées sur un problème Friedman synthétique. Un minimum peu marqué invite à considérer la variabilité, pas à choisir une itération à la décimale près. Early stopping constitue une sélection d'hyperparamètre : les données utilisées pour arrêter sont des données de validation. Un jeu temporel demande une validation d'arrêt qui respecte lui aussi le temps.
Sources: R07, R09

## Boosting par histogrammes
- Regrouper les valeurs continues dans un nombre fini de bins.
- Évaluer les divisions sur ces bins pour réduire le coût.
- Régler feuilles, taux d'apprentissage, itérations et régularisation.
> Un gain de calcul permet davantage d'expériences, pas un protocole moins strict
Notes: Expliquer le compromis résolution/coût sans promettre une accélération universelle. HistGradientBoosting est disponible dans scikit-learn et suffit au socle des TP. Son comportement sur valeurs manquantes et catégories dépend des entrées et de la version. Notre pipeline générique prépare explicitement les colonnes pour rendre la comparaison transparente, même lorsqu'un autre pipeline natif serait possible.
Sources: R07, R12

## Quatre implémentations à connaître
Table: libraries
Notes: Présenter ce tableau comme des choix d'implémentation, pas un classement de performance. Les paramètres qui portent le même nom ne sont pas toujours strictement comparables. XGBoost expose des mécanismes de régularisation et une optimisation du second ordre. LightGBM est notamment connu pour sa croissance par feuille. CatBoost propose un traitement spécialisé des catégories et de l'ordered boosting. Les trois bibliothèques sont des extensions, pas des dépendances indispensables cette semaine.
Sources: R11, R12, R13

## Voting et stacking
- Voting : combiner plusieurs prédictions selon une règle fixée.
- Stacking : apprendre un méta-modèle sur les prédictions de modèles de base.
- Pour le stacking, fabriquer ces prédictions sans avoir entraîné sur leur cible.
> Prédictions hors pli pour le méta-modèle, test final pour l'ensemble
Notes: Expliquer pourquoi un méta-modèle recevant des prédictions d'entraînement trop parfaites apprend un signal trompeur. StackingRegressor produit des prédictions hors pli pour cette phase. Si l'on évalue le stacking dans une boucle externe, ses propres ajustements doivent rester dans le train externe. Discuter la complexité opérationnelle d'un ensemble de nombreuses familles.
Sources: R07

## TP02 : comparer les ensembles
- Comparer Ridge, arbre, forêt et boosting sur les mêmes plis.
- Tracer l'erreur du boosting au fil des itérations.
- Justifier un compromis entre RMSE, coût et complexité.
> 90 minutes · notebooks/etudiants/02_ensembles.ipynb
Notes: La source synthétique permet de connaître les variables informatives sans télécharger un nouveau jeu. Demander de conserver tous les résultats, y compris les essais moins bons. Le temps d'ajustement dépend du matériel. Une extension stacking est proposée si les objectifs centraux sont atteints. Le débrief compare les mécanismes, pas seulement le classement des chiffres.
Sources: R07

## Définir un espace d'hyperparamètres
- Séparer les paramètres appris des réglages choisis avant fit.
- Utiliser une échelle logarithmique pour C, λ ou le learning rate.
- Limiter les plages grâce aux contraintes de temps et de mémoire.
> Écrire le budget d'essais avant de lancer la recherche
Notes: Exercice court : proposer un espace pour un boosting avec 4 valeurs de learning rate, 5 capacités d'arbre et 6 nombres d'itérations. La grille contient déjà 120 configurations, donc 360 ajustements pour une CV à trois plis, avant refit. Certains paramètres interagissent fortement. Conserver la même règle d'arrêt et le même budget pour comparer les méthodes de recherche.
Sources: R09

## Grille, recherche aléatoire et TPE
- La grille couvre une liste cartésienne de choix.
- La recherche aléatoire explore une distribution de configurations.
- TPE adapte les essais à l'historique de la recherche.
> Le meilleur score interne est un résultat de sélection
Notes: TPE est une méthode d'optimisation séquentielle fondée sur un modèle des bonnes et moins bonnes régions. Elle n'est pas magique et a besoin d'un budget approprié. Sur huit essais, la phase initiale aléatoire compte beaucoup ; le TP fixe quatre essais initiaux. Le pruning évite de terminer certaines expériences peu prometteuses si des mesures intermédiaires comparables sont disponibles.
Sources: R09, R10

## Validation croisée imbriquée
- Boucle interne : choisir les hyperparamètres sur le train externe.
- Boucle externe : évaluer le choix sur un pli qu'il n'a pas vu.
- Répéter pour estimer la performance de la procédure de sélection.
> La boucle externe évalue une méthode de travail, pas un unique modèle final
Notes: Faire dessiner trois plis externes et trois plis internes dans un train externe. Pour chaque pli externe, la recherche repart de zéro. Si l'on sélectionne ensuite une nouvelle méthode en regardant tous les scores externes, ces scores participent à un nouveau niveau de sélection. Un test final séparé reste utile pour une décision finale importante.
Sources: R03, R09

## L'optimisation a un coût mesurable
Equation: 3 × (8 × 3 + 1) = 75 ajustements
- Trois plis externes, huit essais, trois plis internes.
- Un réajustement du gagnant dans chaque train externe.
- Fixer le parallélisme pour ne pas saturer les machines.
Notes: Faire calculer le coût avant exécution. Ce total correspond au TP03 pour une recherche RandomizedSearchCV avec refit. Distinguer nombre d'ajustements et temps : deux familles peuvent avoir des coûts très différents. Les threads BLAS et n_jobs peuvent se multiplier ; on limite ici le parallélisme. Archiver le budget avec les scores.
Sources: R09

## Interpréter une petite différence
- Comparer les modèles sur les mêmes splits.
- Examiner la dispersion, les segments et le coût d'usage.
- Une différence de 0,003 AP n'est pas automatiquement utile ni robuste.
> Les scores de plis corrélés ne sont pas des répétitions indépendantes
Notes: Ne pas calculer un intervalle de confiance naïf en traitant des plis recouvrants comme des échantillons indépendants. Les variations d'entraînement, de population et d'étiquetage doivent être distinguées. Un bootstrap du test suppose lui aussi une unité de rééchantillonnage adaptée, par exemple le client, et ne mesure pas toutes les sources d'incertitude du réentraînement.
Sources: R03

## TP03 : optimiser avec un budget fixé
- Huit essais aléatoires et huit essais TPE par pli externe.
- Même modèle, mêmes bornes et même métrique.
- Restituer les scores externes et les limites de la comparaison.
> 90 minutes · notebooks/etudiants/03_optimisation.ipynb
Notes: Le TP utilise une logistique et des données synthétiques pour que le coût reste léger et que le protocole soit visible. L'objectif n'est pas de gagner un concours d'AP. Demander aux étudiants d'annoter quelles observations sont visibles à chaque étape. Les résultats aléatoires doivent être enregistrés, pas relancés jusqu'à obtenir une préférence attendue.
Sources: R09, R10

## Quiz J2 : mécanismes et protocole
- Pourquoi 1 000 arbres identiques n'améliorent-ils pas une moyenne ?
- Quel objet est appris à chaque étape du gradient boosting ?
- Pourquoi le score du meilleur essai surestime-t-il sa performance future ?
> Donner une justification avant de citer une bibliothèque
Notes: Réponses : leurs erreurs sont corrélées, donc la variance ne s'annule pas ; un estimateur de la direction de correction, souvent le gradient négatif ; le maximum a été sélectionné parmi plusieurs scores bruités. Ajouter que la boucle externe réduit le biais de sélection lorsqu'elle encapsule bien toute la procédure.
Sources: R08, R11, R09

## Les acquis du jour 2
Kind: summary
- Diversifier pour stabiliser et corriger progressivement pour réduire l'erreur.
- Régulariser les ensembles et surveiller le coût.
- Évaluer la recherche elle-même avec une validation indépendante.
> Demain : transformer une probabilité en décision dans un problème déséquilibré
Notes: Faire formuler un cas où la forêt constitue un choix raisonnable et un autre où un boosting est à expérimenter. Refuser une réponse universelle. Vérifier que les binômes ont conservé les graines, les budgets et les scores de tous les plis.
