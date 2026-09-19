# Exécuter les exemples dans Google Colab

Cybersup · Machine Learning Avancé · Chrys Fé-Marty NIONGOLO · 21–25 septembre 2026

Les versions Colab sont autonomes. Elles installent leurs bibliothèques et produisent leurs
données synthétiques, ou téléchargent le jeu public UCI pour la démonstration 08.
Le dépôt privé n'est pas requis pendant l'exécution.

## Parcours proposé

| Notebook | Jour / durée dans la séance | Calcul et données |
|---|---|---|
| `02_ensembles.ipynb` | J2 · 70 min de TP, puis démo 08 | CPU · Friedman synthétique |
| `03_optimisation.ipynb` | J2 · 90 min | CPU · recherche aléatoire et Optuna |
| `06_interpretation.ipynb` | J5 · 90 min | CPU · permutation, PDP/ICE et conforme |
| `08_xgboost_colab.ipynb` | J2 · démo guidée de 20 min dans les 90 min du TP02 | CPU ou GPU facultatif · UCI, 41 188 lignes |

Les trois premiers sont dans `notebooks/colab/etudiants/`, le quatrième dans
`notebooks/colab/demonstrations/`. Les autres TP restent dans le parcours local.
Le stacking du TP02 peut être poursuivi après le cours. Les créneaux totalisent toujours 35 h.

## Depuis le pack étudiant : chemin recommandé

1. Décompresser le pack remis par le formateur.
2. Ouvrir [Google Colab](https://colab.research.google.com/) et se connecter à son compte Google.
3. Choisir **Fichier → Importer le notebook** et sélectionner un fichier du dossier `notebooks/colab/`.
4. Démarrer avec un runtime **Python 3.12 ou ultérieur, CPU**. Exécuter d'abord la cellule d'installation.
5. Si Colab demande un redémarrage après installation, l'accepter puis reprendre depuis le début.
6. Exécuter les cellules dans l'ordre, compléter les exercices, enregistrer une copie du notebook.
7. Pour la démo 08, télécharger les trois fichiers de `results/colab08/` depuis le panneau Fichiers.

Les corrigés ne sont pas dans le pack. Le répertoire local `results/` du runtime Colab disparaît
avec sa session. Une copie dans Drive du notebook n'emporte pas automatiquement ces fichiers.
Pas de montage Drive ni de jeton GitHub nécessaire.

## Avec un accès au dépôt privé

Ces liens ne sont utilisables que si le compte GitHub est autorisé et si l'intégration Colab
peut accéder au dépôt. Si la page refuse l'accès, télécharger le notebook depuis GitHub puis
l'importer dans Colab ; ne pas placer de jeton dans une cellule.

- [TP02 dans Colab](https://colab.research.google.com/github/svngoku/cybersup-machine-learning-avance/blob/main/notebooks/colab/etudiants/02_ensembles.ipynb)
- [TP03 dans Colab](https://colab.research.google.com/github/svngoku/cybersup-machine-learning-avance/blob/main/notebooks/colab/etudiants/03_optimisation.ipynb)
- [TP06 dans Colab](https://colab.research.google.com/github/svngoku/cybersup-machine-learning-avance/blob/main/notebooks/colab/etudiants/06_interpretation.ipynb)
- [Démo08 dans Colab](https://colab.research.google.com/github/svngoku/cybersup-machine-learning-avance/blob/main/notebooks/colab/demonstrations/08_xgboost_colab.ipynb)

## GPU : facultatif pour la démonstration 08

Dans **Exécution → Modifier le type d'exécution**, demander un GPU NVIDIA si disponible.
Recommencer ensuite l'installation dans la nouvelle session. La démo détecte le GPU et la
prise en charge CUDA par XGBoost. Sans GPU, ou si son initialisation échoue, elle entraîne sur CPU.
Pour forcer le CPU, mettre `REQUESTED_DEVICE = "cpu"` dans la cellule de configuration.

XGBoost 3.1.3 est épinglé avec `tree_method="hist"` et `device="cuda"` lorsque disponible.
La branche 3.1 demande CUDA >= 12.0. Les transformations pandas/scikit-learn et la baseline
restent sur CPU. Le simple choix d'un accélérateur ne déplace pas tous les calculs sur GPU.
Sur 41 188 lignes, aucune accélération n'est promise. Comparer le coût total, transferts inclus.

Colab impose des limites variables et ne garantit aucun accélérateur gratuit. Ce cours peut
être suivi sans abonnement payant. Voir la [FAQ officielle](https://research.google.com/colaboratory/faq.html)
et la [documentation XGBoost utilisée](https://xgboost.readthedocs.io/en/release_3.1.0/gpu/index.html).

## Repli local et diagnostic

- Runtime trop ancien ou conflit de bibliothèques : repartir d'une session neuve, puis installer avant les imports.
- Pas de GPU / quota atteint : exécuter la démo sur CPU avec les mêmes données et paramètres.
- UCI indisponible : déposer le CSV officiel complet dans `data/bank-additional-full.csv` ; l'empreinte doit correspondre à celle du notebook.
- Connexion indisponible : les huit TP locaux utilisent les données incluses ou synthétiques, après installation des dépendances.
- Démo locale : `uv sync --frozen --extra colab`, puis `uv run --extra colab jupyter lab` depuis le dépôt ou le pack.

Les versions principales sont épinglées dans chaque notebook ; le verrou `uv.lock` fixe aussi
les dépendances transitives pour le parcours local. Les tests automatiques lancent chaque fichier
Colab dans un dossier vide et sur CPU. Ils vérifient son autonomie, pas l'attribution d'un GPU
par Google ni le fonctionnement d'un compte Google particulier.


## Résultat de référence pour le débrief de la démo 08

Lors de l'exécution locale sur CPU du 19 septembre 2026, les prévalences observées sont
4,81 % sur train, 11,07 % sur validation et 30,83 % sur test. XGBoost est retenu par l'AP de
validation (0,119 contre 0,098 pour la logistique) et l'arrêt anticipé retient le premier tour.
Sur le test réservé : AP 0,294, ROC-AUC 0,469, log-loss 0,971. Ce classement est faible ;
le modèle ne justifie pas une recommandation de déploiement.

L'AP brute de deux périodes à prévalences différentes ne se compare pas directement comme
une amélioration du modèle. Le score AP du test doit se lire avec la prévalence de 0,308.
Ce résultat reste dans la démonstration : un budget de 600 arbres n'oblige pas à les entraîner,
et un modèle plus complexe ne résout pas une différence de population. Ne pas retoucher les
paramètres après ce test pour produire une démonstration plus flatteuse.

Ces valeurs sont des observations locales reproductibles avec les versions indiquées ; les
chronométrages et de petits écarts numériques peuvent dépendre du matériel. L'installation
pip et les sept notebooks ont été exécutés dans un environnement Python neuf et des dossiers
vides. Une session hébergée par Google et le chemin GPU n'ont pas été validés ici.
