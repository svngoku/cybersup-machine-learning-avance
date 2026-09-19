"""Convert the transparent percent-format lab sources to student/solution notebooks."""
from pathlib import Path
import re
import nbformat

ROOT=Path(__file__).resolve().parents[1]
for source in sorted((ROOT/"labs").glob("*.py")):
    parts=re.split(r"^# %%(?: \[([^\]]+)\])?\s*$",source.read_text(),flags=re.M)
    for version in ["etudiants","corriges"]:
        cells=[]
        for i in range(1,len(parts),2):
            kind=parts[i] or "code"; body=parts[i+1].strip()
            if kind in ["markdown","exercise"]:
                body=re.sub(r"^# ?","",body,flags=re.M)
                cells.append(nbformat.v4.new_markdown_cell(body))
            else:
                if kind=="solution" and version=="etudiants":
                    body="# Votre réponse / votre code ici.\n# Les cellules d'exemple au-dessus restent exécutables."
                cell=nbformat.v4.new_code_cell(body)
                if kind=="solution":cell.metadata["tags"]=["solution" if version=="corriges" else "exercice"]
                cells.append(cell)
        nb=nbformat.v4.new_notebook(cells=cells)
        nb.metadata["kernelspec"]={"display_name":"Python 3","language":"python","name":"python3"}
        nb.metadata["language_info"]={"name":"python","version":"3.12"}
        nb.metadata["authors"]=[{"name":"Chrys Fé-Marty NIONGOLO"}]
        dest=ROOT/"notebooks"/version/source.with_suffix(".ipynb").name
        dest.parent.mkdir(parents=True,exist_ok=True);nbformat.write(nb,dest)
        nbformat.validate(nb)
        print(dest.relative_to(ROOT))
