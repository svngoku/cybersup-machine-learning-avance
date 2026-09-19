"""Execute every standalone notebook from an empty folder, without repository access."""
from pathlib import Path
import argparse
import json
import os
import tempfile
import time
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--skip-install", action="store_true", help="Use the uv-locked environment; bootstrap still checks exact versions.")
args = parser.parse_args()
os.environ["CYBERSUP_SKIP_INSTALL"] = "1" if args.skip_install else "0"
os.environ["CYBERSUP_XGB_DEVICE"] = "cpu"
for name in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"]:
    os.environ[name] = "2"
out = ROOT / ".build/executed/colab"
out.mkdir(parents=True, exist_ok=True)
notebooks = sorted((ROOT / "notebooks/colab").glob("*/*.ipynb"))
assert len(notebooks) == 7
report = []
for source in notebooks:
    nb = nbformat.read(source, as_version=4)
    nbformat.validate(nb)
    assert nb.metadata.cybersup.standalone
    if source.parent.name == "etudiants":
        assert all("solution" not in c.get("metadata", {}).get("tags", []) for c in nb.cells)
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="cybersup-colab-") as directory:
        NotebookClient(nb, timeout=600, kernel_name="python3",
                       resources={"metadata": {"path": directory}}).execute()
        manifest_path = Path(directory) / "results/colab08/manifest.json"
        if source.name.startswith("08"):
            manifest = json.loads(manifest_path.read_text())
            assert manifest["n_rows"] == 41188 and manifest["used_device"] == "cpu"
            assert set(manifest["excluded_features"]) == {"duration", "campaign"}
            assert len(manifest["features"]) == 18
            assert manifest["split"]["train_end_exclusive"] < manifest["split"]["validation_end_exclusive"] < 41188
            assert 0 <= manifest["test_metrics"]["average_precision"] <= 1
            (out / "demo-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    dest = out / source.parent.name / source.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, dest)
    row = {"notebook": str(source.relative_to(ROOT)), "seconds": round(time.monotonic() - started, 2),
           "errors": 0, "working_directory": "temporary empty folder", "device": "cpu",
           "installation": "version assertions only" if args.skip_install else "pip executed"}
    report.append(row)
    print(row, flush=True)
(out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
