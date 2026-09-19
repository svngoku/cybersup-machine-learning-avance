# %% [markdown]
# # TP 06 · Expliquer et quantifier l'incertitude
# 90 minutes. Régression Friedman synthétique. Séparer entraînement, diagnostic, calibration conforme et test.
# Livrable : importance par permutation, PDP/ICE, couverture observée et largeur d'intervalle.
# Sources : scikit-learn inspection ; Angelopoulos & Bates, arXiv:2107.07511.
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_friedman1
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance, PartialDependenceDisplay
from sklearn.metrics import root_mean_squared_error
X,y=make_friedman1(n_samples=1600,n_features=10,noise=2,random_state=42)
Xbase,Xtest,ybase,ytest=train_test_split(X,y,test_size=.2,random_state=42)
Xtr,Xrest,ytr,yrest=train_test_split(Xbase,ybase,test_size=.375,random_state=43)
Xdiag,Xcal,ydiag,ycal=train_test_split(Xrest,yrest,test_size=.5,random_state=44)
model=HistGradientBoostingRegressor(max_iter=140,max_leaf_nodes=15,l2_regularization=1,random_state=42).fit(Xtr,ytr)
imp=permutation_importance(model,Xdiag,ydiag,n_repeats=5,scoring="neg_root_mean_squared_error",random_state=42)
print(pd.DataFrame({"variable":np.arange(10),"hausse RMSE":imp.importances_mean}).sort_values("hausse RMSE",ascending=False))
PartialDependenceDisplay.from_estimator(model,Xdiag,[0,1],kind="both",subsample=35,random_state=42)
plt.show()
# %% [exercise]
# Exercice 1 (25 min). Construire des intervalles split-conformal à 90%. Utiliser le rang fini-échantillon ceil((n_cal+1)(1-alpha)) et non un quantile approximatif ordinaire.
# %% [solution]
alpha=.1
scores=np.abs(ycal-model.predict(Xcal)); n=len(scores)
rank=int(np.ceil((n+1)*(1-alpha)))
q=np.sort(scores)[rank-1] if rank<=n else np.inf
pred=model.predict(Xtest)
lower,upper=pred-q,pred+q
coverage=np.mean((ytest>=lower)&(ytest<=upper))
print("n calibration",n,"rang",rank,"q",q,"couverture test",coverage,"largeur",2*q)
assert lower.shape==ytest.shape and np.all(lower<=upper)
print("Garantie marginale sous échangeabilité. La couverture de ce test fini peut être inférieure à 90%.")
# %% [exercise]
# Exercice 2 (20 min). Calculer la couverture séparément pour x0<0.5 et x0>=0.5. Quelle garantie manque ?
# %% [solution]
for mask in [Xtest[:,0]<.5,Xtest[:,0]>=.5]:
    print("n",mask.sum(),"couverture",np.mean((ytest[mask]>=lower[mask])&(ytest[mask]<=upper[mask])))
print("La couverture marginale n'implique pas une couverture conditionnelle par groupe.")
# %% [exercise]
# Exercice 3 (15 min). Une importance élevée prouve-t-elle qu'agir sur cette variable améliore la cible ? Donner un contre-exemple.
# %% [solution]
print("Non. Le score mesure une dépendance prédictive du modèle. Une variable peut être un proxy ou une conséquence. Exemple : parapluie et pluie.")
