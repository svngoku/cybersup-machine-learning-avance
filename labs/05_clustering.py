# %% [markdown]
# # TP 05 · Géométrie du clustering
# 150 minutes. Comparer K-means, GMM, DBSCAN et HDBSCAN. Mesurer silhouette, taux de bruit et stabilité.
# Les étiquettes des données synthétiques servent uniquement à l'analyse finale. Un cluster n'est pas une vérité métier.
# Sources : scikit-learn clustering, mixture et decomposition.
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, HDBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score
X, truth = make_moons(n_samples=600,noise=.07,random_state=42)
X = StandardScaler().fit_transform(X)
models = {"K-means": KMeans(2,n_init=10,random_state=42),
          "GMM": GaussianMixture(2,random_state=42),
          "DBSCAN": DBSCAN(eps=.28,min_samples=8),
          "HDBSCAN": HDBSCAN(min_cluster_size=25)}
rows=[]
fig,axs=plt.subplots(1,4,figsize=(14,3))
for ax,(name,model) in zip(axs,models.items()):
    labels=model.fit_predict(X); mask=labels!=-1; k=len(np.unique(labels[mask]))
    sil=silhouette_score(X[mask],labels[mask]) if 1<k<mask.sum() else np.nan
    rows.append([name,k,(~mask).mean(),sil,adjusted_rand_score(truth,labels)])
    ax.scatter(X[:,0],X[:,1],c=labels,s=9,cmap="tab10"); ax.set_title(name)
plt.tight_layout(); plt.show()
print(pd.DataFrame(rows,columns=["méthode","K","bruit","silhouette hors bruit","ARI synthétique"]))
# %% [exercise]
# Exercice 1 (30 min). Faire varier eps de DBSCAN. Toujours rapporter le bruit avec la silhouette. Pourquoi exclure 80% des points pourrait tromper ?
# %% [solution]
for eps in [.12,.2,.28,.4,.7]:
    labels=DBSCAN(eps=eps,min_samples=8).fit_predict(X); mask=labels!=-1; k=len(np.unique(labels[mask]))
    sil=silhouette_score(X[mask],labels[mask]) if 1<k<mask.sum() else np.nan
    print(eps,"clusters",k,"bruit",round((~mask).mean(),3),"silhouette",round(sil,3))
# %% [exercise]
# Exercice 2 (30 min). Mesurer l'accord entre deux K-means sur les mêmes points mais avec deux graines. Cet accord prouve-t-il l'utilité métier ?
# %% [solution]
a=KMeans(2,n_init=1,random_state=1).fit_predict(X)
b=KMeans(2,n_init=1,random_state=8).fit_predict(X)
print("ARI entre partitions",adjusted_rand_score(a,b))
print("La stabilité est nécessaire à l'usage, mais ne prouve ni la vérité ni la pertinence métier.")
# %% [exercise]
# Exercice 3 (35 min). Sur 12 dimensions synthétiques, appliquer PCA après scaling et choisir le nombre d'axes pour 90% de variance. Est-ce une garantie de classification ?
# %% [solution]
Z,_=make_blobs(n_samples=500,n_features=12,centers=4,random_state=42)
Zs=StandardScaler().fit_transform(Z)
pca=PCA(n_components=.9).fit(Zs)
print("Composantes retenues",pca.n_components_,"variance",pca.explained_variance_ratio_.sum())
print("PCA maximise la variance de X, pas l'information sur une cible.")
# %% [exercise]
# Extension (20 min). Réaliser une CAH Ward, puis expliquer la contrainte de distance et le coût mémoire.
# %% [solution]
labels=AgglomerativeClustering(n_clusters=2,linkage="ward").fit_predict(X)
print("ARI Ward",adjusted_rand_score(truth,labels))
print("Ward minimise une augmentation de variance et utilise la distance euclidienne. Réduire ou échantillonner avant de traiter de gros volumes.")
