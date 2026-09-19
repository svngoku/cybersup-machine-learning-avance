# Programme pédagogique · 35 heures

**Machine Learning Avancé — Cybersup, M2 Data / IA**  
**Formateur : Chrys Fé-Marty NIONGOLO**  
Présentiel à Paris, du lundi 21 au vendredi 25 septembre 2026. Lieu communiqué : 8 Terrasse Bellini. Les temps ci-dessous sont pédagogiques, hors pauses et déjeuner. Exemple de plage quotidienne : 9 h–17 h 30 avec 1 h de déjeuner et deux pauses de 15 minutes. Les horaires précis restent ceux de l'école.

Les objectifs supplémentaires validés sont l'interprétabilité, l'évaluation fiable et la reproductibilité/préparation à la mise en production. Le cours privilégie les données tabulaires. Le deep learning, le traitement d'images, le NLP et le déploiement d'un service réel ne sont pas des objectifs de cette semaine.

## Lundi · Évaluation et régularisation

| Séquence | Minutes | Modalité / preuve |
|---|---:|---|
| Accueil, diagnostic, objectif métier | 45 | Diagnostic individuel et décision écrite |
| Contrat des données et TP00 | 45 | Installation, checksum, discussion de duration |
| Découpages, pipelines et métriques | 90 | Matrice de confusion et étude des fuites |
| Biais-variance, régularisation et SVM | 90 | Calculs guidés et lecture de courbes |
| TP01 baseline sans fuite | 120 | Notebook et comparaison sur plis communs |
| Débrief, quiz et protocole du projet | 30 | Une page de protocole |
| **Total** | **420** | **7 h** |

## Mardi · Ensembles et optimisation

| Séquence | Minutes | Modalité / preuve |
|---|---:|---|
| Arbres, Gini, bagging et Random Forest | 60 | Gain de Gini et formule de variance |
| Boosting, calcul d'une itération, histogrammes | 60 | Exemple numérique et courbe d'erreur |
| TP02 ensembles et démo Colab08 | 90 | 70 min de TP02 + 20 min XGBoost sur UCI complet |
| Hyperparamètres, recherche, CV imbriquée | 75 | Schéma interne/externe et budget |
| TP03 optimisation | 90 | Huit essais par méthode, scores externes |
| Comparaison critique, quiz et débrief | 45 | Justifier une petite différence |
| **Total** | **420** | **7 h** |

## Mercredi · Déséquilibre et features

| Séquence | Minutes | Modalité / preuve |
|---|---:|---|
| Coûts, seuil, Fβ et capacité opérationnelle | 60 | Calcul de seuil théorique et coût |
| Sampling, SMOTE et calibration | 75 | Choix d'un protocole sans fuite |
| Features, target encoding et disponibilité | 75 | Contrat de variables |
| TP04 classes rares et décision | 120 | Calibration, seuil validé, test final |
| Atelier features | 60 | Deux transformations et une ablation |
| Quiz et débrief | 30 | Une recommandation justifiée |
| **Total** | **420** | **7 h** |

## Jeudi · Non supervisé

| Séquence | Minutes | Modalité / preuve |
|---|---:|---|
| Représentation, distances et PCA | 75 | Choix d'axes et critique d'une projection |
| K-means, GMM et EM | 75 | Itération à la main et choix d'hypothèses |
| CAH, DBSCAN et HDBSCAN | 60 | Comparaison géométrique |
| TP05 clustering | 150 | Silhouette, bruit, stabilité et rapport |
| Anomalies et étude d'usage | 30 | Distinguer anomalie et classe rare |
| Quiz, restitution et synthèse | 30 | Fiche de segmentation |
| **Total** | **420** | **7 h** |

## Vendredi · Interprétation et projet

| Séquence | Minutes | Modalité / preuve |
|---|---:|---|
| Permutation, PDP/ICE, SHAP, conforme, documentation | 60 | Calcul Shapley et hypothèses de couverture |
| Veille 2025–2026 et évolution des outils | 15 | 10 min publications/benchmarks + 5 min Ray à l’oral |
| TP06 interprétation et incertitude | 90 | Couverture, largeur et explications |
| Projet final en binôme | 180 | Notebook, manifeste et model card |
| Soutenances et synthèse | 45 | 5 min par binôme, jusqu'à 8 binômes |
| Quiz final individuel | 30 | Raisonnement sur des cas nouveaux |
| **Total** | **420** | **7 h** |

**Total général : 2 100 minutes = 35 heures.** Les heures de TP incluent les essais, l'interprétation, la rédaction et l'aide du formateur. Exécuter les corrigés en quelques secondes ne remplace pas ce travail.

Pour plus de huit binômes, utiliser une restitution par posters avec questions individuelles dans le créneau prévu, ou réduire le projet à 150 min et porter la restitution à 75 min. La somme reste 420 min. Le formateur peut déplacer une extension facultative sans supprimer les objectifs centraux.

## Exécution en salle et dans Colab

Les TP02, TP03 et TP06 existent en variantes Colab autonomes, avec versions étudiantes et corrigées.
La démonstration 08 utilise XGBoost et le jeu UCI complet de 41 188 lignes : CPU suffisant, GPU
facultatif si disponible. Les données restent historiques et les scores sont discutés avec leur
protocole. Le créneau de 20 minutes remplace l'extension stacking en séance ; elle reste disponible
après le cours. Préparer les installations avant le démarrage du premier TP.

Voir le [guide Colab](COLAB.md). Distribuer le pack étudiant pour éviter une dépendance aux accès
au dépôt privé. Les autres TP restent exécutables localement. Ray est présenté uniquement à
l'oral avec les [notes du formateur](NOTES_ORALES_RAY.md), sans installation ni TP additionnel.

## Différenciation et animation

- Si les bases Python manquent, fournir le pipeline guidé et travailler d'abord l'interprétation. Le MOOC Inria [R33](../resources/RESSOURCES.md) sert de remédiation.
- Si le groupe avance vite, utiliser stacking, target encoding avec cross-fitting et CAH Ward comme extensions. Ne pas allonger le temps d'optimisation au détriment de l'analyse.
- Alterner prédiction au tableau, expérimentation, confrontation au résultat puis justification écrite.
- Conserver les mêmes splits pour comparer les variantes d'un exercice. Garder les décisions et les échecs dans un journal d'expériences.
- Le barème sur 20 du projet est une proposition pédagogique. Les règles administratives de notation sont celles de Cybersup.
