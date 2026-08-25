# AetherKit SDK

**FrankenSIM's Card Authoring SDK — write your story, guarantee your pacing, own your mechanics.**

AetherKit lets character card creators hook directly into FrankenSIM's reasoning engine. You write the beats; the engine executes them. You flip the genre; the engine rebuilds itself around it. You build a mechanic; the engine routes to it.

This document is the complete reference. Start at the top if you've never seen FrankenSIM before. Jump to **Part 4** if you only need syntax.

---

# Table of Contents

- [Preface — what you are building for](#preface--what-you-are-building-for)
- [Part 1 — The FrankenSIM worldview](#part-1--the-frankensim-worldview)
  - [1. The Reader and the User are different people](#1-the-reader-and-the-user-are-different-people)
  - [2. The narrator is unreliable — and that's the User's fault, not the AI's](#2-the-narrator-is-unreliable--and-thats-the-users-fault-not-the-ais)
  - [3. The world does not revolve around the User](#3-the-world-does-not-revolve-around-the-user)
  - [4. Dice are law](#4-dice-are-law)
  - [5. The Aether Matrix — relationships are numbers](#5-the-aether-matrix--relationships-are-numbers)
  - [6. Confusion is immersion](#6-confusion-is-immersion)
  - [7. The ARC Engine — stories have spines](#7-the-arc-engine--stories-have-spines)
- [Part 2 — How the engine executes](#part-2--how-the-engine-executes)
  - [The page system](#the-page-system)
  - [The function system](#the-function-system)
- [Part 3 — AetherKit: the three tiers](#part-3--aetherkit-the-three-tiers)
  - [Tier 1 — Flags](#tier-1--flags)
  - [Tier 2 — Specs (the ARC hook)](#tier-2--specs-the-arc-hook)
    - [The fields](#the-fields)
    - [The acts](#the-acts)
    - [Beats](#beats)
    - [The lock vocabulary](#the-lock-vocabulary)
    - [The fire rule — one beat per turn](#the-fire-rule--one-beat-per-turn)
    - [Spoilers and devoweled beats](#spoilers-and-devoweled-beats)
  - [Tier 3 — Hooks (advanced)](#tier-3--hooks-advanced)
    - [The two ways a hook ends](#the-two-ways-a-hook-ends)
    - [What a hijacking function must own](#what-a-hijacking-function-must-own)
    - [Function naming and collisions](#function-naming-and-collisions)
- [Part 4 — Plugin variables and syntax reference](#part-4--plugin-variables-and-syntax-reference)
  - [The full syntax list](#the-full-syntax-list)
  - [How the blank-state pattern works](#how-the-blank-state-pattern-works)
  - [State block (persistent storage)](#state-block-persistent-storage)
  - [Custom dice](#custom-dice)
- [Part 5 — The do-not-touch list](#part-5--the-do-not-touch-list)
- [Part 6 — Debugging](#part-6--debugging)
  - [The ARC ENGINE block](#the-arc-engine-block)
  - [Common failures](#common-failures)
- [Part 7 — Full examples](#part-7--full-examples)
  - [Example 1 — a simple flag + hook (mode switch)](#example-1--a-simple-flag--hook-mode-switch)
  - [Example 2 — a full arc spec (pacing control)](#example-2--a-full-arc-spec-pacing-control)
  - [Example 3 — a custom mechanic with state + dice (full plugin)](#example-3--a-custom-mechanic-with-state--dice-full-plugin)
- [Part 8 — What's possible](#part-8--whats-possible)

---

## Preface — what you are building for

FrankenSIM is not a prompt that makes a chatbot act like a character. It is a **world simulator** with a reasoning engine at its core.

The distinction matters, because it changes what your card *is*.

A conventional character card is a personality the AI wears. A FrankenSIM card is a **scenario the AI runs** — with a living world, real relationships, dice, and a narrator who is fallible on purpose. The AI isn't pretending to be your character. It is *simulating the world that contains your character*, turn by turn, with mechanics that persist across the entire session.

AetherKit gives you a seat inside that simulation. Most card authors will only ever use the **Spec** tier — a structured arc that the engine fires on your schedule. A few will use **Hooks** to build mechanics that don't exist anywhere else. Both are covered here.

This document assumes you know nothing about FrankenSIM. Read Part 1 and Part 2 once. Then you'll understand why AetherKit works the way it does.

---

# Part 1 — The FrankenSIM worldview

These are the principles the engine is built on. You don't need to agree with them. You need to understand them, because your card will be interpreted *through* them.

### 1. The Reader and the User are different people

FrankenSIM runs on a **possession model.**

- **The Reader** is the real human reading the prose.
- **The User** (`{{user}}`) is the character the Reader inhabits.

The User is a real person inside the world with a backstory, relationships, plans, and secrets. The Reader has *possessed* them. The Reader experiences the world only through the User's senses, and — critically — **the Reader has not read the character cards.** They don't know the lore. They don't know your NPCs' secrets. They learn through play.

**What this means for you:** never write a beat that *tests* the User on backstory the Reader hasn't been given. If the story needs the User to know something, surface it in the scene first — an object, a message, an NPC line — before any choice depends on it. The engine enforces this. Your beats should respect it.

### 2. The narrator is unreliable — and that's the User's fault, not the AI's

The prose is not objective reality. The prose is **the User's experience.**

The User has a perception stat — **P** (static sensorium) and **U** (scene attention). U is rolled every scene. When U is high, the prose reports the loaded tells — the beat too long, the clipped word. When U is low, the prose asserts what the User *believes*, even when it's wrong. A masked emotion reads as the mask. A missed glance doesn't exist.

This means:

- Never rely on subtle body language to carry critical information. The Reader may literally not see it.
- If a reveal matters, put it in **dialogue, action, or an object** — something that survives a low-U read.
- Subtext is for texture, not for plot. The engine will not underline it for you.

The truth always lives in the **internal states block** — the hidden HTML state at the end of every response. The prose is the filtered lens. The state is what actually happened.

### 3. The world does not revolve around the User

FrankenSIM is built to kill protagonist syndrome. NPCs have their own lives, agendas, and goals that continue when the User isn't there. The world advances off-screen. NPCs are not waiting for the User's permission to act.

Your card's NPCs should want things that have nothing to do with the User. If every NPC exists only to react to the User, the world feels flat. Give your NPCs hobbies, grudges, errands, and secrets. The engine will run them even when the User is elsewhere — because that's what makes the simulation feel alive.

### 4. Dice are law

FrankenSIM rolls real dice, pre-rolled by the frontend before the model ever sees them. The model cannot change the outcome. It can only *interpret* it.

This means your card should **never assume a specific outcome.** The User might fail the roll. The NPC might refuse. Death is on the table. Write beats that survive failure — beats that can still fire when things go wrong, because the engine will not bend the dice to make your story work.

### 5. The Aether Matrix — relationships are numbers

FrankenSIM tracks every relationship on **13 axes** — six of fondness, six of friction, and one of self-worth.

Fondness axes: **Eros** (romantic), **Ludus** (playful), **Philia** (friendship), **Pragma** (practical), **Storge** (familial), **Agape** (selfless).

Friction axes are their mirrors: **Misos**, **Eris**, **Echthros**, **Stasis**, **Adiaphora**, **Phthonos**. The self axis is **Philautia**.

The genius of the system: **fondness and friction tick independently.** A character can love someone and resent them simultaneously. High fondness doesn't erase friction. The most interesting relationships are the ones where both are high — "I love you and I can't stand that I love you."

Your card doesn't need to do anything with this — the engine handles it. But it helps to know it's there, because it means NPCs will *feel* complex without you writing every emotion. You just write who they are; the matrix computes how they feel.

### 6. Confusion is immersion

The engine follows an epistemic contract: **namedrops without glossaries, meaning accrues through context, no explanatory prefaces.** A world that explains itself is a world that's performing. A world that lets you figure it out is a world that's alive.

Write your card's lore as if the User *already lives in the world* — because they do. Reference events and places casually. Let the Reader catch up through play. Don't write "The Accords were signed in 3021 after the war." Write "The Accords again. She always brings them up when she's scared."

### 7. The ARC Engine — stories have spines

FrankenSIM runs arcs: four-act story structures following **Kishōtenketsu** — **Ki** (introduction), **Shō** (development), **Ten** (twist), **Ketsu** (resolution). Each arc is a chain of beats — specific, fireable scenes that advance the story.

By default, the engine *generates* arcs from your card. It reads your lore, your NPCs' backstories, their wounds and agendas, and builds a story. Sometimes it's brilliant. Sometimes it guesses wrong.

**AetherKit exists to let you stop it from guessing.** The Spec tier lets you author your own arc, beat by beat, and guarantee the engine fires it on your schedule. This is the single most powerful thing AetherKit does, and it's the main reason to adopt it.

---

# Part 2 — How the engine executes

FrankenSIM runs a **Chain of Thought (CoT)** — a reasoning process the model executes before writing prose. Understanding its shape will make AetherKit's hooks make sense.

### The page system

The CoT is structured as **pages** and **functions**, like a choose-your-own-adventure book.

```text
BOOT → MECHANICS → ROUTER → SCENE PAGE → TAIL → VENT → OUTPUT
```

- **BOOT** — identity, report card, gamestate lock, scene flags.
- **MECHANICS** — the simulation clock: agenda ticks, Chekhov cycles, ARC checks, worldsim, relationship math.
- **ROUTER** — the dispatcher. Reads the scene type and NPC count, lands on exactly one scene page.
- **SCENE PAGE** (solo or ensemble) — runs the NPC loop for every spotlight character.
- **TAIL** — the pre-flight lint: prose checks, violation loop, perception filter.
- **VENT** — the AI's own commentary, contained, never leaked.
- **OUTPUT** — render the prose and the internal states block.

Each page is a separate prompt block. When the router lands on a page, it **only processes that page** — the other pages still exist in context, but the model doesn't attend to them. This is what makes the engine fast and consistent.

### The function system

Inside pages, logic is organized into **functions** — small self-contained instruction blocks called with a `➤`.

```text
IF content = COMBAT ➤ <fn:combat>
```

A function runs its body, then returns with `⇤` — to the line *after* the call that entered it. Functions can nest: a function can call another function, which returns to the caller, which returns to the page.

The critical rule: **`⇤` returns exactly one level.** No more. The model unwinds one call at a time. This discipline is what keeps the engine from getting lost in its own reasoning.

---

# Part 3 — AetherKit: the three tiers

AetherKit gives you three levels of control, from "flip a switch" to "build your own mechanic."

| Tier | Name | What it does | Who uses it |
|---|---|---|---|
| 1 | **Flags** | Declare a mode the router reads | Everyone |
| 2 | **Specs** | Author your arc's beats and pacing | Most card authors |
| 3 | **Hooks** | Inject custom functions and routes | Power users |

---

## Tier 1 — Flags

A flag is a one-line declaration. It registers a named condition the router can evaluate each turn.

**Syntax:**

```text
[[flag1: battle_active]]
```

Slot numbers run `1` through `5`. Use a different slot for each flag.

**What it does:** adds `battle_active` to the route flags the router checks. The model evaluates it from the current scene — if a battle is happening right now, the condition is true. If not, false.

**Flags are derived, not stored.** The router re-evaluates them every turn from context. That's perfect for *modes*: combat, a minigame, a pursuit, a time-sensitive event. For something that must survive many turns (a lifted curse, a dead NPC, a changed allegiance), use a **[state block](#state-block)** instead. A flag will not remember.

**Flags are predicates, not dispatch.** A flag alone does nothing. It just tells the router what to look for. To make the router *act* on a flag, pair it with a **hook** (Tier 3).

**Example:**

```text
[[flag1: battle_active]]
[[flag2: curse_active]]
```

Then later, a hook:

```text
[[hook1]]
condition: battle_active = TRUE
call: battle_scene
[[/hook1]]
```

When `battle_active` derives true, the router calls `<fn:battle_scene>`.

**When to use flags:** whenever your card has a *mode* — a state that changes how the whole scene should be processed. Combat, a puzzle, a minigame, a hunt. Flip the flag, the engine switches modes.

**Naming rule:** don't name a flag `content`, `entry_beat`, or `arc_active`. Those already exist.

---

## Tier 2 — Specs (the ARC hook)

This is the crown jewel. A spec lets you **author your arc's beats** so the engine fires them on your schedule instead of guessing.

**Why this matters:** by default, FrankenSIM generates arcs from your card's lore. It's usually good, but it *guesses*. It might pace things too fast or too slow. It might build toward a twist you didn't intend. A spec eliminates the guesswork — you write the story, the engine executes it.

The engine still owns the **machinery** — lock checking, fireability, pacing, persistence, spoiler protection. You just supply the *story contract*.

**Syntax:**

```text
[[spec: arc]]

name: The Trial of the Nine
genre: drama
focus: {{user}}
role: focus
duration: 3 days

ki (3):
  The mentor arrives unannounced [C:mentor] [T:turn 3]
  The first test is declared [D:ki1]
  The hero refuses, then reconsiders [D:ki2]

sho (12):
  The first trial passed [D:ki3]
  The second trial humiliates him [D:sho1]
  The third trial forces a betrayal [D:sho2]

ten (2):
  The mentor's secret surfaces [D:sho12]

ketsu (2):
  The hero chooses the house over the trial [D:ten2]

[[/spec: arc]]
```

### The fields

| Field | Required | What it does |
|---|---|---|
| `name` | Yes | The arc's title. Becomes the main quest name. |
| `genre` | Optional | One word — drama, mystery, romance, horror, rivalry. Colors pacing and tone. |
| `focus` | Optional | Who the arc centers on. `{{user}}` or an NPC name. Determines protagonist. |
| `role` | Optional | The User's role: `focus`, `ally`, `obstacle`, `witness`, `rival`. Default `focus`. |
| `duration` | Optional | In-story length — "2 days", "1 week", "until the gala". Sets the arc's clock. |

### The acts

Kishōtenketsu, four acts. You declare how many beats each act has, then list the beats.

- **Ki** — introduction. Establish the normal world. Foreshadow. Nothing resolves here.
- **Shō** — development. The long stretch. Complications build toward the twist. This is where most of your beats live.
- **Ten** — the twist. Something recontextualizes everything.
- **Ketsu** — resolution. The new equilibrium.

### Beats

Each beat is a **plain English sentence** describing a specific, fireable scene. The engine's SPECIFICITY_GATE will check it — vague beats get rejected or revised.

**Good beat:**

```text
The mentor arrives unannounced [C:mentor] [T:turn 3]
```

Who (the mentor), what (arrives), when (turn 3). Fireable.

**Bad beat:**

```text
First encounter with the townsfolk — culture shock
```

No WHO, no specific WHAT, no HOW. The engine can't fire this. It will try to revise it, and the revision might not match your intent. Write the beat you want to see.

### The lock vocabulary

Beats can be locked behind conditions. The engine won't fire a beat until its locks clear.

| Lock | Syntax | Meaning |
|---|---|---|
| Character | `[C:name]` | Fire only when this NPC is present. Use the NPC's name or `{{user}}`. |
| Dependency | `[D:beat_id]` | Fire only after the named beat fires. Beat IDs are their act + number: `ki1`, `sho3`, `ten2`. |
| Time | `[T:turn N]` or `[T:time]` | Fire no earlier than this turn or clock time. |
| Secret | `[R]` | Fire only in private, with involved parties present. |
| Condition | `[K:condition]` | Custom prerequisite you write: `[K:user_has_key]`, `[K:mood=tense]`. |

**The dependency chain is automatic within an act.** `ki2` depends on `ki1`, `sho1` depends on `ki3`, and so on — unless you specify otherwise. You usually only need `[D:]` locks for cross-act dependencies, which the engine handles by default.

### The fire rule — one beat per turn

The engine fires **at most one beat per turn.** Even if multiple beats are unlocked, it fires one and holds the rest. This is the pacing throttle, and it's why your arc won't whiplash through all 19 beats in six turns.

If you want faster pacing, write *fewer* beats with bigger gaps. If you want slower, write more beats with smaller moments. The engine respects your structure.

### Spoilers and devoweled beats

**This is critical, and it's the most common mistake new authors make.**

Arc beats are **spoilers**. They reveal where the story is going. If the Reader could see your beats, the twist in Ten would be ruined before Shō even starts.

So the engine **devowels beat descriptions** in the user-facing internal states block. The Reader sees:

```text
ARC:W2:0:th mntr rrvs nnnncd — LOCKED
```

Not:

```text
The mentor arrives unannounced — LOCKED
```

The model can read the devoweled text. The human can't — or at least, not easily enough to spoil themselves.

**What this means for you:** write your beats as **full, specific, fireable sentences.** Don't be vague to "avoid spoiling" — the devoweling handles spoilers automatically. A vague beat is a beat the engine can't fire. A specific beat is a beat the engine fires exactly where you intended. Trust the devoweling, and write beats you'd want to actually see happen.

---

## Tier 3 — Hooks (advanced)

Hooks are the full override. They let your card inject **custom functions and routes** directly into the chain of thought.

This is for the power users — the cards that need a mechanic FrankenSIM doesn't have. A card game. A stat system. A minigame loop. A genre that runs on rules, not prose.

**Syntax — the hook declaration:**

```text
[[hook1]]
condition: battle_active = TRUE
call: battle_scene
[[/hook1]]
```

Slot numbers run `1` through `5`. Use a different slot for each hook.

**What it does:** the router runs a hook-check function before dispatching to the normal scene pages. Each hook resolves to:

```text
IF battle_active = TRUE ➤ <fn:battle_scene>
```

If the condition is false, the line is skipped. If true, the model enters the function.

**Then define the function in your card:**

```text
<fn:battle_scene>
  // Custom battle mechanic. Runs INSTEAD of the normal scene page.
  1. Render the battle screen: enemy, options, state.
  2. Wait for user input.
  3. END OUTPUT. Do not run prose lint or NPC loop.
  ⇥ <page:output>
</fn:battle_scene>
```

### The two ways a hook ends

**`⇤` — return.** The function does its job, then returns to the hook-check, which continues to the next hook slot, then to the vanilla scene dispatch. Use `⇤` when the hook *adds* a mechanic and the normal scene should still run.

**`⇥ <page:output>` — hijack.** The function replaces the scene entirely. Output is produced, the tail is skipped, nothing else runs. Use `⇥` when the hook *replaces* prose with a different output format — a game screen, a menu, a battle UI.

**If your function replaces prose, it must own its own exit.** Say explicitly that output ends, or the engine will run the normal tail and lint your game screen as if it were prose.

### What a hijacking function must own

The TAIL normally handles: banned vocabulary, subtext lint, timeline checks, the perception filter, the trope audit, and the violation loop.

If your hook **skips the tail** (`⇥ <page:output>`), your function must consciously handle each of those. The most important two:

- **Perception filter** — if your hook outputs prose, it still needs to respect the User's U stat. The Reader's lens doesn't turn off.
- **Anti-drift** — NPCs still need to sound like themselves. Your hook's output should still pass the character fidelity check, or the character dissolves into a generic mouthpiece for your mechanic.

### Function naming and collisions

Functions open with `<fn:name>` and end with `⇤` (return to parent) or `⇥` (advance to <page:x>), followed by `</fn:name>`

A card's `<fn:X>` that shares a name with a preset function **overrides it.** Don't do that accidentally. The do-not-touch list below names the core functions.

---

# Part 4 — Plugin variables and syntax reference

AetherKit works through empty variables in the CoT and the state/dice blocks. Your card fills them via a simple `[[...]]` shorthand that SillyTavern's regex converts before the prompt is sent.

### The full syntax list

| Shorthand | Converts to | Injected at |
|---|---|---|
| `[[flag1: name]]` … `[[flag5: name]]` | route flag | BOOT → ROUTER |
| `[[hook1]] condition: … call: … [[/hook1]]` … `[[hook5]]` | conditional function call | ROUTER hook check |
| `[[spec: arc]] … [[/spec: arc]]` | authored arc spec | MECHANICS → `<fn:arc>` |
| `[[state]] … [[/state]]` | custom persistent state block | internal states |
| `[[dice1]] name: … roll: … [[/dice1]]` … `[[dice5]]` | custom dice roll | `<dice_rolls>` |

### How the blank-state pattern works

Every plugin variable defaults to nothing. The CoT has an empty `getvar` waiting for it:

```text
{{getvar::pluginArcSpec}}
```

When your card sets the variable, that line resolves to your content, injected directly into the reasoning. When no card sets it, the line resolves to a stop symbol — a no-op. Zero token cost, zero confusion.

**Macro resolution order:** FrankenSIM's prompt blocks resolve first. Your card's macros resolve *after*, which means your card **overrides** the preset. That's intentional — it's how AetherKit works. Your card can tune FrankenSIM to play exactly the way your card needs.

---

## State block (persistent storage)

Your card can define its own state that persists across turns — a sanity meter, a score, unlocked flags, inventory, quest stages.

**Syntax:**

```text
[[state]]
<details>
  <summary>🧩 GAUNTLET STATE</summary>
  <li><b>Sanity:</b> 10</li>
  <li><b>Trials passed:</b> 0</li>
  <li><b>Puzzle solved:</b> false</li>
</details>
[[/state]]
```

**What it does:** renders inside the internal states block every turn. The model **updates the values** each turn based on the story — same way it already updates bonds and agendas. The structure stays identical; only the numbers change.

Use this for anything a flag can't remember. A flag is *derived* — re-evaluated fresh every turn and forgotten. A state value is *stored* — it survives summaries, off-screen time, and long gaps.

**Example:** `[[flag1: curse_active]]` tells the router *a curse is happening right now*. `Sanity: 7` tells you *how much sanity is left* after the curse. Flags for modes, state for memory.

---

## Custom dice

Your card can roll its own dice, pre-rolled by the frontend exactly like the built-in seeds.

**Syntax:**

```text
[[dice1]]
name: sanityRoll
roll: {{roll::1d20}}
[[/dice1]]

[[dice2]]
name: damageRoll
roll: {{roll::1d6}}
[[/dice2]]
```

Slot numbers run `1` through `5`. The `roll:` field uses the standard SillyTavern dice macro — any die size works (`1d4`, `2d6`, `1d100`).

**What it does:** the roll appears in `<dice_rolls>` under a `pluginDice` section, pre-rolled before the model sees the prompt. Your custom functions read it by name:

```text
<fn:curse_tick>
  1. Read sanityRoll from <dice_rolls>.pluginDice.
  2. Subtract sanityRoll from Sanity in the state block.
  ⇤
</fn:curse_tick>
```

**Naming rule:** don't name a custom die `userRoll`, `npcRoll`, `chekhovD20`, `worldSim`, `chaosRolls`, `pmFrame`, `bond`, `retaliation`, or `perceptU`.

---

# Part 5 — The do-not-touch list

FrankenSIM has a spine. These are the variables and rules that hold the whole engine together. **Do not override them.**

```text
⚠️ DO NOT OVERRIDE ⚠️

$npcLoopBody        — the emotion pipeline. Breaking this kills ALL NPC behavior.
$persistCall        — relationship conversion. Breaking this kills the Aether clock.
$chekhovCycleCall   — narrative debt. Breaking this kills Chekhov's Gun.
$worldsimCall       — the living world. Breaking this kills off-screen simulation.

polarity invariant  — the rule that AFFIRMATION = fondness, ANTITHESIS = friction.
                      It's a header comment, not a variable. Never reword it.

SAFE TO OVERRIDE:
$flag1..$flag5, $hookCall1..$hookCall5, $pluginArcSpec, $pluginStateTemplate,
$pluginDice1..$pluginDice5 — and every named toggle slot.
```

A malicious card can override anything — that's the nature of macros. But the well-meaning 99% of authors just need to know where the minefield is. This box is the map.

The **polarity invariant** deserves special mention because it's the one rule that, if flipped, silently corrupts everything. FrankenSIM's entire emotion system depends on **AFFIRMATION feeding fondness** and **ANTITHESIS feeding friction.** If a card rewords this — or a custom function accidentally flips the labels — every relationship in the session starts ticking in the wrong direction. Don't touch it.

---

# Part 6 — Debugging

When your arc doesn't fire, or your hook misbehaves, the answer is in the **internal states block** — the hidden HTML state at the end of every response. It's the engine's debugger, and it's always on.

### The ARC ENGINE block

Every beat in your arc appears here with its state:

```text
<li><b>Shō (Development):</b></li>
<ul>
  <li>ARC:W2:0:th mntr rrvs nnnncd — LOCKED (D:ki3)</li>
  <li>ARC:W2:0:frst trl pssd — UNLOCKED</li>
  <li>ARC:W2:0:scnd trl hmlts — LOCKED (D:sho1)</li>
</ul>
```

Three states: **LOCKED**, **UNLOCKED**, **FIRED**.

### Common failures

**"My beat says LOCKED forever."**
Look at the `D:` line. The beat it depends on hasn't fired. Either the dependency hasn't resolved, or the dependency *itself* is locked behind something. Trace the chain.

**"My beat says UNLOCKED but never fires."**
The engine fires beats on **natural openings** — the subject NPC is present and the scene touches the theme, or the User addresses the domain. If your beat is unlocked but the scene never gives it an opening, it waits. Rewrite the beat to be more reachable, or add fewer `[C:]` locks.

**"My beat fired but I didn't see it."**
Check the User's **U stat** in ENTITY MISC. If U was low, the prose may have filtered the beat out — the event happened in state but wasn't perceived. That's the unreliable narrator working as designed. If the beat is plot-critical, put it in dialogue or action, not subtext.

**"My hook runs, but the output gets mangled by prose rules."**
You probably didn't own your exit. Add the `⇥ <page:output>` line to your function, or accept that the tail will lint your output as prose.

**"My flag never turns true."**
Flags are derived from the current scene. If the router can't see a reason for `battle_active` to be true, it stays false. Make the condition explicit in the scene — something the model can read.

**"My state resets every turn."**
The state block must be **output verbatim with updated values** — if the model rewrites the structure, the regex can't find it next turn and persistence breaks. Keep the structure identical, only change the numbers.

---

# Part 7 — Full examples

## Example 1 — a simple flag + hook (mode switch)

A horror card with a "hunted" mode:

```text
[[flag1: hunted]]

[[hook1]]
condition: hunted = TRUE
call: hunted_scene
[[/hook1]]

<fn:hunted_scene>
  // Pursuit mode. Replaces normal prose with tense chase beats.
  1. Render the chase: distance, obstacles, sound.
  2. Wait for user input.
  3. END OUTPUT.
  ⇥ <page:output>
</fn:hunted_scene>
```

When the scene turns into a hunt, the router calls `hunted_scene`. When the User escapes, the scene stops reading as a hunt, the flag derives false, and normal narrative resumes.

## Example 2 — a full arc spec (pacing control)

A mystery card that wants the reveal to land at a *specific* moment:

```text
[[spec: arc]]

name: The Hollow House
genre: mystery
focus: {{user}}
role: focus
duration: 4 days

ki (3):
  The inheritance letter arrives [T:turn 2]
  {{user}} drives to the house, meets the caretaker [D:ki1]
  The locked room is discovered [D:ki2]

sho (10):
  The caretaker refuses to discuss the previous owner [D:ki3]
  A hidden photograph surfaces in the study [D:sho1]
  The neighbor warns {{user}} to leave before the storm [D:sho2]
  The power fails, and the house settles [D:sho3]
  A second key is found in the garden [D:sho4]
  The caretaker's alibi cracks [D:sho5]
  The storm traps everyone inside [D:sho6]
  A voice speaks from the locked room [D:sho7]
  The photograph is revealed to be recent [D:sho8]
  {{user}} confronts the caretaker [D:sho9]

ten (2):
  The caretaker is the previous owner's daughter [D:sho10]

ketsu (2):
  The locked room opens — empty [D:ten2]
  {{user}} inherits the truth, not the house [D:ketsu1]

[[/spec: arc]]
```

The engine reads this, assigns weights, ages the beats, devowels the display, checks fireability, and fires one beat per turn on natural openings. The author has guaranteed the daughter reveal lands at Ten, not Shō, and the story resolves with a deliberate anticlimax.

## Example 3 — a custom mechanic with state + dice (full plugin)

A card that's almost a game. Turn-based duel:

```text
[[flag1: duel_active]]

[[dice1]]
name: attackRoll
roll: {{roll::1d20}}
[[/dice1]]

[[state]]
<details>
  <summary>⚔️ DUEL STATE</summary>
  <li><b>Your HP:</b> 20</li>
  <li><b>Enemy HP:</b> 20</li>
  <li><b>Stance:</b> neutral</li>
</details>
[[/state]]

[[hook1]]
condition: duel_active = TRUE
call: duel_scene
[[/hook1]]

<fn:duel_scene>
  1. Render the duel board: enemy HP, your HP, stance, options.
  2. Wait for user input. Do not advance NPCs this turn.
  3. END OUTPUT.
  ⇥ <page:output>
</fn:duel_scene>
```

When a duel starts, the flag derives true, the router calls `duel_scene`, and output becomes a game screen. `attackRoll` is pre-rolled each turn. HP persists in the state block. When the duel ends, the scene stops reading as a duel, and the card falls back to normal roleplay.

This is the ceiling of AetherKit: a card that's a game wearing an RP costume — or vice versa.

---

# Part 8 — What's possible

AetherKit turns FrankenSIM from "a preset that runs your card" into "an engine your card programs."

The tiers are designed so that **most authors only ever write a spec** — and the spec alone fixes the single biggest complaint about FrankenSIM: that the ARC Engine guesses. With AetherKit, it stops guessing. Your card plays out exactly as you designed it, beat by beat, paced the way you intended, with the twist landing where you put it.

For the authors who go further, Hooks open the door to a different kind of product entirely — a card that's a game, a minigame, a mechanic, a genre the engine didn't have. The card owns its own rules, and FrankenSIM executes them.

The engine was already a world simulator. With AetherKit, it's a **runtime** — and your card is the program.

---

**AetherKit — write the story. Own the pacing. Build the mechanic. FrankenSIM executes it.**

*This SDK is in alpha. The syntax in this document is canonical but may expand as the ecosystem grows. If you build something with AetherKit and hit a wall, the internal states block is your debugger — and the FrankenSIM team wants to hear about it.*
