# Jour 4 · Structure des données et apprentissage non supervisé

## Clustering et anomalies
Kind: section
> Jeudi 24 septembre · Explorer une structure sans inventer une vérité
Notes: L'objectif est de relier une partition à une représentation, une distance et une hypothèse. Insister sur le fait que l'absence de cible n'élimine pas le besoin d'évaluation. TP05 compare les mêmes points avec plusieurs méthodes, puis discute la stabilité et l'utilité. Les anomalies sont une extension vers la détection et le triage.

## Un cluster dépend de la représentation
- Choisir les variables définit ce qui peut rendre deux observations proches.
- Choisir une distance définit la notion de ressemblance.
- Choisir un algorithme ajoute des hypothèses sur la forme des groupes.
> Un identifiant de cluster est un résultat d'algorithme, pas une classe naturelle
Notes: Faire décrire deux segmentations plausibles d'une population de clients : comportement d'achat ou contraintes de contact. Des variables et unités différentes conduisent à des partitions différentes. Les numéros de clusters sont arbitraires : le groupe 0 n'est pas intrinsèquement inférieur au groupe 1. Les étiquettes métier viennent après l'examen des profils.
Sources: R20

## Distances et échelles
- Euclidienne : compare les écarts numériques coordonnée par coordonnée.
- Cosinus : compare l'orientation de vecteurs, utile dans certains espaces textuels.
- Des variables de grande amplitude peuvent dominer une distance brute.
> Standardiser selon le sens métier, pas par automatisme
Notes: Exemple : revenu en euros et âge en années. Passer le revenu en centimes multiplie sa contribution à la distance euclidienne au carré. Standardiser peut équilibrer les contributions mais aussi donner du poids au bruit. Les données mixtes ne se traitent pas sans réflexion par une simple distance euclidienne sur un encodage one-hot. Demander quelles ressemblances le problème cherche réellement à représenter.
Sources: R18, R20

## PCA : projeter en conservant de la variance
Equation: Xcentré = U Σ Vᵀ     Zk = Xcentré Vk
- Les axes principaux sont orthogonaux.
- Les premières composantes maximisent la variance projetée.
- Réduire la dimension perd de l'information.
Notes: La SVD donne une formulation stable : les colonnes de V sont des directions de l'espace des features. La PCA centre les données, mais le scaling préalable dépend des unités et de l'objectif. La cible n'intervient pas : une direction de faible variance peut être très prédictive. Dans un pipeline supervisé, ajuster la PCA uniquement sur le train de chaque pli.
Sources: R22

## Lire la variance expliquée
Chart: pca
- Deux axes expliquent ici 75 %.
- Trois axes expliquent 88 %.
- Quatre axes sont nécessaires pour dépasser 90 %.
Notes: Spectre construit pour un calcul au tableau, pas extrait d'un benchmark. Faire additionner les pourcentages et expliquer ce que l'on conserve. Un seuil de 90% est une convention de compression, pas une garantie de classification ni de clustering. Vérifier la stabilité et le sens des composantes, et comparer le résultat avec l'espace initial lorsque c'est raisonnable.
Sources: R22

## K-means : minimiser l'inertie
Equation: J = Σk Σi∈Ck ||xi − μk||²
- Affecter chaque point au centre le plus proche.
- Recalculer chaque centre comme la moyenne de son groupe.
- Répéter jusqu'à convergence vers une solution locale.
Notes: Décomposer la fonction objectif et expliquer pourquoi la moyenne minimise une somme de distances euclidiennes au carré. Une initialisation différente peut mener à une autre solution locale. k-means++ choisit des centres initiaux espacés, sans garantir le minimum global. Fixer explicitement n_init dans les exemples pour contrôler le nombre de redémarrages.
Sources: R20

## Une itération de K-means
Table: kmeansstep
> Points 1, 2, 8, 9 : les deux moyennes sont 1,5 et 8,5
Notes: Les centres initiaux sont 0 et 10. L'affectation place 1 et 2 dans A, 8 et 9 dans B. L'inertie initiale est 1²+2²+2²+1²=10. Après mise à jour, quatre écarts de 0,5 donnent 1. Le prochain tour conserve les affectations. Faire varier les centres initiaux pour discuter les minima locaux et les groupes vides.
Sources: R20

## Une géométrie que K-means représente mal
Chart: kmeans
- Les deux lunes sont des groupes courbes.
- K-means favorise des régions proches de centres.
- Une partition peut être stable et mal correspondre à la structure voulue.
Notes: Les points sont des données synthétiques originales produites avec make_moons et la graine 42. Les couleurs montrent les groupes prédits, pas les classes de génération. Demander aux étudiants de proposer une notion de voisinage plutôt qu'une notion de centre. La comparaison suivante utilisera exactement les mêmes points et échelles.
Sources: R20

## L'inertie ne choisit pas K à votre place
Chart: inertia
- Ajouter des centres peut toujours réduire l'inertie optimale.
- Le coude n'est pas toujours visible ni unique.
- Croiser le diagnostic avec stabilité et utilité métier.
Notes: La courbe est mesurée sur les mêmes lunes synthétiques. Un coude peut refléter une approximation géométrique plutôt que des classes naturelles. Ne pas choisir K à partir d'un seul critère puis annoncer une découverte. Demander comment le nombre de groupes s'articule avec le nombre d'actions réellement possibles dans une équipe.
Sources: R20

## Silhouette : séparation et compacité
Equation: s(i) = [ b(i) − a(i) ] / max(a(i), b(i))
- a(i) : distance moyenne aux membres de son groupe.
- b(i) : plus petite distance moyenne vers un autre groupe.
- Une silhouette négative signale une affectation localement discutable.
Notes: La silhouette est définie lorsqu'il existe au moins deux groupes et pas un groupe par observation. Elle favorise certaines géométries compactes selon la distance choisie. Pour une méthode avec bruit, calculer la silhouette hors bruit et publier aussi la proportion exclue. Une bonne silhouette après exclusion de presque tous les points peut être peu utile.
Sources: R20

## GMM : une appartenance probabiliste
Equation: p(x) = Σk πk N(x ; μk, Σk)
- Une composante porte un poids, une moyenne et une covariance.
- Les covariances autorisent des formes elliptiques.
- Une observation peut avoir des responsabilités réparties entre composantes.
Notes: Contrairement à une affectation dure, la responsabilité représente une probabilité de composante conditionnelle au modèle. Elle n'est pas une probabilité de catégorie métier correcte. Comparer covariance sphérique, diagonale et complète : la flexibilité augmente le nombre de paramètres et le risque d'estimation fragile. Une régularisation des covariances évite certaines singularités numériques.
Sources: R21

## EM : alterner deux problèmes plus simples
- Étape E : estimer les responsabilités avec les paramètres courants.
- Étape M : réestimer poids, moyennes et covariances avec ces responsabilités.
- Répéter, puis comparer initialisations et complexités.
> EM peut converger vers un optimum local
Notes: Ne pas dire que l'étape E prédit des labels vrais. Elle calcule des poids latents dans le modèle courant. BIC/AIC comparent ajustement et complexité dans leur cadre d'hypothèses. Les scores ne prouvent pas qu'un mélange gaussien est une bonne description métier. Tester plusieurs initialisations et inspecter les composantes minuscules ou dégénérées.
Sources: R21

## Classification hiérarchique agglomérative
- Partir de petits groupes puis fusionner progressivement.
- Le linkage définit le coût ou la distance entre groupes.
- La coupe du dendrogramme fixe la granularité retenue.
> Ward s'appuie sur la variance et une géométrie euclidienne
Notes: Comparer single linkage, qui peut produire un effet de chaîne, et complete linkage, sensible au diamètre maximal. La hauteur de fusion dépend du linkage et n'a pas un sens universel. Un dendrogramme sur des milliers de points devient illisible. Les structures de distances et la mémoire limitent souvent l'usage direct sur un très grand volume.
Sources: R20

## DBSCAN : relier les régions denses
- eps définit le rayon du voisinage.
- min_samples définit le soutien local requis pour un point cœur.
- Les points non rattachés à une région dense peuvent être marqués bruit.
> Densité et distance dépendent de l'échelle des variables
Notes: Distinguer points cœur, frontière et bruit. Le min_samples de scikit-learn compte le point lui-même. Un point frontière peut avoir une affectation dépendant de l'ordre dans certains cas. DBSCAN n'impose pas K, mais cela ne signifie pas qu'il n'a pas de paramètres à choisir. Un eps unique peut mal représenter des densités très différentes.
Sources: R20

## Les mêmes lunes avec DBSCAN
Chart: dbscan
- La connexité locale suit ici les formes courbes.
- Les points isolés peuvent rester sans groupe.
- Changer eps peut fusionner ou fragmenter la partition.
Notes: Les points et leur standardisation sont exactement ceux du graphique K-means. Seul l'algorithme change. Cette réussite synthétique ne prouve pas une supériorité générale de DBSCAN. Discuter sa sensibilité au bruit, aux densités variables et à la dimension. Faire anticiper le résultat pour un eps très grand, puis très petit.
Sources: R20

## HDBSCAN : examiner plusieurs échelles
- Construire une hiérarchie fondée sur la densité.
- Extraire des groupes selon leur persistance dans cette hiérarchie.
- Régler min_cluster_size et examiner le taux de bruit.
> Vérifier la convention de min_samples selon l'implémentation
Notes: Le TP utilise sklearn.cluster.HDBSCAN. Le package externe hdbscan n'a pas exactement la même convention pour min_samples : éviter de copier des valeurs sans lire la documentation. Le résultat reste sensible à la représentation et aux hypothèses de densité. Un groupe persistant ne reçoit pas automatiquement un sens métier ni une justification causale.
Sources: R23

## Comparer les familles de clustering
Table: clusters
Notes: Demander aux binômes de choisir deux méthodes pour une population compacte, puis deux méthodes pour des groupes non convexes. Ils doivent justifier ce qu'ils considèrent comme une distance légitime. Certains estimateurs n'ont pas de méthode predict pour de nouveaux points : anticiper comment la segmentation sera utilisée après l'analyse.
Sources: R20, R21, R23

## Évaluer sans labels
- Tester la sensibilité aux graines, aux sous-échantillons et aux paramètres.
- Décrire tailles, profils, bruit et cas atypiques de chaque groupe.
- Faire valider une utilité concrète avec les personnes concernées.
> Stabilité, séparation et utilité répondent à des questions différentes
Notes: L'ARI compare deux partitions en tenant compte de l'accord attendu au hasard, avec des correspondances de numéros de groupes inutiles. Pour des partitions issues de sous-échantillons différents, comparer les observations communes ou utiliser une procédure d'affectation cohérente. Un score interne élevé n'est pas une garantie de pertinence. Ne pas utiliser les labels synthétiques pour régler puis pour annoncer une évaluation indépendante.
Sources: R20

## Projections : explorer avec prudence
- PCA représente principalement de la variance linéaire.
- t-SNE privilégie certaines relations de voisinage local.
- Les paramètres peuvent modifier l'apparence des « îlots ».
> Un joli nuage 2D ne démontre pas le nombre de clusters
Notes: Montrer que la projection peut rapprocher ou éloigner des observations autrement qu'une lecture naïve ne le suggère. Ne pas interpréter automatiquement la taille d'un îlot ou les distances entre tous les groupes. UMAP peut être mentionné comme prolongement, sans en faire un socle obligatoire. Toujours revenir aux variables, aux voisins et à une validation dans l'espace pertinent.
Sources: R22, R42

## Anomalie, nouveauté et classe rare
- Une anomalie est atypique selon une représentation et un modèle de référence.
- Une classe rare peut être parfaitement normale.
- La détection de nouveauté suppose un apprentissage représentatif du fonctionnement normal.
> Un score d'anomalie doit être relié à une procédure de vérification
Notes: Présenter Isolation Forest, qui isole les points par des divisions aléatoires, et LOF, qui compare une densité locale à celle des voisins. Pour LOF, le mode novelty change l'usage sur de nouvelles données. Une forte anomalie n'est pas une preuve de fraude ni d'incident. Prévoir le volume de triage, les faux positifs et le délai de retour de labels.
Sources: R24

## TP05 : expliquer une partition
- Comparer quatre méthodes sur les mêmes données et les mêmes échelles.
- Rapporter silhouette, bruit, stabilité et ARI sur les données synthétiques.
- Présenter un exemple de partition trompeuse et sa cause.
> 150 minutes · notebooks/etudiants/05_clustering.ipynb
Notes: Le temps comprend les trois exercices centraux et une analyse rédigée des profils. L'extension Ward est facultative si le groupe doit revenir sur PCA. Donner la priorité aux comparaisons contrôlées et à l'argumentation. Exiger qu'aucune conclusion métier soit tirée de simples numéros de clusters.
Sources: R20, R21

## Quiz J4 : reconnaître les hypothèses
- Une baisse d'inertie prouve-t-elle que le nouveau K est meilleur ?
- Une bonne silhouette suffit-elle si 70 % des points sont classés bruit ?
- Une composante PCA est-elle forcément prédictive de la cible ?
Notes: Réponses : non, l'inertie décroît avec la flexibilité ; non, il faut examiner les points exclus et l'objectif ; non, PCA ne voit pas la cible. Demander à chacun un exemple qui contredit une intuition trop simple. Reprendre les schémas du jour pour rattacher chaque réponse à une hypothèse.
Sources: R20, R22

## Les acquis du jour 4
Kind: summary
- Une représentation et une distance explicites.
- Des méthodes comparées selon leurs hypothèses géométriques.
- Une partition évaluée par plusieurs diagnostics et un usage concret.
> Demain : expliquer, documenter et défendre le modèle final
Notes: Faire rédiger une fiche de segmentation : variables, transformations, distance, paramètres, profils, stabilité et limites. Cette fiche permet d'évaluer une analyse non supervisée même sans chiffre unique de performance. Elle peut servir d'extension au projet final, sans remplacer la classification demandée.
