# %% [markdown]
# # TP 00 · Installation et contrat des données
# 30 minutes. Objectif : ouvrir l'environnement, contrôler la provenance et définir ce qui est connu au moment de la décision.
# Lire `data/README.md`. Les données sont historiques et anonymisées. Le cours ne constitue pas un système bancaire déployable.
# Sources : UCI Bank Marketing, DOI 10.24432/C5K306 ; documentation scikit-learn 1.9.1.
# %%
from pathlib import Path
import sys
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "mlcourse.py").exists())
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
import sklearn
from mlcourse import load_bank, split_bank, SEED
print("Python", sys.version.split()[0], "scikit-learn", sklearn.__version__)
X, y = load_bank()
print("Dimensions", X.shape, "prévalence", round(y.mean(), 4))
print(X.dtypes.value_counts())
assert "duration" not in X and "y" not in X
assert y.nunique() == 2 and len(X) == 4119
# %% [exercise]
# Exercice 1. Pourquoi supprimer `duration` alors que cette variable peut améliorer le score ?
# Définir la décision « contacter un client avant l'appel ». Écrire trois variables disponibles à cet instant.
# %% [solution]
print("La durée n'est connue qu'après l'appel. L'utiliser avant l'appel crée une fuite temporelle.")
print("Exemples à auditer selon le SI : age, job, historique previous.")
# %% [exercise]
# Exercice 2. Vérifier l'absence de chevauchement des indices après le découpage. Ce contrôle prouve-t-il l'indépendance des personnes ?
# %% [solution]
X_dev, X_test, y_dev, y_test = split_bank()
assert set(X_dev.index).isdisjoint(X_test.index)
print("Indices disjoints. Sans identifiant personne, on ne peut pas garantir des personnes disjointes.")
