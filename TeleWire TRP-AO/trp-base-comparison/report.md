# TeleWire TRP-AO versus reconstructed compact TeleWire TRP

Token-count estimate · November 3, 2026

## Result

Across **all 17 selected examples counted once each**, AO used **12.94–13.82% more tokens** than the reconstructed compact base versions. This is a selected mixed pack, not a measured full prompt.

Within that pack, the **12 complete tagged rule modules** used **9.72–10.17% more tokens**. A practical description of this experiment is **about 10% overhead for the rule modules, or about 13–14% for this particular mix of rules, procedures, legend and state row.**

The middle half of individual rule-module differences spans roughly **4.8–14.4%** across the two counters. This describes the sample, not a confidence interval or a guaranteed 5–15% range for every prompt.

Your earlier 5–10% estimate is close to the rule-module result. The mixed selection is higher, and procedural/state costs vary, so the experiment does not establish 5–10% as a universal bound.

| Scope | Encoding | Reconstructed base | AO | AO overhead |
|---|---|---:|---:|---:|
| All 17 examples, once each | `cl100k_base` | 2,098 | 2,388 | +13.82% |
| All 17 examples, once each | `o200k_base` | 2,086 | 2,356 | +12.94% |
| 12 rule modules | `cl100k_base` | 1,691 | 1,863 | +10.17% |
| 12 rule modules | `o200k_base` | 1,688 | 1,852 | +9.72% |
| 3 procedural excerpts | `cl100k_base` | 290 | 344 | +18.62% |
| 3 procedural excerpts | `o200k_base` | 283 | 333 | +17.67% |
| One-time axis legend | `cl100k_base` | 64 | 89 | +39.06% |
| One-time axis legend | `o200k_base` | 62 | 83 | +33.87% |
| One matrix template row | `cl100k_base` | 53 | 92 | +73.58% |
| One matrix template row | `o200k_base` | 53 | 88 | +66.04% |

Positive percentages mean AO is larger. Formula: `100 × (AO / base − 1)`. Group counts tokenize the selected texts joined by two newlines; they are not percentages averaged across blocks.

## Where the difference comes from

**Rules:** individual differences range from 0% to about 34%. Modules already close to base style change little. Shorter tags, flatter wording, removal of redundant reinforcement, and punctuation changes all contribute. This is a reconstruction of the style, not a pure measurement of emoji cost.

**Procedures:** the three selected bodies cost about 18% more in AO. The mechanics page is about 32% larger than its flat reconstruction; the other two procedures differ by about 3–6%. Both versions retain the procedure order, guards, and return/transition meaning in text. Execution equivalence was not tested.

**State markers:** replacing twelve emoji identities with established short labels such as E, L, and Ph saves 35–39 tokens on one isolated matrix row. The row itself is only 53 base tokens, so the reported 66–74% increase has a small denominator. It is not a 66–74% increase in the complete state block or prompt.

The label replacement also changes the contextual-framing intervention described in the whitepaper. The count compares the same twelve value/accumulator slots; it does not show that short labels produce the same behavior as the targeted emoji associations.

### State-template denominator check

A follow-up diagnostic changes only the axis legend and matrix-row labels inside the **full, otherwise unchanged state-template source**. It is not a full base-style conversion or a captured response.

| Encoding | Short-label control | Original AO template | Extra tokens | Difference |
|---|---:|---:|---:|---:|
| `cl100k_base` | 3,380 | 3,444 | +64 | +1.89% |
| `o200k_base` | 3,371 | 3,427 | +56 | +1.66% |

Thus the isolated emoji-row percentage and the full-template percentage answer different questions. Live history cost depends on the number of pair records, actual values, emitted sections, history cleaning, and repeated state. The source template is counted before expansion.

### ASCII-marker control

A separate deterministic control changes Unicode markers to ASCII spellings while keeping the rest of the AO wording. It deliberately does **not** enforce the complete base guide: it is a diagnostic for marker selection, not a second reconstructed base.

| Scope | `cl100k_base` AO over ASCII control | `o200k_base` AO over ASCII control |
|---|---:|---:|
| 12 rule modules | +0.22% | +0.22% |
| 3 procedural excerpts | +4.24% | +3.42% |

Most of the approximately 10% rule-module difference is therefore associated with reconstruction choices in tags, wording and format, rather than a large net tax from Unicode characters alone in those modules. That observation says nothing about which version a model follows better.

## Method and scope

- The 17 primary pairs were frozen before tokenization: 12 complete declarative modules, 3 complete procedural excerpts, one legend, and one state row. Selection was a stratified convenience sample across topics, not a random sample of the entire preset.
- AO text is extracted exactly from the unchanged Vexa v5 snapshot, with CRLF normalized to LF. The base side is a newly authored compact reconstruction guided by the archived TeleWire TRP guide. It is not a historical base implementation or a proven minimum-token solution.
- The review preserves intended rules, order, counts, examples, exceptions, and protected identifiers. Original contradictions remain. Baseline synonym, segmentation and verbosity choices affect the estimate; model-level semantic equivalence was not established.
- Machine identifiers, macro names, literal state targets and HTML wrappers remain protected where needed, even if the abstract base grammar discourages punctuation. These counterfactual texts are for counting and review, not preset import.
- The state-template denominator diagnostic was added after inspecting the initial result to put the isolated-row cost in context; it is separate from the frozen primary sample.
- Backend: `tiktoken` 0.14.0; reference encodings `cl100k_base` and `o200k_base`. Neither is claimed to match a particular production model or provider billing.
- Counts cover stored text only. No model generation, latency, attention, adherence, equivalence, or full assembled-prompt test was run.

The result is an empirical count for these specific paired strings and an estimate of reconstruction cost. It should not be generalized into a whole-preset or universal AO overhead without a larger corpus and the actual target tokenizer.

## Reproduce and inspect

From the repository root:

```powershell
python docs/frankenwire/trp-base-comparison/compare.py
```

- [All source/base pairs](pairs.md): inspect the conversion decisions and per-sample counts.
- [Frozen fixtures](fixtures.json): full strings, source locations, and conversion notes.
- [Measured results](results.json): group totals, individual counts, descriptive statistics, and ASCII controls.
- [State-template diagnostic](state-context.json): full paired diagnostic text.

The JSON also contains explicitly artificial repeated-row scenarios. They keep this selected static pack once and repeat only a matrix row; they are not measurements of an actual chat or full repeated state blocks.

Source preset SHA-256: `a26276225f8beccd06bfc0cddde916d485541c2cd0607614c13a0547fa2dbd88`. Frozen-fixture SHA-256: `a78b7e6ba11f76b616ab56c96e2ef4e48970b1b253e65b8fd2af7acf210bc700`.

Existing whitepapers and their newer workspace copies were left unchanged. This report adds a separate reconstructed-base estimate; it does not replace the earlier AO-versus-expanded-prose examples.
