# Atelier features · 60 minutes

Travailler à partir de TP01, du dictionnaire UCI et de la pipeline de référence. Garder le test fermé. Le but est de transformer une hypothèse métier en comparaison falsifiable.

## 1. Contrat de cinq variables · 15 min

Renseigner un tableau avec les colonnes : nom, type, unité/modalités, instant de disponibilité, valeurs spéciales, transformation envisagée et risque de fuite. Inclure `pdays`, `previous`, `duration`, `campaign` et une catégorie au choix.

Pour `campaign`, préciser si la prédiction se fait avant chaque appel de la campagne ou avant le tout premier. Une variable utilisable dans un scénario peut devenir invalide dans l'autre. Ne pas inventer une date complète à partir du seul mois.

## 2. Deux transformations · 15 min

- Pour `pdays`, le dictionnaire indique 999 lorsque le client n'a pas été précédemment contacté. Proposer un indicateur `contact_precedent` et une représentation des jours pour les clients concernés. Éviter de traiter 999 comme une distance ordinaire.
- Choisir une seconde hypothèse : catégorie manquante explicite, regroupement documenté d'une modalité rare, transformation d'un compte, interaction ou ratio justifié. Préciser le domaine, les cas limites et les informations nécessaires.

## 3. Ablation contrôlée · 20 min

Définir baseline, baseline + transformation A, baseline + transformation B, puis A+B. Conserver les mêmes plis, métrique et budget. Placer toute statistique apprise dans la pipeline. Reporter les scores par pli, la dispersion et le coût. Une règle déterministe fondée sur le dictionnaire ne doit pas utiliser y ni des statistiques calculées sur l'ensemble du jeu.

Ne pas ajouter simultanément de nouvelles features et une recherche beaucoup plus large puis attribuer tout le gain aux features.

## 4. Conclusion · 10 min

Choisir de garder, écarter ou approfondir les transformations. Une feature sans gain mesuré peut être rejetée. La conclusion précise le scénario d'usage, les effectifs et l'incertitude.

**Extension M2 :** proposer un target encoding lissé d'une catégorie de forte cardinalité. Tracer les sous-plis qui servent à fabriquer les encodages d'entraînement. Expliquer la différence entre `fit_transform` et `fit(...).transform(...)` de TargetEncoder. Si la validation principale dépend du temps ou des groupes, auditer aussi les sous-plis internes de l'encodeur.

Références : [R18, R19, R32, R41](../resources/RESSOURCES.md). Corrigé réservé au formateur dans `ATELIER_FEATURES_CORRIGE.md`.
