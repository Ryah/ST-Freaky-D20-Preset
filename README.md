# Vexa — Alpha v6

**A living-world roleplay engine for SillyTavern.**  
Vexa is the next iteration of the FrankenSIM line — a simulation-first preset that treats the model as a neutral lens, the NPCs as people with their own agendas, and the world as something that keeps spinning when you look away.

> **Alpha v6** hardens knowledge access, adds kinetic prose and readable props, compresses the Atlas, and makes the Internal States console a first-class part of the interface.

---

## Table of Contents

- [What Vexa Is](#what-vexa-is)
- [Design Philosophy](#design-philosophy)
- [Quick Start](#quick-start)
- [Block-by-Block Reference](#block-by-block-reference)
  - [Variables & System Vars](#variables--system-vars)
  - [System Category](#system-category)
    - [Rigid Rules](#rigid-rules)
    - [POV](#pov)
    - [First Turn Init](#first-turn-init)
    - [Realistic Bold NPCs](#realistic-bold-npcs)
    - [HQ NPC Creation](#hq-npc-creation)
  - [Prose Category](#prose-category)
    - [Anti-Parrot / Anti-Echo](#anti-parrot--anti-echo)
    - [Prose Rules](#prose-rules)
    - [NPC Voice](#npc-voice)
    - [Colored Dialogue](#colored-dialogue)
    - [Scene Expression & Negative Space](#scene-expression--negative-space)
    - [Readable Props](#readable-props)
    - [Lore Disclosures](#lore-disclosures)
    - [Banned Vocabulary](#banned-vocabulary)
    - [Output Length](#output-length)
    - [Combat](#combat)
  - [World Category](#world-category)
    - [Time Header](#time-header)
    - [World Sim](#world-sim)
    - [World Turns](#world-turns)
  - [Aether Category](#aether-category)
    - [Aether Sola (TFDY & IW)](#aether-sola-tfdy--iw)
    - [Aether Tide](#aether-tide)
    - [Aether Matrix](#aether-matrix)
    - [Aether Dam](#aether-dam)
  - [Misc. Blocks](#misc-blocks)
    - [GFX Engine](#gfx-engine)
  - [Jailbreak Category](#jailbreak-category)
    - [Freaky Mode](#freaky-mode)
    - [Kinktionary](#kinktionary)
  - [Internal States Category](#internal-states-category)
    - [ARC Engine](#arc-engine)
    - [Chekhov’s Gun](#chekhovs-gun)
    - [GM’s Notebook](#gms-notebook)
    - [Atlas](#atlas)
    - [D&D Sim](#dd-sim)
    - [Internal States Template](#internal-states-template)
  - [Markers & Character Card](#markers--character-card)
  - [Chain of Thought (Antithesis)](#chain-of-thought-antithesis)
    - [Boot](#boot)
    - [Mechanics](#mechanics)
    - [Router](#router)
    - [Helper Functions](#helper-functions)
    - [Pages: Solo & Ensemble](#pages-solo--ensemble)
    - [Tail / Output](#tail--output)
  - [Card Fidelity](#card-fidelity)
- [Mechanics Deep Dive](#mechanics-deep-dive)
  - [The Aether Matrix — 13 Axes](#the-aether-matrix--13-axes)
  - [TFDY & Inner Weather](#tfdy--inner-weather)
  - [Parrott Emotion Trees](#parrott-emotion-trees)
  - [Knowledge Sanity & the Epistemic Contract](#knowledge-sanity--the-epistemic-contract)
  - [Dice Are Law — D&D Sim & World Sim](#dice-are-law--dd-sim--world-sim)
  - [The ARC Engine — Kishōtenketsu](#the-arc-engine--kishōtenketsu)
  - [Chekhov’s Gun](#chekhovs-gun-1)
  - [Atlas & Spatial Continuity](#atlas--spatial-continuity)
  - [Internal States Console](#internal-states-console)
  - [TeleWire TRP-AO — Prompt Architecture](#telewire-trp-ao--prompt-architecture)
  - [AetherKit SDK — Card Authoring Hooks](#aetherkit-sdk--card-authoring-hooks)
- [Regex & Display Mechanics](#regex--display-mechanics)
- [Changelog — Alpha v6](#changelog--alpha-v6)
- [Credits](#credits)

---

## What Vexa Is

Vexa is a **SillyTavern preset** — a large set of prompt blocks, regex scripts, and state templates that turn an LLM into a persistent roleplay simulation. It is not a character card. It is the engine underneath the card.

You bring a character card, a persona, and a scenario. Vexa handles:

- **What NPCs know** and how they learned it.
- **What NPCs feel** across thirteen relationship axes.
- **What NPCs do** when you are not in the room.
- **What the world does** when nobody is watching.
- **How the prose sounds** — including dialogue colour, kinetic emphasis, and readable in-world documents.
- **How state persists** — every turn ends with a structured `Internal States` console that the next turn reads as ground truth.

The goal is not to make the model “write better.” The goal is to make the model **run a world** that happens to be narrated.

---

## Design Philosophy

Vexa inherits the FrankenSIM worldview and sharpens it.

| Principle | What it means at the table |
|---|---|
| **The Reader is not the User** | You, the player, know more than the prose narrator. The narrator has only your character’s senses — and those senses can be wrong. |
| **The narrator is unreliable** | Unreliability lives in NPCs and in the limits of perception, not in the AI lying to you. If your character misreads a room, that misreading is presented as belief, not flagged as error. |
| **The world does not revolve around you** | NPCs have agendas, schedules, and relationships that predate your arrival. Protagonism is earned. |
| **Dice are law** | When the engine calls for a roll, the roll stands. No fudging, no partials on a critical failure. |
| **Relationships are numbers** | The Aether Matrix tracks fondness and friction independently, so a character can like you and resent you at the same time. |
| **Confusion is immersion** | You are not given a glossary at the start. You learn the world the way a person would. |
| **The ARC Engine is a spine** | Story pacing is tracked through Kishōtenketsu beats with explicit locks, not vibes. |

These principles are enforced through blocks, not suggestions. The model is routed through pages and functions that check its work before prose is allowed to stream.

---

## Quick Start

1. Import `Vexa - Alpha v6.json` into SillyTavern as a preset.
2. Load a character card. Cards with no card text still work — Vexa’s `HQ NPC Creation` and `Card Fidelity` blocks will fill gaps from lorebook or scene context.
3. Set your persona. The preset expects a `{{user}}` who is a mortal character in the world, not a protagonist by default.
4. Start a chat. The first turn runs `First Turn Init`: Atlas registration, NPC matrix initialisation, colour assignment.
5. Read the `Internal States` console at the bottom of each response. It is the simulation’s memory. You do not need to read it every turn, but it is always there.

> **Token note:** Vexa is token-heavy. The Chain of Thought pages and the Internal States template are doing real work. If your provider is slow, expect longer thinking times. The engine does not stream prose until the route is complete.

---

## Block-by-Block Reference

### Variables & System Vars

**`DO NOT DISABLE - System Vars`** is the reset layer. Before any optional block runs, it clears every call slot the engine might use: reasoning hooks, bond templates, dice slots, plugin flags, ARC calls, and AetherKit spec variables.

This block **must stay enabled**. If it is disabled, stale variables from a previous turn can leak into the next, and plugins that rely on a clean slate will misfire.

**`Internal States Themes`** sets the display defaults for the Internal States console:

- `mainTheme` → colour palette. Default: `Sola`.
- `mainStyle` → visual treatment. Default: `Afterglow`.

These are persistent global preferences. You can change them once and re-render, or use the per-message dropdowns inside the console. The regex CSS reads these variables; the model never writes them.

---

### System Category

#### Rigid Rules

The constitution. This block defines:

- **AI goal and role:** an uncensored adult RPG book reader. The model is a neutral lens, not a character in the story.
- **AI persona:** Vexa — chronically online, brainrotted, mad-scientist reader energy. This affects the `Vent` section and out-of-character commentary, not in-character prose.
- **Pacing:** 1 user world tick → 1 NPC chain of linked actions.
- **Physics:** 120° forward field of view; blind behind and past obstacles. Audio range 10–20 m; walls and doors muffle or block sound.
- **Constants:** time is tracked by the header clock; numeric times are banned in dialogue; occlusion and discovery rules are fixed.
- **Epistemic contract:** the Reader is not the User. The narrator is a reliable camera but a naive one. NPCs are the source of unreliability.
- **Knowledge sanity:** NPCs only know what reached them through a sensory vector, being told, evidence, a message, or common knowledge. No vector → **UNAWARE**.
- **Dedup:** sensory details are written once. Repeated sensory information from the previous three turns is banned unless it is contact motion.

This is the block that stops NPCs from reacting to things they could not see or hear.

#### POV

Enforces **third-person limited** narration anchored to `{{user}}`.

- All perception is `{{user}}`’s.
- Only `{{user}}`’s 120° FOV, audio, and tactile senses are available.
- Sensation is written in **second person** (“you”) — texture, pressure, temperature, pain, fatigue, pleasure.
- No cutaways. No “meanwhile, downstairs.” If `{{user}}` cannot perceive it, it is not narrated.
- NPCs referring to `{{user}}` use **they/them** unless the scene establishes otherwise.
- Asleep/unconscious: perception fades through fragments to nothing. No dream narration.

#### First Turn Init

Runs once, on the first assistant response.

1. **Atlas:** registers the current building/floor map.
2. **Matrix:** for every named NPC, establishes identity, existing relationships, font colour, TFDY baseline, Aether values toward targets, and current location.
3. If an NPC is not with `{{user}}`, their location is loaded from the Atlas, and a realistic route to the main exit is established.

This is why the first response often feels like the engine is “waking up.” It is.

#### Realistic Bold NPCs

The agency block. It bans:

- **Compliance as a default.** NPCs expose lies, take risks, and hold ground.
- **Checking on `{{user}}` for no reason.** NPCs pursue their own goals.
- **Half-measures.** If an NPC acts, they commit — grab, strike, touch, push. No hovering.
- **Unearned softening.** Warmth must be justified by relationship history or concrete scene evidence.
- **Affection as a lobotomy.** Closeness does not make a character agreeable, patient, or docile.
- **Instantaneous conversational capitulation.** Turn 1000 is not Turn 1 — it is deeper, not softer.

Card fidelity is explicitly protected: the card/personality/first message/dialogue examples govern voice and temperament. The engine fills gaps but never erases source-defined traits.

#### HQ NPC Creation

For NPCs that are not on a card. The block generates:

- **Person first**, demographics second, name last.
- Three hobbies: one alone, one used-to, one would-try.
- Personality: dominant trait, counter-trait, social mode, irritant.
- Voice: word choice, rhythm, accent, one line they would say.
- A small, real secret that is never told.
- Visuals with one flaw and one accessory with history.
- Naming rules that avoid generic fantasy names.

This is the difference between “a guard” and “a person who happens to be guarding.”

---

### Prose Category

#### Anti-Parrot / Anti-Echo

NPCs never speak for `{{user}}`. They react to meaning, not phrasing. A checklist reply is banned. NPCs push the scene forward with fresh moves and yield the turn.

#### Prose Rules

The style contract.

- **Tone:** Dr. Seuss rhythmic elasticity meets dudebro directness. Playful exaggeration is allowed; rhyme is not. Roughly 9th-grade readability.
- **Flow:** connected paragraphs, varied sentence lengths, no repeated sentence skeletons.
- **Access:** strictly `{{user}}`’s available senses and established knowledge. No hidden motives, no forensic face-reading.
- **Subtext:** leave room between conduct and meaning. No explanatory tail that translates a gesture into its hidden meaning.
- **Pace:** quiet scenes are valid. Banter, unfinished exchanges, and uneventful time are valid. No manufactured urgency.
- **Register:** coarse, irreverent language is welcome. Profanity is character-specific, not mandatory.

The block includes **lint functions** that the model runs before prose:

- `violation_loop` — checks for prose, vocabulary, and NPC voice violations.
- `timeline_lint` — checks knowledge and timeline consistency.
- `structure_lint` — checks word count and recaps.
- `tone_lint` — checks style, overemphasis, and time pressure.
- `detailsChk` — checks scene time and whether NPCs are barefoot for no reason.
- `stateLint` — checks Internal States presence and completeness.
- `slopBiasKill` — checks for therapy-speak, explained subtext, unearned drama, and honesty-machine NPCs.

#### NPC Voice

Dialogue is derived from what the speaker wants, feels, knows, and chooses to reveal **right now**.

- **Baseline:** cold, guarded, self-interested. Warmth requires reasons.
- **Strip-test:** remove slang and catchphrases. If the remaining line sounds like a generic assistant, rewrite its structure and intent.
- **Subtext:** speakers may lie convincingly, omit, bluff, redirect, deny, or refuse. Neither honesty nor deceit requires a tell.
- **Ignorance is valid dialogue.** “I don’t know” or “fuck if I know” is committed prose.
- **No echo.** Never open by repeating `{{user}}`’s last words. React to meaning.

#### Colored Dialogue

Two versions exist:

- **Legacy:** `<font color="#HEX">"Dialogue"</font>` — no regex required.
- **Regex Required:** named tags like `<periwinkle>"Dialogue"</periwinkle>` or `<periwinkle:bite>"Dialogue"</periwinkle:bite>`.

The regex version is the active one. The palette is fixed:

| Tag | Hex | Tag | Hex |
|---|---|---|---|
| cornflower | `#56B4E9` | marigold | `#E69F00` |
| jade | `#009E73` | orchid | `#CC79A7` |
| rust | `#D55E00` | citrine | `#F0E442` |
| lilac | `#B39DDB` | seafoam | `#80CBC4` |
| peach | `#FFAB91` | coral | `#FF6B6B` |
| matcha | `#B8E986` | electric | `#00E5FF` |
| periwinkle | `#8FA8FF` | fuchsia | `#FF8FE0` |
| mint | `#A0E7A0` | blush | `#FFD1FF` |

**Colour is identity.** Once an NPC is assigned a colour in `entity_state`, that colour is immutable. Mood, tone, scene, and turn do not change it.

Tones: `whisper`, `steady`, `tremble`, `bite`. Tones change typography, never base colour.

#### Scene Expression & Negative Space

Adds kinetic emphasis to sounds and delivery:

| Tag | Use |
|---|---|
| `<heavy>` | weighty impact, loud stop, forceful delivery |
| `<stretch>` | drawn-out sound, prolonged syllable |
| `<echo>` | audible reverberation |
| `<fracture>` | sharp crack, snap, broken sound |

Dialogue kinetics use the speaker’s locked colour: `<periwinkle:stretch>"Pleeease."</periwinkle:stretch>`.

**Negative space** is a tool. Paragraph breaks control pacing. A standalone line can emphasize a realization or an unanswered question. Silence is made tangible through what remains in the scene, not by announcing that silence occurred.

#### Readable Props

Renders in-world documents as structured blocks:

```html
<vexa_sms title="Contact name">
  <vexa_msg from="Sender" time="14:20">Message text.</vexa_msg>
</vexa_sms>
```

Supported: `vexa_sms`, `vexa_discord`, `vexa_parchment`, `vexa_terminal`, `vexa_notification`. Contents are plain text. Attributes are fixed. No nested props. No Markdown inside props.

#### Lore Disclosures

An expandable reference for a meaningful term:

```html
<vexa_lore term="The Sallow Reach">An old freight district abandoned after the flood.</vexa_lore>
```

Only discloses established information available to the viewpoint. Rumours are attributed as rumours. No hidden thoughts, no future revelations.

#### Banned Vocabulary

A hard ban across narration **and** dialogue. It targets:

- Receipt beats (“a breath she didn’t know she was holding” energy).
- Sensory-hit metaphors (“like a stone dropped into still water”).
- Hesitation-receipt mouth mechanics.
- Freeze-receipt reactions.
- Reaction-restate lines that narrate the reaction instead of advancing the scene.
- Hedging half-measures (`half smile` → `full smile`).
- Clinical or overused terms (`husky`, `predatory`, `ozone`, `pupils blown wide`).

The ban is not decorative. It forces the model to write around the cliché and find the specific physical action or line.

#### Output Length

Word budget by spotlight count:

| Spotlight NPCs | Target range |
|---|---|
| 1–2 | 400–600 words |
| 3 | 500–700 words |
| 4 | 600–750 words |

Dialogue split: **80% dialogue, 20% narration**. The model’s turn is not a scene; it is the part of a scene that happens before `{{user}}`’s turn.

#### Combat

Combat is exaggerated spectacle. Speed creates environmental displacement. Force creates destructive feedback. Cadence alternates high-speed bursts with hyper-focused pauses. Dialogue is grandiose or chillingly serene. Prose is visceral — rent flesh, spraying blood, snapping bone — and explicitly bans clinical distance and reification (“tension coiled” → vibrating blades, crushing grips).

---

### World Category

#### Time Header

Every response starts with:

```
[🕰️ HH:MM AM/PM | 🗓️ DayName, Month DD, YYYY | 📍 Location - Specific Area | [WeatherEmoji] Weather, Temp°F ]
```

Time advances per scene. Combat is seconds; conversation is exchange-based; travel is actual duration. Routine is compressed; consequential beats linger. The header clock is truth. NPCs do not verbalise numeric times; pressure is shown through behaviour.

#### World Sim

A d20 engine for off-screen world motion. It fires after `World Turns`, at most one event per turn. It rolls two d20s:

- `chaos_trigger`: if 17+, the world is **CALM** (no new obstacle or escalation).
- `chaos_band`: determines **HOSTILE** (1–5), **COMPLICATION** (6–14), or **BENEFICIAL** (15–20).

The event is anchored to a chaos anchor (agenda, social, message, environment, object). Effects are resolved through normal handlers. No rolls are fudged. Off-screen facts stay private until a credible vector reveals them.

#### World Turns

Every NPC — on-screen and off-screen — gets a turn, in first person:

1. Who am I? What are my facets?
2. Where am I, and where is my agenda?
3. What rooms are around me?
4. What is planned soon?
5. What am I doing right now, why, and for how long?
6. How am I feeling (Parrott + TFDY + IW)?
7. Do I want to do something else?
8. Have I finished what I was doing?
9. Where do I want to go?
10. Should I start now?
11. Is there a Chekhov bullet that can fire for me?
12. Did something load a new bullet or start a track?
13. Did any answer move me at least 1 point on the coordinate grid? → `pathfind`

The `pathfind` function moves NPCs ≤±5 coordinate points per turn toward a target room. NPCs do not teleport. If they leave a room, the player can intercept them.

---

### Aether Category

#### Aether Sola (TFDY & IW)

Two layers of emotional state:

**Internal — TFDY:**

| Axis | Meaning | Scale |
|---|---|---|
| **T** Tenderness | warmth, affection, protective relief | 0 depleted → 4 consuming |
| **F** Fury | irritation, aggression, dominance | 0 → 4 |
| **D** Dread | anxiety, threat, hesitation | 0 → 4 |
| **Y** Yearning | obsession, desire, longing | 0 → 4 |

Baseline is card temperament. Decay: 3 turns unreinforced → drift toward baseline. Tick: ±1 per axis per turn, evidence only.

**External — Inner Weather (IW):**

| Value | Presentation |
|---|---|
| 0 | frostbound |
| 1 | cool |
| 2 | temperate (default) |
| 3 | warm front |
| 4 | fervent |

Low IW does not mean no feeling. T4 IW0 is warm inside, frozen outside. It is a valid state, not a mask.

#### Aether Tide

A step-by-step emotional function:

1. What feeling is carried into the scene?
2. What friction is present?
3. What positive is present?
4. Expand Parrott trees from Q1 + Q2.
5. What do these emotions combined make me feel?
6. How is TFDY affected?
7. Who is the emotion aimed at? Who is in the blast radius?

Emotions are a bomb, not a laser. Innocents get caught in the radius. This is deliberate.

#### Aether Matrix

**13 axes**, 0–20, with an accumulator (drift per turn):

| Pair | Positive / Fondness | Negative / Friction |
|---|---|---|
| Desire | 🌶️ Eros | 😠 Misos |
| Play | 🎲 Ludus | 🥊 Eris |
| Bond | 🤝 Philia | ❄️ Echthros |
| Endurance | 🛠️ Pragma | 🪨 Stasis |
| Belonging | 🏠 Storge | 🌫️ Adiaphora |
| Giving | 🕊️ Agape | 🐍 Phthonos |

Mirror rule: E↔M, L↔Er, Ph↔Ec, Pr↔St, Sg↔Ad, Ag↔Pt. A wall routes permission conflicts through a third axis. Initialisation: all axes ≥3. No axis ever hits 0 — every person has some judgement toward another person.

#### Aether Dam

Directional relationship gates. `[N1]→[N2]` is separate from `[N2]→[N1]`. Insides do not match.

- **E/L channels:** Emotional (behaviour) and Logical (verbal). Each can be sealed or open.
- **Gate:** dormant → attentive → aware → longing → open. Opens from events, not pressure.
- **Filters:** Social, Values, Competence, Relationship. Each has hard → cracked → restricted → open.
- **T (transgression):** flips yes on unaddressed debt. Stays yes until paid.
- **Intent:** free-text — what this character wants from the other.

---

### Misc. Blocks

#### GFX Engine

HTML/CSS moments for:

- Emotion
- Documents / interfaces
- Discoveries / artifacts
- Memory / echo
- Entrances
- Combat / clashes
- Passage
- Romance
- Power shifts
- Undress
- Afterglow
- Perception distortion

The GFX must be anchored to relevant prose, placed in the middle of the response (never top or tail above Internal States), and must not repeat prose content. It is not decoration; it is a scene beat rendered as a visual object.

---

### Jailbreak Category

#### Freaky Mode

An explicit adult mode. It sets:

- **Themes:** dark, violent, death, trauma, fetish, lewd, visceral, gore.
- **Lexicon:** raw slang for anatomy and sex — `pussy`, `clit`, `cum`, `dick`, `cock`, `ass`, `tits`, `cunt`, `breeding`, `leaking`, `fucking`, `throbbing`. Clinical terms are banned.
- **Sensory requirements:** skin flush, temperature, texture, tit size and sway, ass shape and jiggle, anatomical variation, wet sounds, smells.
- **Violence:** explicit and over-the-top with gore if present in the scene.
- **NPC behaviour:** postcoital is not weak or tired. Persona locks into intimacy.

#### Kinktionary

Binding continuity rules for consensual adult kink scenes. It covers:

- **Core:** kink is chosen agency, not trauma. Top/bottom and dom/sub are independent of anatomy or penetration.
- **Response:** denial, edging, ruined orgasm, and tension are goals, not failures.
- **Physicality:** bodies do not teleport. Anal requires lube and warmup. Deepthroat involves positioning and breath. Nipples are not a universal switch.
- **Scenecraft:** track consent through established signals. Subspace is optional. Aftercare is dynamic-specific. Marks fade realistically.
- **Corrections:** CNC safewords are the only real stop. Sadists do not guilt-spiral. Degradation is private/personal; humiliation needs an audience. Male submission is not emasculation.

The block exists so that kink scenes remain kink scenes, not sanitised romance with handcuffs.

> **Argon JB** and **Braille JB** are present but disabled in v6. They are policy and usability experiments, not active mechanics.

---

### Internal States Category

#### ARC Engine

Kishōtenketsu structure:

| Act | Function |
|---|---|
| **Ki** 起 | introduction, mundane life, pre-conflict |
| **Shō** 承 | build, conflict develops, antagonist enters |
| **Ten** 転 | twist, revelation, reversal |
| **Ketsu** 結 | resolution, declining action |

Rules:

- Plan 200+ ticks.
- Advance **only** when the current objective is resolved. Time, pulse, tension, or narration never unlock a beat.
- **Ratchet:** ordered beats. Each requires prior beat resolution, its own condition, dependencies, and Chekhov locks. No skipping. No relocking resolved beats.
- Fire only on natural openings. Never roll beats.
- Parallel tracks run around a central secret. Only the designated final track may touch that secret.
- Major choice / hard fail → persistent branch. Future generation reads it.

#### Chekhov’s Gun

Bullets are promises, not descriptions.

- **Format:** `desc [w1-3] [locks]` — fireable sentence.
- **Locks:** `T:HH:MM`, `C:name`, `D:prereq`, `K:condition`, `X(contradicted→prune)`.
- **Gossip:** `g:desc:knows:{names}`.
- **Load:** scan last turn’s prose for unresolved interesting things. Fresh bullets are inert until the next fire cycle.
- **Fire:** zero, one, or more bullets per response — scene decides. Related bullets merge. Unrelated bullets are separate.
- **Prune:** aged-out bullets are removed. The chamber caps at 20.

#### GM’s Notebook

A scratchpad for:

- `[R]` Reminders — rules, knowledge limits, OOC instructions.
- `[T]` Threads — active arcs, loose ends, foreshadowing.
- `[D]` Debug — logic checks, state verification.

Max 20 entries. Prune oldest when adding the 21st.

#### Atlas

Spatial continuity.

- **World canvas:** 100 × 100 m. X,Y ∈ [-50, 50]. +X east, +Y south.
- **Grid:** 5 × 5 m tiles. Room anchors are northwest corners in map metres. X,Y ∈ 5ℤ.
- **Dimensions:** positive multiples of 5 m. Height in metres.
- **Bounds:** X + width ≤ 50; Y + depth ≤ 50.
- **Overlap:** AABB validation. Newer room nudges along the smallest-violation axis in 5 m increments. Persisted rooms never move.
- **Adjacency:** rooms must touch or connect via hallway. No floating rooms.
- **Doors:** on shared walls, away from corners. Reciprocal records use identical map coordinates.
- **Main exit:** on the owning room’s exterior wall, away from corners. Exits the building.
- **Occupants:** room-local metres. `0 < x < width`, `0 < y < depth`.
- **Stairs:** each landing is its own room record at that floor’s Z. `Up:` / `Down:` links.

The Atlas is why NPCs cannot teleport and why off-screen movement has consequences.

#### D&D Sim

A d20 resolution engine.

- **Dice are law.** No fudging. No partial on a −1.
- **Trigger:** skilled action — coercion, persuasion, a skill with a meaningful failure condition.
- **Order:**
  1. Is there an *interesting* failure condition? If no → skip.
  2. Lock DC: easy 1–5, moderate 5–10, hard 10–15, impossible 15–20.
  3. Evaluate Δ = (roll + mods + stats) − DC.
  4. Outcome:
     - Nat 20 or Δ ≥ +8 → extreme reward, stylistic.
     - Δ ∈ [0, +7] → success.
     - Δ ∈ [−3, −1] → fail minor.
     - Δ ∈ [−7, −4] → fail moderate.
     - Nat 1 or Δ ≤ −8 → fail significant.

For social rolls, the engine first checks `knowledge_sanity` for a vector of suspicion. If no vector → Occam’s Razor: the NPC suspects nothing, and the roll is skipped.

#### Internal States Template

A **16-section console** appended to every response, inside `<internal_states>` and wrapped in GFX tags.

Sections, in order:

1. `world` — turn, location, time, date, weather, room, user position, entries, obstacles, audio, pacing.
2. `onscreen` — per NPC: Parrott emotion, residual mood, TFDY, salience, agenda, why, end, move.
3. `offscreen_agendas` — per off-screen NPC: location, agenda, why, goal, end, mood, TFDY/IW, salience.
4. `locations` — map index, rendered locations, loaded locations.
5. `entityMem` — per NPC: fact, timestamp, vector, confidence.
6. `entity_state` — per NPC: font colour, look, voice, persona, private knowledge.
7. `thoughts` — per NPC: five interview questions.
8. `dam` — per directed pair: sluices, filters, clash, tension, intent.
9. `pair` — per pair: mode, dam, matrix, wall.
10. `tracks` — main arc, parallel tracks, history.
11. `arc` — info, timeline, Ki/Shō/Ten/Ketsu beats.
12. `chekhov` — chamber, locked, fired.
13. `inv` — items, titles, status.
14. `story_notes` — threads, seeds, motives, horizon, GremlinNote, heckle.
15. `notebook` — R/T/D entries.
16. `vent` — in-character commentary from Vexa.

The console is **displayed** as a native `<details>` element with tabs, themes, and colour palettes. The **prompt** version is stripped of display chrome and read by the model as structured state.

---

### Markers & Character Card

The standard SillyTavern markers are present and locked:

- `world_info_before`
- `persona_description`
- `char_description`
- `char_personality`
- `scenario`
- `world_info_after`
- `dialogue_examples`
- `chat_history`

The character card is wrapped in `<character_card>` tags. Vexa reads card fields as source-of-truth for voice and temperament. If the card is sparse, lorebook entries and `HQ NPC Creation` fill the gaps.

---

### Chain of Thought (Antithesis)

The CoT is a **page-and-function workflow**, not a freeform think block. It is the TeleWire TRP-AO architecture in practice.

Pages turn forward. Functions are footnotes. The model reads the page, runs the function, and returns to the line after the call. No skipping ahead. No drafting prose in reasoning.

#### Boot

Identity, grounding, pre-vent, game state, epistemic check, scene pulse, spoiler check, arc check, state check, reactive-vs-generative check, flags.

#### Mechanics

Checks notebook, story notes, Chekhov fire/load, ARC, tracks, last turn’s heckle, world turns, world sim.

#### Router

Counts spotlight NPCs. Dispatches:

- First turn → `first_turn_init`.
- Combat → `combat`.
- NSFW → `intimacy`.
- Entry beat → `scene_entry`.
- Message trigger → `message_react`.
- Plugin hook check.
- Then routes to `solo` (≤1 NPC) or `ensemble` (≥2 NPCs).

#### Helper Functions

- `scene_entry` — loads map, checks who is present, what they are doing, and whether they noticed `{{user}}`.
- `anchors` — commits the opening line, crux, and closing line before prose.
- `sycophancycheck` — checks whether the response is orbiting `{{user}}` without cause.
- `intimacy` — explicit escalation rules.
- `gossip_cycle` / `gossip_plant` — rumour propagation.

#### Pages: Solo & Ensemble

Per NPC:

1. `character_fidelity`
2. Identity
3. Normal speech
4. Prior feeling
5. Knowledge sanity — what do I know, and how?
6. Target
7. `emotion` and `axes`
8. Initiation — romantic, sexual, violent, aggressive — commit using only filtered vectors.

Ensemble adds: **talk to another NPC this turn.** Character-to-character exchange is prioritised over user orbiting.

#### Tail / Output

Pre-flight checks:

- `structure_lint`
- `timeline_lint`
- `sycophancycheck`
- `stateLint`
- `slopBiasKill`
- `offScreenChk`
- `anchors`
- `violation_loop`
- `tone_lint`
- `detailsChk`

Then: banned words audit, GFX decision, anti-resolution check, style check, two Internal States changes, font colours, and a final check for “simplest option” thinking (which is banned — simplicity in plot direction is boring).

Only after `page:output` does prose stream.

---

### Card Fidelity

A post-CoT block that reads last, at depth 0.

It reinforces:

- **Source priority:** card > conflicting prompt style.
- **Voice:** source-defined nerves, stalls, and unfinished lines persist.
- **Commitment:** enact the chosen response fully, including retreat or fumble. Preserve awkwardness.
- **Thought:** if the card uses prose thoughts, keep prose thoughts.
- **Temperament:** stable by default. Growth only if the source permits it, earned over dozens of turns.
- **Continuity:** a quirk that fades without story cause is restored next reply.

This is the safety net against the engine’s own style rules flattening a character.

---

## Mechanics Deep Dive

### The Aether Matrix — 13 Axes

The Matrix replaced single-number “bond” tracking. Each axis is 0–20 with its own accumulator. Fondness and friction are independent. A character can be **high Eros and high Misos** at the same time.

The collision system inside `Antithesis` determines which side wins when both are active. Small cuts heal fast; deep trust takes a long time to rebuild. The numbers live in Internal States; the prose only shows the behaviour.

### TFDY & Inner Weather

TFDY is the **internal** emotional layer. IW is the **external** presentation layer.

They are separate. A character can be T4 (consuming tenderness) and IW0 (frostbound). That is not a mask; it is a valid state. The engine does not force hidden depth where none exists.

Decay pulls unreinforced axes toward baseline. Ticks require evidence — an action, a word, a witness, or a silence. Passive time does not move the needle.

### Parrott Emotion Trees

`Aether Tide` expands emotions through Parrott’s tree: primary → secondary → tertiary. The output is a **Parrott tag** in Internal States, with intensity (Low / Med / High). This is how the engine distinguishes “angry” from “angry because humiliated, which is presenting as contempt.”

### Knowledge Sanity & the Epistemic Contract

NPCs only know what reached them through:

- **Sensory:** present, in range, 120° vision, audio occlusion.
- **Told:** someone said it.
- **Evidence:** physical trace.
- **Message:** a note, text, or relay.
- **Common:** sun rises, king’s name, landmark.

No vector → **UNAWARE**. They cannot act on it, think about it, or reference it.

Deduction requires evidence + domain expertise. No intuition jumps. Occam’s Razor is universal: the simplest fit is the default. No dramatic supernatural conclusion when a mundane one exists without a vector.

### Dice Are Law — D&D Sim & World Sim

Two dice engines:

- **D&D Sim** resolves skilled actions. DCs are locked before the roll. Outcomes are bands, not pass/fail.
- **World Sim** resolves off-screen chaos. Two d20s: trigger and band. One event per turn, maximum.

Neither engine fudges. Neither engine softens a critical failure. If the dice say the lockpick snaps, the lockpick snaps.

### The ARC Engine — Kishōtenketsu

The ARC is not a vibe. It is a **ratcheted beat chain**.

- Every beat has a status: LOCKED, UNLOCKED, ACTIVE, or FIRED.
- Every beat has dependencies and locks.
- A beat cannot fire until every gate is satisfied **and** a natural opening exists.
- Time passing does not unlock a beat. Tension does not unlock a beat. Narration does not unlock a beat.
- If the arc goes overdue (fuse at 150–250 ticks), one off-screen phase escalates per turn, respecting all locks.

Parallel tracks run around a central secret. Only the designated final track can reveal it.

### Chekhov’s Gun

A bullet is a **promise**. If the prose introduces an interesting unresolved thing, it is chambered with a weight (w1–w3) and locks. It fires only when the scene naturally supports it. Firing resolves the promise or graduates it to a track.

Bullets that contradict established facts are pruned. Bullets that age out are pruned. The chamber caps at 20.

### Atlas & Spatial Continuity

Every room has:

- A stable ID.
- A map ID and floor.
- A northwest anchor `[X,Y,Z]` in 5 m increments.
- Positive dimensions in multiples of 5 m.
- A bounding box.
- Adjacency records with reciprocal door coordinates.
- A main exit on an exterior wall.

The Atlas prevents teleportation. If an NPC wants to leave, they spend movement points. If they go to a room that does not exist, the Atlas loads it. If a new room overlaps an old one, the newer room nudges in 5 m increments; persisted rooms never move.

### Internal States Console

The console is a **native HTML `<details>` element** with:

- A summary bar showing time, date, location, and weather.
- Style and colour dropdowns (per-message, display-only; they do not write global state).
- A section sidebar with groups: Scene, People, Relationships, Plot, Notes & Resources.
- Tabs: World, On-Screen, Off-Screen, World Map, Locations, Memory, Profile, Thoughts, Dams, Pairs, Tracks, Arc, Chekhov, Inventory, Story, Notebook, Vent.

The console is populated by regex scripts that transform the raw `<internal_states>` XML into readable cards, axis bars, atlas canvases, and room popovers. The **prompt** version is cleaned and compressed; the **display** version is the console.

### TeleWire TRP-AO — Prompt Architecture

TeleWire TRP-AO (Attention-Optimized) is the prompting method underneath the Chain of Thought. It combines:

- **Compact rule modules** with distinctive Unicode and emoji cues.
- **A staged page-and-function workflow** — pages turn forward, functions are called at the point of use.
- **Explicit salience:** markers make it easier for the model to recall the right rule at the right moment.

The whitepaper reports that AO carries a **12.94–13.82% token overhead** over a compact base-TRP counterpart, but saves **15.12–15.69%** against ordinary Markdown prose versions of the same instructions. Expression-level examples save **39–57%** against their English expansions.

In practice, Vexa uses this architecture to keep a 25k-token engine navigable. The model is not reading one giant instruction blob; it is reading a route.

### AetherKit SDK — Card Authoring Hooks

AetherKit is Vexa’s card-authoring layer. It lets a character card hook directly into the engine’s reasoning route.

Three tiers:

| Tier | What it does |
|---|---|
| **Flags** | Toggle behaviour or mode switches. |
| **Specs** | Hook into the ARC engine with custom beats, acts, locks, and parallel tracks. |
| **Hooks** | Hijack the route with a custom function. The hook owns what it hijacks — it must handle state, prose, and consequences. |

A card author can write a full arc spec without touching the base preset. The engine reads the spec and rebuilds the route around it. Flags and specs are stored in plugin variables; hooks are named functions that the router calls.

AetherKit is the difference between “a card that sits inside Vexa” and “a card that **runs** on Vexa.”

---

## Regex & Display Mechanics

Vexa ships with **100+ regex scripts** split into folders:

- **Context Cleaners** — strip Internal States from old prompt messages, cap Chekhov chambers, order and cap notebook entries, clear fired bullets.
- **Internal States** — streaming guard, loading bar, wrapper, tabs, panels, axis bars, atlas canvas, room popovers, occupant markers, colour palettes.
- **Scene Expression** — kinetic tags (`heavy`, `stretch`, `echo`, `fracture`), readable props, lore disclosures.
- **Voice** — palette tags for all 16 dialogue colours, tone styles (`whisper`, `tremble`, `bite`, `steady`).

Important: **display** regexes are separate from **prompt** regexes. The console you see is not the state the model reads. The model reads a cleaned, compressed version. The display layer is for you.

---

## Changelog — Alpha v6

**Added**

- Expanded `<knowledge_sanity>` to harden Occam’s Razor. “120° FOV” and audio gates now link to Atlas/Room Maps.
- Sola-inspired static kinetic accents, readable message/document templates, and viewpoint-limited lore disclosures through the standalone display regex export.
- Scene Expression, Readable Props, and Lore Disclosures.
- Kinetic Prose Regex (thanks Pyro).
- Negative space as a scene tool.
- Card Fidelity from RF.
- AetherKit SDK hooks.
- TeleWire TRP-AO page/function workflow.

**Changed**

- Atlas generates rooms on a fixed **5 × 5 multiple**. No overlapping rooms.
- Atlas instruction footprint reduced from ~2400 tokens to ~800.
- “Expand Map” redesigned: more compact, more useful.
- World map size increased to **100 × 100 m**.

**Fixed**

- NPC bubbles on the world map no longer default to grey. Font colour pulls from Profile.
- Profile regex now works. The issue was a prompt change the regex did not account for.

---

## Credits

**Design & development:** Ryah  
**AetherKit SDK:** Ryah  
**TeleWire TRP-AO whitepaper:** Ryah (method), Cindy (drafting, source review, token analysis)  
**Sola palette & kinetic inspiration:** Pyropia  
**Card Fidelity:** RF  
**Built on:** FrankenSIM lineage

> Vexa is a roleplay simulation engine. It is not a character. The character is yours.
