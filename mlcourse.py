"""Small, explicit helpers used by the course notebooks. No network at import."""
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import (average_precision_score, roc_auc_score,
    precision_score, recall_score, f1_score, brier_score_loss, confusion_matrix)

ROOT = Path(__file__).resolve().parent
SEED = 42
BANK_SHA256 = "7e59cf650004d65d1c9d6b08553bad2ee9a9ad70d594f536e3c584ee6ed5df50"

def load_bank():
    """Official random 10% subset, 4,119 rows. duration excluded before prediction."""
    path = ROOT / "data/bank-additional.csv"
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != BANK_SHA256:
        raise ValueError("Dataset checksum differs from the documented UCI source")
    df = pd.read_csv(path, sep=";")
    assert df.shape == (4119, 21)
    y = df["y"].eq("yes").astype(int)
    X = df.drop(columns=["y", "duration"]).replace("unknown", np.nan)
    return X, y

def split_bank():
    X, y = load_bank()
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)

def preprocessor():
    numeric = Pipeline([("impute", SimpleImputer(strategy="median", add_indicator=True)),
                        ("scale", StandardScaler())])
    categorical = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                            ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
    return ColumnTransformer([
        ("num", numeric, make_column_selector(dtype_include=np.number)),
        ("cat", categorical, make_column_selector(dtype_exclude=np.number)),
    ], verbose_feature_names_out=False)

def bank_pipeline(model):
    return Pipeline([("prepare", preprocessor()), ("model", model)])

def cv3(seed=SEED):
    return StratifiedKFold(n_splits=3, shuffle=True, random_state=seed)

def classification_report(y, probability, threshold=0.5):
    prediction = np.asarray(probability) >= threshold
    tn, fp, fn, tp = confusion_matrix(y, prediction, labels=[0, 1]).ravel()
    return {"AP": average_precision_score(y, probability),
            "ROC_AUC": roc_auc_score(y, probability),
            "precision": precision_score(y, prediction, zero_division=0),
            "recall": recall_score(y, prediction, zero_division=0),
            "F1": f1_score(y, prediction, zero_division=0),
            "Brier": brier_score_loss(y, probability),
            "threshold": float(threshold), "TN": int(tn), "FP": int(fp),
            "FN": int(fn), "TP": int(tp)}

def best_threshold(y, probability, cost_fp=1.0, cost_fn=5.0):
    """Minimize an explicit illustrative cost on validation data, never test data."""
    p = np.asarray(probability)
    candidates = np.r_[0.0, np.unique(p), np.nextafter(1.0, 2.0)]
    costs = [cost_fp * np.sum((p >= t) & (np.asarray(y) == 0))
             + cost_fn * np.sum((p < t) & (np.asarray(y) == 1)) for t in candidates]
    return float(candidates[int(np.argmin(costs))])
