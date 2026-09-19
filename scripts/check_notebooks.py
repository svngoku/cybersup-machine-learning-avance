"""Execute each notebook from a fresh kernel, with bounded CPU parallelism."""
from pathlib import Path
import argparse,json,os,time
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument("--version",default="corriges",choices=["corriges","etudiants"])
args=parser.parse_args()
for var in ["OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"]:os.environ[var]="2"
out=ROOT/".build/executed"/args.version;out.mkdir(parents=True,exist_ok=True)
report=[]
for f in sorted((ROOT/"notebooks"/args.version).glob("*.ipynb")):
    start=time.monotonic();nb=nbformat.read(f,as_version=4)
    NotebookClient(nb,timeout=240,kernel_name="python3",resources={"metadata":{"path":str(ROOT)}}).execute()
    nbformat.write(nb,out/f.name)
    errors=[o for c in nb.cells if c.cell_type=="code" for o in c.outputs if o.output_type=="error"]
    assert not errors
    report.append({"notebook":str(f.relative_to(ROOT)),"seconds":round(time.monotonic()-start,2),"errors":0})
    print(report[-1],flush=True)
(out/"report.json").write_text(json.dumps(report,indent=2))
