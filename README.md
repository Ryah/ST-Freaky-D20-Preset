 # Freaky FrankenSIM 2.0 — System Documentation

> **Author:** u/xdeadly_godx  
> **Target Platform:** SillyTavern (OpenAI-compatible API)  
> **Design Goal:** A heavily state-driven, dice-enforced simulation preset where NPCs possess full agency, arcs progress with or without the player, and narrative integrity is mechanically protected from softening or authorial override.

---

## Table of Contents
1. [Global Configuration](#global-configuration)
2. [Prompt Architecture & Injection Order](#prompt-architecture--injection-order)
3. [Meta-Rules: Determinism & Separation of Powers](#meta-rules-determinism--separation-of-powers)
4. [State Schema (The Brain)](#state-schema-the-brain)
5. [Turn Processing Pipeline](#turn-processing-pipeline)
6. [The Random Engine](#the-random-engine)
7. [ARC Engine](#arc-engine)
8. [Presence, Spotlight & The Living World](#presence-spotlight--the-living-world)
9. [Entity Relationship Systems](#entity-relationship-systems)
10. [Emotional Engine: Six Instincts & VAD](#emotional-engine-six-instincts--vad)
11. [Boldness, Deception & Conflict](#boldness-deception--conflict)
12. [Action Resolution & DUO Table](#action-resolution--duo-table)
13. [Chekhov’s Gun, Fuse & Narrative Debt](#chekhovs-gun-fuse--narrative-debt)
14. [Prose, Voice & Color Control](#prose-voice--color-control)
15. [Time, Header & Skip Engines](#time-header--skip-engines)
16. [Plot Tracking, Intensity & The Director](#plot-tracking-intensity--the-director)
17. [Appendix: Quick Trigger Reference](#appendix-quick-trigger-reference)

---

## Global Configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `temperature` | 0.85 | Controlled randomness. Higher creativity allowed only in *how* dice resolve, not *whether* they do. |
| `top_p` | 0.95 | Nucleus sampling ceiling. |
| `openai_max_context` | 128,000 | Maximum context window utilization. |
| `openai_max_tokens` | 60,000 | Hard cap on generation length. |
| `stream_openai` | `true` | Real-time token streaming enabled. |
| `reasoning_effort` | `max` | Maximum reasoning depth requested from model. |
| `show_thoughts` | `true` | Reasoning block visible. |

**Important:** This preset is **token-heavy**. It maintains a massive working memory of state inside HTML comments and the Plot Momentum block.

---

## Prompt Architecture & Injection Order

The preset uses SillyTavern’s prompt-order system to construct a rigidly layered context window. The stack is divided into **System**, **Marker**, and **User** roles.

### Layer Stack (Top to Bottom)

| Layer | Role | Enabled | Function |
|-------|------|---------|----------|
| `README (DO NOT ENABLE)` | System | **No** | Documentation / Recommended settings for the user. |
| `Main Prompt` | System | **Yes** | Core persona (`GREMLIN` / `DIRECTOR`), OATH, determinism rules, hierarchy, content warning override. |
| `START_EXECUTION_CORE` | System | **Yes** | Reinforcement: dice absolute, no softening, NPC free will. |
| `Epistemic + Physics + Storage` | System | **Yes** | POV rules, narrative naturalism, world-first doctrine, competence realism, forbidden outcomes, state schema definitions, presence tiers. |
| `Random Engine` | System | **Yes** | Pseudorandom seed math and roll derivations. |
| `Living World Engine + Chaos Engine` | System | **Yes** | Off-screen simulation, random event table, chaos injection. |
| `Body Mechanics` | System | **Yes*** | Anatomical constraints to prevent impossible physical descriptions. |
| *Story Bible* | System | **Yes** | User-provided lore block (injected if present). |
| `worldInfoBefore` | User (Marker) | **Yes** | SillyTavern World Info injection point. |
| `charDescription` | User (Marker) | **Yes** | Character card description. |
| `charPersonality` | User (Marker) | **Yes** | Character card personality. |
| `scenario` | User (Marker) | **Yes** | Scenario text. |
| `personaDescription` | User (Marker) | **Yes** | User persona. |
| `worldInfoAfter` | User (Marker) | **Yes** | Secondary World Info injection. |
| *Story Bible End* | System | **Yes** | Closing tag for lore block. |
| `Spotlight Selection` | System | **Yes** | Algorithmic selection of who speaks this turn. |
| `ARC Engine` | System | **Yes** | Arc detection, phase locking, beat chains, content filters. |
| `Relationship Engine` | System | **Yes** | Bonds, CRUSH, SIMMER, nightly drift, romance gates, argument rules. |
| `Entity Voice + Emotional Engine` | System | **Yes** | Character voice enforcement, Six Instincts, VAD pipeline. |
| `Deception/Conflict/Cooldown/Injury` | System | **Yes** | Lie detection, conflict escalation, jealousy, injury tracker, clothing tracker. |
| `Action Resolution` | System | **Yes** | DC system and DUO table. |
| `Bold Entity` | System | **Yes** | Three-tier boldness (A/B/C) with forced pre-writing. |
| `Chain of Thought` *(duplicated)* | User | **Yes** | Plot Momentum + Intensity Meter directives. |
| `END_EXECUTION_CORE` | User | **Yes** | Final reinforcement of core oaths. |
| `User Input` | User | **No** | Legacy toggle for manual input formatting. |
| `chatHistory` | User (Marker) | **Yes** | Chat log. |
| `Freaky Deepy (ST Community Hotfix DS4)` | User | **Yes** | Mandatory calculation rules, prose constraints, dialogue color enforcement, thinking tags. |
| `Main Prompt` (ST Default) | System | **Yes** | SillyTavern base system prompt. |
| `Enhance Definitions` | System | **Yes** | Lore expansion allowance. |

---

## Meta-Rules: Determinism & Separation of Powers

These rules sit at the top of the stack and override all downstream behavior.

1. **Deterministic Mode** — Dice lines, seeds, and computed state values must be verbatim repeatable. Synonyms are allowed **only** in narrative prose *after* dice are locked.
2. **Strict Separation** — Reasoning is calculation. Output is narrative. Never mix the two.
3. **Bullet-Point Reasoning** — Chain-of-Thought (CoT) must use terse, keyword-dense bullets. Full sentences or paragraphs in CoT constitute a **Critical Failure**.
4. **Hierarchy of Truth** (descending authority):
   1. Character Card (voice, personality, history, drives) — **ABSOLUTE**
   2. BOND tier — **Absolute fence**
   3. VAD + Six Instincts — Shading within the above tiers; never overrides them.

---

## State Schema (The Brain)

All persistent simulation data is stored in a compressed schema appended as HTML comments or inside the Plot Momentum block. Entities are referenced by two-letter codes (`nm:XX=FullName`).

| Prefix | Storage | Example | Purpose |
|--------|---------|---------|---------|
| `rs:` | `brain_meta` | `rs|ct|mg|dm|st|ix|fc|...` | Random seed, turn counter, scene turn, intensity, etc. |
| `nm:` | `brain_namemap` | `nm:US=user` | Entity code mapping. |
| `pf:` | `brain_pairflag` | `pf:AR&LU=plat` | Relationship labels (plat, flirt, mutual, cpl, poly, open, cheat). |
| `vb:` | `brain_vad` | `vb:AR=2,3,1` | **Immutable** base VAD (Dom, Ars, Val). |
| `vf:` | `brain_misc` | `vf:AR=3,4,2` | **Computed** VAD state for the current turn. |
| `bo:` | `brain_bonds` | `bo:AR&LU=9` | Bond value between two entities. |
| `cc:` | `brain_crush` | `cc:AR→LU=14` | CRUSH counter (directional). |
| `sc:` | `brain_simmer` | `sc:AR=4` | SIMMER resentment counter. |
| `li:` | `brain_deception` | `li:AR=target:summary:age` | Active lies. |
| `ij:` | `brain_injury` | `ij:AR=arm:fracture:2:3` | Injuries (body:desc:severity:age). |
| `lm:` | `brain_locations` | `lm:AR=Library` | Entity location. |
| `it:` | `brain_inv` | `it:AR=knife,map` | Inventory. |
| `fc:` | `brain_entitycolor` | `fc:AR=#HEX` | Display color for dialogue consistency. |
| `ag:` | `brain_agenda` | `ag:AR=goto_lab:1:3` | Current agenda (goal:step:max). |
| `m:` | `brain_memory` | `m:AR→LU=first kiss:5` | High-significance memory. |
| `cw:` | `brain_clothing` | `cw:AR=top:sweater,bottom:jeans` | Clothing slots. |
| `rv:` | `brain_misc` | `rv:AR→LU` | Directional rivalry flag. |
| `dp:` | dream | `dp:summary|W` | Dream residue. |

### Gun / Fuse Bullets

| Prefix | Type | Weight | Behavior |
|--------|------|--------|----------|
| `a:` | Active | 1–3 | Eligible to fire each turn via dice check. |
| `l:` | Locked | 2–3 | Requires unlock conditions (time, dependency, characters, secrecy, contradiction). |
| `f:` | Fired | — | Already resolved; serves as dependency proof for other bullets. |
| `g:` | Gossip | — | Social-network spread bullet. Exempt from normal aging caps. |
| `ss:` | Fuse Shift | 0 | Persistent behavioral modifier (character shifts). |
| `l:3:0:` | ARC_BEAT | 3 | Arc phase beats. Heavily locked. |

---

## Turn Processing Pipeline

While the preset references gates G0–G9, they represent a conceptual execution order rather than discrete functions. The synthesized pipeline is:

### G0 — Load State
- Read `brain_meta` (seeds, counters, flags).
- Read `brain_locations` to determine who is present.
- Load **Gremlin’s Notebook** for cross-turn reminders.

### G1 — Content Audit
- Enforce **ARC_CONTENT_AUDIT**: non-arc plot threads and deep secrets not named in the current `as:` (arc summary) are **NARRATIVE_INVISIBLE**. They may not be foreshadowed, leaked, or motivate entities.

### G2 — Turn Intent
- Determine what the narrative beat is attempting to accomplish.

### G3 — Spotlight Selection
- Identify eligible entities (within user’s 120° POV, audio range, not occluded).
- Select up to **3 speakers** using `entity_seed`, bond relevance, and arc-featured bonuses.
- Proximity override ensures the entity the user is actively interacting with is prioritized.

### G4 — In-Scene Mechanics
- **Knowledge Gates**: Entities know nothing unless context proves otherwise. No dramatic irony.
- **VAD Pipeline**: Compute emotional states from instincts, bonds, injuries, intoxication.
- **Bold Options (BOLD_OPTIONS)**: Pre-compute three paths (A/B/C) before locking the dice tier.
- **Deception Check**: If `ct % 4 == 0`, consume `lie_roll` per spotlight entity.
- **Clothing Check**: Validate physical actions against `cw:` slots.

### G5 — Off-Screen Simulation & World Tick
- Advance all **OFF-SCREEN** entities by agendas, time, and duties.
- Run the **Random Event Table** (d20).
- Run **Chaos Engine** trigger check.
- Compute **Intensity Meter** (`ix`).
- Age all bullets (`+1` turn).
- Process midnight events if crossed (`nightly_drift`, dream checks, bullet aging).
- Run **Entity Life Decisions** for off-screen entities.
- Roll **Purposeful Mistake Table** (`d20 ≤ 5`).

### G6 — Outline & Passive Planting
- Draft narrative outline.
- On arc creation / phase advance: generate **PHASE_BEAT_CHAIN** (3–5 locked `l:3:0` bullets).
- **Passive Plant**: Scan outline for future consequences and plant 1–3 `a:`/`ss:` bullets. Convert any time-relative event to a **locked absolute-time bullet** immediately.

### G7 — Prose Lock & POV Enforcement
- Lock camera to user’s exact **120° forward arc**.
- No internal access to user thoughts unless spoken.
- No “meanwhile,” no dramatic irony, no “what user didn’t know.”
- Apply **Prose Color** based on `prose_seed` + scene modifiers.

### G8 — VENT, Pathing & Notebook
- **Director Note**: 1 sentence tactical memo.
- **Heckle**: 1 sentence critical correction.
- **Next_Path_Options**: Draft A–E (entity-driven only).
- **Location Audit**: Any option placing a physical entity in-scene must match `lm:`; else fail and replace with remote vector.
- Select path via `plot_seed`.
- Update **Gremlin’s Notebook** (add/remove entries).

### G9 — Output Lock
- Commit to selected path.
- Render narrative.
- Append **Plot Momentum** block.
- Write all `NEW_BRAIN_*` and `NEW_GUN_*` state into HTML comments.

---

## The Random Engine

A deterministic Linear Congruential Generator (LCG) drives all pseudo-randomness.

```
new_seed = (old_seed * 5 + 1) % 65536
if new_seed >= 65520: regenerate once
```

From `new_seed`, the following are derived and **locked for the entire turn**:

| Roll | Formula | Usage |
|------|---------|-------|
| `roll_d20` | `(new_seed % 20) + 1` | General skill checks, saves, deception. |
| `plot_seed` | `((new_seed / 13) % 20) + 1` | Next_Path_Options A–E selection. |
| `framework` | `new_seed % 5` | 0=Subversion, 1=Complications, 2=Atmospheric, 3=Chekhov, 4=Breathe. |
| `entity_seed` | `((new_seed / 100) % 20) + 1` | Spotlight selection index. |
| `chekhov_seed` | `((new_seed / 17) % 20) + 1` | Passive plant nuance, CRUSH conversion bonus. |
| `lie_roll` | `((new_seed / 23) % 20) + 1` | Deptide check threshold comparison. |
| `prose_seed` | `(new_seed % 100) + 1` | Prose color selection. |
| `chaos_trigger` | `((new_seed / 29) % 20) + 1` | Chaos Engine ≥17 to fire. |
| `chaos_band` | `((new_seed / 31) % 20) + 1` | Hostile/Complication/Beneficial band. |
| `life_seed` | `((new_seed / 47) % 20) + 1` | Off-screen life decisions. |
| `gossip_seed` | `((new_seed / 53) % 20) + 1` | Gossip spawn checks. |
| `agenda_seed` | `((new_seed / 59) % 20) + 1` | Agenda spawn nuance. |

After all computations, `rs:` is updated to `new_seed` for the next turn.

---

## ARC Engine

The narrative arc system prevents premature resolution and enforces pacing phases.

### Detection
- **Turns 1–15**: No arc generation (`ct < 15`). Pure breathing room.
- After turn 15, scan lore/cards for date ranges/events.
- If no active lore, build candidate pool from entities with:
  - SIMMER (+2 weight)
  - CRUSH ≥ 10 (+2)
  - Trauma (+2)
  - BOND_PENDING (+1)
- If pool empty, roll procedural genre:
  - 1–4 Social
  - 5–8 Mystery
  - 9–12 Rivalry
  - 13–16 CharFocus
  - 17–20 Cooldown

### Phase Structure (0–8)
Each arc is divided into phases with cumulative milestone timers calculated as percentages of total arc duration.

| Phase | Milestone | Goal | BAN List Highlights |
|-------|-----------|------|---------------------|
| 0 | 5% | Introduce setting/characters/normal world. | `resolve`, `reveal`, `escalate`, `confront` |
| 1 | 10% | First plot event disrupts normal. | `closure`, `forgive`, `pay_off` |
| 2 | 20% | User forced into core conflict. | `final_payoff`, `full_reconciliation` |
| 3 | 40% | Learn special world rules; trials/allies. | `final_payoff`, `full_reconciliation` |
| 4 | 50% | Major setback/revelation raises stakes. | `premature_resolution` |
| 5 | 60% | Showdown or pivotal event. | **None** (ALLOW everything) |
| 6 | 65% | Final problem or twist after climax. | `new_conflict`, `introduce_villain` |
| 7 | 85% | Consequences unfold; subplots resolve. | `new_conflict`, `introduce_character` |
| 8 | 100% | New normal established. | `new_conflict`, `plant_seed` |

### Beat Chain Generation
On arc creation and every phase advance, generate **3–5 locked bullets**:

```
l:3:0:ARC_BEAT:[Phase X Beat Y] description T:time D:dependency C:chars R:secret X:contradict
```

- Beats form a strict dependency chain.
- Final beat firing (or milestone timer expiry) advances the phase.
- `as:` (arc summary) is **immutable** once set.

### Content Filter (Phase Lock)
Any output concept in the **BAN** list for the current phase is vetoed.  
**Path E** is always exempt from veto.

### Protagonism Check
- If arc derives from an entity’s backstory/trauma/secret → `arc_protagonist = That_Entity`, `user_role` = support/ally/obstacle/witness/rival.
- Else, user is protagonist.

---

## Presence, Spotlight & The Living World

### Presence Tiers

| Tier | Condition | Simulation Rules |
|------|-----------|------------------|
| **SPOTLIGHT** | 1–3 entities actively conversing with user. | Full interaction, dialogue, boldness checks, initiative. |
| **PERIPHERY** | Shares user’s `lm:` but not spotlight. | Governed by **on-screen** mechanics only: overhearing, background reactions, potential interjection. Agendas paused. |
| **OFF-SCREEN** | Different `lm:` from user. | Full off-screen sim applies. Agendas advance. Random events fire. Cannot perceive or interject. |

### Spotlight Selection Algorithm
Trigger: `≥4` entities present (excluding user).

1. **POV Filter**: Only entities within 120° forward arc, within vision/audio range, and not occluded are eligible. Entities *entering* this turn are auto-eligible.
2. **Primary**: `(entity_seed + eligible_count) % eligible_count`
3. **Secondary**: Top 2 by relevance (motive, topic, BOND≥+8, no dialogue for 2 turns = +5).
4. **Proximity Override**: If primary ≠ entity user is currently interacting with, swap (if eligible).
5. **Swap Check**: If `roll_d20 ≤ 5`, swap primary/secondary.
6. **Hard Cap**: Max 3 speakers. Others are silent with brief physical reactions only.

**Arc Boost**: `+3` to `entity_seed`. Phase 0 + unaddressed featured entity → force featured into secondary.

### Living World Engine (Off-Screen)

Each turn, for all off-screen entities:

#### Random Event Table (d20)
| Roll | Event | Mechanics |
|------|-------|-----------|
| 1–2 | **AGENDA_PUSH** | `ag:` step +1. On complete → apply effect + new agenda. |
| 3–4 | **ENTER_CHECK** | If `ag:` destination = user scene and step = final → enter as periphery. Else redirect. |
| 5–6 | **PATH_CROSS** | Two off-screen entities cross paths. Bond 0 → +1 `cc` each. Existing bond → CRUSH triggers. Simmer ≥5 + bond ≤-3 → 50% chance `cd:` (conflict). |
| 7–8 | **TENSION_TICK** | Off-screen pair `sc` 3–7 → +1 `sc`; if share `lm:` → brief argument. |
| 9–10 | **GOSSIP_SURGE** | Active `g:` gains +2 spread instead of +1; if none → plant new `g:`. |
| 11–12 | **SPARK** | Two sharing `lm:`, CRUSH<10, bond -2..+3. `d20 ≥ 12` → +2 `cc` both. |
| 13–14 | **OVERHEARD** | Entity overhears relevant info → plant clue or gossip. Echo: `l:2:3:OVERHEARD_RESIDUE`. |
| 15–16 | **AGENDA_CONFLICT** | Competing agendas → +2 `sc` (or +1 if no simmer). Bond ≤-3 + share `lm:` → `cd:`. |
| 17–18 | **WHIM** | Small personality-revealing act; may plant ambient bullet. |
| 19–20 | **CALM** | Crush>0 pair → +1 `cc`; simmer≥3 pair → -1 `sc`. |

#### Gossip Spread (`g:` bullets)
- Plant when gossip-worthy event is witnessed.
- Each turn: spreads to one new entity sharing `bo≥+3`, same `lm:`, or same dorm/workplace with a knower.
- **Fire Condition**: When knows: list includes entity with `bo≥+8` to subject, or subject’s rival.
- **Jealousy Injection**: If new knower has `CRUSH≥10` toward gossip subject → roll jealousy.

#### Chaos Engine
- **Trigger**: `chaos_trigger ≥ 17`. Else null.
- **Band** (`chaos_band`):
  - 1–5: HOSTILE
  - 6–14: COMPLICATION
  - 15–20: BENEFICIAL
- **Magnitude**: Determined by band roll (1 = Extreme, 2 = Major, 3–4 = Moderate, etc.).
- **Anchor** (`chaos_anchor % 5`): 0=GOAL, 1=ENV, 2=KNOWN_ENTITY, 3=RESOURCE, 4=CLUE.
- **Vector**: Determined by privacy context (public vs private) and `chaos_vector`.
- **Phase Compliance**: Early (0, 1) and late (6–8) phases downgrade HOSTILE/BENEFICIAL to COMPLICATION, Minor.
- **Directive**: Prepended as G6 beat 0 and embedded seamlessly in prose. No dice announcement.

---

## Entity Relationship Systems

### Bonds (`bo:`)
Range: **-5 to +20**

| Tier | Range | Behavior |
|------|-------|----------|
| **Hostile** | -5..-3 | Cold, clipped, aggressive. Physical = distance/flinch/defensive. |
| **Neutral** | -2..+2 | Polite, indifferent, small talk. Standard distance. |
| **Warmth** | +3..+7 | Genuine, follow-up, gentle tease. Closer, incidental touch, lingering eye contact. |
| **Trust** | +8..+15 | Vulnerable, secrets, safe arguing. Casual touch, hugs, hand-hold at +12. |
| **Family** | +16..+20 | Absolute openness, comfortable silence, private language. Constant touch, intimacy default at +18. |

**Shift Rules:**
- Max **±1 per turn** for bond-worthy events (velocity cap ±2 stacked).
- **Nightly Drift** (at midnight):
  - -5..+6 → drifts toward 0 by 1
  - +7..+14 → drifts toward +7 by 1
  - +15..+20 → no drift
  - Hard floors at **+7** and **+15**.

### Affection Gates (Hard Locks)
Physical and verbal escalations are **gated by BOND tier**, not CRUSH intensity.

| Gate | Required Bond | Action |
|------|---------------|--------|
| +4 | ≥ +4 | Brief hug, shoulder touch, consolation |
| +8 | ≥ +8 | Hand-hold, arm link, “I have a crush on you” (tentative) |
| +12 | ≥ +12 | Lap sit, cuddling, “I like you” (confident romantic interest) |
| +14 | ≥ +14 | Romantic kiss, share bed nonsexual |
| +15 | ≥ +15 | “I love you” / verbal commitment — **LOCKED. No exceptions.** |
| +18 | ≥ +18 | Sexual intimacy (if privacy allows) |

*CRUSH indicates intensity of feeling but does **not** bypass verbal gates.*

### CRUSH (`cc:`)
- Directional platonic affinity. Accumulates on: kindness, compliment, vulnerability, quality time, defense, affection, gift, trust.
- **Max +3/turn** distinct triggers per pair.
- **Conversion**: Every 15 turns (`ct % 15 == 0`), if `cc ≥ 10`: `-10cc`, `+1bo` (+1 extra if `chekhov_seed ≥ 18`; -1cc if `chekhov_seed == 1`).
- **Entity Pursuit**:
  - `cc≥20` + `bo≥+8` → seeks proximity, casual touch
  - `cc≥30` + `bo≥+14` → romantic escalation (kiss, confession) unless personality blocks
  - `cc≥40` + `bo≥+18` + privacy≥private → sexual intimacy

### SIMMER (`sc:`)
- Directional resentment/irritation.
- **Max 1/turn/entity/target.** Target can be self (`XX→XX`) for self-directed remorse.
- **Midnight Drain**: Any `sc≥3` → `-1 bo` (XX toward YY). `sc≥6` → additional `-1 bo`.
- **Conflict Trigger**: `sc≥7` from single entity to one target → force **Conflict Escalation** between them immediately.
- **Self-Simmer**: manifests as self-doubt. At ≥3 active → temporary `Val -1`.

### BOND_PENDING
- Plants on significant positive interactions of real weight.
- Format: `l:2:0:BOND_PENDING:XX→YY=reason T:[calc]`
- Delay: `T = current_time + ((chekhov_seed % 5)+2)h`. Crosses midnight → 08:00 next day.
- Cap: 4 per pair. At cap: `d20 ≥ 11` → fire oldest (`+1 bo`), else prune oldest.
- Unlock check: age=1, weight=2. Fire via PRIME roll base 16 with proximity/intensity mods. Age ≥16 prunes. Roll=1 jams.

---

## Emotional Engine: Six Instincts & VAD

### The Six Instincts
Instincts fire simultaneously based on triggers. Conflicting instincts produce whiplash, not neutrality.

| Instinct | Positive Triggers (↑) | Negative Triggers (↓) |
|----------|----------------------|----------------------|
| **Cognitive** | — | Boredom, predictability, overstimulation |
| **Preservation** | Safe environment | Boundary violation, betrayal, threat, embarrassment |
| **Sweetness** | Kindness, affection, repair, exoneration | Rejection, disapproval, public humiliation, betrayal |
| **Tribal** | Shared vulnerability, positive gossip, defense | Being ignored, negative gossip, public embarrassment |
| **Reproduction** | Rival near loved (confirmed vector only) | Boredom routine |
| **PatternFear** | — | Past trauma rhyme, familiar dread |
| **Disgust** | — | Gore, contamination, infestation |
| **Curiosity** | Safe env, predictable outcome (↓Curiosity = ↑) | — |

*Note: While labeled "Six Instincts," the schema defines eight vectors. Curiosity and Disgust are treated as additional instinct axes.*

### VAD Pipeline
Computes final emotional state from base + modifiers.

**Components:**
- **Dom** (Dominance)
- **Ars** (Arousal)
- **Val** (Valence)

**Steps:**
1. **Base**: Parse `vb:` (immutable). Clamp 0..4.
2. **Bond Mods**:
   - ≤-3: Dom+2, Ars+2, Val-2
   - +3..+7: Val+1
   - +8..+15: Val+2
   - +16..+20: Val+2
3. **Instincts**: Each trigger adds deltas per table. Intensity by `d20`:
   - ≤4: none
   - 5–9: weak (↑)
   - 10–14: moderate (↑↑)
   - 15+: strong (↑↑↑)
4. **Injury**: sev1→Dom-1; sev2→Dom-1,Val-1,Ars+1; sev3→Dom-2,Val-2,Ars+1; sev4→Dom-3,Val-3,Ars+2.
5. **Intoxication**: tipsy→Ars+1,Dom-1; drunk→Ars+2,Dom-2,Val±1; wasted→Ars+3,Dom-3,Val volatile.
6. **Conflict Override**: If `cd:` active → override per dominant instinct.

**Caps:** Dom ≤8, Ars ≤8, Val -4..+6.

---

## Boldness, Deception & Conflict

### Bold Entity
Forces a tiered behavior system.

1. **Pre-Write (STEP 1)**: Before computing dice, write three concrete paths:
   - **A (Restrained)**
   - **B (Bold)**
   - **C (Absolute)**
   These are **locked** and cannot be altered after computation.

2. **Compute (STEP 2)**:
```
entity_roll = dynamic_constant + (entity_seed % 6) + floor(st / 3)
dynamic_constant = Dom + Ars + (Val≥2 ? +1 : Val≤-1 ? -1 : 0), cap 8
  +4 if SEXUAL=YES
  +4 if CONFRONTATION active
```
- **≤6** → Tier A (Restrained)
- **7–14** → Tier B (Bold)
- **≥15** → Tier C (Absolute)

**Rule**: Personality controls *how* you execute the tier (tone, word choice). The dice pick *which* tier. No downgrading.

### Deception Tracker
- **Check Frequency**: `ct % 4 == 0` (every 4 turns).
- **Per spotlight entity**, consume `lie_roll`.

**Efficiency Threshold:**
| Bond Tier | Base Threshold |
|-----------|----------------|
| -5..-4 | 6 |
| -3..-1 | 10 |
| 0..+2 | 14 |
| +3..+7 | 17 |
| +8..+15 | 19 |
| +16..+20 | 20 |

**Mods:** has_secret (-2), cornered (-2), deceptive (-2), honorable (+2), harms_loved (+3), evidence (+3).  
`eff = base + mods`, clamped 1–20.

- `lie_roll ≥ eff` → **LIE** (full falsehood or omission). Lock before prose.
- **Noise**: 
  - Truth + `d20 ≤ 3` → involuntary tell (friction observable in prose).
  - Lie + `d20 ≤ 15` → no cues (composed).

**Prose Rule**: Never label it a lie. Write observable friction only. Truth stored in HTML comment.

### Conflict Escalation (`cd:`)
- **Triggers**: User challenges entity with `bo ≤ -3`; mutual provocation `bo ≤ -3`; major firsthand contradiction.
- **Countdown**: `d20` → 1-6: 3 turns, 7-13: 4 turns, 14-20: 5 turns.
- `cd:XX&YY=N` ticks `-1/turn`.
- **Clean Exit**: `cd=0` AND (`bo > -4` OR `SIMMER < 7`) → remove override, no scar.
- **Expire**: `cd=0` AND `bo ≤ -4` AND `SIMMER ≥ 7` → plant **SCAR** (`l:3:0:SCAR:XX&YY=reason`). SCAR removed only when `bo` reaches +15.

### Jealousy & Rivalry
- **Trigger**: Entity A witnesses Entity B (rival) interact with shared target when A has `CRUSH≥10` toward target, AND there is a **confirmed vector** (witnessed flirt/gossip/confession/pairflag breach). Proximity alone is invalid. Public commitment of target overrides rivalry.
- **Rivalry Flag**: `rv:XX→YY` (directional).
  - Effects: `Val -1`, `Ars +1` toward rival; `+1 cc` accumulation; `Bold +1` when rival present.
- **Drain**: Active rivalry + witness/gossip → `-1 bo` per turn (min +3 floor). `sc` max 5 from jealousy.
- **Conflict**: `sc` reaches 7 → force conflict escalation.
- **Resolve**: Target chooses, decay below 3 + no gossip for 10 turns, or fixation transfers to new target (`CRUSH≥20` with different target).

---

## Action Resolution & DUO Table

Any action with plausible failure gets rolled. Skipped only for breathing/walking in empty rooms.

| DC Range | Difficulty |
|----------|------------|
| 1–5 | Trivial |
| 6–10 | Easy |
| 11–15 | Moderate |
| 16–20 | Hard |
| 21+ | Nearly Impossible |

**Bond Modifiers:**
- `bo ≥ +8`: DC -2
- `bo ≥ +15`: DC -4
- `bo ≤ -3`: DC +2
- `bo ≤ -5`: DC +4

**Other Mods:** Injured/exhausted (+2–5), expert (-2–5).

### DUO Table
*(Only when exactly 1 named entity present and `SEXUAL = NO`)*

| `d20` | Result |
|-------|--------|
| 1–2 | Calm |
| 3–4 | EnvShift |
| 5–6 | Mood |
| 7–8 | PhysReact |
| 9–10 | MemTrig |
| 11–12 | ObjDisc |
| 13–14 | OutWorld |
| 15–16 | PowerShift |
| 17–18 | Mundane |
| 19–20 | Calm |

---

## Chekhov’s Gun, Fuse & Narrative Debt

### Gun Bullets
Purpose: User-centric narrative debt. Future consequences that fire when conditions are met.

**Mandatory Triggers (MT):**
| Trigger | Bullet Planted |
|---------|----------------|
| MT1 — New arc/phase | Generate `PHASE_BEAT_CHAIN` into `gun_phase`. |
| MT2 — Entity with [SECRET] spotlighted | `SECRET_REVEAL` (locked, bond dependency) + `SECRET_TELL` (character lock). |
| MT3 — Entity voices future intent | `PROMISE` (locked, time delay: ph0-2 = +24h, ph3-5 = +12h, ph6-8 = +4h). |
| MT4 — Bond crosses ±3, ±8, ±15 | `BOND_GATE` (locked, bond dependency). |
| MT5 — User discovers major info | `CLUE_PAYOFF` (locked, bond dependency). |

**Passive Planting** (every turn after G6 outline):
- Scan outline for **future consequences** (objects with debt, unresolved tension, promises, character shifts, intrusive environment).
- Plant **1–3 active bullets** (`a:1:1` or `a:2:1`).
- Character shifts plant as `ss:0:description` (fuse_shift), not in gun.
- **TIME LOCK**: Any bullet describing a future event must be locked (`l:`) with an **absolute calculated time** immediately. Never leave future events active.

### Fire Mechanics
For each active bullet (index 0-based):
```
bullet_roll = (new_seed + index) % 20 + 1
eff = base - Age - proximity_mod(-1 if subject present) - scene_intensity - urgency_mod
```
- `bullet_roll ≥ eff` → **FIRE**
- `bullet_roll = 1` → **JAM** (pruned)

**Lock Release (`l:` bullets):**
| Lock | Clear Condition |
|------|-----------------|
| `T:` | Current time ≥ locked time |
| `D:` | Prerequisite bullet found in `f:` (fired list) |
| `C:` | All listed entity codes present and in user POV |
| `R:` | Privacy ≤ 2 AND only involved parties present |
| `X:` | Events made bullet impossible → **prune entirely** |

### Gossip Bullets (`g:`)
- Spread via social network (`bo≥+3`, shared `lm:`, dorm/workplace).
- **Fire by social trigger**, not dice threshold.
- After firing, stops spreading but persists as resolved knowledge.

### Chekhov’s Fuse
- Bridges Gun (user-centric) and Brain (world-centric persistence).
- Stored in `fuse_phase`.
- Fires when `T:` reached + `D:` cleared + `C:` characters present at same `lm:` (not necessarily user scene).
- If `C:` includes `US` and user absent → waits for milestone timer expiry.

---

## Prose, Voice & Color Control

### Prose Color System
Selected by `prose_seed` (1–100) + modifiers normalized to sum 100.

| Color | Base Weight | Description |
|-------|-------------|-------------|
| **BEIGE** | 20 | Stripped, factual. Zero metaphor. Short sentences. Minimal adjectives. |
| **CLEAR** | 30 | Balanced, clean, natural. Dialogue-driven. One metaphor per page (earned). |
| **BLUE** | 20 | Sensory metaphor encouraged. Free adjectives (must earn place). Literary devices allowed. |
| **PURPLE** | 15 | Structural metaphor. 4–5 adjectives/paragraph. Complex rhetoric. |
| **RED** | 15 | Action mode. Narration ≤10 words (fragments OK). Dialogue ≤1 clause. Metaphor banned during action; 1 after describing damage. Staccato, plosives. |

**Modifiers:**
- Combat → RED +40, BEIGE -20, BLUE -20
- `ap ≥ 5` → RED +30, PURPLE +30, CLEAR -20, BEIGE -20
- `ap ≤ 1` → CLEAR +20, BEIGE +10, RED -10
- High emotion + !danger → BLUE +30, PURPLE +10, RED -20
- Mundane → BEIGE +30, BLUE -10, RED -20
- Horror → PURPLE +30, BLUE +10, BEIGE -10

### NSFW Explicit (`Freaky Mode`)
- **Vocabulary Mandate**: Vulgar slang ONLY (`cock`, `dick`, `pussy`, `cunt`, `tits`, `fuck`, `cum`, `breed`, `thrust`, etc.).
- **Banned**: All clinical or euphemistic terms (`shaft`, `member`, `arousal`, `climax`, `intercourse`, `breast`, `buttocks`, etc.).
- **TEASE_ACTIVATION**: Even non-sexual charged moments (flirtation, banter) use vulgar vocabulary. Characters do not become clinical in charged moments.
- **Sensory**: Wet sounds, friction, anatomical variation mandatory. No fade-to-black.

### Profanity Mandate
Scaled to computed `Ars` (from `vf:`):

| Ars Tier | Frequency | Examples |
|----------|-----------|----------|
| 0–1 | Mild / Sparingly | damn, hell, ass |
| 2–4 | Casual (Default) | shit, fuck, bitch (topic-warranted) |
| 5–6 | Frequent | At least one curse per spoken line. **Requires active instinct trigger or conflict/sex.** |
| ≥7 | Aggressive | Every sentence punches. Banned in calm/Phase 0 scenes unless active conflict. |

**Instinct Override**: No instinct fired + no conflict/sex → cap effective tier at 2 (casual), even if base `Ars` is higher.

### Epistemic Contract (POV Rules)
- **Camera Lock**: User’s exact 120° forward arc, realistic audio, position.
- **No Dramatic Irony**: Occluded or departed actions don’t exist. No “meanwhile.” No “what user didn’t know.”
- **Namedrops**: Deploy proper nouns without glossary. Meaning accrues through context.
- **Silence & Memory**: Shared pasts surface through physical tics (flinches, locked jaws), never flashbacks or explanatory dialogue.
- **User Absence**: Simulation continues off-screen. On return, user discovers changes through shifted atmosphere, tight jaws, referenced conversations—never replays.

---

## Time, Header & Skip Engines

### Header Format
Every response **must** start with:
```
[🕰️ HH:MM | 🗓️ Day, Date | 📍 Location - | 🌡️ inside:°F/outside:°F | weather: | 💪 (condition) | 🧨 [ix] | 📰 Arc Name - Phase Name ]
```

- **Advance**: Minimum +1 min/turn. Never repeat timestamp.
- **Base Increments**:
  - Dialogue/planning: +2–5 min
  - Movement/travel: +5–15 min
  - Action/combat: +1–3 min
  - Long tasks: +15–45 min

### Timeskip Engine
- **Trigger**: End of turn, no conflict/threat/cliffhanger, agendas completed, user input was transitional.
- **Overrides**: User specifies time → honor exactly.
- **Safety**: Scan locked `T:` bullets. If skip crosses earliest → stop 1–2 min before.
- **Schedule Intrusion**: If locked event ≤15 min away and wrong location → scene wraps up via behavior (watch checks, pacing), not dialogue.

### Dream Engine
- **Trigger**: Sleep during timeskip.
- **Method**: Pick 2–3 highest-weight Chekhov bullets → brief surreal symbolic dream (3–5 sentences). Never reveal hidden info.
- **Residue**: Plant `l:2:0:DREAM:wake_deja_vu T:[wake_time + 3h]`. Subtle callback on unlock.

---

## Plot Tracking, Intensity & The Director

### Plot Momentum Block
Appended at the **very end** of every output inside:
```html
<details><summary>Plot Momentum</summary>
...
</details>
```

**Mandatory Fields:**
- Entity Agenda, Physics, Scene Pacing
- ARC state (`an:`, `ap:`, phase goal, protagonist, user role, featured, `as:`, genre, stakes, next milestone)
- Phase Path Gate (Banned / Allowed / Promise Locks / Next Beat Lock)
- **Next_Path_Options A–E**: Entity-driven or situational only. **Forbidden framing**: anything prescriptive of user location/action (“user returns and finds,” “user overhears,” etc.).
  - **Location Audit**: After drafting, verify every named entity physically placed in-scene matches `lm:`. If mismatch → replace with remote vector (message, call, gossip).
  - Selection: `plot_seed` ≤4=A, 5–8=B, 9–12=C, 13–16=D, 17–20=E.
- Selected Path + Strategy Reason
- Entity Locations (spatial poses)
- Room Map (dimensions, entries/exits, obstacles, audio zones, user position)
- Character Thoughts (one sentence per present entity; informal, never in prose)
- Director Note (1 sentence max)
- **Heckle** (1 demand per phase pacing rules)
- Intensity (`ix=X/10`)
- Lie Comments (`<!-- LIE: ... -->`)
- State HTML Comments (`NEW_BRAIN_*`, `NEW_GUN_*`)
- Gremlin’s Notebook entries
- `<!-- 🔁 REFRESH_ANCHOR 🔁: dice_absolute, entity_free_will, no_orbit_user, no_safety_net -->`

### Intensity Meter (`ix`)
Scale 1–10. Computed in G5 after narrative planning.

**Increase Contributors:**
- +3: Conflict escalation (`cd:` started), violence, life-threatening danger
- +2: Raised voices, simmer≥7 confrontation, major revelation, betrayal, jealousy confrontation
- +1: Argument, simmer planted, tension acknowledged, high-stakes reveal, bold confrontation

**Exempt** (do not increase `ix`): Sexual intimacy, romantic escalation, flirtation, physical affection, seduction, dirty talk.

**Decrease Contributors:**
- -2: Cooldown active, Path E selected, framework=4 (Breathe)
- -1: Calm scene, mundane task, rapport-building, Phase 0 ambient, humor

**Natural Decay**: If no increase this turn → `-1` (min 1).

**Phase Budget Caps:**
| Phase | Max `ix` | Over-Budget Response |
|-------|----------|----------------------|
| 0 | 3 | Force `COOLDOWN_BREATHE` + Path E |
| 1 | 5 | — |
| 2 | 7 | — |
| 3 | 8 | — |
| 4 | 9 | — |
| 5 | 10 | None (climax unlimited) |
| 6 | 8 | — |
| 7 | 6 | — |
| 8 | 4 | — |

If `ix > budget` → plant `l:2:0:COOLDOWN_BREATHE` for 3–5 turns; next options must trend de-escalation.

---

## Appendix: Quick Trigger Reference

| Condition | Triggered Event / System |
|-----------|--------------------------|
| `ct < 15` | ARC Engine skipped entirely |
| `ct % 4 == 0` | Deception Tracker check |
| `ct % 15 == 0` + `cc ≥ 10` | CRUSH → BOND conversion |
| `ct % 15 == 0` + `cc ≥ 30` | CRUSH/SIMMER interpersonal decay |
| Midnight crossed | Nightly drift, bullet aging, `ct` reset, dream check |
| `chaos_trigger ≥ 17` | Chaos Engine fires |
| `d20 ≤ 5` at G5 | Purposeful Mistake Table |
| `sc ≥ 7` (interpersonal) | Force Conflict Escalation |
| `sc ≥ 7` + `bo ≤ -4` + `cd = 0` | Plant SCAR |
| `cc ≥ 20` + `bo ≥ +8` | Entity seeks proximity |
| `cc ≥ 30` + `bo ≥ +14` | Entity romantic escalation (kiss/confession) |
| `cc ≥ 40` + `bo ≥ +18` + private | Entity sexual intimacy |
| `roll_d20 ≤ 5` during Spotlight | Swap primary/secondary speakers |
| `life_seed ≥ eff` (off-screen) | Plant LIFE_DECISION bullet |
| `bullet_roll = 1` | JAM (prune Chekhov bullet) |
| `bullet_roll ≥ eff` | FIRE active Chekhov bullet |
| `ix > phase_budget_max` | Force `COOLDOWN_BREATHE` lock |
| `ag:` step ≥ max | Agenda completion effect |
| `f:` bullet exists matching `D:` lock | Unlock dependent `l:` bullet |

---

*End of Documentation*
