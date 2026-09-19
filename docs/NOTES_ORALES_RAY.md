# Ray : ouverture orale de cinq minutes

**Notes du formateur · Chrys Fé-Marty NIONGOLO · J5 · dans les 15 minutes de veille**

Objectif : situer l'évolution du notebook individuel vers plusieurs essais ou entraînements
coordonnés. Aucun code, installation Ray, cluster ou compétence évaluée supplémentaire.
Le créneau devient 10 minutes de lecture critique des modèles/benchmarks + 5 minutes à l'oral.

## 0:00–1:00 · Partir du TP03

« Nous avons limité la recherche à huit essais. Imaginons maintenant des dizaines d'expériences,
des modèles plus coûteux et plusieurs machines. Comment répartir le travail, respecter la mémoire
disponible et reprendre après une interruption ? »

Colab fournit un environnement de notebook avec un runtime. Ray est un ensemble de bibliothèques
pour organiser du calcul parallèle et distribué. Un GPU accélère certaines opérations prises en
charge ; un ordonnanceur distribue des tâches. Ce sont des niveaux différents.

## 1:00–2:00 · Les briques à nommer

| Brique | Exemple verbal dans le prolongement du cours |
|---|---|
| Ray Core | Exécuter des tâches en parallèle ; des acteurs conservent un état entre appels. |
| Ray Tune | Coordonner les essais, leurs ressources, leurs rapports de métriques et leur arrêt. |
| Ray Train | Organiser un entraînement distribué pris en charge et sa reprise via checkpoints. |
| Ray Data | Lire, transformer et alimenter des traitements de données à plus grande échelle. |

Ne pas présenter ces briques comme une conversion automatique de n'importe quel `.fit()` en
entraînement distribué. Les intégrations et le découpage des données restent à concevoir.

## 2:00–3:00 · Relier Tune et Optuna

« Dans notre TP, Optuna propose une valeur de C puis observe le score. Ray Tune peut orchestrer
des essais et s'appuyer sur une recherche Optuna. Proposer une configuration et lui allouer un
CPU ou un GPU sont deux responsabilités. »

Un scheduler peut arrêter un essai peu prometteur s'il reçoit des métriques intermédiaires
comparables. Un checkpoint est une sauvegarde exploitable de l'état, pas seulement un score imprimé.
Paralléliser doit respecter les plis, les graines, la mémoire et les budgets de chaque candidat.

## 3:00–4:00 · Expliquer le coût

Sur notre CSV de 41 188 lignes, mesurer d'abord un pipeline local : les données tiennent en
mémoire. Sérialiser, transférer les données, démarrer des workers et coordonner le travail peut
coûter plus cher que le calcul économisé. Un nombre élevé de tâches très courtes n'est pas
automatiquement efficace. Éviter aussi de multiplier les threads internes par le nombre de workers.

Distribuer ne corrige ni une fuite de données ni une mauvaise métrique. Le manifeste doit encore
conserver versions, matériel, budget, partitions et procédure de sélection.

## 4:00–5:00 · Question de sortie

« Quel signal vous ferait envisager plusieurs machines : un score faible, un essai trop long,
une mémoire saturée ou un nombre d'expériences devenu élevé ? Quelle mesure feriez-vous d'abord ? »

Attendu : un score faible n'est pas à lui seul une raison de distribuer. Mesurer calcul, mémoire,
transferts et parallélisme utile avant de choisir. Annoncer l'approfondissement comme un autre cours.

Ray n'est pas une invention de 2026 : son article fondateur date d'**OSDI 2018**. L'ouverture
illustre une évolution des pratiques et des outils utilisés aujourd'hui. Documentation consultée
le **19 septembre 2026** ; les liens `latest` peuvent changer.

## Sources primaires accessibles

- [R44 · Vue d'ensemble de Ray](https://docs.ray.io/en/latest/ray-overview/index.html)
- [R45 · Ray Tune et intégrations de recherche](https://docs.ray.io/en/latest/tune/index.html)
- [R47 · Moritz et al., Ray, OSDI 2018](https://www.usenix.org/conference/osdi18/presentation/moritz)
- [R48 · Ray Train](https://docs.ray.io/en/latest/train/train.html)
- [R49 · Ray Data](https://docs.ray.io/en/latest/data/data.html)
