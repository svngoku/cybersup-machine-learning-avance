# Machine Learning Avancé · Cybersup

Formation **M2 Data / IA**, en présentiel à Paris du **21 au 25 septembre 2026**, **35 heures**.

**Formateur : Chrys Fé-Marty NIONGOLO** · [LinkedIn](https://www.linkedin.com/in/chrys-f%C3%A9-marty-niongolo-410770153/)

Ce dépôt privé contient le support de cours dérivé du template Cybersup, les travaux pratiques, les ressources et les outils d'animation. Les originaux de Julie Hor restent hors dépôt. La bibliographie précise leurs apports et les pages concernées.

## Commencer

1. Installer [uv](https://docs.astral.sh/uv/getting-started/installation/), puis cloner ce dépôt avec un compte autorisé.
2. Dans le dossier du dépôt, exécuter `uv sync --frozen`.
3. Lancer `uv run jupyter lab` et ouvrir `notebooks/etudiants/00_demarrage.ipynb`.
4. Lire le [programme de 35 h](docs/PROGRAMME_35H.md) et les [consignes du projet](evaluation/PROJET.md).

Python 3.12 est demandé. Le socle est testé sur CPU. L'installation initiale nécessite Internet ; les données obligatoires des TP sont ensuite locales. Sur une machine sans uv, créer un environnement Python 3.12 et exécuter `python -m pip install -r requirements.txt`, puis `python -m jupyter lab`. Le verrou uv reste la référence.

## Supports

- [PowerPoint complet](output/CYBERSUP-Machine-Learning-Avance-2026.pptx), éditable, avec notes formateur et références.
- [Pack étudiant sans corrigés](output/CYBERSUP-ML-Avance-Pack-Etudiant.zip).
- [Version PDF](output/CYBERSUP-Machine-Learning-Avance-2026.pdf), sans les notes du présentateur.
- [Programme et déroulé](docs/PROGRAMME_35H.md).
- [Guide d'animation](docs/GUIDE_FORMATEUR.md).
- [Ressources annotées](resources/RESSOURCES.md), [provenance](resources/PROVENANCE.md) et [données](data/README.md).
- [Questions étudiantes](evaluation/QUIZ.md), [projet et barème](evaluation/PROJET.md), [modèle de model card](evaluation/MODEL_CARD.md).

## Parcours des TP

| Notebook | Compétence |
|---|---|
| 00 · Démarrage | Environnement, provenance et contrat des données |
| 01 · Évaluation | Pipeline, baseline, CV, régularisation |
| 02 · Ensembles | Arbres, forêt, boosting et extension stacking |
| 03 · Optimisation | Recherche aléatoire, TPE, CV imbriquée |
| 04 · Déséquilibre | Pondération, SMOTE, calibration et seuil |
| 05 · Clustering | PCA, K-means, GMM, DBSCAN, HDBSCAN, CAH |
| 06 · Interprétation | Permutation, PDP/ICE, split-conformal |
| 07 · Projet | Comparaison, décision, artefact et model card |

Les notebooks étudiants contiennent un socle guidé exécutable et des cellules d'exercice. Les corrections sont séparées dans `notebooks/corriges/`. Les sources lisibles des corrigés sont dans `labs/`. **Un accès au dépôt donne aussi accès aux corrigés** : diffuser l'archive étudiante de `output/` si l'on souhaite les réserver au formateur. Un dossier n'est pas une barrière d'accès.

## Exemples dans Google Colab

Trois TP autonomes sont disponibles dans `notebooks/colab/etudiants/` : **02 Ensembles**,
**03 Optimisation** et **06 Interprétation**. La démonstration guidée
`notebooks/colab/demonstrations/08_xgboost_colab.ipynb` compare une logistique et XGBoost
sur les **41 188 lignes** du fichier UCI complet, avec split chronologique, early stopping,
courbes et manifeste des résultats. Le CPU suffit ; le GPU est facultatif pour XGBoost.

Le [guide Colab](docs/COLAB.md) explique l'import depuis le pack étudiant, les liens directs
pour les comptes autorisés, la sauvegarde et le repli CPU. Aucun jeton GitHub n'est nécessaire.
Les variantes corrigées des trois TP restent dans `notebooks/colab/corriges/`.

**Ray : cinq minutes à l'oral uniquement**, au sein de la veille du vendredi, pour situer
Core, Tune, Train et Data et discuter le passage au calcul distribué. Les
[notes orales](docs/NOTES_ORALES_RAY.md) relient Tune au TP Optuna et citent les sources primaires.
Ray n'est pas une dépendance du cours. Le programme reste de **35 heures**.

## Reproduire et vérifier

- `uv run python scripts/build_notebooks.py` régénère les deux versions des huit TP à partir de `labs/`.
- `uv run python scripts/build_colab_notebooks.py` régénère les sept fichiers Colab, dont les trois corrigés.
- `uv sync --frozen --extra colab`, puis `uv run --extra colab python scripts/check_colab_notebooks.py --skip-install` les exécute chacun dans un dossier temporaire vide sur CPU ; la cellule initiale vérifie les versions. Sans `--skip-install`, elle lance aussi l'installation pip.
- `uv run python scripts/build_student_pack.py` régénère l'archive : huit TP locaux, trois variantes Colab et une démo guidée, sans corrigés ni notes orales.
- `uv run python scripts/check_notebooks.py --version corriges` exécute chaque correction dans un noyau neuf.
- `uv run python scripts/check_notebooks.py --version etudiants` vérifie le socle guidé, sans prétendre valider des réponses non écrites.
- `uv run python scripts/build_assets.py` recalcule les données des graphiques. La copie UCI incluse est vérifiée par empreinte lors du chargement.
- `uv run python scripts/check_links.py` contrôle les liens. Certains hébergeurs peuvent limiter les requêtes automatisées.

L'intégration GitHub exécute les notebooks sous Linux. Les sorties temporaires et les modèles du projet vont dans `.build/` et `results/`, non versionnés. Les tests d'exécution ne prouvent ni l'utilité réelle du modèle ni la validité d'un futur déploiement.

## Modifier le diaporama

Le PowerPoint final peut être modifié directement dans PowerPoint. Pour conserver sa typographie, installer les polices gratuites [Archivo Black](https://fonts.google.com/specimen/Archivo+Black), [DM Sans](https://fonts.google.com/specimen/DM+Sans) et [Roboto Mono](https://fonts.google.com/specimen/Roboto+Mono). La version PDF embarque les polices et reste la référence de projection portable. Les sources de contenu sont `course/0_*.md` à `course/5_*.md`, les tableaux `course/tables.json`, les références `resources/sources.json` et les graphiques `assets/chart-data.json`.

La génération automatisée utilise `scripts/build_deck.mjs`, le runtime de présentations Codex avec `@oai/artifact-tool`, et le template original fourni. Ce générateur n'est pas un paquet npm public autonome. Dans un environnement Codex équipé, définir `RUNTIME_NODE_MODULES`, `RUNTIME_PYTHON`, `PRESENTATION_SKILL_DIR` et éventuellement `COURSE_TEMPLATE`. Le runtime ne remplace pas le template par un autre design. Le diaporama préconstruit permet d'utiliser le cours sans ce runtime.

`uv run python scripts/build_teacher_guide.py` régénère le guide après le PowerPoint, à partir de `.build/slide-manifest.json`.

Les sources du cours indiquent pour chaque diapositive les notes, références et données illustratives. Une nouvelle version doit être rendue et relue après toute modification. Les graphiques schématiques ne sont pas des résultats expérimentaux réels ; ceux calculés sur données synthétiques sont identifiés comme tels.

## Cadre et limites

Les trois objectifs complémentaires à la fiche sont l'interprétabilité, l'évaluation fiable et la reproductibilité/préparation à la mise en production. La veille est datée du **19 septembre 2026**. Le cours traite le ML tabulaire avancé ; les modèles tabulaires de fondation sont présentés en lecture critique, sans dépendance GPU ni service payant.

Les données UCI sont historiques. `duration` est exclue ; les autres variables doivent encore être auditées selon l'instant exact de décision. Le split aléatoire pédagogique des TP locaux ne garantit pas une généralisation temporelle ou par personne. La démo Colab08 utilise l’ordre chronologique du fichier complet et retire aussi `campaign` ; l’absence d’identifiant client limite encore le protocole. Les coûts sont illustratifs. Aucune conclusion causale ni autorisation d'usage réel ne découle des TP.

Pour les droits : voir [PROVENANCE](resources/PROVENANCE.md). La licence CC BY 4.0 ne concerne que le dataset UCI ; elle ne s'étend pas aux logos, au template ou aux documents de tiers. Ce dépôt privé ne concède pas de licence globale supplémentaire.
