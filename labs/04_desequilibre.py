# %% [markdown]
# # TP 04 · Déséquilibre, calibration et décision
# 120 minutes. Données numériques synthétiques, environ 8% de positifs. Coûts pédagogiques : FP = 1 unité, FN = 5 unités.
# Comparer pondération et SMOTE dans les plis. Calibrer sur le train par CV. Choisir le seuil sur validation. Ouvrir le test à la fin.
# Sources : imbalanced-learn common_pitfalls ; scikit-learn calibration et classification_threshold.
# %%
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.calibration import CalibratedClassifierCV, CalibrationDisplay
from sklearn.metrics import average_precision_score, confusion_matrix, brier_score_loss
from pathlib import Path
import sys
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "mlcourse.py").exists())
sys.path.insert(0, str(ROOT))
from mlcourse import best_threshold, classification_report
X,y = make_classification(n_samples=2400,n_features=12,n_informative=6,weights=[.92,.08],flip_y=.01,random_state=42)
Xa, Xtest, ya, ytest = train_test_split(X,y,test_size=.2,stratify=y,random_state=42)
Xtr, Xval, ytr, yval = train_test_split(Xa,ya,test_size=.25,stratify=ya,random_state=43)
cv = StratifiedKFold(3,shuffle=True,random_state=42)
models = {"simple": make_pipeline(StandardScaler(),LogisticRegression(max_iter=1500)),
          "pondéré": make_pipeline(StandardScaler(),LogisticRegression(class_weight="balanced",max_iter=1500)),
          "SMOTE": ImbPipeline([("scale",StandardScaler()),("sample",SMOTE(random_state=42)),("model",LogisticRegression(max_iter=1500))])}
scores = {k: cross_val_score(v,Xtr,ytr,cv=cv,scoring="average_precision").mean() for k,v in models.items()}
print(scores)
name = max(scores,key=scores.get)
calibrated = CalibratedClassifierCV(models[name],method="sigmoid",cv=cv).fit(Xtr,ytr)
pval = calibrated.predict_proba(Xval)[:,1]
threshold = best_threshold(yval,pval,cost_fp=1,cost_fn=5)
print("Modèle",name,"seuil validation",threshold)
# %% [exercise]
# Exercice 1 (20 min). Comparer la calibration avant/après sur validation. Une meilleure AP garantit-elle un meilleur Brier ?
# %% [solution]
import matplotlib.pyplot as plt
uncalibrated = models[name].fit(Xtr,ytr)
praw = uncalibrated.predict_proba(Xval)[:,1]
CalibrationDisplay.from_predictions(yval,praw,n_bins=6,name="brut")
CalibrationDisplay.from_predictions(yval,pval,n_bins=6,name="calibré",ax=plt.gca()); plt.show()
print("Brier brut/calibré", brier_score_loss(yval,praw),brier_score_loss(yval,pval))
print("Le classement et la qualité des probabilités sont deux propriétés distinctes.")
# %% [exercise]
# Exercice 2 (20 min). Seuil figé : évaluer une seule fois sur test et comparer au seuil 0.5 sans le retoucher. Calculer les deux coûts.
# %% [solution]
ptest = calibrated.predict_proba(Xtest)[:,1]
reports = [classification_report(ytest,ptest,t) for t in [0.5,threshold]]
for r in reports:
    r["coût unités"] = r["FP"] + 5*r["FN"]
print(pd.DataFrame(reports).to_string(index=False))
assert len(ptest) == len(ytest) and np.all((ptest >= 0) & (ptest <= 1))
# %% [exercise]
# Exercice 3 (15 min). Pourquoi ne pas interpoler directement les colonnes one-hot de catégories ? Proposer une solution aux données mixtes.
# %% [solution]
print("Des catégories fractionnaires n'ont pas toujours de sens. Comparer d'abord pondération et seuil, puis SMOTENC avec colonnes et distances adaptées.")
