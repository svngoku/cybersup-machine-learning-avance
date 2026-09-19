from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
refs=json.loads((ROOT/"resources/sources.json").read_text())
lines=["# Ressources du cours", "", "Consultation : 19 septembre 2026. Les liens `stable` sont vivants ; l'environnement des TP est figé par `uv.lock`.", "", "Les articles, livres et documentations ci-dessous sont consultables sans abonnement. Un accès gratuit n'autorise pas automatiquement leur redistribution. Les liens locaux signalent les deux supports fournis par le formateur, non inclus dans le dépôt.", ""]
for key,r in refs.items():
    lines.extend([f"## {key} · {r['title']}","",f"{r['author']} · {r['date']}","",f"[Accéder à la ressource]({r['url']})" if r['url'].startswith('http') else r['url'],"",r.get('use',''),"",f"Accès / réutilisation : {r.get('rights','Lire à la source ; ne pas republier sans vérifier la licence.')}",""])
(ROOT/"resources/RESSOURCES.md").write_text('\n'.join(lines),encoding='utf-8')
