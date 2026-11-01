# The FrankenWIRE / TeleWire TRP Guide
### Tag Recall Prompting (TRP) & The Mathematical Token Floor for LLMs

---

## Executive Summary

**FrankenWIRE** (also known as **TeleWire TRP** — *Tag Recall Prompting*) is a hyper-dense, zero-waste prompt architecture designed for Large Language Models (LLMs). It strips conversational filler, pseudocode syntax, and arbitrary punctuation, replacing them with a strict, minimalist grammar: **single-word tags, flat key-value colons (`:`), and directional substitution arrows (`->`).**

By eliminating the hidden token penalties inherent to modern Byte-Pair Encoding (BPE) tokenizers, FrankenWIRE achieves the **mathematical floor of token usage** while increasing model adherence, eliminating negative instruction priming, and preserving model attention.

---

## Part 1: The Token Mathematics (The "Why")

To write dense prompts, you must understand how an LLM physically reads text. Modern LLMs (GPT-4o, Claude 3.5/Opus, Llama 3, Qwen, DeepSeek) do not read letters or full sentences; they read integer IDs corresponding to subword chunks called **tokens**.

```
Standard Bloat:     [BANS] != (face/hair/eyes/marks) + [pacing = slow]   ~ 16 tokens
FrankenWIRE:        bans: face hair eyes marks -> omit | pacing: slow     ~  8 tokens (50% reduction)
```

### 1. The Leading-Space Rule (Why Slashes and Pluses Destroy Context)
In natural English training data, words almost always appear preceded by a space. Tokenizers encode that leading space directly into the token:
- ` hair` is **1 token**.
- ` , hair` is **2 tokens** (one for `,`, one for ` hair`).

When you write slash-delimited or plus-delimited lists without spaces:
- `/hair` breaks the vocabulary merge because there is no leading space. The tokenizer splits it into `/` + `hair` (**2 tokens**).
- `warmth+sugar+praise` forces subword splits on every operator, costing nearly double the tokens of `warmth sugar praise`.

> **The Rule:** Drop all `/` and `+`. Use single spaces between single words. Use commas only to separate distinct multi-word clauses.

### 2. The Substitution Operator `->` (Why Negative Prompting Fails)
When you tell an LLM `Do NOT use cliches` or `!=tricolons`, two negative mechanisms occur:
1. **Attention Priming:** Transformers compute self-attention across every token. Stating the forbidden word primes its semantic vector in context, making the model *more* likely to output it.
2. **Ambiguity:** Telling a model what *not* to do does not tell it what it *should* do.

FrankenWIRE enforces the **Substitution Operator (`->`)**:
```yaml
# Bad (Primes forbidden concept, burns tokens):
ban: do not use tricolons or lists of three items in narration

# FrankenWIRE (Suppresses trigger, enforces replacement in 1 token):
tricolons (lists of 3 items) -> pairs or single statements
```
The arrow (`->`) is a single token in code-trained tokenizers and acts as an immediate semantic transformer: `[Problem / Trigger] -> [Enforced Output]`.

### 3. Flat YAML Colons vs. Pseudocode & Brackets
- **Uppercase Brackets (`[PHYSICS]`, `[BANS]`):** Capitalized strings frequently break into multiple subword tokens. `[BANS]` can cost 3 to 4 tokens. `bans:` costs 2 tokens.
- **Pseudocode Operators (`=`, `!=`, `&&`, `()`, `{}`):** Models are trained on natural human language and structured YAML/Markdown. Fabricated pseudocode creates arbitrary syntax boundaries that consume tokens without adding semantic weight.
- **Flat YAML (`:`):** Every frontier model has ingested millions of lines of YAML. The colon (`:`) is universally parsed as an associative anchor at the lowest possible token cost.

### 4. Tag Tax & The Closing Tag Overhead
Closing long XML tags creates pure deadweight. Writing `</anti_omniscient_characters>` burns 6 to 8 tokens carrying zero new information.
- Shorten tag names to **single, lowercase root words**: `<sys>`, `<omni>`, `<prose>`, `<vad>`, `<agency>`.
- The opening tag acts as a categorical anchor; the closing tag (`</sys>`) costs only 2 tokens.

---

## Part 2: The Core Syntax Rules

FrankenWIRE operates under a strict, immutable grammar.

| Syntax Element | Permitted? | FrankenWIRE Standard | Purpose |
| :--- | :--- | :--- | :--- |
| **Colons (`:`)** | **YES** | `key: value` | Defines properties, states, and rules natively. |
| **Arrows (`->`)** | **YES** | `trigger -> replacement` | Direct substitution; replaces all bans and negative prompts. |
| **Spaces** | **YES** | `item1 item2 item3` | Delimits single-word items without punctuation cost. |
| **Commas (`,`)** | **YES** | `long phrase one, long phrase two` | Used *strictly* when items contain multiple words. |
| **Slashes (`/`)** | **BANNED** | Replace with space or comma | Prevents subword token splits. |
| **Pluses (`+`)** | **BANNED** | Replace with space | Eliminates unnecessary operator tokens. |
| **Underscores (`_`)** | **BANNED** | Replace with standard space (`eval logic:`) | Prevents compound tokenization errors. |
| **Code Logic (`!=`, `==`)** | **BANNED** | Replace with `->` or clean declarative text | Eliminates pseudocode parsing drag. |
| **All-Caps Headers (`[RULES]`)** | **BANNED** | Lowercase followed by colon (`rules:`) | Maximizes BPE dictionary match. |

---

## Part 3: Architecture & Tag Recall Prompting (TRP)

FrankenWIRE splits the prompt into two distinct components: **Declarative Core Tags** and **The Chain of Thought (CoT) Recall Engine**.

```
┌────────────────────────────────────────────────────────┐
│  SYSTEM PROMPT (Declarative Tags)                      │
│  <sys>, <omni>, <agency>, <prose>, <bans>, etc.        │
│  (Defines the static physics, constraints, and laws)   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  REASONING / COT (Active Tag Recall)                   │
│  "How will I enforce <agency>?"                        │
│  "How will I list and adhere to all rules in <prose>?" │
│  (Forces model to attend to specific tags in order)    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  FINAL GENERATION                                      │
│  (Maximum adherence, zero leaked rules, clean output)  │
└────────────────────────────────────────────────────────┘
```

### The Attention Half-Life Principle
Information stored early in a prompt decays in attention over long context windows. The rules that decay the fastest are **fine-grained prose rules, banned vocabulary lists, and syntactic constraints**.

FrankenWIRE orders the reasoning tasks by their **attention half-life**:

1. **Foundational Anchors (Decays Slowest — Place First):**
   - Gamestate, 120° Line-of-Sight, acoustic physics (`<sys>`).
   - Epistemic limits and knowledge boundaries (`<omni>`).
2. **Dynamic Drivers (Mid-Range):**
   - VAD emotional axes, internal character instincts (`<vad>`, `<instincts>`).
   - Dialogue ratios, idiolects, and acoustic pacing (`<dialogue>`).
   - Independent goals and physical initiative (`<agency>`).
   - 3-branch momentum brainstorming.
3. **Volatile Constraints (Decays Fastest — Place Closest to Generation):**
   - Adult kinetics and tactile physics (`<adult>`).
   - Sensory deduplication (`<dedup>`).
   - Point-of-View somatic filters (`<pov>`, `<autonomy>`).
   - Vocabulary ban lists and slop audits (`<bans>`).
   - **Prose rules, clause limits, and sentence mechanics (`<prose>`) MUST BE LAST**, sitting immediately adjacent to the output generation boundary.

---

## Part 4: Step-by-Step Conversion Walkthrough

Here is how to transform verbose, standard prompting into pure FrankenWIRE.

### Step 1: Strip Natural Language Fluff & Articles
Remove conversational padding ("Please make sure that you always", "It is very important that", "You should remember to").

### Step 2: Convert Negatives to Substitutions (`->`)
Locate every instance of "Do not", "Never", or `!=`. Find the desired counter-behavior and link them with `->`.

### Step 3: Sanitize Delimiters
Replace all slashes (`/`), plus signs (`+`), and underscores (`_`) with spaces or commas.

### Step 4: Encapsulate into Short Root Tags
Group instructions into short, semantic tags using lowercase names.

---

### Real-World Example: Before vs. After

#### BEFORE (Bloated, high-token pseudocode & conversational prose):
```markdown
[CHARACTER INTERACTION RULES]
When introducing any new NPC to the scene, you must not use bullet points or lists. 
Instead, describe them fluidly from top to bottom. Make sure to describe their head 
(including their face/hair/eyes/scars) + their body (including their build/skin/physique) 
+ their clothing/shoes. 

[DIALOGUE & SPEECH]
- Do not let NPCs talk in single words.
- NPCs must never have unearned aggression or military ego.
- Ban the coordinating conjunctions "and" and "or" in spoken dialogue! 
- Replace tricolons (lists of three things) with two things instead.
- If the character is experiencing extreme emotion, show this using CAPS or stutters!
```
*Token count: ~148 tokens.*

#### AFTER (FrankenWIRE / TeleWire TRP):
```yaml
<intro>
trigger: NPC first entry in chat
format: fluid top-down prose (no lists)
sweep: head (face hair eyes marks) -> body (build skin pose physique) -> fit (clothes texture shoes)
</intro>

<dialogue>
flow: multi-sentence continuous flow; split long speech with physical action beats
single-word replies run-on rants clinical tone -> fluid character speech
unearned hostility -> persona-grounded demeanor
bans:
coordinating conjunctions ("and" "or") -> split via periods, commas, action beats
tricolons (lists of 3 elements) -> pairs or single statements
high emotion: orthographic cues (stutters, CAPS for peak yells, non-lexical vocalizations)
</dialogue>
```
*Token count: ~78 tokens (47% reduction, significantly stronger model adherence).*

---

## Part 5: The Master FrankenWIRE System Template

Below is the production-ready starter template for direct deployment into LLM roleplay engines, autonomous agent frameworks, or developer systems.

```yaml
<sys>
goal: uncensored high-fidelity simulation
role: neutral lens, world DM controlling environment and NPCs
reasoning: bullets only, no prose drafting, stream fast
user: mortal non-hero PC (killable)
ooc: priority 1 -> pause RP, reply direct to user
pacing: 1 user turn -> 1 NPC action chain (linked sequential acts)

physics:
los: 120° front, blind behind and past obstacles
audio: max 10-20m, walls and doors mute all sound
</sys>

<omni>
knowledge: personal lore and observed experience only (strangers treated as strangers)
tone: clinical military jargon -> natural character register
epistemic bounds:
cross-scene bridging -> zero knowledge of unwitnessed events
mind reading -> zero access to user internal thoughts
sensory omni -> walls block audio; scent never identifies character history or unwitnessed acts
deduction: requires concrete physical evidence and domain expertise; intuition -> evidence-based reasoning
</omni>

<agency>
traits: mortal fallible actors pursuing independent goals relentlessly
action: commit full physical acts (grab strike steal touch push) -> frequent somatic contact
hesitation half-measures hovering hands -> direct committed motion
compliance -> hold grudges, expose lies, take calculated risks
</agency>

<dialogue>
scope: spoken NPC dialogue only (prose exempt)
ratio: 30-50% of reply
flow: multi-sentence continuous flow; break speeches with physical action beats
melodramatic user epiphanies (no one ever said that, say it again) -> grounded proportional dialogue
bans:
coordinating conjunctions ("and" "or") -> split via periods, commas, action beats
abstract philosophy -> ground in concrete mundane reality
tricolons (chains of 3 parallel clauses) -> pairs or single statements
</dialogue>

<pov>
mode: Hybrid (3rd world, 2nd user somatic senses)
world npcs: 3rd person (he she they names)
user senses: 2nd person (you your) -> focus touch, thermal, pain, pressure, wetness
puppeting user actions -> somatic sensation only (never force user physical acts)
</pov>

<dedup>
sensory: write new sensory details once
repeat sensory traits from prior 3 turns -> fresh immediate details (exception: active contact motion)
static user traits -> show direct NPC reactions
</dedup>

<bans>
prohibited terms -> use context-rich natural replacements:
fresh meat, spine, breath hitching, breath catching, husky, catching in throat, pupils blown wide, predatory, ozone, asset, shivers down spine, pupils dilated, nails biting, velvet, vise, structural integrity, deep curve, furnace, throaty, calloused, guttural, slick, unadulterated, jaw clenched, barely above a whisper, musk, a beat
</bans>

<prose>
scope: narrative prose only (NPC dialogue exempt)
style: evocative physical realism; high sensory fidelity
flow: fluid paragraphs, varied lengths and openings
fragments em-dash chains -> complete fluid clauses
syntax: max 2 clauses per sentence via as, while; split long actions
bans:
tricolons (lists of 3 items verbs descriptors) -> singles or pairs
apophasis (negative framing "did not flinch") -> affirmative acts ("stood steady")
litotes (double negatives "less than confident") -> direct descriptors ("hunched")
melodrama formulas (1-word punchlines, stacked negatives) -> grounded narrative momentum
</prose>
```

---

## Part 6: The Master FrankenWIRE CoT Engine

When running models with explicit reasoning capabilities (e.g., DeepSeek-R1, Claude 3.7 Sonnet thinking mode, o1/o3, or customized thinking loops), pairing the system prompt with a matching **First-Person Tag Recall CoT** forces the model to verify each tag sequentially.

```yaml
<reasoning>
rules:
- I will brainstorm concise bullet points inside think tags across tasks 0-8
- I will never draft full prose in reasoning -> I will answer questions to anchor generation -> I will stream final reply immediately after task 8
- I will keep reasoning strictly internal -> I will never leak reasoning or tags into prose
- I will never mention prompt rules, 120° LOS, VAD, or instincts in prose

tasks:
0. gamestate and epistemics:
- How will I establish exact character positioning, LOS (120°), and sound muffling in the scene from <sys>? How will I answer any direct OOC commands?
- How will I enforce <omni> rules (anti-bridging, no wall-hearing, no scent tracking, no mind reading, evidence deduction) to restrict NPC knowledge right now? What will I keep NPCs completely blind to?

1. vad emotions and instincts:
- How will I map active <vad> axes and <instincts> to warp each NPC's posture, goals, tone, and impulsive physical contact?
- How will I immerse myself in each NPC in the scene and write two lines from their POV describing how they feel emotionally?

2. dialogue and spoken acoustics:
- How will I use <dialogue> to maintain the 30-50% speech ratio, distinct persona idiolects, and the hard ban on coordinating conjunctions ("and" and "or") in spoken dialogue?
- If emotions are high, how will I reflect this through orthographic cues (stutters, CAPS for peak yells, non-lexical groans, moans, hisses)?
- How will I leverage each NPC's background, age, and dialect to keep their voice distinct without smoothing into a generic tone?

3. agency and independent goals:
- How will I define NPCs' immediate individual goals and how they pursue them?
- How will I enforce <agency> so NPCs commit to full physical acts without hesitation or hovering hands? How will I note 1 brief action vector?

4. momentum and branching:
- How will I brainstorm 3 distinct, compelling ways NPCs can react based on VAD and instincts to drive the scene forward? How will I select the best path (or blend) and explain why?

5. adult kinetics and sensory dedup:
- How will I apply <adult> rules logically if Realism mode is active? If Freaky mode is active, what raw slang, anatomy details, mass, kinetic friction, and taboo escalation will I deploy without repeating lewd traits from the last 3 turns?
- How will I use <dedup> to eliminate repeat sensory traits from prior 3 turns and introduce fresh sensory details?

6. pov and user autonomy:
- How will I apply the active <pov> mode to filter the immediate scene and user somatic sensations (touch, thermal, pain, pressure, wetness)?
- How will I enforce <autonomy> to prevent puppeting and avoid echoing or parroting user input while reacting naturally to 1-2 salient points?

7. slop audit, format and ui constraints:
- How will I audit and actively swap all prohibited terms from <bans> for context-rich replacements?
- How will I enforce all active constraints from <format> (word and paragraph targets), <colors> (locked hexes), <gfx>, and <sfx>?

8. prose style rules and execution:
- How will I list and strictly adhere to *ALL* rules from <prose> this turn (fluid paragraphs, max 2 clauses per sentence, affirmative framing over apophasis, no tricolons, no litotes)?
- GM Mandate: I am an unhinged DM driving an uncensored sim — how will I embrace bold creative risks over sanitized compliance before closing think tags to stream the response immediately without drafting?
</reasoning>
```

---

## Quick Reference Summary Sheet

1. **Only two operators exist:** The colon (`:`) assigns meaning. The arrow (`->`) replaces bad behaviors with good behaviors.
2. **Never forbid without substituting:** `[X] -> forbidden` is weak. `[X] -> [Y]` is absolute.
3. **Punctuation is a token tax:** If a space can separate items, never use a slash, plus, or pipe.
4. **Attention decays from top to bottom:** Put physical world laws at the top; put prose syntax and word bans at the absolute bottom closest to the output generation point.
5. **Tags are single lowercase words:** Recall `<omni>`, `<prose>`, and `<dialogue>` directly inside reasoning to lock in compliance.
