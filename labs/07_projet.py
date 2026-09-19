# %% [markdown]
# # Projet final · Prioriser une campagne d'appels
# 180 minutes. Lire `evaluation/PROJET.md` avant d'ouvrir ce corrigé.
# Pipeline, baseline, sélection par CV sur le train, seuil validation, test fermé puis une évaluation finale.
# Coûts illustratifs FP=1/FN=5 : ils ne décrivent pas la rentabilité réelle d'une banque.
# Ne pas confondre propension à souscrire et effet causal d'un appel. Aucune décision réelle n'est autorisée par cet exercice.
# %%
from pathlib import Path
import sys,json
ROOT=next(p for p in [Path.cwd(),*Path.cwd().parents] if (p/"mlcourse.py").exists())
sys.path.insert(0,str(ROOT))
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.calibration import CalibratedClassifierCV
from mlcourse import split_bank,bank_pipeline,cv3,best_threshold,classification_report,SEED
Xdev,Xtest,ydev,ytest=split_bank()
Xtr,Xval,ytr,yval=train_test_split(Xdev,ydev,test_size=.25,stratify=ydev,random_state=43)
assert set(Xtr.index).isdisjoint(Xval.index)
assert set(Xdev.index).isdisjoint(Xtest.index)
models={"baseline":bank_pipeline(DummyClassifier(strategy="prior")),
        "logistique":bank_pipeline(LogisticRegression(max_iter=2000,C=.1)),
        "boosting":bank_pipeline(HistGradientBoostingClassifier(max_iter=100,max_leaf_nodes=15,l2_regularization=1,random_state=42))}
# %% [exercise]
# Étape 1 (45 min). Comparer les modèles par AP sur trois plis. Justifier la métrique et enregistrer toutes les configurations, pas seulement le gagnant.
# %% [solution]
cv_scores={name:cross_val_score(model,Xtr,ytr,cv=cv3(),scoring="average_precision") for name,model in models.items()}
print(pd.DataFrame({name:values for name,values in cv_scores.items()}))
winner=max(cv_scores,key=lambda k:cv_scores[k].mean())
print("Famille choisie",winner)
# %% [exercise]
# Étape 2 (45 min). Dans le corrigé, la suite utilise son propre choix pour rester exécutable indépendamment. Calibrer uniquement sur train. Figer le seuil sur validation et expliquer ce qu'implique un changement de prévalence.
# %% [solution]
scores_for_selection={k:cross_val_score(v,Xtr,ytr,cv=cv3(),scoring="average_precision").mean() for k,v in models.items()}
chosen=max(scores_for_selection,key=scores_for_selection.get)
final_model=CalibratedClassifierCV(models[chosen],method="sigmoid",cv=cv3()).fit(Xtr,ytr)
pval=final_model.predict_proba(Xval)[:,1]
fixed_threshold=best_threshold(yval,pval,1,5)
print("Choix figés",chosen,fixed_threshold)
# %% [exercise]
# Étape 3 (45 min). Évaluer une seule fois le modèle figé. Pour rendre cette étape autonome, elle reconstruit le protocole sans utiliser le test pour aucun choix. Exporter modèle, manifeste et limite d'usage.
# %% [solution]
selection={k:cross_val_score(v,Xtr,ytr,cv=cv3(),scoring="average_precision").mean() for k,v in models.items()}
choice=max(selection,key=selection.get)
frozen_model=CalibratedClassifierCV(models[choice],method="sigmoid",cv=cv3()).fit(Xtr,ytr)
frozen_threshold=best_threshold(yval,frozen_model.predict_proba(Xval)[:,1],1,5)
ptest=frozen_model.predict_proba(Xtest)[:,1]
report=classification_report(ytest,ptest,frozen_threshold)
report["cost_units"]=report["FP"]+5*report["FN"]
report["n_test"]=len(ytest)
print(json.dumps(report,indent=2))
out=ROOT/"results/projet";out.mkdir(parents=True,exist_ok=True)
joblib.dump({"model":frozen_model,"threshold":frozen_threshold},out/"modele.joblib")
manifest={"dataset":"UCI bank-additional.csv", "random_state":SEED,"model":choice,
          "test_report":report,"limits":["Historical sample","No causal claim","No independent future-time validation","No person identifier"]}
(out/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
restored=joblib.load(out/"modele.joblib")  # Only the artifact just produced locally is trusted.
np.testing.assert_allclose(restored["model"].predict_proba(Xtest.iloc[:8]),frozen_model.predict_proba(Xtest.iloc[:8]))
# %% [exercise]
# Étape 4 (45 min). Compléter une model card et présenter une recommandation en 5 minutes. Lire le barème : le score brut ne suffit pas.
# %% [solution]
print("Usage : priorisation expérimentale. Limites : historique 2008-2010, contacts répétés non identifiables, pas de gain causal, pas de validation future. Prochain test : blocs temporels sur le fichier complet et validation métier.")
