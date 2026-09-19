# Provenance et réutilisation

## Template Cybersup

Le PowerPoint final dérive du fichier fourni `CYBERSUP - TEMPLATE DATA_IA.pptx` : format 16:9, couverture orange, sommaire bleu, intercalaires, bandeau de spécialité, logos et pieds de page. Polices du modèle : Archivo Black, DM Sans et Roboto Mono. Les textes pédagogiques restent éditables. Les graphiques et tableaux sont des objets natifs du diaporama. Le fichier original n'est pas redistribué dans le dépôt.

La biographie, la photo et les certifications d'exemple du template ne décrivent pas Chrys Fé-Marty NIONGOLO et ont été retirées. Seuls le nom fourni et le [profil LinkedIn fourni](https://www.linkedin.com/in/chrys-f%C3%A9-marty-niongolo-410770153/) sont repris. L'accès automatisé au profil n'a pas permis d'en vérifier le contenu ; aucun parcours professionnel n'en a été inféré.

## Supports locaux de Julie Hor, Sup de Vinci, 2020

Les numéros ci-dessous sont les **pages PDF**. Certains numéros imprimés à l'intérieur du premier support diffèrent.

| Support / pages | Apport | Traitement dans le cours |
|---|---|---|
| Cours 2020 Final - M1, p. 9–10 | Découverte de connaissances | Cadrage et passage de données à décision |
| Même support, p. 36–41 | CRISP-DM | Retour entre métier, données, modèles et évaluation |
| Même support, p. 48–49 | Description / prédiction | Objectifs du supervisé et du clustering |
| Méthodo Data Mining 2020, p. 8–11 | Types et transformations | Features, disponibilité et scaling |
| Même support, p. 36–39 | Échantillons et confusion | Pipeline, découpage et exemple original chiffré |
| Même support, p. 40–52 | Arbres | Gini, complexité puis ensembles |
| Même support, p. 63–73 | Scoring et ciblage | Fil rouge d'appels, seuil, capacité et limites causales |

La mention visible dans ces fichiers interdit la reproduction sans autorisation et citation. Le dépôt et le diaporama ne recopient donc ni leurs pages, ni leurs schémas, ni leur contenu textuel. Les concepts ont été reformulés et approfondis avec les références primaires. Les fichiers restent dans le dossier local d'origine.

Deux précisions ont été intégrées :

1. Le coefficient de Pearson est invariant aux transformations affines à échelle positive. C'est la covariance et certaines distances qui dépendent des unités.
2. Une taille de 30 observations par feuille n'est pas une règle universelle des arbres. La complexité se choisit selon les données et la validation.

## Illustrations et exemples

Les graphiques du cours sont originaux : leurs données se trouvent dans `assets/chart-data.json`. Chaque graphique indique s'il s'agit d'une construction théorique ou d'une expérience synthétique. Le calcul est traçable dans `scripts/build_assets.py`. Aucun graphique de recherche n'est réutilisé comme illustration de performance locale.

Les comparaisons ROC/PR et K-means/DBSCAN utilisent respectivement les mêmes observations afin de rendre le mécanisme comparable. Les nombres du Gini, de l'itération de boosting, du K-means 1D et du jeu de Shapley sont des exercices construits, explicitement identifiés.

Le jeu Bank Marketing est redistribué sous CC BY 4.0 avec attribution et empreinte du fichier original. Les articles et documentations sont référencés, pas copiés. Les marques et logos restent la propriété de leurs titulaires. Aucune licence globale ne prétend couvrir des ressources de tiers.
