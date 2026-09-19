# Atelier features · Attendus formateur

- `duration` : durée du dernier appel en secondes, connue après l'appel. À exclure pour une décision avant l'appel.
- `pdays` : jours depuis le dernier contact d'une campagne précédente ; 999 est une sentinelle de non-contact. Créer un indicateur distinct et coder la valeur des jours non applicable comme manquante. Le choix exact d'imputation reste à valider.
- `previous` : nombre de contacts avant cette campagne. Vérifier la définition de disponibilité retenue.
- `campaign` : nombre de contacts durant la campagne, comprenant le dernier contact selon le dictionnaire. Pour prédire avant le premier appel, la valeur finale de cette variable n'est pas disponible. Notre baseline avant un appel est simplifiée ; exiger que le binôme identifie cette ambiguïté et propose exclusion ou reconstruction à l'instant voulu.
- Catégorie `unknown` : elle peut être conservée comme modalité explicite plutôt qu'imputée. Il faut comparer ce choix et prévoir les modalités nouvelles.

L'ablation attendue compare quatre configurations sur les mêmes plis du développement. Une différence faible ou instable ne suffit pas à retenir une transformation. Les variables dérivées ne doivent pas être construites en regardant les labels du test.

Pour target encoding, le lissage ramène une catégorie peu observée vers une moyenne de référence apprise sur train. Le cross-fitting sépare les observations dont on calcule l'encodage de celles dont on utilise la cible. Une validation par groupe ne suffit pas si l'encodage interne mélange le même groupe. Un pipeline logiciel ne remplace pas cet audit.

Ne pas imposer un gain chiffré prédéfini : il dépend du modèle, du scénario, des choix et de l'échantillon. Noter le contrat de disponibilité, la validité des transformations, la comparaison contrôlée et la qualité de la conclusion.
