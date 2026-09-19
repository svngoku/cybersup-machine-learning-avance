# Model card · À compléter par le binôme

## Identité

Nom du modèle, version, date, auteurs, commit Git, chemin du manifeste et responsable du suivi.

## Usage prévu

Qui utilise la prédiction, pour quelle décision, à quel instant, sur quelle population et avec quelles limites de capacité ? Quel résultat n'est pas couvert ?

## Données

Source et attribution, licence, fichier exact et empreinte, période, population, cible, disponibilité des variables et transformations. Lister les variables exclues et les raisons. Préciser les populations absentes et la qualité des labels.

## Méthode

Famille, pipeline, paramètres, graine, budget de recherche, choix du prétraitement et du traitement des classes rares. Méthode de calibration et règle de seuil avec leurs jeux respectifs.

## Évaluation

Décrire train/validation/test et la CV. Indiquer la date de gel des choix. Rapporter effectifs, prévalence, AP, ROC-AUC, précision, rappel, Brier, matrice de confusion et coût. Distinguer scores de développement et score final. Ajouter des analyses de segments pertinentes avec effectifs.

## Interprétation

Méthode utilisée, jeu de référence, échelle de sortie, observations principales et limites. Les explications ne sont pas des effets causaux.

## Limites et risques d'usage

Données historiques, contacts répétés non identifiables, absence de validation future, coûts conventionnels, risque de dérive et de biais de sélection. Justifier toute autre limite identifiée.

## Reproductibilité et exploitation

Versions de Python et dépendances, commit, commandes d'exécution, artefact et vérification de relecture. Préciser les contrôles d'entrée, le suivi nécessaire, les conditions de retour arrière et de réévaluation avant un usage réel.

## Décision recommandée

Recommander expérimentation complémentaire, maintien en étude ou passage à une étape suivante explicitement définie. Relier la recommandation aux preuves disponibles.

Référence : Mitchell et al., *Model Cards for Model Reporting*, [R30](../resources/RESSOURCES.md).
