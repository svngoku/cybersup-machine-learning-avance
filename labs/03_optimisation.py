# %% [markdown]
# # TP 03 · Optimisation et validation imbriquée
# 90 minutes. Comparer une recherche aléatoire et une recherche TPE à budget égal de huit essais.
# Le score gagnant de la recherche est optimiste : la boucle externe estime la procédure entière.
# Sources : documentation scikit-learn model_selection ; documentation Optuna 4.9.0.
# %%
import numpy as np
import pandas as pd
import optuna
from scipy.stats import loguniform
from sklearn.datasets import make_classification
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV, cross_val_score
X, y = make_classification(n_samples=900, n_features=16, n_informative=6, weights=[0.85,0.15], random_state=42)
inner = StratifiedKFold(3, shuffle=True, random_state=17)
outer = StratifiedKFold(3, shuffle=True, random_state=42)
base = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1500))
search = RandomizedSearchCV(base, {"logisticregression__C": loguniform(1e-3,1e2)},
    n_iter=8, scoring="average_precision", cv=inner, random_state=42, n_jobs=1)
nested_scores = cross_val_score(search, X, y, cv=outer, scoring="average_precision", n_jobs=1)
print("AP externe", nested_scores, "moyenne", nested_scores.mean())
# %% [exercise]
# Exercice 1 (20 min). Calculer le nombre d'ajustements de la recherche imbriquée, y compris les réajustements par pli externe. Expliquer pourquoi il n'y a pas besoin de voir le test.
# %% [solution]
print("3 plis externes × (8 essais × 3 plis internes + 1 refit) =", 3 * (8 * 3 + 1))
print("Chaque validation externe reste invisible à sa recherche interne.")
# %% [exercise]
# Exercice 2 (30 min). Implémenter huit essais TPE par pli externe, avec les mêmes bornes. Fournir la distribution externe sans conclure sur un seul meilleur score.
# %% [solution]
optuna.logging.set_verbosity(optuna.logging.WARNING)
tpe_scores = []
for fold, (itr, iva) in enumerate(outer.split(X,y)):
    def objective(trial):
        c = trial.suggest_float("C", 1e-3, 1e2, log=True)
        model = make_pipeline(StandardScaler(), LogisticRegression(C=c, max_iter=1500))
        return cross_val_score(model, X[itr], y[itr], cv=inner, scoring="average_precision").mean()
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42+fold, n_startup_trials=4))
    study.optimize(objective, n_trials=8)
    winner = make_pipeline(StandardScaler(), LogisticRegression(C=study.best_params["C"], max_iter=1500)).fit(X[itr], y[itr])
    from sklearn.metrics import average_precision_score
    tpe_scores.append(average_precision_score(y[iva], winner.predict_proba(X[iva])[:,1]))
print(pd.DataFrame({"random": nested_scores, "TPE": tpe_scores}))
# %% [exercise]
# Exercice 3 (15 min). Le modèle TPE gagne de 0.003 AP : quelle information manque pour le déclarer meilleur ?
# %% [solution]
print("Sensibilité aux plis et aux graines, budget identique, incertitude, coût et intérêt pratique. Les trois plis ne sont pas indépendants.")
