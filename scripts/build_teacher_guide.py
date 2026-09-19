"""Regenerate teacher notes from the validated deck manifest."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
slides = json.loads((ROOT / ".build/slide-manifest.json").read_text())
refs = json.loads((ROOT / "resources/sources.json").read_text())
charts = json.loads((ROOT / "assets/chart-data.json").read_text())
lines = ["# Guide formateur · Machine Learning Avancé", "",
         "**Chrys Fé-Marty NIONGOLO · Cybersup · 21–25 septembre 2026 · 35 h**", "",
         "Notes du PowerPoint. Corrigés réservés au formateur. Voir [Colab](COLAB.md) et les [notes orales Ray](NOTES_ORALES_RAY.md).", ""]
for i, slide in enumerate(slides, 1):
    lines += [f"## Diapositive {i} · {slide['title']}", "", slide['notes'].strip(), ""]
    if slide.get('takeaway'):
        lines += ["À retenir : " + slide['takeaway'], ""]
    if slide.get('chart'):
        lines += [charts[slide['chart']]['disclosure'], ""]
    for ref in slide['refs']:
        r = refs[ref]
        label = f"{ref} · {r['title']} — {r['author']}, {r['date']}"
        lines.append(f"- [{label}]({r['url']})" if r['url'].startswith('http') else f"- {label}. {r['url']}")
    if slide['refs']:
        lines.append("")
(ROOT / 'docs/GUIDE_FORMATEUR.md').write_text('\n'.join(lines), encoding='utf-8')
print(f"Guide : {len(slides)} diapositives")
