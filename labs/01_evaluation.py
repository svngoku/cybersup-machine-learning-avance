# %% [markdown]
# # TP 01 · Une baseline sans fuite
# 120 minutes. Livrable : protocole écrit, pipeline, comparaison à une baseline et interprétation de la dispersion.
# On conserve le test final fermé. L'AP est l'average precision, pas l'aire trapézoïdale de la courbe PR.
# Sources : https://scikit-learn.org/stable/common_pitfalls.html et https://scikit-learn.org/stable/modules/cross_validation.html
# %%
from pathlib import Path
import sys
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "mlcourse.py").exists())
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from mlcourse import split_bank, bank_pipeline, cv3, SEED
X_dev, X_test, y_dev, y_test = split_bank()
assert set(X_dev.index).isdisjoint(X_test.index)
models = {
    "Prévalence": bank_pipeline(DummyClassifier(strategy="prior")),
    "Logistique": bank_pipeline(LogisticRegression(C=1, max_iter=2000)),
}
rows = []
for name, model in models.items():
    scores = cross_validate(model, X_dev, y_dev, cv=cv3(),
        scoring={"AP": "average_precision", "ROC": "roc_auc"}, n_jobs=1)
    rows.append({"modèle": name, "AP moyenne": scores["test_AP"].mean(),
                 "AP écart-type": scores["test_AP"].std(),
                 "ROC moyenne": scores["test_ROC"].mean()})
print(pd.DataFrame(rows).to_string(index=False))
# %% [exercise]
# Exercice 1 (25 min). Comparer C = 0.01, 0.1, 1 et 10 sur les mêmes plis. Expliquer le sens de C.
# %% [solution]
comparison = []
for C in [0.01, 0.1, 1, 10]:
    model = bank_pipeline(LogisticRegression(C=C, max_iter=2000))
    result = cross_validate(model, X_dev, y_dev, cv=cv3(), scoring="average_precision", n_jobs=1)
    comparison.append((C, result["test_score"].mean(), result["test_score"].std()))
print(pd.DataFrame(comparison, columns=["C", "AP", "écart-type"]))
print("Un C petit renforce la régularisation. La dispersion entre plis n'est pas un intervalle de confiance indépendant.")
# %% [exercise]
# Exercice 2 (20 min). Faire cinq permutations de la cible et vérifier si un signal subsiste. Ne pas interpréter ce mini-test comme un test statistique définitif.
# %% [solution]
rng = np.random.default_rng(SEED)
null_scores = []
for i in range(5):
    yp = pd.Series(rng.permutation(y_dev), index=y_dev.index)
    result = cross_validate(models["Logistique"], X_dev, yp, cv=cv3(), scoring="average_precision")
    null_scores.append(result["test_score"].mean())
print("AP sous permutation", np.round(null_scores, 3), "prévalence", round(y_dev.mean(), 3))
# %% [exercise]
# Exercice 3 (20 min). Rédiger pourquoi une CV aléatoire ne prouve pas la performance sur de futurs appels. Proposer une validation temporelle sur le fichier complet ordonné.
# %% [solution]
print("Le sous-échantillon fourni est aléatoire et n'a pas de date complète. Utiliser le fichier complet ordonné et des blocs temporels, puis auditer les contacts répétés.")
