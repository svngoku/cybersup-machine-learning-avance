"""Build standalone Colab notebooks; never depend on the private repository at runtime."""
from pathlib import Path
import hashlib
import json
import re
import nbformat

ROOT = Path(__file__).resolve().parents[1]
COMMON = {"numpy": "2.5.3", "pandas": "3.0.6", "scipy": "1.18.1",
          "scikit-learn": "1.9.1", "matplotlib": "3.11.2"}
LABS = {"02_ensembles": {}, "03_optimisation": {"optuna": "4.9.0"},
        "06_interpretation": {}, "08_xgboost_colab": {"xgboost": "3.1.3"}}

for name, extra in LABS.items():
    source = ROOT / "labs" / ("colab" if name.startswith("08") else "") / (name + ".py")
    parts = re.split(r"^# %%(?: \[([^\]]+)\])?\s*$", source.read_text(), flags=re.M)
    demo = name.startswith("08")
    versions = ["demonstrations"] if demo else ["etudiants", "corriges"]
    for version in versions:
        title = ("Démonstration guidée" if demo else "TP · " + version) + " · Google Colab"
        intro = f"""# {title}

Cybersup · Machine Learning Avancé · **Chrys Fé-Marty NIONGOLO** · septembre 2026

Ce notebook est autonome : aucun clonage, jeton GitHub ou fichier du dépôt n'est nécessaire.
Dans Colab : **Fichier → Importer le notebook**, puis exécuter la cellule d'installation
dans une nouvelle session avant les autres cellules. Python 3.12 ou ultérieur requis.
Si Colab demande de redémarrer la session après installation, accepter puis reprendre
depuis le début. Enregistrer une copie du notebook et télécharger ses sorties avant de quitter.

{'CPU par défaut ; GPU NVIDIA facultatif pour XGBoost (détection automatique et repli CPU).' if demo else 'Le CPU suffit. Ces estimateurs scikit-learn ne deviennent pas des modèles GPU en sélectionnant un accélérateur.'}
Internet est nécessaire pour installer les bibliothèques{' et télécharger le jeu public UCI' if demo else '; les données sont synthétiques'}.
Les ressources Colab ne sont pas garanties : [FAQ officielle](https://research.google.com/colaboratory/faq.html).
Les versions ci-dessous sont celles du cours, pas une recommandation de toujours installer les dernières.
"""
        requirements = COMMON | extra
        bootstrap = f'''# Exécuter en premier, dans une session neuve.
import os, sys, subprocess
from importlib.metadata import version as package_version
if sys.version_info < (3, 12):
    raise RuntimeError("Choisir un runtime Python >= 3.12, ou utiliser le pack local Python 3.12.")
required = {requirements!r}
if os.environ.get("CYBERSUP_SKIP_INSTALL") != "1":
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", *[f"{{k}}=={{v}}" for k, v in required.items()]])
for key, expected in required.items():
    assert package_version(key) == expected, f"Version incorrecte : {{key}}. Reprendre dans une session neuve."
for key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"]:
    os.environ[key] = "2"
print("Python", sys.version.split()[0], "· dépendances", {{k: package_version(k) for k in required}})
'''
        cells = [nbformat.v4.new_markdown_cell(intro),
                 nbformat.v4.new_code_cell(bootstrap, metadata={"tags": ["installation"]})]
        for i in range(1, len(parts), 2):
            kind, body = parts[i] or "code", parts[i + 1].strip()
            if kind in ["markdown", "exercise"]:
                body = re.sub(r"^# ?", "", body, flags=re.M)
                cells.append(nbformat.v4.new_markdown_cell(body))
            else:
                if kind == "solution" and version == "etudiants":
                    body = "# Votre réponse / votre code ici.\n# Les exemples guidés restent exécutables."
                cell = nbformat.v4.new_code_cell(body)
                if kind == "solution":
                    cell.metadata["tags"] = ["solution" if version == "corriges" else "exercice"]
                cells.append(cell)
        if name == "02_ensembles":
            cells[2].source += "\n\nPendant la séance : 70 min de TP + 20 min de démonstration 08 XGBoost. Le stacking est une extension après le cours si nécessaire."
        for i, cell in enumerate(cells):
            cell.id = hashlib.sha256(f"{name}:{version}:{i}".encode()).hexdigest()[:12]
        nb = nbformat.v4.new_notebook(cells=cells, metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "colab": {"name": name + ".ipynb", "provenance": []},
            "authors": [{"name": "Chrys Fé-Marty NIONGOLO"}],
            "cybersup": {"source": str(source.relative_to(ROOT)), "requirements": requirements,
                         "version": version, "standalone": True}
        })
        nbformat.validate(nb)
        dest = ROOT / "notebooks/colab" / version / (name + ".ipynb")
        dest.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(nb, dest)
        print(dest.relative_to(ROOT))
