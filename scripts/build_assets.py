"""Generate chart DATA, not drawings. Slides contain native editable charts."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
import pandas as pd
import qrcode
from sklearn.datasets import make_moons, make_friedman1, make_classification
from sklearn.cluster import KMeans,DBSCAN
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor,HistGradientBoostingRegressor
from sklearn.metrics import roc_curve,precision_recall_curve,root_mean_squared_error
from sklearn.inspection import permutation_importance

ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/"assets";dest.mkdir(exist_ok=True)
data=ROOT/"data";data.mkdir(exist_ok=True)
if not (data/"bank-additional.csv").exists():
    shutil.copy(ROOT/".build/bank-additional.csv",data/"bank-additional.csv")
    shutil.copy(ROOT/".build/bank-additional-names.txt",data/"bank-additional-names.txt")
charts={}
def chart(key,kind,categories,series,xlabel,ylabel,disclosure):
    charts[key]={"type":kind,"categories":[str(x) for x in categories],"series":series,"xlabel":xlabel,"ylabel":ylabel,"disclosure":disclosure}
def series(name,values,x=None):
    d={"name":name,"values":np.asarray(values,dtype=float).round(5).tolist()}
    if x is not None:d["xValues"]=np.asarray(x,dtype=float).round(5).tolist()
    return d
x=np.arange(1,11)
chart("bias","line",x,[series("Biais²",4/x),series("Variance",.055*x*x),series("Erreur totale",4/x+.055*x*x+.5)],"Complexité","Erreur quadratique","Courbes schématiques originales ; erreur = biais² + variance + bruit (0,5).")
n=np.array([50,100,200,400,800,1600])
chart("learning","line",n,[series("Entraînement",[.98,.94,.90,.88,.87,.86]),series("Validation",[.62,.69,.75,.80,.83,.84])],"Taille d'entraînement","Score","Valeurs construites pour expliquer un diagnostic ; aucun résultat de benchmark.")
lam=np.array([0,.25,.5,1,2,4,8])
chart("regularization","line",lam,[series("L2 : 2 / (1+λ)",2/(1+lam)),series("L1 : max(2−λ,0)",np.maximum(2-lam,0))],"λ","Coefficient","Exemple analytique à une variable, norme de x fixée et perte quadratique normalisée.")
m=np.array([1,2,5,10,30,100])
chart("bagging","line",m,[series(f"ρ = {rho}",rho+(1-rho)/m) for rho in [0,.3,.8]],"Nombre d'estimateurs","Variance / σ²","Formule théorique avec variance égale et corrélation commune ρ.")
X,y=make_friedman1(n_samples=600,n_features=10,noise=1.5,random_state=42)
Xt,Xv,yt,yv=train_test_split(X,y,test_size=.3,random_state=42)
gb=GradientBoostingRegressor(n_estimators=120,max_depth=2,random_state=42).fit(Xt,yt)
tr=[root_mean_squared_error(yt,p) for p in gb.staged_predict(Xt)]
va=[root_mean_squared_error(yv,p) for p in gb.staged_predict(Xv)]
idx=np.arange(0,120,5)
chart("boosting","line",idx+1,[series("Train",np.array(tr)[idx]),series("Validation",np.array(va)[idx])],"Nombre d'arbres","RMSE","Expérience synthétique Friedman, n=600, graine 42 ; code dans scripts/build_assets.py.")
A,b=make_classification(n_samples=1400,n_features=10,n_informative=5,weights=[.9,.1],random_state=42)
At,Av,bt,bv=train_test_split(A,b,stratify=b,test_size=.3,random_state=42)
clf=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)).fit(At,bt)
p=clf.predict_proba(Av)[:,1];fpr,tpr,_=roc_curve(bv,p);pr,re,_=precision_recall_curve(bv,p)
def subsample(a,b,limit=60):
    ix=np.unique(np.linspace(0,len(a)-1,min(len(a),limit)).astype(int));return a[ix],b[ix]
fx,ty=subsample(fpr,tpr)
chart("roc","scatter",[],[series("Modèle",ty,fx),series("Aléatoire",fx,fx)],"Taux de faux positifs","Rappel","Validation synthétique (n=420) ; les points de la courbe correspondent à différents seuils.")
rx,py=subsample(re,pr)
chart("pr","scatter",[],[series("Modèle",py,rx),series("Prévalence",np.full(len(rx),bv.mean()),rx)],"Rappel","Précision","Même validation que la ROC ; ligne de référence = prévalence observée. AP et aire trapézoïdale diffèrent.")
th=np.linspace(0,1,21)
cost=[np.sum((p>=t)&(bv==0))+5*np.sum((p<t)&(bv==1)) for t in th]
chart("threshold","line",np.round(th,2),[series("Coût FP + 5 FN",cost)],"Seuil","Coût (unités)","Coûts pédagogiques sur validation synthétique. Le test ne sert pas à choisir le seuil.")
bins=np.linspace(0,1,11)
chart("calibration","scatter",[],[series("Idéal",bins,bins),series("Surconfiant",bins**2,bins)],"Probabilité annoncée","Fréquence positive","Exemple schématique : une prédiction à 0,8 correspond ici à 0,64 observé.")
chart("pca","bar",["PC1","PC2","PC3","PC4","PC5"],[series("Variance expliquée",[.52,.23,.13,.08,.04])],"Composante","Part de variance","Spectre construit pour l'exercice : les 3 premiers axes expliquent 88%, les 4 premiers 96%.")
pts,truth=make_moons(n_samples=180,noise=.07,random_state=42);pts=StandardScaler().fit_transform(pts)
for key,model in [("kmeans",KMeans(2,n_init=10,random_state=42)),("dbscan",DBSCAN(eps=.38,min_samples=5))]:
    labels=model.fit_predict(pts)
    chart(key,"scatter",[],[series("Bruit" if label==-1 else f"Groupe {label+1}",pts[labels==label,1],pts[labels==label,0]) for label in np.unique(labels)],"Variable 1 standardisée","Variable 2 standardisée","Mêmes 180 lunes synthétiques, graine 42. Les couleurs représentent les clusters estimés.")
chart("inertia","line",range(1,8),[series("Inertie",[KMeans(k,n_init=10,random_state=42).fit(pts).inertia_ for k in range(1,8)])],"Nombre de clusters K","Inertie","L'inertie optimale décroît avec K ; cette courbe ne prouve pas le vrai nombre de groupes.")
imp=permutation_importance(gb,Xv,yv,scoring="neg_root_mean_squared_error",n_repeats=5,random_state=42)
chart("importance","bar",[f"x{i}" for i in range(10)],[series("Hausse RMSE",imp.importances_mean)],"Variable permutée","Hausse de RMSE","Friedman synthétique : x0 à x4 sont informatives par construction. Importance sur validation, 5 permutations.")
X0,y0=make_friedman1(n_samples=1000,n_features=10,noise=2,random_state=7)
Xbase,Xtest,ybase,ytest=train_test_split(X0,y0,test_size=.2,random_state=42)
Xtrain,Xcal,ytrain,ycal=train_test_split(Xbase,ybase,test_size=.25,random_state=43)
mod=HistGradientBoostingRegressor(max_iter=100,max_leaf_nodes=15,random_state=42).fit(Xtrain,ytrain)
res=np.sort(np.abs(ycal-mod.predict(Xcal)));q=res[int(np.ceil((len(res)+1)*.9))-1]
pred=mod.predict(Xtest);order=np.argsort(pred)[:40]
chart("conformal","line",range(1,41),[series("Prédiction",pred[order]),series("Borne basse",pred[order]-q),series("Borne haute",pred[order]+q),series("Observé",ytest[order])],"40 observations triées par prédiction","Cible synthétique","Split-conformal 90% : 600 train, 200 calibration, 200 test ; extrait des 40 plus petites prédictions. Couverture marginale, pas individuelle.")
chart("drift","bar",["0–1","1–2","2–3","3–4","4–5"],[series("Référence",[.1,.3,.4,.15,.05]),series("Production",[.05,.15,.3,.3,.2])],"Tranche de feature","Fréquence","Distributions construites : un changement de P(X) ne prouve pas une baisse de performance.")
for key in ["regularization", "learning", "bagging"]:
    c=charts[key]; xs=[float(x) for x in c["categories"]]; c["type"]="scatter"
    for v in c["series"]: v["xValues"]=xs
    c["categories"]=[]
(dest/"chart-data.json").write_text(json.dumps(charts,ensure_ascii=False,indent=2))
qrcode.make("https://github.com/svngoku/cybersup-machine-learning-avance").save(dest/"qr-repository.png")
print(len(charts),"graphiques natifs prêts")
