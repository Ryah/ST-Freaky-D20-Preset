# COMPLETE SYMBOL REFERENCE TABLE

## Core Logic Operators

| Symbol | Meaning | Usage Example |
| :---: | :--- | :--- |
| `∀` | For all / apply to each | `∀ bullet ∈ active` — apply to every active bullet |
| `∃` | There exists / at least one | `∃ axis ≥ 8` — at least one axis is ≥ 8 |
| `∈` | Element of / belongs to set | `axis ∈ {E,L,Ph}` — axis belongs to this set |
| `∉` | Not element of / excluded from | `user ∉ paths` — user is excluded from paths |
| `→` | Then / implies / assignment | `acc ≥ 8 → axis += 1` — if acc ≥ 8, then increment axis |
| `↔` | Bidirectional / mirror pair | `E ↔ M` — Eros mirrors Misos |
| `∅` | Null / no modifier / skip | `|Δ| ≤ 2 → ∅` — if difference ≤ 2, no change |
| `Ψ` | Set of all axes | `Ψ = {E,L,Ph,Pr,Sg,Ag,M,Er,Ec,St,Ad,Pt}` |
| `ℱ` | Set of all Fondness axes | `ℱ = {E,L,Ph,Pr,Sg,Ag}` |
| `ℱ̄` | Set of all Friction axes | `ℱ̄ = {M,Er,Ec,St,Ad,Pt}` |

---

## Numeric & Comparison Operators

| Symbol | Meaning | Usage Example |
| :---: | :--- | :--- |
| `Σ` | Sum of all values | `Σlove = E+L+Ph+Pr+Sg+Ag` |
| `\|x\|` | Absolute value | `\|Φ₋\|` — absolute value of negative Philautia |
| `Δ` | Difference / delta | `Δ = (roll + mods) - DC` |
| `δ` | Collision gap (emotion difference) | `δ = \|w_ant - w_aff\|` |
| `≥` | Greater than or equal to | `axis ≥ 4` — axis must be at least 4 |
| `≤` | Less than or equal to | `Φ ≤ 0` — Philautia is zero or negative |
| `>` | Greater than | `Σlove > Σshadow` |
| `<` | Less than | `acc < threshold` |
| `=` | Equal to / assignment | `axis = 0` — assign zero |
| `+` | Addition / positive | `axis += 1` — increment by 1 |
| `-` | Subtraction / negative | `axis -= 1` — decrement by 1 |
| `*` | Multiplication | `5s + 1` |
| `%` | Modulo operator | `ct % 3 = 0` — every 3rd turn |
| `^` | Power / exponent | `s²` — seed squared |
| `mod` | Modulo operation | `s mod 20` — remainder after division by 20 |
| `floor(x)` | Floor / integer division | `floor(s / 13)` — integer division by 13 |

---

## Set & Sequence Notation

| Symbol | Meaning | Usage Example |
| :---: | :--- | :--- |
| `{ }` | Set definition | `{E,L,Ph,Pr,Sg,Ag}` |
| `[ ]` | Array / range | `Δ ∈ [0, +7]` — delta between 0 and 7 |
| `( )` | Grouping / operation order | `(5s + 1) mod 65536` |
| `:` | Such that / defines | `∀ bullet ∈ active:` — for each bullet such that it's active |
| `…` | Continuation / range | `1-5, 6-10, 11-15, 16-20` |
| `\|` | Conditional / such that | `s = {b \| b ∈ active ∧ age ≥ 4}` |

---

## State & Variable Notation

| Symbol | Meaning | Usage Example |
| :---: | :--- | :--- |
| `ct` | Current tick count | `ct % 5 = 0` — every 5th turn |
| `s₀` | Initial seed | `s₀ = hash(π, chat, timestamp)` |
| `sₙ` | Seed at iteration n | `sₙ₊₁ = (5sₙ + 1) mod 65536` |
| `Φ` | Philautia (self-love) | `Φ ∈ [-20, +20]` |
| `Φ₋` | Negative Philautia (abs value) | `\|Φ₋\|` |
| `Φ_acc` | Philautia accumulator | `Φ_acc ∈ [-30, +30]` |
| `E` | Eros axis value | `E ≥ 6` |
| `M` | Misos axis value | `M ≥ 6` |
| `L` | Ludus axis value | `L ≥ 8` |
| `Er` | Eris axis value | `Er ≥ 4` |
| `Ph` | Philia axis value | `Ph ≥ 10` |
| `Ec` | Echthros axis value | `Ec ≥ 6` |
| `Pr` | Pragma axis value | `Pr ≥ 12` |
| `St` | Stasis axis value | `St ≥ 4` |
| `Sg` | Storge axis value | `Sg ≥ 12` |
| `Ad` | Adiaphora axis value | `Ad ≥ 4` |
| `Ag` | Agape axis value | `Ag ≥ 10` |
| `Pt` | Phthonos axis value | `Pt ≥ 6` |
| `x` | Mirror axis pair variable | `M(x)` — mirror of axis x |
| `w_ant` | Antithesis emotion weight | `w_ant ∈ [1,5]` |
| `w_aff` | Affirmation emotion weight | `w_aff ∈ [1,5]` |

---

## Assignment & Conditional Operators

| Symbol | Meaning | Usage Example |
| :---: | :--- | :--- |
| `:=` | Assignment / set to | `acc := 0` — reset accumulator to zero |
| `+=` | Increment by | `axis += 1` — increase axis by 1 |
| `-=` | Decrement by | `trailing -= 1` — decrease trailing by 1 |
| `IF...THEN` | Conditional | `IF acc ≥ 8 THEN axis += 1` |
| `ELSE` | Alternative path | `IF Φ < 0 THEN... ELSE...` |
| `AND` | Logical AND | `IF acc ≥ 8 AND ct % 3 = 0` |
| `OR` | Logical OR | `IF axis ≥ 10 OR acc ≥ 12` |

---

## Quick Reference: Sets & Axes

| Notation | Definition |
| :---: | :--- |
| `ℱ` | Fondness axes: `{E, L, Ph, Pr, Sg, Ag}` |
| `ℱ̄` | Friction axes: `{M, Er, Ec, St, Ad, Pt}` |
| `Ψ` | All axes: `ℱ ∪ ℱ̄ ∪ {Φ}` |
| `M(x)` | Mirror axis of x: `M(E)=M, M(L)=Er, M(Ph)=Ec, M(Pr)=St, M(Sg)=Ad, M(Ag)=Pt` |

---

## Common Formula Examples

| Formula | Meaning |
| :--- | :--- |
| `Σlove = E+L+Ph+Pr+Sg+Ag` | Sum of all Fondness axes |
| `Σshadow = M+Er+Ec+St+Ad+Pt + \|Φ₋\|` | Sum of all Friction axes + negative Philautia |
| `IF Σlove ≥ Σshadow + 5 → aff +1` | If love exceeds shadow by 5, increase affirmation |
| `IF Σshadow ≥ Σlove + 5 → ant +1` | If shadow exceeds love by 5, increase antithesis |
| `\|Δ\| ≤ 2 → ∅` | If absolute difference ≤ 2, no modifier |
| `Δ = (roll + mods + stats) - DC` | Dice outcome calculation |
| `sₙ₊₁ = (5sₙ + 1) mod 65536` | LCG random seed generation |
| `threshold = base - age - proximity - scene - urgency` | Chekhov firing threshold |
