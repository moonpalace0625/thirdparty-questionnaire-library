
import yaml, pathlib, pandas as pd, sys
base = pathlib.Path(__file__).resolve().parents[1]
with open(base / 'categories.yaml', 'r', encoding='utf-8') as f:
    categories = {c['key']: c for c in yaml.safe_load(f)}
rows = []
for yml in sorted((base / 'questions').glob('*.yml')):
    with open(yml, 'r', encoding='utf-8') as f:
        q = yaml.safe_load(f)
    rows.append({
        "uid": q['uid'],
        "category_order": categories[q['category']]['order'],
        "category_name": categories[q['category']]['name_ja'],
        "order": q['order'],
        "text": q['text_ja'],
        "edit_link": f"[✏️](../questions/{yml.name})"
    })
df = pd.DataFrame(rows)
df.sort_values(["category_order", "order", "uid"], inplace=True)
md_lines = []
current_cat = None
for _, r in df.iterrows():
    if r['category_name'] != current_cat:
        md_lines.append(f"\n### {r['category_name']}\n")
        md_lines.append("| ID | 質問 | Link |")
        md_lines.append("|----|------|------|")
        current_cat = r['category_name']
    md_lines.append(f"| {r['uid']} | {r['text']} | {r['edit_link']} |")
(base / 'docs').mkdir(exist_ok=True)
with open(base / 'docs' / 'INDEX.md', 'w', encoding='utf-8') as out:
    out.write("\n".join(md_lines))
