"""Count frozen reconstructed base/AO fixtures, without generation or preset edits.

Run with Python 3 and tiktoken installed. Results use explicit reference encodings.
"""
from collections import defaultdict
from importlib.metadata import version
from pathlib import Path
import hashlib
import json
import statistics
import tiktoken

ROOT = Path(__file__).resolve().parent
ASCII_MARKERS = {
    '🌶️': 'E', '🎲': 'L', '🤝': 'Ph', '🛠️': 'Pr', '🏠': 'Sg', '🕊️': 'Ag',
    '😠': 'M', '🥊': 'Er', '❄️': 'Ec', '🪨': 'St', '🌫️': 'Ad', '🐍': 'Pt',
    '→': '->', '↔': '<->', '⇄': '<->', '∀': 'all', '∅': 'none',
    '≥': '>=', '≤': '<=', '≠': '!=', '±': '+/-', '×': 'x',
    '➤': 'call', '⇤': 'return', '⇥': 'next', '↺': 'each', '↳': 'loop',
    '↑': 'up', '↓': 'down', '°': ' degrees', '—': '-', '–': '-',
    '“': '"', '”': '"', '’': "'",
}


def ascii_control(text):
    for marker, replacement in ASCII_MARKERS.items():
        text = text.replace(marker, replacement)
    return text


def overhead(ao, baseline):
    return round(100 * (ao / baseline - 1), 2)


def run():
    raw = (ROOT / 'fixtures.json').read_bytes()
    data = json.loads(raw)
    assert len(data['fixtures']) == 17
    report = {
        'backend': 'tiktoken', 'version': version('tiktoken'),
        'fixtures_sha256': hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest(),
        'artifact_hash_policy': 'JSON file hashes normalize CRLF to LF; encoded sample strings remain unchanged.',
        'source_sha256': data['source_sha256'],
        'formula': '100 * (AO_tokens / reconstructed_base_tokens - 1); positive means AO is larger',
        'selection': data['selection'], 'conversion_policy': data['conversion_policy'],
        'limits': data['evidence_limits'],
        'ascii_control_definition': 'Fixed symbol-to-ASCII substitutions in otherwise unchanged AO text. Diagnostic control, not a base-TRP-compliant reconstruction or a behavior-equivalence claim.',
        'ascii_substitutions': ASCII_MARKERS,
        'encodings': {},
    }
    context_raw = (ROOT / 'state-context.json').read_bytes()
    context = json.loads(context_raw)
    assert context['source_sha256'] == data['source_sha256']
    report['state_context_diagnostic'] = {
        'purpose': context['purpose'],
        'input_sha256': hashlib.sha256(context_raw.replace(b'\r\n', b'\n')).hexdigest(),
        'counts': {},
    }
    for name in ['cl100k_base', 'o200k_base']:
        enc = tiktoken.get_encoding(name)
        rows = []
        groups = defaultdict(list)
        for fixture in data['fixtures']:
            ao = len(enc.encode(fixture['ao']))
            base = len(enc.encode(fixture['base']))
            control = len(enc.encode(ascii_control(fixture['ao'])))
            row = {
                'id': fixture['id'], 'group': fixture['group'],
                'ao_tokens': ao, 'base_tokens': base, 'ascii_control_tokens': control,
                'ao_minus_base_tokens': ao - base,
                'ao_overhead_percent': overhead(ao, base),
                'ao_over_ascii_control_percent': overhead(ao, control),
            }
            rows.append(row)
            groups[fixture['group']].append((fixture, row))
        summaries = {}
        for group, items in groups.items():
            ao = len(enc.encode('\n\n'.join(f['ao'] for f, _ in items)))
            base = len(enc.encode('\n\n'.join(f['base'] for f, _ in items)))
            control = len(enc.encode('\n\n'.join(ascii_control(f['ao']) for f, _ in items)))
            percentages = [row['ao_overhead_percent'] for _, row in items]
            quartiles = statistics.quantiles(percentages, n=4, method='inclusive') if len(items) > 1 else None
            summaries[group] = {
                'samples': len(items), 'joined_ao_tokens': ao, 'joined_base_tokens': base,
                'joined_ascii_control_tokens': control,
                'joined_ao_overhead_percent': overhead(ao, base),
                'joined_ao_over_ascii_control_percent': overhead(ao, control),
                'median_sample_overhead_percent': round(statistics.median(percentages), 2),
                'sample_min_percent': min(percentages), 'sample_max_percent': max(percentages),
                'sample_IQR_percent': [round(quartiles[0], 2), round(quartiles[2], 2)] if quartiles else None,
                'sum_separately_counted_ao_tokens': sum(row['ao_tokens'] for _, row in items),
                'sum_separately_counted_base_tokens': sum(row['base_tokens'] for _, row in items),
            }
        # Hypothetical coverage of this selected pack, not a real assembled chat prompt.
        static = [f for f in data['fixtures'] if f['group'] != 'state']
        state = next(f for f in data['fixtures'] if f['group'] == 'state')
        scenarios = []
        for repeats in [1, 10, 50]:
            ao = len(enc.encode('\n\n'.join([f['ao'] for f in static] + [state['ao']] * repeats)))
            base = len(enc.encode('\n\n'.join([f['base'] for f in static] + [state['base']] * repeats)))
            scenarios.append({'row_repetitions': repeats, 'ao_tokens': ao,
                              'base_tokens': base, 'ao_overhead_percent': overhead(ao, base)})
        report['encodings'][name] = {'groups': summaries, 'samples': rows,
                                    'synthetic_pack_state_repetition_scenarios': scenarios}
        context_ao = len(enc.encode(context['ao']))
        context_base = len(enc.encode(context['short_label_control']))
        report['state_context_diagnostic']['counts'][name] = {
            'full_template_ao_tokens': context_ao,
            'full_template_short_label_control_tokens': context_base,
            'extra_tokens': context_ao - context_base,
            'ao_over_control_percent': overhead(context_ao, context_base),
        }
    prose_raw = (ROOT / 'prose-fixtures.json').read_bytes()
    prose = json.loads(prose_raw)
    prose_index = {f['id']: f for f in prose['fixtures']}
    assert set(prose_index) == {f['id'] for f in data['fixtures']}
    report['markdown_baseline'] = {
        'fixtures_sha256': hashlib.sha256(prose_raw.replace(b'\r\n', b'\n')).hexdigest(),
        'policy': prose['policy'], 'state_policy': prose['state_policy'],
        'savings_formula': '100 * (1 - compact_tokens / markdown_tokens)',
        'encodings': {},
    }
    for name, result in report['encodings'].items():
        enc = tiktoken.get_encoding(name)
        for row in result['samples']:
            tokens = len(enc.encode(prose_index[row['id']]['markdown']))
            row.update(markdown_tokens=tokens,
                       ao_savings_vs_markdown_percent=round(100 * (1-row['ao_tokens']/tokens), 2),
                       base_savings_vs_markdown_percent=round(100 * (1-row['base_tokens']/tokens), 2))
        subsets = {'rules': [f for f in data['fixtures'] if f['group']=='rules'],
                   'procedures': [f for f in data['fixtures'] if f['group']=='procedures'],
                   'instructions_and_setup': [f for f in data['fixtures'] if f['group']!='state'],
                   'mixed_pack': data['fixtures']}
        totals = {}
        for scope, fixtures in subsets.items():
            counts = {key: len(enc.encode('\n\n'.join(f[key] for f in fixtures))) for key in ('ao','base')}
            counts['markdown'] = len(enc.encode('\n\n'.join(prose_index[f['id']]['markdown'] for f in fixtures)))
            totals[scope] = {'samples':len(fixtures), **{key+'_tokens':value for key,value in counts.items()},
                             'ao_savings_percent':round(100*(1-counts['ao']/counts['markdown']),2),
                             'base_savings_percent':round(100*(1-counts['base']/counts['markdown']),2)}
        report['markdown_baseline']['encodings'][name] = totals
    return data, report


def write_pair_review(data, report):
    prose = {f['id']: f['markdown'] for f in json.loads((ROOT/'prose-fixtures.json').read_text(encoding='utf-8'))['fixtures']}
    text = ['# Markdown prose, compact base, and AO comparison samples', '',
            'The original AO/base pairs were frozen before their first count. The Markdown baseline was authored later and frozen before its own first count. These are experimental comparison texts, not importable preset replacements.', '',
            data['conversion_policy'], '']
    counts = {name: {r['id']: r for r in result['samples']}
              for name, result in report['encodings'].items()}
    for f in data['fixtures']:
        text += [f"## {f['id']} ({f['group']})", '',
                 f"Source: `{f['source_block']}`. {f['conversion_notes']}", '',
                 '**AO — exact source excerpt**', '', '```text', f['ao'], '```', '',
                 '**Base — manual reconstruction**', '', '```text', f['base'], '```', '',
                 '**Ordinary Markdown prose — authored baseline**', '', '```markdown', prose[f['id']], '```', '',
                 '| Encoding | Markdown | Base | AO | AO savings vs Markdown | Base savings vs Markdown |', '|---|---:|---:|---:|---:|---:|']
        for name, index in counts.items():
            row = index[f['id']]
            text.append(f"| `{name}` | {row['markdown_tokens']} | {row['base_tokens']} | {row['ao_tokens']} | {row['ao_savings_vs_markdown_percent']:.2f}% | {row['base_savings_vs_markdown_percent']:.2f}% |")
        text += ['']
    (ROOT/'pairs.md').write_text('\n'.join(text) + '\n', encoding='utf-8')


def write_report(data, report):
    encodings = report['encodings']
    packs = {name: result['synthetic_pack_state_repetition_scenarios'][0] for name, result in encodings.items()}
    pack_ranges = [p['ao_overhead_percent'] for p in packs.values()]
    rule_ranges = [r['groups']['rules']['joined_ao_overhead_percent'] for r in encodings.values()]
    iqrs = [r['groups']['rules']['sample_IQR_percent'] for r in encodings.values()]
    text = [
        '# Token comparison: Markdown prose, compact TeleWire TRP, and TRP-AO', '',
        'Token-count estimate · November 3, 2026', '',
        '## Result', '',
        f"Across **all 17 selected examples counted once each**, AO used **{min(pack_ranges):.2f}–{max(pack_ranges):.2f}% more tokens** than the reconstructed compact base versions. This is a selected mixed pack, not a measured full prompt.", '',
        f"Within that pack, the **12 complete tagged rule modules** used **{min(rule_ranges):.2f}–{max(rule_ranges):.2f}% more tokens**. A practical description of this experiment is **about 10% overhead for the rule modules, or about 13–14% for this particular mix of rules, procedures, legend and state row.**", '',
        f"The middle half of individual rule-module differences spans roughly **{min(q[0] for q in iqrs):.1f}–{max(q[1] for q in iqrs):.1f}%** across the two counters. This describes the sample, not a confidence interval or a guaranteed 5–15% range for every prompt.", '',
        'Your earlier 5–10% estimate is close to the rule-module result. The mixed selection is higher, and procedural/state costs vary, so the experiment does not establish 5–10% as a universal bound.', '',
        '| Scope | Encoding | Reconstructed base | AO | AO overhead |',
        '|---|---|---:|---:|---:|',
    ]
    labels = {'rules': '12 rule modules', 'procedures': '3 procedural excerpts',
              'setup': 'One-time axis legend', 'state': 'One matrix template row'}
    for name, pack in packs.items():
        text.append(f"| All 17 examples, once each | `{name}` | {pack['base_tokens']:,} | {pack['ao_tokens']:,} | {pack['ao_overhead_percent']:+.2f}% |")
    for group, label in labels.items():
        for name, result in encodings.items():
            s = result['groups'][group]
            text.append(f"| {label} | `{name}` | {s['joined_base_tokens']:,} | {s['joined_ao_tokens']:,} | {s['joined_ao_overhead_percent']:+.2f}% |")
    text += [
        '', 'Positive percentages mean AO is larger. Formula: `100 × (AO / base − 1)`. Group counts tokenize the selected texts joined by two newlines; they are not percentages averaged across blocks.', '',
        '## Where the difference comes from', '',
        '**Rules:** individual differences range from 0% to about 34%. Modules already close to base style change little. Shorter tags, flatter wording, removal of redundant reinforcement, and punctuation changes all contribute. This is a reconstruction of the style, not a pure measurement of emoji cost.', '',
        '**Procedures:** the three selected bodies cost about 18% more in AO. The mechanics page is about 32% larger than its flat reconstruction; the other two procedures differ by about 3–6%. Both versions retain the procedure order, guards, and return/transition meaning in text. Execution equivalence was not tested.', '',
        '**State markers:** replacing twelve emoji identities with established short labels such as E, L, and Ph saves 35–39 tokens on one isolated matrix row. The row itself is only 53 base tokens, so the reported 66–74% increase has a small denominator. It is not a 66–74% increase in the complete state block or prompt.', '',
        'The label replacement also changes the contextual-framing intervention described in the whitepaper. The count compares the same twelve value/accumulator slots; it does not show that short labels produce the same behavior as the targeted emoji associations.', '',
        '### State-template denominator check', '',
        'A follow-up diagnostic changes only the axis legend and matrix-row labels inside the **full, otherwise unchanged state-template source**. It is not a full base-style conversion or a captured response.', '',
        '| Encoding | Short-label control | Original AO template | Extra tokens | Difference |',
        '|---|---:|---:|---:|---:|',
    ]
    for name, counts in report['state_context_diagnostic']['counts'].items():
        text.append(f"| `{name}` | {counts['full_template_short_label_control_tokens']:,} | {counts['full_template_ao_tokens']:,} | {counts['extra_tokens']:+d} | {counts['ao_over_control_percent']:+.2f}% |")
    text += [
        '', 'Thus the isolated emoji-row percentage and the full-template percentage answer different questions. Live history cost depends on the number of pair records, actual values, emitted sections, history cleaning, and repeated state. The source template is counted before expansion.', '',
        '### ASCII-marker control', '',
        'A separate deterministic control changes Unicode markers to ASCII spellings while keeping the rest of the AO wording. It deliberately does **not** enforce the complete base guide: it is a diagnostic for marker selection, not a second reconstructed base.', '',
        '| Scope | `cl100k_base` AO over ASCII control | `o200k_base` AO over ASCII control |',
        '|---|---:|---:|',
    ]
    for group in ['rules', 'procedures']:
        values = [encodings[name]['groups'][group]['joined_ao_over_ascii_control_percent'] for name in ['cl100k_base', 'o200k_base']]
        text.append(f"| {labels[group]} | {values[0]:+.2f}% | {values[1]:+.2f}% |")
    text += [
        '', 'Most of the approximately 10% rule-module difference is therefore associated with reconstruction choices in tags, wording and format, rather than a large net tax from Unicode characters alone in those modules. That observation says nothing about which version a model follows better.', '',
        '## Method and scope', '',
        '- The 17 primary pairs were frozen before tokenization: 12 complete declarative modules, 3 complete procedural excerpts, one legend, and one state row. Selection was a stratified convenience sample across topics, not a random sample of the entire preset.',
        '- AO text is extracted exactly from the unchanged Vexa v5 snapshot, with CRLF normalized to LF. The base side is a newly authored compact reconstruction guided by the archived TeleWire TRP guide. It is not a historical base implementation or a proven minimum-token solution.',
        '- The review preserves intended rules, order, counts, examples, exceptions, and protected identifiers. Original contradictions remain. Baseline synonym, segmentation and verbosity choices affect the estimate; model-level semantic equivalence was not established.',
        '- Machine identifiers, macro names, literal state targets and HTML wrappers remain protected where needed, even if the abstract base grammar discourages punctuation. These counterfactual texts are for counting and review, not preset import.',
        '- The state-template denominator diagnostic was added after inspecting the initial result to put the isolated-row cost in context; it is separate from the frozen primary sample.',
        f"- Backend: `tiktoken` {report['version']}; reference encodings `cl100k_base` and `o200k_base`. Neither is claimed to match a particular production model or provider billing.",
        '- Counts cover stored text only. No model generation, latency, attention, adherence, equivalence, or full assembled-prompt test was run.', '',
        'The result is an empirical count for these specific paired strings and an estimate of reconstruction cost. It should not be generalized into a whole-preset or universal AO overhead without a larger corpus and the actual target tokenizer.', '',
        '## Reproduce and inspect', '',
        'From the repository root:', '',
        '```powershell', 'python docs/frankenwire/trp-base-comparison/compare.py', 'python docs/frankenwire/trp-base-comparison/render.py', '```', '',
        '- [All three versions](pairs.md): inspect the conversion decisions and per-sample counts.',
        '- [Frozen fixtures](fixtures.json): full strings, source locations, and conversion notes.',
        '- [Markdown prose fixtures](prose-fixtures.json): ordinary instruction versions and output-contract policy.',
        '- [Measured results](results.json): group totals, individual counts, descriptive statistics, and ASCII controls.',
        '- [State-template diagnostic](state-context.json): full paired diagnostic text.', '',
        'The JSON also contains explicitly artificial repeated-row scenarios. They keep this selected static pack once and repeat only a matrix row; they are not measurements of an actual chat or full repeated state blocks.', '',
        f"Source preset SHA-256: `{data['source_sha256']}`. Frozen-fixture SHA-256: `{report['fixtures_sha256']}`.", '',
        'The whitepaper summarizes these measurements. The original three expression-level prose examples remain a separate illustrative comparison.',
    ]
    baseline = report['markdown_baseline']
    section = ['## Ordinary Markdown prose baseline', '',
               'Cindy authored normal Markdown versions of the same samples using headings, bullets, numbered steps, and full sentences. The texts were frozen before counting, without a target token reduction. Required identifiers and output syntax remain; instruction module wrappers become headings. The original AO/base fixtures are unchanged.', '',
               '| Scope | Encoding | Markdown prose | Compact base | AO | Base savings | AO savings |',
               '|---|---|---:|---:|---:|---:|---:|']
    for scope, label in [('instructions_and_setup','16 instruction/setup samples'),('rules','12 rule modules'),('procedures','3 procedures'),('mixed_pack','17 samples including state row')]:
        for name, totals in baseline['encodings'].items():
            s = totals[scope]
            section.append(f"| {label} | `{name}` | {s['markdown_tokens']:,} | {s['base_tokens']:,} | {s['ao_tokens']:,} | {s['base_savings_percent']:.2f}% | {s['ao_savings_percent']:.2f}% |")
    section += ['', 'Savings use `100 × (1 − compact / Markdown)`. Counts include Markdown punctuation and headings, with the same two-newline joining rule as the AO/base comparison. These are direct counts for one authored prose baseline; wording choices affect the estimate.', '',
                'The 16 instruction/setup samples are the primary prose comparison. The seventeenth sample is serialized state, not an instruction: the prose baseline keeps the exact AO state row as a shared output contract. Compact base keeps its existing short-label row. Its mixed-pack savings therefore include that state-label difference. The prose legend retains emoji mappings to preserve the AO output contract and semantic associations.', '',
                'No generation-based equivalence test was run. The [Markdown fixtures](prose-fixtures.json) and [all three versions](pairs.md) make semantic coverage and editorial choices inspectable. This baseline was added after the original AO/base results were known; it does not turn the convenience sample into a representative corpus.', '',
                f"Markdown-fixture SHA-256: `{baseline['fixtures_sha256']}`.", '']
    text[4:4] = section
    (ROOT/'report.md').write_text('\n'.join(text) + '\n', encoding='utf-8')


if __name__ == '__main__':
    data, report = run()
    (ROOT/'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    write_pair_review(data, report)
    write_report(data, report)
    for name, result in report['encodings'].items():
        print(name)
        prose = report['markdown_baseline']['encodings'][name]['instructions_and_setup']
        print(f"  16 instruction/setup samples: {prose['markdown_tokens']} Markdown, {prose['base_tokens']} base, {prose['ao_tokens']} AO; savings {prose['base_savings_percent']}% base / {prose['ao_savings_percent']}% AO")
        for group, s in result['groups'].items():
            print(f"  {group}: {s['joined_base_tokens']} base, {s['joined_ao_tokens']} AO, {s['joined_ao_overhead_percent']:+.2f}%; ASCII control {s['joined_ao_over_ascii_control_percent']:+.2f}%")
        for row in result['samples']:
            print(f"    {row['id']}: {row['base_tokens']} -> {row['ao_tokens']} ({row['ao_overhead_percent']:+.2f}%)")
        print('  Hypothetical repeated-row scenarios:', result['synthetic_pack_state_repetition_scenarios'])
