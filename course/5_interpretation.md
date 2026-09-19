# Jour 5 · Interpréter, quantifier et restituer

## Interpréter et restituer
Kind: section
> Vendredi 25 septembre · Défendre une décision avec ses limites
Notes: Les concepts du jour complètent le projet. Commencer par distinguer explication, performance et causalité. Le socle est permutation, PDP/ICE, split-conformal et model card. La veille récente est une lecture critique, sans installation lourde ni promesse de supériorité. Le temps de projet reste protégé.

## Trois niveaux d'explication
- Global : quelles variables le modèle utilise-t-il sur une population ?
- Local : pourquoi produit-il cette prédiction pour cet exemple ?
- Action : quelle intervention changerait réellement le résultat ?
> Une explication prédictive ne répond pas automatiquement à une question causale
Notes: Exemple : une variable liée à une situation sociale peut être très prédictive sans constituer une action pertinente ou acceptable. Les explications dépendent d'un modèle, de données de référence et d'une méthode. Ne pas utiliser l'existence d'un graphique explicatif comme preuve de qualité ou d'absence de biais. Vérifier d'abord que le modèle prédit de façon utile.
Sources: R25, R27

## Importance par permutation
Chart: importance
- Mélanger une variable puis mesurer la dégradation du score.
- Répéter pour observer la variabilité.
- Interpréter sur un jeu de diagnostic réservé.
Notes: Le graphique est réellement calculé sur la régression synthétique Friedman du cours. Les cinq premières variables portent le signal par construction. L'importance dépend de la métrique et du modèle. Une importance négative faible peut refléter du bruit d'estimation ou une variable qui nuit à la prédiction. Si ce diagnostic sert à modifier le modèle, conserver encore un test final indépendant.
Sources: R25

## Variables corrélées : une explication ambiguë
- Deux variables substituables peuvent se partager une information.
- La permutation isolée peut sous-estimer leur rôle conjoint.
- Permuter un groupe cohérent ou comparer une ablation groupée.
> Une faible importance individuelle ne signifie pas « variable inutile »
Notes: Faire imaginer deux copies presque identiques d'une variable informative. Si l'une est permutée, le modèle peut utiliser l'autre. Les méthodes d'attribution conditionnelle et marginale ne posent pas la même question. Documenter la méthode choisie et les dépendances plutôt que présenter un classement de variables comme une vérité intrinsèque des données.
Sources: R25, R27

## PDP et ICE
- PDP : moyenne des prédictions lorsque l'on fait varier une feature.
- ICE : une courbe par observation pour montrer l'hétérogénéité.
- Les combinaisons fabriquées peuvent être irréalistes avec des variables corrélées.
> Lire l'échelle de sortie et l'espace dans lequel les observations sont plausibles
Notes: Le TP trace les deux premiers facteurs d'un problème Friedman connu. Le PDP peut masquer des interactions car il moyenne des effets différents. Une ICE ne prouve pas l'effet d'une intervention : elle décrit la réponse du modèle lorsque l'on modifie artificiellement une entrée. Discuter la couverture du domaine et la présence de peu d'observations dans certaines zones.
Sources: R26

## SHAP : répartir une différence de prédiction
Equation: f(x) = φ₀ + Σj φj
- φ₀ est une valeur de référence définie par l'explication.
- φj répartit une contribution selon une règle de coopération.
- La référence et les dépendances entre variables changent l'interprétation.
Notes: Décrire les valeurs de Shapley comme la moyenne pondérée de contributions marginales sur les ordres possibles des variables. L'additivité est une propriété de la représentation, pas une preuve causale. Selon l'explainer et la configuration, les valeurs peuvent s'additionner en score brut ou log-odds plutôt qu'en probabilité. Toujours vérifier l'échelle. L'installation SHAP reste facultative cette semaine.
Sources: R27, R28

## Un calcul de Shapley à deux variables
Table: shap
> φA = ½ [(14−10) + (20−12)] = 6 ; φB = 4
Notes: Exemple original fondé sur un jeu de coalition arbitraire mais cohérent. La contribution de A vaut 4 lorsqu'elle arrive avant B et 8 lorsqu'elle arrive après B ; la moyenne vaut 6. Pour B : 2 puis 6, moyenne 4. L'interaction de 4 est répartie équitablement. Les nombres ne sont pas une explication d'un modèle bancaire réel.
Sources: R27

## Une prédiction ponctuelle laisse une incertitude
- ŷ donne un centre, sans dire à quel point l'erreur peut être grande.
- Un intervalle vise une fréquence de couverture définie.
- Sa largeur doit être interprétée avec cette couverture.
> Un intervalle large peut être honnête mais peu utile pour décider
Notes: Distinguer un intervalle de prédiction pour une nouvelle observation d'un intervalle de confiance sur un paramètre ou une moyenne. Le TP montre une méthode conforme simple. Il ne fournit ni une garantie conditionnelle pour toute personne ni une protection automatique contre tous les changements de distribution.
Sources: R29

## Split-conformal : trois ensembles séparés
Equation: si = |yi − f(xi)|     q = s(k), k = ⌈(ncal+1)(1−α)⌉
- Entraîner f sans utiliser les données de calibration conforme.
- Calculer les résidus absolus sur calibration et choisir le rang corrigé.
- Produire [f(x)−q, f(x)+q] pour une nouvelle observation.
Notes: Les scores sont ordonnés et le rang est indexé à partir de 1. Si k dépasse ncal, on prend un intervalle infini dans la formulation conservatrice. Pour ncal=200 et alpha=0,1, k=181. La correction fini-échantillon compte. Les hypothèses portent notamment sur l'échangeabilité des scores de calibration et de la nouvelle observation, et sur la séparation des données d'ajustement.
Sources: R29

## Lire les intervalles conformes
Chart: conformal
- Certaines observations peuvent sortir de leur intervalle.
- Une couverture de 90 % est une propriété marginale sous hypothèses.
- Le test fini peut afficher une couverture différente de 90 %.
Notes: Le graphique montre un extrait trié des prédictions d'un test synthétique. Le TP calcule la couverture sur tout le test et par deux sous-groupes. La garantie conforme ne promet pas 90% pour chaque segment ni après une dérive temporelle. Ne pas régler le niveau ou le modèle en regardant ce même test puis conserver la qualification de test final.
Sources: R29

## Évaluer des segments
- Rapporter performance et effectifs pour des groupes pertinents.
- Examiner rappel, calibration et types d'erreurs.
- Signaler les petits échantillons et les populations absentes.
> Une moyenne satisfaisante peut masquer un échec local
Notes: Les segments doivent répondre à des questions d'usage et être définis avec prudence. Les différences observées peuvent venir de composition, de qualité de labels, de prévalence ou d'un comportement du modèle. Aucun indicateur isolé ne certifie l'équité. Le support donne une méthode de diagnostic et de documentation, pas un avis juridique ni une autorisation de décision automatisée.
Sources: R30, R16

## Préparer un modèle à être utilisé
- Sérialiser toute la pipeline avec son schéma d'entrée.
- Enregistrer versions, données, paramètres, seuil et protocole.
- Prévoir surveillance, responsable et procédure de retour arrière.
> Une bonne notebook n'est pas encore un service exploité
Notes: Montrer le manifeste créé dans le projet et expliquer ce qui manque pour une production : contrat d'API, tests de données, supervision, gestion des accès, validation métier et processus de maintenance. Le projet vérifie seulement la relecture d'un artefact local. Un fichier joblib/pickle non fiable peut exécuter du code ; n'ouvrir que des artefacts de confiance. Les versions compatibles doivent être documentées.
Sources: R31, R30

## Trois dérives à distinguer
Table: monitor
Notes: Distinguer une défaillance de schéma, un changement de distribution des entrées P(X), un changement de prévalence P(y) et une évolution de la relation P(y|X). Certains labels arrivent tard, donc des indicateurs sans labels sont nécessaires mais insuffisants. Définir des seuils d'action avec une période de référence et un responsable. Le réentraînement automatique n'est pas la seule réponse possible.
Sources: R30

## Une distribution différente n'est qu'un signal
Chart: drift
- Les nouvelles entrées se déplacent vers les grandes valeurs.
- Cela peut changer la fréquence des décisions.
- Les labels restent nécessaires pour mesurer certaines pertes de qualité.
Notes: Distributions construites, pas données de production. Demander deux explications possibles : saisonnalité attendue et changement de collecte. Une dérive statistiquement détectable peut être sans impact opérationnel, tandis qu'une baisse de performance peut survenir sans forte variation des marges de X. Les indicateurs doivent être reliés à une investigation et à une décision.
Sources: R30

## La model card rend les limites visibles
- Usage prévu, utilisateurs et cas exclus.
- Données, protocole, métriques globales et par segment.
- Hypothèses, limites, responsable et conditions de réévaluation.
> Écrire ce que le modèle ne permet pas de conclure
Notes: Utiliser evaluation/MODEL_CARD.md. Exiger au minimum les limites réelles du fil rouge : données historiques, disponibilité temporelle à auditer, contacts répétés sans identifiant personne et absence de preuve d'effet causal. Un bon rapport peut recommander de ne pas déployer. L'évaluation porte sur la qualité du raisonnement et la traçabilité, pas sur une promesse de performance.
Sources: R30, R32

## TP06 : expliquer et quantifier
- Mesurer une importance par permutation et discuter les corrélations.
- Comparer PDP et ICE sur une relation synthétique connue.
- Construire un intervalle conforme et vérifier sa couverture observée.
> 90 minutes · notebooks/etudiants/06_interpretation.ipynb
Notes: Une variante Colab autonome est disponible dans notebooks/colab/etudiants/06_interpretation.ipynb ; elle utilise le CPU. Quatre sous-ensembles sont explicités : train, diagnostic, calibration conforme et test. Le jeu diagnostic ne doit pas devenir un substitut du test final. La calibration conforme est distincte de la calibration probabiliste du jour 3. Demander aux étudiants de dire à voix haute de laquelle ils parlent.
Sources: R25, R26, R29

## Veille au 19 septembre 2026
- scikit-learn 1.9.1 : environnement utilisé pour les TP.
- TabArena : comparer les méthodes avec leurs budgets et protocoles.
- Modèles tabulaires de fondation : un axe de recherche à évaluer.
> La nouveauté ne dispense pas d'une baseline ni d'un test adapté
Notes: La version 1.9.1 est documentée en septembre 2026. Les TP figent les versions dans uv.lock plutôt que dépendre d'un site stable évolutif. Présenter TabArena comme un benchmark vivant : les rangs varient avec les réglages, le budget et les jeux. Aucune supériorité universelle ni mesure de vitesse locale n'est affirmée dans ce cours. Dans les 15 minutes de veille, réserver 10 minutes aux publications/benchmarks et 5 minutes à une ouverture uniquement orale sur Ray. Suivre docs/NOTES_ORALES_RAY.md : du TP Optuna à la coordination d'essais avec Tune, rôle de Core, Data et Train, checkpoints et coût de distribution. Ray remonte à 2018 ; le situer dans les pratiques actuelles sans le présenter comme une invention de 2026. Aucun TP, installation Ray ou évaluation supplémentaire.
Sources: R34, R36, R44, R45, R47, R48, R49

## TabPFN : publication et annonce récente
- 2025 : article Nature sur TabPFN v2 et les petits jeux tabulaires.
- 15 septembre 2026 : rapport technique TabPFN-3.5 publié par Prior Labs.
- Comparer qualité, coût, conditions d'accès et proximité avec nos données.
> Une annonce de l'éditeur et une validation indépendante n'ont pas le même statut
Notes: L'article Nature 2025 étudie notamment des jeux jusqu'à 10 000 observations et 500 variables ; ne pas transposer ces limites au modèle annoncé en 2026. Le rapport 3.5 est une source primaire de l'éditeur, récente de quatre jours lors de la préparation. Ses affirmations ne sont pas reprises comme un résultat reproduit ici. Le cours n'exige ni compte payant, ni GPU, ni transmission des données à une API.
Sources: R35, R37

## Lire un benchmark de façon critique
- Quels jeux, tailles, types de variables et risques de contamination ?
- Quels budgets, hardware, tuning et ensembles par méthode ?
- Quelles distributions de résultats et quels cas d'échec ?
> Une moyenne ou un rang ne remplace pas une expérience sur notre problème
Notes: Activité de lecture critique : ouvrir R36 et R37, relever une information sur les budgets et une limite du protocole. Vérifier la date, le statut de publication, les jeux et l'accès au code. Un benchmark est une preuve située, pas une vérité sur tous les problèmes tabulaires. Proposer un protocole de comparaison avec le pipeline du cours sans lancer un service externe.
Sources: R36, R37

## Projet final : prioriser une campagne
- Reprendre les données UCI, la décision et les contraintes de disponibilité.
- Comparer une baseline et deux familles avec un budget explicite.
- Figer modèle et seuil, évaluer le test puis défendre la recommandation.
> 180 minutes · binôme · notebook, manifeste, model card et restitution
Notes: Consignes détaillées dans evaluation/PROJET.md. Fournir les fichiers étudiants sans les corrections si nécessaire. Un bonus clustering peut décrire les profils mais ne doit pas remplacer la tâche supervisée. Aucun seuil de score absolu n'est imposé. La cible historique ne permet pas de conclure au bénéfice incrémental d'une campagne.
Sources: R32, R30

## Une évaluation sur des preuves
Table: rubric
Notes: Barème pédagogique proposé sur 20, à articuler avec les modalités officielles de l'école. Une fuite non corrigée met à zéro le critère protocole ; elle doit aussi être signalée comme invalidant les conclusions de performance. Ne pas sanctionner un résultat moins élevé si le protocole est honnête et la conclusion solide. Les critères détaillés figurent dans evaluation/PROJET.md.

## Soutenance : cinq minutes pour décider
- Quelle décision et quelle population avez-vous définies ?
- Quelle preuve justifie votre choix de modèle et de seuil ?
- Quelle limite vous empêche encore de recommander un usage réel ?
> Répondre avec un résultat, son protocole et une limite concrète
Notes: Proposition pour huit binômes au maximum : cinq minutes par binôme puis cinq minutes de synthèse collective. Pour un groupe plus grand, remplacer une partie des échanges par des posters et une évaluation croisée structurée. Le temps total de formation reste inchangé. Prévoir une question individuelle pour s'assurer de la compréhension de chaque membre.

## Quiz final : raisonner sur un cas nouveau
- Un score augmente après ajout d'une variable connue après l'événement.
- Une méthode de clustering exclut la majorité des points comme bruit.
- Un intervalle conforme perd sa couverture après un changement de population.
> Identifier l'hypothèse rompue, proposer une vérification et une correction
Notes: Utiliser le questionnaire complet et son corrigé séparé dans evaluation/. Le quiz final dure 30 minutes. Les réponses doivent exposer un raisonnement et non recopier un nom d'algorithme. Le projet et le quiz donnent deux vues complémentaires de la maîtrise. Leurs poids éventuels dans une note officielle restent ceux de l'école.

## Ressources : apprendre et pratiquer
- R01 : livre gratuit ISLP, chapitres sur validation, ensembles et non supervisé.
- R33 : MOOC Inria avec exercices, notebooks et vidéos.
- R02–R26 : documentation officielle, exemples et fonctions utilisées.
> Liens complets dans les notes et resources/RESSOURCES.md
Notes: Parcours de consolidation : choisir une faiblesse du diagnostic, faire une activité du MOOC et reproduire un exemple de documentation en changeant une seule hypothèse. Le livre et les ressources sont en anglais pour une large part ; les explications et exercices du cours restent en français.
Sources: R01, R33, R02

## Ressources : articles et veille
- R15 : SMOTE ; R27 : SHAP ; R29 : prédiction conforme.
- R30 : model cards et documentation des limites.
- R35–R37 : modèles tabulaires et lecture critique des benchmarks récents.
Notes: Les ressources sont accessibles à la lecture sans abonnement. Un texte gratuit n'est pas nécessairement libre de redistribution ; les liens sont préférés aux copies. Le dépôt conserve auteur, titre, date et rôle pédagogique pour chaque source. Les deux supports de 2020 sont référencés séparément avec leurs pages d'origine.
Sources: R15, R27, R29, R30, R35, R36, R37

## Ce que vous savez maintenant défendre
Kind: summary
- Un protocole, des features et une métrique cohérents avec la décision.
- Un modèle comparé, régularisé et optimisé sans utiliser le test pour choisir.
- Une recommandation avec incertitude, explications et conditions de réévaluation.
> Le livrable est une décision justifiée, accompagnée de preuves reproductibles
Notes: Revenir aux six objectifs et demander à chaque participant une preuve issue de son travail. Recueillir une question restant ouverte. Donner une action après formation : reproduire le protocole sur un problème autorisé, puis documenter les différences de population, de coût et de disponibilité des données.

## Merci
Kind: closing
Notes: Remercier le groupe. Formateur : Chrys Fé-Marty NIONGOLO. Le lien cliquable mène au dépôt GitHub privé des ressources. Les droits d'accès sont nécessaires. Le dossier étudiant peut aussi être diffusé hors ligne par le formateur. Le profil LinkedIn est accessible depuis la diapositive formateur.
