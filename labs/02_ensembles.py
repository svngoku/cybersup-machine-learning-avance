# %% [markdown]
# # TP 02 · Arbres, bagging et boosting
# 90 minutes. Régression synthétique Friedman : relations non linéaires connues, sans prétention métier.
# Livrable : RMSE de validation, temps d'ajustement et courbe du boosting. Choisir un compromis argumenté.
# Source : https://scikit-learn.org/stable/modules/ensemble.html
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_friedman1
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.metrics import root_mean_squared_error
X, y = make_friedman1(n_samples=1000, n_features=10, noise=1.5, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25, random_state=42)
models = {"Ridge": make_pipeline(StandardScaler(), Ridge(alpha=10)),
          "Arbre": DecisionTreeRegressor(max_depth=5, random_state=42),
          "Forêt": RandomForestRegressor(n_estimators=100, min_samples_leaf=3, n_jobs=1, random_state=42),
          "Boosting": HistGradientBoostingRegressor(max_iter=100, max_leaf_nodes=15, random_state=42)}
cv = KFold(3, shuffle=True, random_state=42)
rows = []
for name, model in models.items():
    r = cross_validate(model, X_train, y_train, cv=cv, scoring="neg_root_mean_squared_error")
    rows.append([name, -r["test_score"].mean(), r["fit_time"].mean()])
print(pd.DataFrame(rows, columns=["modèle", "RMSE CV", "secondes fit"]))
# %% [exercise]
# Exercice 1 (25 min). Tracer RMSE train/validation pour les étapes successives d'un boosting. Où arrêter ? Pourquoi ce choix ne doit-il pas utiliser le test ?
# %% [solution]
gb = GradientBoostingRegressor(n_estimators=180, learning_rate=0.1, max_depth=2, random_state=42).fit(X_train, y_train)
train_errors = [root_mean_squared_error(y_train, p) for p in gb.staged_predict(X_train)]
val_errors = [root_mean_squared_error(y_val, p) for p in gb.staged_predict(X_val)]
plt.plot(np.arange(1,181), train_errors, label="train")
plt.plot(np.arange(1,181), val_errors, label="validation")
plt.xlabel("Nombre d'arbres"); plt.ylabel("RMSE"); plt.legend(); plt.show()
print("Étape au minimum de validation", int(np.argmin(val_errors)) + 1)
# %% [exercise]
# Exercice 2 (20 min). Réduire max_features de la forêt de 1 à 0.6. Comparer sur les mêmes plis. La décorrélation améliore-t-elle toujours le score ?
# %% [solution]
for f in [1.0, 0.6]:
    model = RandomForestRegressor(n_estimators=100, max_features=f, min_samples_leaf=3, n_jobs=1, random_state=42)
    r = cross_validate(model, X_train, y_train, cv=cv, scoring="neg_root_mean_squared_error")
    print(f, -r["test_score"].mean())
print("Réduire la corrélation peut aussi affaiblir les arbres. Mesurer le compromis.")
# %% [exercise]
# Extension (20 min). Construire un stacking avec des prédictions hors pli pour le méta-modèle. Comparer son coût à son bénéfice.
# %% [solution]
stack = StackingRegressor(estimators=[("ridge", models["Ridge"]), ("forest", models["Forêt"])],
    final_estimator=Ridge(alpha=10), cv=3, n_jobs=1)
stack.fit(X_train, y_train)
print("RMSE validation stacking", root_mean_squared_error(y_val, stack.predict(X_val)))
