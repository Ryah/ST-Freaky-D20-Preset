from pathlib import Path
from html import escape
import json
from markdown_it import MarkdownIt

root = Path(__file__).resolve().parent
md = MarkdownIt('commonmark', {'html': False}).enable('table')
tokens = md.parse((root/'report.md').read_text(encoding='utf-8'))
headers = []
column = 0
in_head = False
for i, token in enumerate(tokens):
    if token.type == 'table_open':
        headers = []
    elif token.type == 'thead_open':
        in_head = True
    elif token.type == 'thead_close':
        in_head = False
    elif token.type == 'th_open' and in_head:
        headers.append(tokens[i+1].content.replace('`', ''))
    elif token.type == 'tr_open':
        column = 0
    elif token.type == 'td_open':
        token.attrSet('data-label', headers[column])
        column += 1
body = md.renderer.render(tokens, md.options, {})
data = json.loads((root/'fixtures.json').read_text(encoding='utf-8'))
results = json.loads((root/'results.json').read_text(encoding='utf-8'))
index = {name: {r['id']: r for r in result['samples']} for name, result in results['encodings'].items()}
prose = {f['id']: f['markdown'] for f in json.loads((root/'prose-fixtures.json').read_text(encoding='utf-8'))['fixtures']}
pairs = []
for f in data['fixtures']:
    stats = ' · '.join(f"{name}: {index[name][f['id']]['markdown_tokens']} Markdown / {index[name][f['id']]['base_tokens']} base / {index[name][f['id']]['ao_tokens']} AO ({index[name][f['id']]['ao_overhead_percent']:+.2f}%)" for name in index)
    pairs.append(f'''<details class="pair"><summary>{escape(f['id'])} <span>{escape(f['group'])}</span></summary>
    <p class="meta">Source: {escape(f['source_block'])}</p><p>{escape(f['conversion_notes'])}</p>
    <p class="counts">{escape(stats)}</p><div class="pair-columns"><section><h3>AO · exact source</h3><pre>{escape(f['ao'])}</pre></section>
    <section><h3>Compact base · reconstructed</h3><pre>{escape(f['base'])}</pre></section><section><h3>Ordinary Markdown prose</h3><pre>{escape(prose[f['id']])}</pre></section></div></details>''')
style = '''
:root { color-scheme:light dark; --bg:#f3f5f7; --paper:#fff; --ink:#172332; --muted:#566579; --line:#dce3ea; --accent:#285d73; --code:#f4f7f9; }
* { box-sizing:border-box; } body { margin:0; color:var(--ink); background:var(--bg); font:16px/1.7 system-ui,-apple-system,'Segoe UI',sans-serif; }
main { max-width:1100px; padding:48px 56px; margin:32px auto; background:var(--paper); border:1px solid var(--line); }
.masthead { color:var(--muted); font-size:11px; letter-spacing:.14em; text-transform:uppercase; border-bottom:2px solid var(--accent); padding-bottom:16px; margin-bottom:28px; }
h1 { font-size:clamp(30px,4vw,43px); letter-spacing:-.04em; line-height:1.17; font-weight:650; max-width:850px; margin:10px 0 25px; }
h2 { font-size:23px; line-height:1.25; margin:42px 0 18px; letter-spacing:-.02em; } h3 { font-size:17px; margin:24px 0 12px; }
p { margin:0 0 18px; } li { margin-bottom:9px; } ul { padding-left:24px; } a { color:var(--accent); overflow-wrap:anywhere; text-underline-offset:3px; }
table { width:100%; border-collapse:collapse; table-layout:fixed; margin:24px 0; font-size:14px; } th,td { border-bottom:1px solid var(--line); text-align:left; padding:12px 9px; vertical-align:top; overflow-wrap:anywhere; } th { background:var(--code); font-size:11px; text-transform:uppercase; letter-spacing:.05em; }
code,pre { font-family:Consolas,'Liberation Mono',monospace; font-size:.84em; } code { padding:.1em .25em; background:var(--code); overflow-wrap:anywhere; }
pre { padding:16px; background:var(--code); white-space:pre-wrap; overflow-wrap:anywhere; tab-size:2; border-left:2px solid var(--accent); line-height:1.7; }
.pair { border-top:1px solid var(--line); padding:14px 0; } .pair summary { cursor:pointer; font-weight:650; } .pair summary span { font-size:12px; color:var(--muted); font-weight:400; margin-left:10px; }
.pair-columns { display:grid; grid-template-columns:1fr; gap:20px; } .pair-columns>* { min-width:0; } .meta { color:var(--muted); font-size:12px; margin-top:14px; } .counts { font-size:12px; color:var(--accent); }
footer { margin-top:40px; border-top:1px solid var(--line); padding-top:18px; font-size:12px; color:var(--muted); }
@media(prefers-color-scheme:dark) { :root { --bg:#101820; --paper:#16212d; --ink:#e3ebf1; --muted:#a8b7c7; --line:#354455; --accent:#98c8de; --code:#1e2c39; } }
@media(max-width:650px) { main { margin:0; padding:26px 20px; border:0; } body { font-size:15px; } .pair-columns { grid-template-columns:1fr; } table,tbody,tr,td { display:block; width:100%; } thead { display:none; } tr { border:1px solid var(--line); padding:10px; margin-bottom:12px; } td { display:flex; justify-content:space-between; gap:14px; border:0; padding:5px 0; text-align:right; } td::before { content:attr(data-label); flex:0 0 42%; text-align:left; color:var(--muted); font-size:12px; } pre { padding:12px; font-size:12px; } }
@media print { :root { color-scheme:light; --paper:white; --ink:#111; --muted:#555; --line:#ccc; --code:#f4f4f4; --accent:#285d73; } @page { size:A4; margin:18mm; } main { border:0; margin:0; padding:0; max-width:none; } body { background:white; font-size:10pt; } h1,h2,h3 { break-after:avoid; } tr,pre { break-inside:avoid; } table { font-size:8.5pt; } .pair-columns { display:block; } }
'''
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TeleWire TRP-AO versus reconstructed base — token estimate</title><style>{style}</style></head><body><main>
<div class="masthead">FrankenSIM / Vexa · Token-count experiment · 17 comparison samples</div>
<article>{body}</article><h2 id="all-pairs">Inspect all three versions</h2><p>These are offline counting fixtures. They do not change your preset or establish behavioral equivalence.</p>{''.join(pairs)}
<footer>Self-contained report · tiktoken {escape(results['version'])} · Two reference encodings · No generation or model-behavior test</footer>
</main></body></html>'''
(root/'report.html').write_text(html,encoding='utf-8')
print('Rendered self-contained report with',len(pairs),'expandable three-way samples.')
