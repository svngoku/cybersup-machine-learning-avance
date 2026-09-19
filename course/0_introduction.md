# Ouverture de la formation

## Machine Learning Avancé
Kind: cover
Notes: Accueillir les participants. Formation Cybersup en présentiel à Paris, du 21 au 25 septembre 2026, niveau M2 Data / IA, 35 heures pédagogiques. Faire annoncer à chacun un problème rencontré avec un modèle. Les temps de pause sont exclus des 35 heures. Le QR code mène au dépôt privé ; distribuer les notebooks par archive si les accès GitHub ne sont pas encore ouverts.

## Votre formateur
Kind: trainer
- Formateur : Chrys Fé-Marty NIONGOLO.
- Une démarche centrée sur les mécanismes, l'expérimentation et la justification des choix.
- Des exemples calculables, des notebooks Python et un projet à présenter en binôme.
Notes: Le lien LinkedIn a été fourni par le formateur. Aucune expérience, certification ni biographie supplémentaire n'est affirmée. Inviter les participants à préciser leur maîtrise de Python, des statistiques et de scikit-learn. Présenter le fonctionnement des échanges en présentiel.

## Programme de la semaine
Kind: agenda
Notes: Présenter les cinq journées. Les notions d'évaluation sont reprises dans tous les TP. Le projet final utilise des compétences accumulées pendant la semaine. Les corrections sont dans un dossier réservé à l'animation ; les notebooks étudiants contiennent les exemples guidés et les espaces d'exercice.

## Six compétences à démontrer
Table: objectives
Notes: Les trois premières compétences reprennent la fiche de formation. Les trois suivantes, interprétabilité, évaluation fiable et reproductibilité/mise en production, complètent les objectifs masqués dans la fiche et ont été validées par le formateur. Il s'agit d'une préparation à la mise en production, pas d'un déploiement réel ni d'une certification de conformité.

## Prérequis et diagnostic
- Python : fonctions, tableaux NumPy, DataFrame pandas et graphiques simples.
- Statistiques : moyenne, variance, probabilité conditionnelle, corrélation.
- ML : entraînement/test, régression, classification et lecture d'une matrice de confusion.
> Diagnostic de 10 minutes puis groupes de travail complémentaires
Notes: Faire répondre au diagnostic de evaluation/QUIZ.md sans noter. Distinguer une difficulté de code d'une difficulté de raisonnement. Prévoir la ressource R33 pour la remédiation. Les mathématiques sont utilisées pour comprendre un mécanisme, puis reliées à une expérimentation.
Sources: R01, R33

## Le rythme des cinq journées
Table: schedule
> Chaque jour : 7 heures pédagogiques, pauses exclues
Notes: Le détail minute par minute figure dans docs/PROGRAMME_35H.md. Les créneaux totalisent 420 minutes par jour. Les TP longs incluent recherche, essais, rédaction et débrief, pas seulement l'exécution des cellules. Adapter le nombre d'extensions au diagnostic sans supprimer le projet ni le débrief.

## Le fil rouge : prioriser des appels
- Décision : quels clients contacter avant une campagne ?
- Prédiction : estimer une probabilité de souscription à partir des informations disponibles.
- Évaluation : comparer au hasard, justifier le seuil et documenter les limites.
> Un score de propension n'est pas l'effet causal d'un appel
Notes: La question métier précède le choix d'algorithme. La cible historique est la souscription, pas un bénéfice ni un effet du traitement. Le gain incrémental d'une campagne demanderait une expérimentation ou une méthode causale appropriée. Les coûts FP/FN utilisés dans le cours sont des unités pédagogiques choisies explicitement.
Sources: R32, R39

## Nos ressources de travail
- Le diaporama pose les mécanismes et les questions à discuter.
- Les notebooks contiennent des exemples, des exercices et des vérifications.
- Le dépôt conserve le programme, les sources, le barème et les versions des dépendances.
> CPU suffisant ; données des TP disponibles hors ligne après installation
Notes: Ouvrir le README avec les étudiants. Exécuter uv sync --frozen avant la formation, puis uv run jupyter lab. Sans uv, installer les dépendances depuis requirements.txt dans un environnement Python 3.12. Les corrections ne sont pas protégées par le simple nom d'un dossier : fournir une archive étudiante si l'on veut les masquer.

## Exécuter un exemple dans Colab
- Importer un notebook autonome depuis le pack étudiant.
- Installer les dépendances, puis exécuter les cellules dans l'ordre.
- Sauvegarder le notebook et ses résultats avant de quitter la session.
> CPU pour les TP ; GPU facultatif pour la démonstration XGBoost
Notes: Suivre docs/COLAB.md. Les variantes des TP02, TP03 et TP06 utilisent des données synthétiques. La démo08 télécharge le jeu UCI complet et vérifie son empreinte. Le dépôt reste privé : l'import du fichier local évite de demander un jeton GitHub aux étudiants. Colab nécessite un compte Google et une connexion ; les runtimes sont temporaires et l'accès au GPU n'est pas garanti. Le choix d'un GPU n'accélère pas automatiquement les estimateurs scikit-learn. Préparer la première installation avant la séance ; le parcours local reste disponible.
Sources: R43, R46

## Ce que nous reprenons des supports de 2020
- Le cadrage du problème, les types de variables et le cycle de projet.
- Les arbres, la matrice de confusion et le raisonnement par scoring.
- Une extension vers les ensembles, la validation robuste et l'incertitude.
> Exemples et illustrations du cours reconstruits et attribués
Notes: Les supports de Julie Hor sont cités avec les pages PDF dans resources/PROVENANCE.md. Ne pas distribuer les PDF originaux sans autorisation. Corriger deux raccourcis : le coefficient de Pearson est invariant aux changements positifs d'unité, et il n'existe pas de règle universelle imposant 30 observations par feuille d'arbre.
Sources: R38, R39
