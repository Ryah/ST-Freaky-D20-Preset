"""Reproduce illustrative TeleWire TRP-AO fragment and marker token counts.

Requires tiktoken. These reference encodings do not identify the user's model.
No generation, provider billing measurement, or attention experiment is performed.
"""
from pathlib import Path
from importlib.metadata import version
import json
import tiktoken

FIXTURES = [
    {
        "name": "gossip_age",
        "expanded": "Increase the age of every gossip record g by one.",
        "ao": "AGE ∀ g +1",
    },
    {
        "name": "conditional_call",
        "expanded": "If the current turn count ct is divisible by three, call chekhov_fire; after the function returns, continue with the next instruction.",
        "ao": "IF ct%3=0 ➤ <fn:chekhov_fire>",
    },
    {
        "name": "membership",
        "expanded": "If participant n does not belong to the gossip witness set K(g), add participant n to that set.",
        "ao": "n ∉ K(g) → add n",
    },
]
MARKERS = ["→", "∀", "≥", "∈", "∅", "➤", "⇥", "⇤", "↺", "Ψ", "ℱ̄", "🌶️", "🎲"]


def measure():
    result = {
        "purpose": "Illustrative stored-fragment counts; not a representative preset benchmark.",
        "backend": "tiktoken",
        "version": version("tiktoken"),
        "evidence_scope": {
            "fixtures": "Documentation-authored expansions and AO expressions; not the author's historical before/after corpus.",
            "assumptions": "g means a gossip record, ct is the tick count, K(g) is its witness set; arrow and function semantics are already defined.",
            "excluded": "Legend/setup costs, assembled prompt wrappers, macro expansion, provider formatting, output tokens, attention and behavioral outcomes.",
            "semantics": "Intended equivalence for illustration; no generation-based equivalence test was run.",
            "ao_overhead_vs_base_trp": "Not measured; author reports approximately 5-10% depending on complexity.",
            "author_reported_savings": "Typically 30-50% versus expanded prompt wording; historical raw pairs and tokenizer metadata were not supplied here.",
        },
        "encodings": {},
    }
    for name in ["cl100k_base", "o200k_base"]:
        encoding = tiktoken.get_encoding(name)
        rows = []
        for fixture in FIXTURES:
            expanded = len(encoding.encode(fixture["expanded"]))
            ao = len(encoding.encode(fixture["ao"]))
            rows.append({**fixture, "expanded_tokens": expanded, "ao_tokens": ao,
                         "saved_tokens": expanded - ao,
                         "savings_percent": round(100 * (1 - ao / expanded), 1),
                         "expanded_characters": len(fixture["expanded"]),
                         "ao_characters": len(fixture["ao"])})
        result["encodings"][name] = {
            "fixtures": rows,
            "markers": [{"text": marker, "standalone_tokens": len(encoding.encode(marker)),
                         "space_prefixed_tokens": len(encoding.encode(" " + marker))}
                        for marker in MARKERS],
        }
    return result


if __name__ == "__main__":
    output = Path(__file__).with_suffix(".json")
    report = measure()
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name, data in report["encodings"].items():
        print(name)
        for row in data["fixtures"]:
            print(f"  {row['name']}: {row['expanded_tokens']} -> {row['ao_tokens']} tokens ({row['savings_percent']}% saved)")
    print("Wrote", output)
