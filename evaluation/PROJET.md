# Projet final · Prioriser une campagne d'appels

**Durée : 180 min en binôme, suivies d'une restitution.** Le barème proposé est pédagogique et ne remplace pas les règles officielles de l'école.

## Situation et décision

Une équipe souhaite prioriser les clients à contacter **avant l'appel**. Utiliser `bank-additional.csv`, fourni sous licence CC BY 4.0. La cible est la souscription (`y=yes`). Ne pas utiliser `duration`. Les coûts conventionnels de l'exercice sont FP = 1 unité et FN = 5 unités. Ils n'expriment ni la rentabilité réelle d'un appel ni un effet causal de la campagne.

## Travail demandé

1. **Protocole (30 min).** Décrire la population, la cible, l'instant de décision, les variables interdites et la stratégie de découpage. Réserver 20% pour le test final avec la graine 42. Sur le développement, réserver une validation de décision ou définir une procédure hors pli équivalente. Auditer les limites du split aléatoire.
2. **Comparaisons (45 min).** Comparer DummyClassifier, régression logistique régularisée et un ensemble. Utiliser AP comme métrique principale de classement et des plis communs. Rapporter moyenne et dispersion. Définir un budget borné. Toutes les transformations apprises et sélections de variables doivent rester dans les plis.
3. **Décision (30 min).** Examiner la calibration et sélectionner un seuil sur validation selon les coûts. Documenter la sensibilité du seuil et le volume d'alertes. Le seuil 0,5 sert de référence, pas de vérité métier.
4. **Évaluation finale (30 min).** Figer les choix. Ouvrir une fois le test et publier AP, ROC-AUC, précision, rappel, Brier, matrice de confusion et coût. Si le résultat déçoit, le documenter sans retoucher le seuil sur test. Toute nouvelle sélection change le statut de ce test.
5. **Restitution (45 min).** Exporter la pipeline, le seuil et un manifeste. Vérifier la relecture et quelques prédictions identiques. Compléter la model card et préparer une recommandation en cinq minutes.

Une expérience supplémentaire est autorisée si elle n'empiète pas sur la restitution : ablation de features ou diagnostic de segmentation. Un score plus élevé ne rapporte pas automatiquement plus de points.

## Livrables

- Notebook exécutable depuis un noyau neuf, avec les résultats et conclusions.
- Tableau de comparaison incluant la baseline, les paramètres et le budget.
- Pipeline enregistrée, manifeste JSON et contrôle de relecture.
- Model card de une à deux pages, à partir du modèle fourni.
- Restitution : décision, preuve, limite et prochaine validation nécessaire.

## Barème sur 20

| Critère | Points | Attribution |
|---|---:|---|
| Protocole sans fuite | 5 | 2 découpage, 2 transformations dans les plis, 1 test figé |
| Comparaisons et optimisation | 4 | 1 baseline, 1 familles, 1 budget/paramètres, 1 dispersion |
| Classes rares et décision | 3 | 1 métriques, 1 calibration, 1 seuil validé/coût |
| Interprétation et limites | 3 | 1 explication pertinente, 2 limites concrètes |
| Reproductibilité | 3 | 1 exécution, 1 versions/données, 1 manifeste et relecture |
| Restitution | 2 | 1 conclusion claire, 1 réponses individuelles |
| **Total** | **20** | |

Une fuite non corrigée met le critère « protocole » à zéro et invalide les conclusions de performance. Les autres compétences restent évaluables ; signaler explicitement ce qui doit être repris. Une recommandation de ne pas déployer peut obtenir tous les points si elle est bien justifiée.

## Attendus et limites à connaître

La comparaison est locale et pédagogique. Le sous-échantillon n'offre ni dates complètes ni identifiants permettant de garantir l'indépendance des personnes. Les données sont anciennes. La probabilité de souscrire n'est pas l'effet d'un appel supplémentaire. Un pipeline sérialisé n'est pas un service de production. Les résultats réels varient avec les configurations ; aucun score cible n'est imposé.
