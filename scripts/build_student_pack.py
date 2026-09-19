"""Package only teaching material intended for students; no solutions or notes."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "output/CYBERSUP-ML-Avance-Pack-Etudiant.zip"
PREFIX = "CYBERSUP-ML-Avance-Etudiant/"
files = [".python-version", "pyproject.toml", "uv.lock", "requirements.txt", "mlcourse.py",
         "output/CYBERSUP-Machine-Learning-Avance-2026.pdf",
         "docs/PROGRAMME_35H.md", "docs/ATELIER_FEATURES.md",
         "evaluation/QUIZ.md", "evaluation/PROJET.md", "evaluation/MODEL_CARD.md",
         "resources/RESSOURCES.md", "resources/sources.json", "resources/PROVENANCE.md",
         "data/README.md", "data/bank-additional.csv", "data/bank-additional-names.txt",
         "assets/chart-data.json"]
files += [p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "notebooks/etudiants").glob("*.ipynb"))]
readme = """# Machine Learning Avancé · Pack étudiant

Cybersup · M2 Data / IA · 21–25 septembre 2026 · 35 heures
Formateur : **Chrys Fé-Marty NIONGOLO**

## Démarrage

1. Décompresser toute cette archive dans un dossier local.
2. Installer uv : https://docs.astral.sh/uv/getting-started/installation/
3. Ouvrir un terminal dans ce dossier et exécuter `uv sync --frozen`.
4. Lancer `uv run jupyter lab` et ouvrir `notebooks/etudiants/00_demarrage.ipynb`.

Python 3.12, CPU. Internet est nécessaire pour installer les dépendances.
Les données obligatoires sont incluses. Sans uv : créer un environnement Python
3.12, puis `python -m pip install -r requirements.txt` et `python -m jupyter lab`.

## Parcours

- Support à projeter : [PDF](output/CYBERSUP-Machine-Learning-Avance-2026.pdf).
- [Programme](docs/PROGRAMME_35H.md) et [atelier features](docs/ATELIER_FEATURES.md).
- Huit notebooks guidés dans `notebooks/etudiants/`, de 00 à 07.
- [Quiz](evaluation/QUIZ.md), [projet](evaluation/PROJET.md), [model card](evaluation/MODEL_CARD.md).
- [Bibliographie](resources/RESSOURCES.md) et [provenance des données](data/README.md).

Les cellules d'exercice restent à compléter. Les exemples guidés peuvent être
exécutés en l'état. Les corrigés et les notes du formateur ne sont pas inclus.
Les modèles et exports des TP sont écrits dans `results/`.

Le dépôt GitHub est privé : son accès nécessite une invitation du formateur.
Cette archive fonctionne sans accès au dépôt.
https://github.com/svngoku/cybersup-machine-learning-avance

Les données UCI sont sous CC BY 4.0 ; cette licence ne s'étend pas au template,
aux logos ou aux ressources de tiers. Voir [provenance](resources/PROVENANCE.md).
"""
with ZipFile(DEST, "w", ZIP_DEFLATED) as archive:
    archive.writestr(PREFIX + "README.md", readme)
    for name in files:
        assert "corrig" not in name.lower() and not name.endswith(".pptx")
        source = ROOT / name
        if name == "docs/ATELIER_FEATURES.md":
            text = source.read_text().replace("Corrigé réservé au formateur dans `ATELIER_FEATURES_CORRIGE.md`.", "Correction remise par le formateur.")
            archive.writestr(PREFIX + name, text)
        else:
            archive.write(source, PREFIX + name)
with ZipFile(DEST) as archive:
    assert archive.testzip() is None
    assert len([n for n in archive.namelist() if n.endswith(".ipynb")]) == 8
print(f"Pack étudiant : {len(files) + 1} fichiers ; {DEST.stat().st_size:,} octets")
