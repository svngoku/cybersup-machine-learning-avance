# %% [markdown]
# # Démonstration 08 · XGBoost, données réelles et GPU facultatif
# **20 minutes d'animation** : protocole (5), exécution et courbes (8), critique (7).
# Bank Marketing, 41 188 lignes : assez pour montrer un pipeline plus complet, mais pas du big data.
# Ce notebook est une démonstration intégralement résolue, sans exercice évalué.
#
# **Question** : classer les contacts selon leur probabilité historique de souscription.
# La validation choisit entre une logistique et un boosting ; un test chronologique reste réservé.
# Les scores ne mesurent ni l'effet causal des appels ni la performance d'une campagne future.
#
# Sources : [UCI Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing),
# Moro, Rita et Cortez (2014), DOI 10.24432/C5K306, **CC BY 4.0** ;
# [XGBoost GPU, documentation de la branche 3.1](https://xgboost.readthedocs.io/en/release_3.1.0/gpu/index.html).
# XGBoost **3.1.3** est figé pour ce cours ; sa branche GPU demande CUDA >= 12.0.
# Le choix vise la compatibilité, il ne prétend pas être la dernière version publiée.
# %%
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import hashlib
import json
import os
import platform
import shutil
import subprocess
import time
from importlib.metadata import version
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score, log_loss, PrecisionRecallDisplay

SEED = 42
THREADS = 2
# "auto", "cpu" ou "cuda". La vérification automatisée impose CPU.
REQUESTED_DEVICE = os.environ.get("CYBERSUP_XGB_DEVICE", "auto")
assert REQUESTED_DEVICE in {"auto", "cpu", "cuda"}
gpu_info = "Aucun GPU NVIDIA détecté"
if shutil.which("nvidia-smi"):
    try:
        probe = subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
                               text=True, capture_output=True, timeout=15)
        if probe.returncode == 0 and probe.stdout.strip():
            gpu_info = probe.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
cuda_available = bool(xgb.build_info().get("USE_CUDA")) and gpu_info != "Aucun GPU NVIDIA détecté"
device = "cuda" if REQUESTED_DEVICE != "cpu" and cuda_available else "cpu"
print("Matériel :", gpu_info, "| périphérique retenu :", device)
print("Choisir un GPU dans Colab ne garantit ni sa disponibilité ni une accélération sur ce jeu.")
# %% [markdown]
# ## 1 · Télécharger et vérifier la provenance
# Le fichier complet est ordonné dans le temps (mai 2008–novembre 2010 selon la source).
# On conserve exactement les octets téléchargés et leur empreinte. En cas d'indisponibilité
# d'UCI, le formateur peut fournir le CSV original dans `data/`, avec la même empreinte.
# %%
DATA_URL = "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip"
DATA_SHA256 = "74adfc578bf77a7ff4bb1ba4a9f8709d9e3c6907342959c2c8416847e0afb4d8"
csv_path = Path("data/bank-additional-full.csv")
if not csv_path.exists():
    with urlopen(DATA_URL, timeout=90) as response:
        archive_bytes = response.read()
    with ZipFile(BytesIO(archive_bytes)) as outer:
        inner_bytes = outer.read("bank-additional.zip")
    with ZipFile(BytesIO(inner_bytes)) as inner:
        csv_bytes = inner.read("bank-additional/bank-additional-full.csv")
    assert hashlib.sha256(csv_bytes).hexdigest() == DATA_SHA256, "Source modifiée : interrompre et vérifier."
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.write_bytes(csv_bytes)
assert hashlib.sha256(csv_path.read_bytes()).hexdigest() == DATA_SHA256
df = pd.read_csv(csv_path, sep=";")
assert df.shape == (41188, 21) and set(df["y"].unique()) == {"no", "yes"}
print(df.shape, "· SHA-256 vérifié · cible positive", round((df.y == "yes").mean(), 4))
# %% [markdown]
# ## 2 · Définir l'instant de décision et les trois périodes
# `duration` est inconnue avant la fin de l'appel. `campaign`, nombre de contacts de la
# campagne incluant le contact courant, est aussi retirée pour ce scénario avant premier contact.
# Il reste **18 entrées**. Les autres variables exigeraient encore un audit de disponibilité réelle.
# Les modalités `unknown` deviennent des valeurs manquantes dans les features.
#
# Les premières 60 % des lignes servent au train, les 20 % suivantes à la validation et les
# dernières 20 % au test. Aucun mélange aléatoire. Sans identifiant client ni horodatage complet,
# ceci ne garantit pas l'absence de clients répétés entre périodes. La prévalence peut changer.
# %%
X = df.drop(columns=["y", "duration", "campaign"]).replace("unknown", np.nan)
y = (df["y"] == "yes").astype(int)
n = len(df)
a, b = int(n * 0.6), int(n * 0.8)
X_train, X_val, X_test = X.iloc[:a], X.iloc[a:b], X.iloc[b:]
y_train, y_val, y_test = y.iloc[:a], y.iloc[a:b], y.iloc[b:]
assert X.shape[1] == 18 and X_train.index.max() < X_val.index.min() < X_test.index.min()
assert len(X_train) + len(X_val) + len(X_test) == n
# Ne pas consulter la cible test avant que le choix soit figé.
split_view = pd.DataFrame({"partition": ["train", "validation", "test réservé"],
                          "lignes": [len(X_train), len(X_val), len(X_test)],
                          "prévalence connue": [y_train.mean(), y_val.mean(), np.nan]})
print(split_view.to_string(index=False))
split_view.plot.bar(x="partition", y="lignes", legend=False, color=["#303C8B", "#FF7900", "#A0A6B4"])
plt.ylabel("Nombre de lignes dans l'ordre source"); plt.tight_layout(); plt.show()
# %% [markdown]
# ## 3 · Apprendre les transformations sur le train uniquement
# Médiane et indicateurs de manque pour les numériques ; modalité fréquente et one-hot pour
# les catégories. Le scaler aide la logistique. Les catégories futures absentes du train sont
# ignorées par l'encodeur. Un tel choix exige aussi une surveillance lors d'un usage réel.
# %%
numeric = X_train.select_dtypes(include="number").columns.tolist()
categorical = [c for c in X_train if c not in numeric]
preprocessor = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler()), numeric),
    ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"),
                          OneHotEncoder(handle_unknown="ignore", sparse_output=False)), categorical)
])
Z_train = preprocessor.fit_transform(X_train).astype(np.float32)
Z_val = preprocessor.transform(X_val).astype(np.float32)
print("Matrice train", Z_train.shape, "·", round(Z_train.nbytes / 1024**2, 1), "MiB")
# %% [markdown]
# ## 4 · Baseline puis boosting régularisé
# Budget maximal : 600 arbres, profondeur 4, learning rate 0,05, deux threads CPU.
# L'early stopping sur la log-loss de validation arrête après 30 tours sans progrès.
# Les hyperparamètres sont fixés avant le test. Les deux candidats sont ensuite comparés
# par average precision sur validation. Cette réutilisation rend le score de validation optimiste.
# %%
def build_booster(target_device):
    return xgb.XGBClassifier(n_estimators=600, max_depth=4, learning_rate=0.05,
        min_child_weight=5, subsample=0.8, colsample_bytree=0.8, reg_lambda=5,
        tree_method="hist", device=target_device, eval_metric="logloss",
        early_stopping_rounds=30, random_state=SEED, n_jobs=THREADS)

start = time.perf_counter()
baseline = LogisticRegression(C=1, max_iter=2000).fit(Z_train, y_train)
baseline_seconds = time.perf_counter() - start
booster = build_booster(device)
start = time.perf_counter()
try:
    booster.fit(Z_train, y_train, eval_set=[(Z_train, y_train), (Z_val, y_val)], verbose=False)
except xgb.core.XGBoostError:
    if device == "cpu":
        raise
    print("CUDA indisponible ou incompatible au démarrage : reprise complète sur CPU.")
    device = "cpu"
    booster = build_booster(device)
    start = time.perf_counter()
    booster.fit(Z_train, y_train, eval_set=[(Z_train, y_train), (Z_val, y_val)], verbose=False)
booster_seconds = time.perf_counter() - start
# Lire le périphérique effectivement retenu, y compris un repli interne de XGBoost.
device = json.loads(booster.get_booster().save_config())["learner"]["generic_param"]["device"]
candidates = {"Logistique": baseline, "XGBoost": booster}
validation = pd.DataFrame([
    {"modèle": name, "AP validation": average_precision_score(y_val, model.predict_proba(Z_val)[:, 1]),
     "secondes fit": baseline_seconds if name == "Logistique" else booster_seconds}
    for name, model in candidates.items()
]).set_index("modèle")
print(validation)
selected_name = validation["AP validation"].idxmax()
selected_model = candidates[selected_name]
print("Choix figé :", selected_name, "· XGBoost meilleur tour (base 1) :", booster.best_iteration + 1)
history = booster.evals_result()
plt.plot(history["validation_0"]["logloss"], label="train")
plt.plot(history["validation_1"]["logloss"], label="validation")
plt.axvline(booster.best_iteration, color="black", linestyle="--", label="meilleur tour")
plt.xlabel("Tour de boosting (base 0)"); plt.ylabel("Log-loss"); plt.legend(); plt.tight_layout(); plt.show()
# %% [markdown]
# ## 5 · Une seule évaluation finale du modèle retenu
# Le code utilise les prédictions du gagnant uniquement. Le test ne sert ni à revenir sur le
# modèle ni à choisir un seuil. AP et ROC-AUC évaluent un classement ; la log-loss évalue les
# probabilités. La droite de prévalence est un repère de précision sans information.
# En cas de résultat décevant, documenter la limite ; tout nouveau réglage réclame un nouveau test.
# %%
Z_test = preprocessor.transform(X_test).astype(np.float32)
p_test = selected_model.predict_proba(Z_test)[:, 1]
test_metrics = {"average_precision": float(average_precision_score(y_test, p_test)),
                "roc_auc": float(roc_auc_score(y_test, p_test)),
                "log_loss": float(log_loss(y_test, p_test)),
                "prevalence": float(y_test.mean())}
print("Résultats test ·", selected_name, test_metrics)
PrecisionRecallDisplay.from_predictions(y_test, p_test, name=selected_name)
plt.axhline(y_test.mean(), color="#FF7900", linestyle="--", label="prévalence test")
plt.title("Test chronologique : lire la courbe avec la prévalence")
plt.legend(); plt.tight_layout(); plt.show()
# %% [markdown]
# ## 6 · Sauvegarder les preuves et discuter les limites
# Le manifeste conserve l'empreinte, les splits, les versions, les réglages et le matériel.
# Le modèle XGBoost est exporté en JSON pour montrer la persistance, même si la baseline gagne.
# Ce fichier seul n'est pas un service déployable : il manque notamment le contrat et le
# prétraitement persisté. Il ne faut pas confondre la démonstration et un artefact de production.
# Dans le panneau Fichiers de Colab, télécharger `results/colab08/` avant de quitter.
# %%
out = Path("results/colab08")
out.mkdir(parents=True, exist_ok=True)
validation.to_csv(out / "validation.csv")
booster.save_model(out / "xgboost-demonstration.json")
manifest = {"author": "Chrys Fé-Marty NIONGOLO", "dataset_url": DATA_URL,
    "dataset_sha256": DATA_SHA256, "n_rows": n, "excluded_features": ["duration", "campaign"],
    "features": X.columns.tolist(), "transformed_features": preprocessor.get_feature_names_out().tolist(),
    "split": {"method": "ordre chronologique source, sans shuffle", "train_end_exclusive": a,
              "validation_end_exclusive": b, "test_end_exclusive": n},
    "seed": SEED, "requested_device": REQUESTED_DEVICE, "used_device": device, "gpu": gpu_info,
    "python": platform.python_version(), "platform": platform.platform(),
    "versions": {p: version(p) for p in ["numpy", "pandas", "scipy", "scikit-learn", "xgboost", "matplotlib"]},
    "selected_model": selected_name, "selection_metric": "AP validation", "test_metrics": test_metrics,
    "xgboost_params": {k: v for k, v in booster.get_params().items() if v is not None and not (isinstance(v, float) and np.isnan(v))}, "xgboost_best_iteration_zero_based": int(booster.best_iteration),
    "limitations": ["données 2008–2010", "identifiant client absent", "disponibilité des variables à auditer",
                    "pas de conclusion causale", "export XGBoost sans prétraitement persistant"]}
(out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, default=str, allow_nan=False), encoding="utf-8")
print("À télécharger :", *[str(p) for p in sorted(out.iterdir())], sep="\n")
# %% [markdown]
# ## Discussion à l'oral
# 1. Le jeu complet change-t-il seulement le temps de calcul, ou aussi le protocole d'évaluation ?
# 2. Pourquoi un GPU peut-il être plus lent sur un petit tableau ? Inclure transferts et initialisation.
# 3. Que faudrait-il conserver avant de comparer CPU et GPU : mêmes données, réglages, versions, mesure du coût total ?
# 4. Pourquoi ne pas retenir automatiquement le modèle le plus complexe ?
# 5. Plusieurs machines seraient-elles utiles ici ? Le volume tient en mémoire ; commencer par mesurer.
