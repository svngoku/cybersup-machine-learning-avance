# Données des travaux pratiques

**Bank Marketing** — Moro, S., Rita, P. et Cortez, P. (2014). UCI Machine Learning Repository. [DOI 10.24432/C5K306](https://doi.org/10.24432/C5K306). [Fiche et téléchargement](https://archive.ics.uci.edu/dataset/222/bank+marketing).

Licence du dataset indiquée par UCI : **[Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)**. Copie récupérée le 19 septembre 2026. La licence autorise le partage et l'adaptation avec attribution. Aucun endossement de ce cours par les auteurs ou UCI n'est suggéré.

Le fichier `bank-additional.csv` est la version officielle aléatoire de 4 119 lignes, représentant environ 10% de `bank-additional-full.csv` (41 188 lignes). Il contient 20 entrées et la cible `y`. Ces chiffres ne doivent pas être mélangés avec ceux de `bank-full.csv`, une autre version présente sur la page UCI.

SHA-256 du CSV non modifié :

`7e59cf650004d65d1c9d6b08553bad2ee9a9ad70d594f536e3c584ee6ed5df50`

Le dictionnaire original `bank-additional-names.txt` est conservé. Le loader transforme explicitement `unknown` en valeur manquante et retire `duration`, indisponible avant la fin de l'appel. Il reste 19 entrées. Les fichiers eux-mêmes ne sont pas modifiés. La cible vaut 1 si `y == "yes"`.

Les observations remontent à 2008–2010. Le sous-échantillon aléatoire ne contient pas de date complète ni d'identifiant personne permettant de garantir une validation temporelle et par client. La stratification utilisée dans le cours est une simplification pédagogique. Elle ne prouve pas une performance sur de futurs appels. La source complète est ordonnée chronologiquement, mais son protocole demanderait encore un audit de la disponibilité des variables et des contacts répétés.

Les TP02 à TP06 emploient aussi des données **synthétiques** produites par scikit-learn avec des graines explicites. Elles n'ont aucune valeur de résultat métier et ne nécessitent pas de téléchargement.
