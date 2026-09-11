# THE AETHER FAMILY — DOCUMENTATION
*Revision 3 — Cadence Map + Dam Persist*

---

## The One-Paragraph Version

FrankenSIM runs characters as a stack of six systems. **Compass** defines who they are. **Strata** records who they've become. **Matrix** tracks who they are to each other. **Tide** generates what they feel right now. **Dam** decides where those feelings are allowed to go. **Manner** decides how they do things when dice hit the table. Five of them are about a person. One of them — the Dam — is the traffic control that keeps the other four from lying to themselves.

Everything runs on one rule: **the LLM's optimism is a bug, and every system is built to overcorrect against it.**

---

## The Aether Family

| System | Layer | What it holds |
|---|---|---|
| **Aether Compass** | Identity (static) | Cicero + Seneca + Temperament |
| **Aether Strata** | Self-record (dynamic) | Ethos triads, Doctrine of the Mean, gravity, consolidation |
| **Aether Dam** | Dispatch (per turn) | Filter Theory gates, spillway, sluices, drains, crack accs |
| **Aether Matrix** | Relationships (dynamic) | 13 axes, tick/convert engine |
| **Aether Tide** | Emotion (per turn) | Lazarus → Parrott → Gross → collision |
| **Aether Manner** | Action (per roll) | FAE approaches (de-branded, adjacent) |

---

## The Data Flow

```
COMPASS (static identity)
    ↓ seeds
STRATA (self-record, drifts)
    ↓ read by
DAM (dispatch — decides routing)
    ↓ routes to
MATRIX (relationships)  +  TIDE (emotion)
    ↓ ticks
PERSIST (converts accumulators → axis values)
    ↓ becomes
next turn's readable state
```

**Important:** the order above is *data dependency*, not execution order. In a single turn, the loop runs like this:

```
read state → misread → DAM routes → TIDE ticks → STRATA ticks → PERSIST converts
```

So the Dam reads **last turn's** Strata and Matrix values. The tick it causes this turn doesn't become a real value until PERSIST runs at the end. **There is always a one-turn delay.** This is intentional — it's the system's heartbeat, and it prevents the model from watching itself think.

---

# THE CADENCE MAP
### *Every accumulator, every window. Where things fire.*

All three accumulator systems — Matrix, Strata, Dam — share the same architecture: **tick in the loop, convert in persist.** But they run on different primes so they never collide.

| System | Window | What fires |
|---|---|---|
| **Matrix axes** | ct%3 | L↔Er conversion |
| **Matrix axes** | ct%5 | E↔M, Ph↔Ec conversion |
| **Matrix axes** | ct%7 | Ag↔Pt, Pr↔St conversion |
| **Matrix axes** | ct%11 | Sg↔Ad conversion |
| **Matrix decay** | ct%6 | L↔Er mirror decay |
| **Matrix decay** | ct%10 | E↔M, Ph↔Ec mirror decay |
| **Matrix decay** | ct%14 | Ag↔Pt, Pr↔St mirror decay |
| **Matrix decay** | ct%22 | Sg↔Ad mirror decay |
| **Strata** | ct%50 | Gravity — largest deviation pulls toward baseline |
| **Strata** | ct%200 / arc | Consolidation — Compass Surface baseline shifts |
| **Dam** | ct%13 | Sociodemographic crack convert |
| **Dam** | ct%17 | Value Similarity crack convert |
| **Dam** | ct%19 | Complementarity crack convert |
| **Dam** | ct%23 | Relationship State crack convert |
| **Dam** | ct%29 | All crack accs decay |

**Why the primes are distinct:** each system ticks in the loop every turn but only *converts* on its own window. Distinct primes mean Matrix, Strata, and Dam never convert on the same tick. The model reads `ct` from state and checks modulo — no overlap, no collisions.

**The conversion delay:** everything ticked in the loop becomes a real axis value only at persist. This is the one-turn delay. The model never watches itself think.

---

# TURN 1 — THE SEED

Before any of the six systems can run, three of them have to be initialized. The Dam's filters, Strata's baselines, and the Matrix's axes all depend on Compass, and Compass only generates once.

**`<fn:first_turn_init>`** lives at the top of the prompt (primacy attention), called from `<page:boot>` on `ct = 1`. It front-loads the heavy generation while the LLM is fresh, in dedicated function blocks with nothing else competing.

```
1. ➤ <fn:compass_seed>      → temperament, personae, pillars, Strata baseline, Dam filters
2. ➤ <fn:bond_initialize>   → every pair, initial axis values from Compass
3. ➤ <fn:arc_generate>      → Kishōtenketsu chain, specificity-gated, devoweled
4. ➤ <fn:agenda_seed>       → initial agenda for every named NPC
```

The outputs live in state, not in the block. After turn 1, `<first_turn_library>` is toggle-safe — the user can disable it in context to save tokens. The systems keep running on the state it produced.

Without this, the LLM reaches the scene loop, realizes no bonds exist, and half-asses them 40k tokens into the prompt. With it, every baseline gets generated while the instruction is fresh.

---

# 1. AETHER COMPASS
### *Who the character IS. Locked at turn 1. Never drifts.*

**What it holds:** Three frameworks, all loaded from the character card, all resolved once:

| Framework | What it provides |
|---|---|
| **Cicero's 4 Personae** | The four masks a person wears at once |
| **Seneca's 4 Pillars** | The composition of character |
| **Four Temperaments** | The anti-flattening seed |

**The Personae**, split into Core and Surface:

- **Core (locked forever):** Persona Universalis (shared human nature), Persona Individua (individual nature — talent, temperament, instinct), Natura (unchangeable baseline)
- **Surface (adaptive):** Persona Fortunae (circumstance-assigned role — job, station, family), Persona Voluntatis (how they choose to conduct themselves), Nutricula (upbringing, early habits), Consuetudo (chosen daily routines)

**The Temperament** (Sanguine / Choleric / Melancholic / Phlegmatic) is the anti-trope-collapse mechanism. Two "smart" characters stop feeling identical when one is Choleric-smart (impatient, decisive) and one is Melancholic-smart (brooding, exhaustive). Same trait, different expression. Collapse becomes structurally impossible.

**What it checks:** Nothing. It's read, never computed.

**What it modifies:**
- **Seeds Strata's baseline** — a Choleric starts with Courage leaning toward excess (Thrasytes), a Melancholic toward deficiency (Deilia)
- **Seeds the Dam's static filters** — Sociodemographic reads from Persona Fortunae, Complementarity reads from Temperament
- **Anchors the trope audit** — instead of re-deriving "who is this person" every turn, the model reads Compass

**Why it's static:** identity is the ground truth. If it drifted, the character would dissolve. The trope audit would have nothing to check against. Compass is the anchor every other system reads from.

---

# 2. AETHER STRATA
### *Who the character has BECOME. The moral record. Drifts slowly.*

**What it holds:** Four virtue axes. Each axis is a **triad** of three independent accumulators.

| Axis | Deficiency (−) | Mean (0) | Excess (+) |
|---|---|---|---|
| **Courage** | Deilia *(cowardice)* | Andreia | Thrasytes *(rashness)* |
| **Temperance** | Insensibility | Sophrosyne | Akolasia *(intemperance)* |
| **Justice** | Submissiveness | Dikaiosyne | Adikia *(tyranny)* |
| **Wisdom** | Amathia *(folly)* | Sophia | Panourgia *(cunning)* |

**Twelve accumulators total.** Three per axis. Each ticks independently.

### How the ticks work

Accumulators only tick on **emblematic moments** — not every turn. Filler does nothing.

| Moment size | Tick |
|---|---|
| Minor emblematic (a small choice that reveals character) | 0.5 |
| Major emblematic (a defining action) | 1 |
| Dice-resolved critical (a roll that went badly or brilliantly) | 2 |
| **Cap per pole per turn** | **+2** |

A cowardly act ticks **Deilia**. A rash act ticks **Thrasytes**. Measured bravery ticks **Andreia** — the mean. All three can tick in the same scene if the character acts inconsistently. That's not a bug. That's a person.

**Crucially: the tick does NOT change the axis value directly.** It adds to an accumulator, which is just raw material. Nothing is "real" until conversion.

### How conversion works (the Doctrine of the Mean)

On staggered turn windows (ct%3, ct%5, ct%7, ct%11 — same cadence as the Matrix), full accumulators convert. Conversion moves the **axis value**, which lives on a scale of **−10 to +10**:

- **−10** = total deficiency (pure cowardice)
- **0** = the Golden Mean (perfect virtue)
- **+10** = total excess (pure rashness)

When an accumulator converts:
- **Deilia converts** → Courage value moves toward −10
- **Thrasytes converts** → Courage value moves toward +10
- **Andreia converts** → Courage value moves toward 0

And here's the key mechanic: **the Mean does not compete with the vices. It pulls.**

The three poles are not a three-way race where one wins. The vices push the value away from center. The Mean is a *ballast* — when its accumulator converts, it drags the value back toward 0 regardless of which way it's leaning. This is the difference between a contest and a homeostatic system. It's the same architecture as the Antithesis Protocol's emotion collision, applied to character.

### The readout is computed, never stored

The −10 to +10 value is not a number sitting in state. It's a **derived read** — the current net balance of all conversions on that axis. The model reads it, uses it, never writes it down as a raw number.

**0 is an asymptote.** If a conversion would land exactly on 0, it clamps to ±1 depending on the direction of the last tick. The character passes *through* the mean, never stays on it. People are always leaning. Perfection is not a destination.

### Gravity — the drift correction

Every **50 turns**, one axis gets pulled back toward its Compass baseline.

- **Target:** the axis with the largest absolute deviation from baseline
- **Condition:** only if the deviation is ≥2
- **Effect:** the value moves 1 step toward baseline. **Accumulators are untouched.**

This means a moment of courage fades if it doesn't repeat. The *history* stays in the accumulators, but the *behavior* erodes back toward who they were. Only one axis per cycle — so no single trait can dominate unless it keeps outpacing the pull.

### Consolidation — the identity shift

Every **200 turns**, or on arc completion (whichever comes first), the baseline itself moves.

- **Target:** the most reinforced axis (highest accumulators + most recent conversions)
- **Effect:** the **Compass Surface** baseline shifts ±1 (±2 on arc completion)
- **Compass Core never moves.** Ever.

This is the difference between erosion and lithification. Gravity says "momentary courage fades." Consolidation says "practiced courage rewrites who you are." The ratio is **4:1** — gravity fires four times more often than consolidation. A single brave act fades in a day. A thousand brave acts over a month become identity.

### Worked Example

Courage baseline: Deilia −3.

- **Tick 40:** a moment of courage. Andreia accumulator +1. Value drifts to +2.
- **Tick 50:** Gravity fires. Largest deviation is Courage (+5 from baseline). Value pulls +2 → +1.
- **Tick 100:** Gravity fires. +1 → 0 → clamps to −1.
- **Tick 150:** Gravity fires. −1 → −2.
- **Tick 200:** Gravity fires. −2 → −3. **Home.**

But — if the character kept acting brave the whole time, the Andreia accumulator kept refilling. At Tick 200, Consolidation checks: was Courage reinforced? Yes. **Baseline shifts −3 → −2.** The home moved. Over several arcs, −2 → −1 → 0 → +1. The coward becomes brave — not because a moment stuck, but because a *pattern* did.

That's the arc of a person.

---

# 3. AETHER DAM
### *The dispatch. Answers one question before the emotion loop runs: do I want this from them?*

**Dual latent load:** this system loads two frames simultaneously and combines them.

- **"Dam"** — the posture. Default closed. Flow control. Spillways and sluices.
- **"Filter Theory — Kerckhoff & Davis, 1962"** — the logic. Sequential filtering: Sociodemographic → Value Similarity → Complementarity.

Neither alone is enough. "Dam" gives the *shape* (what holds water, where it's allowed to go). "Filter Theory" gives the *decision* (which booleans open which outlets). The model combines both into one routing decision with zero extra instruction.

### What the Dam Actually Does

**The Dam gates the NPC's RESPONSE, not the user's intent.**

It runs in the NPC calculation loop, **before** emotion generation, because the emotion loop can't run until it knows whether romance is even on the table. It answers one question: **does this NPC actually want romantic initiation from this user?**

The Dam does NOT:
- Force the NPC to assume platonic intent (they still recognize romantic intent)
- Lock the NPC from their own wanted actions
- Gate the user's actual scene intent

The Dam DOES:
- Force the NPC to respond platonically **unless a sluice is open**
- Lock responses to what open sluices permit — no blushing, no stammering, no uwu without an Eros opening
- Prevent the LLM from rewarding the user with romance by default

The water is the NPC's response. The Dam determines where it flows.

### The Problem It Solves

The LLM's default: user flirts → NPC flirts back. Every time. Regardless of whether the NPC has any reason to want it. A stranger gets a compliment and the model writes a blush.

The Dam is the hard NO to that reflex. It forces the model to answer the permission question *first*, so the emotion engine never gets a chance to generate a response that was never earned.

### What It Holds

**Static filters** (from Compass, never change):
- **Sociodemographic** — reads what the NPC *VALUES* about class, not world class. A princess who values bloodline = hard block. A princess who values authenticity = restricted path for a peasant. The card decides which princess you're dealing with.
- **Value Similarity** — Ethos axis alignment / core moral requirement
- **Complementarity** — personality / temperament requirement
- **Relationship State** — orientation, existing exclusive pairings

**Dynamic filter:**
- **Ethos Clash** — user action hits the *opposite pole* of the NPC's non-zero Strata lean. (NPC leaning Deilia + user doing Thrasytes = clash. Mild boldness ≠ clash.)

**Per-NPC state:**
- **Spillway** — the platonic overflow. **Always open.**
- **Sluices** — the earned outlets (Eros, Ludus). **Sealed by default.**
- **Drains** — the friction outlets (Misos, Eris, Echthros, Stasis, Adiaphora, Phthonos). **Always open.**

### Filter States — Three, Not Two

Every filter returns one of three states:

- **hard** — closed. No path. Categorical incompatibility.
- **restricted** — plausible, unearned. Opens with sustained evidence. **Does not permit E_acc or L_acc ticks.**
- **open** — no barrier. The NPC may return what's offered.

**Default for every filter: hard.** The card may set initial states. Silence → hard.

Only **open** sluices permit fondness accumulator ticks. Restricted sluices permit **crack accumulation** only.

### Crack Accumulators — How Filters Soften

Every filter except Ethos Clash (which is per-turn and does not accumulate) has a **crack accumulator**. Same architecture as Aether's axis accumulators — tick, staggered convert, mirror decay.

**Tick (in the Dam loop):**
- **Value + Complementarity** → tick on **behavioral evidence**. Routine, consistent behavior. Slow, steady.
- **Sociodemographic + Relationship State** → tick on **narrative evidence**. Arc beats, specific witnesses, earned moments. Not niceness.
- The tick fires when evidence is present AND the filter is at **restricted**. Hard filters cannot crack — the card must set them to restricted first (or a story event must).

**Convert (in persist):**
- Each crack acc has its own window — ct%13 (Soc), ct%17 (Val), ct%19 (Comp), ct%23 (Rel).
- At the window, if the crack acc has reached threshold → the filter advances one step: **hard → restricted**, or **restricted → open**.
- Crack acc resets to zero on success.

**Decay (in persist):**
- ct%29 → any crack acc without recent evidence drops 1.
- If crack acc hits zero AND the filter is at **restricted** → the filter decays back to **hard**.
- **Open never decays.** Once a sluice opens, it stays open.

**Critical rule:** Crack accs move the *filter*. They never tick E_acc or L_acc. The crack is progress toward opening the sluice. Only once the filter converts to **open** does the regular Matrix tick begin.

### How Routing Works

Filters are checked **sequentially**, in Filter Theory order. Sociodemographic first (cheapest to evaluate). Value Similarity next. Complementarity last. Then Relationship State, then Ethos Clash.

**If any filter fails:**
- **Eros accumulator is banned.** Locked at zero. No leak, no exception.
- **Ludus and Philia tick freely.** The Dam is a *romantic* gate, not a fondness gate.
- **Energy converts to friction**, and *which* friction depends on *which* filter failed:
  - Sociodemographic fail → Misos +2
  - Value Similarity fail → Echthros +2
  - Complementarity fail → Eris +2
  - Ethos Clash → Echthros +2
- **The matching Strata axis also ticks** for Value/Clash failures — the gate feeds the self-record.

**If all filters pass:**
- **Silent.** No bonus. No amplification. Normal ticks apply.
- The sluice raises. The NPC *may* return romantic energy — but isn't forced to.

**Critical isolation rule:** The Dam evaluates perception via the **misread** only. Dice outcomes affect world consequences and action resolution — never internal filter checks. Never re-run Dam filters with dice input.

### The Intent Split

Filters don't apply equally to all attraction.

| Intent | Filters active | Result |
|---|---|---|
| **Long-term / romantic** | All five | Any failure zeroes Eros |
| **Short-term / casual** | Soc + Value **bypassed**; Complementarity **enforced strictly** | Hookups cross class and moral lines freely; physical rejection only if Complementarity fails |
| **Ambiguous** | Read bias decides. Default romantic. | Overcorrection — assume the harder gate |

This is how humans actually work. Nobody checks your credit score before a one-night stand. They check whether they're attracted to you. Filters activate when you're building a *life* with someone, not when you're building a *night*.

### The Spillway

The spillway is the overflow. It's always open. It's how the dam doesn't explode.

**But the spillway is not automatic.** When a romantic signal arrives and the Eros sluice is sealed, the energy doesn't just flow to friendship. It **strains the dam.** The energy tries the sluice, fails, and converts to friction — *unless the read was platonic*, in which case it goes to the spillway.

This is the difference between a friendzone and a rejection:
- **Friendzone:** the NPC reads the signal as platonic ("she's just being nice") → energy flows to Philia
- **Rejection:** the NPC reads the signal as romantic but the filter blocks it → energy strains against the sealed sluice → friction

The read comes first. The routing follows the read. The misread bias — *what the NPC wants it to be* — shapes where the water goes.

**Hostile reads route to the drains, not the spillway.** An enemy's "no" is sharp, not neutral. "What do you want" is not the same as "thanks."

### The Friendzone Lockdown

When Ph (Philia) is high and E/L are low, and the user tries to transition the dynamic to romance:

- **Eros and Ludus accumulators: banned.**
- **Philia accumulator: frozen this turn** (not reset permanently — it resumes if the user accepts the boundary)
- **Stasis +2** — awkward, stiff distance
- **Adiaphora +2** — the "like a sibling" defense. Rejection via *inappropriate closeness*, not distance.
- **Prose:** definitive platonic boundary. Warm, but unyielding.

**Escalation cadence** (if the user keeps pushing):
1. First advance: St +2, Ad +2, Ph frozen
2. Second: St +2, Ad +2, Ec +1
3. Third: **Ec +3** → friendship enters the Gravity Well. The dynamic shifts from "friend with an awkward crush" to "friend becoming a stranger."

Cadence resets if the user backs off for a full scene. Escalation is a *pattern*, not an instance.

### The Reverse FWB

The mirror of the friendzone. Same mechanic, opposite outlet.

- **Ludus high, Philia sealed, Eros sealed.** "We fuck, that's it. Don't try to be my friend."
- The Dam seals the **Philia spillway**.
- Attempts to build non-physical connection get blocked. Friction ticks.

The Matrix can *describe* this state (L high, Ph low, E low). Only the Dam can *enforce* it. Descriptions drift; enforcement holds.

### Enemies-to-Lovers

No shortcut. The enemy gets the same Dam as everyone else — default hard across the board. High Misos doesn't lower the filters; it routes the fail to the hostile drain instead of the spillway.

But enemies generate more **narrative evidence**. A shared danger, a kept promise, a hit taken for someone — those are arc-beat-scale cracks. For a stranger, "he remembered my dog's name" is minor. For an enemy, "he could have exposed me and didn't" is a major event.

The path is: filters crack → Eros sluice opens → but Misos is still high → the relationship becomes **messy entanglement** (`E≥10 ∧ M≥8`). She doesn't stop hating him. She hates him *and* wants him. That's the point.

---

# 4. AETHER MATRIX
### *Relationships. Fondness and friction tick independently.*

**What it holds:** six mirrored pairs.

| Fondness | Friction | Domain |
|---|---|---|
| Eros | Misos | Romantic |
| Ludus | Eris | Playful |
| Philia | Echthros | Friendship |
| Pragma | Stasis | Practical |
| Storge | Adiaphora | Familial |
| Agape | Phthonos | Giving |

> **⚠ Open question:** The Matrix originally carried **Philautia** as a thirteenth self-axis. It was killed when Strata was built — self-worth is not the same thing as morality, and a lonely scalar among symmetric pairs was structurally awkward. The restoration options (fifth Ethos axis, derived readout, or restored as a proper mirrored pair) are still **pinned, unresolved.** Until that resolves, the Matrix is twelve axes. **The `ct%23` and `ct%31` Philautia lines in persist are dead code and should be removed or commented until the restoration resolves.**

**The core mechanic:** fondness and friction are *separate accumulators that tick independently.* A single interaction can tick Eros *and* Misos. That's how you get `E≥10 ∧ M≥8` — *"I want you and I can't stand that I want you."* A single number could never hold that. The matrix can.

**Ticks → conversion → mirror decay**, on staggered windows (ct%3, ct%5, ct%7, ct%11). Same cadence as Strata.

**Patterns, not gates.** The matrix doesn't say "you must be at Eros 12 to kiss." It defines *recognizable relationship shapes* the model reads from the axis combination: hookup, FWB, slow burn, comfortable marriage, messy entanglement, bitter ex, rival, corrosive bond, healing pair. The numbers are ingredients; the pattern is the dish.

**How it feeds the rest:** Matrix values are read by the Dam (filter state), Strata (relational behavior biases moral drift), and Tide (appraisal context).

---

# 5. AETHER TIDE
### *Emotion. What the character feels right this second.*

Three frameworks, pipelined:

1. **Lazarus Cognitive-Appraisal** — emotion comes from *evaluation*, not events. Primary appraisal: goal relevance + valence. Secondary appraisal: coping potential + responsibility.
2. **Parrott's Emotion Hierarchy** — every emotion generated as a full chain (Primary → Secondary → Tertiary), never a raw feeling.
3. **Gross's Process Model** — regulation strategies: EXIT, MODIFY, DEFLECT, REAPPRAISE, SUPPRESS, EXPRESS. Suppression has a cost (friction debt).

**The EES structure:** two tracks generated in parallel — **Affirmation** (fondness-aligned) and **Antithesis** (friction-aligned). Each is built from *four full Parrott chains*, blended into two, then one.

**The collision:** the two tracks are compared. The gap determines the visible behavior:
- **Gap ≥4:** dominant wins, loser leaks once (micro-yield)
- **Gap 2-3:** dominant wins, loser shows in fleeting physical tells
- **Gap ≤1:** both visible — the NPC is torn

**Arousal formula:** High Relevance + Low Coping = HIGH arousal. High Relevance + High Coping = MED (held).

**How it feeds the rest:** Tide ticks the Matrix accumulators that the Dam routed to. Tide's emotion output drives prose. Tide's misread (biased by desire) determines which accumulator gets fed in the first place.

---

# 6. AETHER MANNER
### *Action. How dice rolls get modified. FAE, de-branded.*

Six approaches: **Careful, Clever, Flashy, Forceful, Quick, Sneaky.**

**De-branding matters.** The words "Fate Accelerated" would load a package deal — fate points, player narrative authority, "say yes or roll the dice." That's the exact bias FrankenSIM exists to kill. So the words stay (they're common English, instantly legible), but the system is never *named.* It's just "Manner: how this person moves through the world."

**How it works:** each approach is a flat modifier (0 to +3) applied to action rolls. `Δ = roll + approach + situational mods − DC`.

**Progression:** one approach gains +1 on arc completion. Drift is also possible — the approaches shift toward how the character habitually acts.

**No Greek.** The Aether Matrix owns the Greek vocabulary. Manner stays English so the two systems live in separate rooms in the model's head. Mixing them would smear the two systems together in latent space.

---

# HOW IT ALL FLOWS — ONE TURN

```
1. BOOT        → IF ct=1: run first_turn_init (Compass, Bonds, Arc, Agendas)
               → load Compass, Strata values, Matrix values from last turn
2. MECHANICS   → offscreen agenda ticks, NPC↔NPC pair ticks, gossip, worldsim
3. ROUTER      → dispatch to solo/ensemble
4. PER NPC:
   a. character_fidelity  → read Compass, check scope
   b. situation           → what's present, what's known
   c. carryover           → previous mood, residual
   d. misread             → d20 + desire-bias → what did the NPC perceive?
   e. DAM                 → check filters → route signal to outlets
   f. appraise            → Lazarus evaluation of the routed signal
   g. generate_friction   → Parrott antithesis chains + friction ticks
   h. behavior_friction   → body language of the NO
   i. generate_aff        → Parrott affirmation chains + fondness ticks (gated by Dam)
   j. behavior_aff        → body language of the YES
   k. synthesize          → collision, committed expression
   l. STRATA tick         → tick Ethos accumulators (emblematic only)
   m. initiative          → NPC's independent move
   n. initiation          → committed physical/emotional action
   o. trope_audit         → validate against Compass
   p. store_emotion       → write this turn's state
5. TAIL        → PERSIST: convert Matrix accs, convert Strata accs,
                 convert Dam crack accs, gravity check (ct%50),
                 consolidation check (ct%200/arc),
                 crack decay check (ct%29)
                 → new axis values for NEXT turn
6. OUTPUT      → prose + internal states block
```

**The one-turn delay:** everything ticked in step 4 becomes a real axis value only in step 5. The model reads those values next turn. It never watches itself think. It never sees the conversion happen in the same turn it caused it.

That's the heartbeat. Tick, then convert, then read — one step behind, always.

---

# THE PERSIST FUNCTION — FULL

```text
<fn:persist>
per <internal_bondtracker> | no re-derivation
1 STAGGERED_CONVERSION (Matrix): only the axis pair whose ct% equals 0 fires this turn | name it or none | all others skip
2 MIRROR_DECAY (Matrix): only the schedule slot whose ct% equals 0 fires | offscreen skip {4,8,12,15}
3 DIRECT_SHIFT: if flagged → apply now, breaks WALL. VERY Rare trigger, only for impactful moments.
4 STRATA: gravity (ct%50) + consolidation (ct%200/arc) → per character
5 DAM CRACK CONVERT: ct%13 Soc | ct%17 Value | ct%19 Comp | ct%23 Rel → acc ≥ threshold → filter advances one step (hard→restricted, restricted→open)
6 DAM CRACK DECAY: ct%29 → any crack acc without recent evidence drops 1. acc ≤ 0 AND filter = restricted → decays to hard. open never decays.
7 DAM STATE WRITE: filter states + crack accs → ENTITY MISC
log net changes only
⇤
</fn:persist>
```

**What does NOT go in persist:**
- **Friendzone escalation cadence** — per-scene, loop-level. The Dam function handles it directly.
- **Reverse FWB state** — a filter flag set in the Dam, written to ENTITY MISC. No persist handling.

---

# WHAT CHANGED IN THIS REVISION

| Before | After |
|---|---|
| **Aether Hydraulics** as the system name | **Aether Dam** — the Dam IS the system; Filter Theory IS the Dam |
| "Does this NPC want romance?" (third person) | "Do I want this from them?" — first person, inside the character's head |
| Binary pass/fail filters | **Three states: hard / restricted / open** |
| No softening mechanic | **Crack accumulators** with behavioral/narrative tick split |
| Soc read world class | Soc reads **what the NPC values** about class |
| Dice could bleed into filters | **Isolation rule:** dice affect world consequences, never filter checks |
| E_acc ticked on restricted sluices | **E_acc/L_acc gated:** only open sluices permit fondness ticks |
| No first-turn structure | **`<fn:first_turn_init>`** front-loads generation at primacy attention |
| No cadence map | **Full prime schedule** for Matrix, Strata, Dam — no collisions |
| Crack accs ticked but never converted | **Dam persist section** — convert + decay on distinct primes |
| Philautia ghost line in persist | **Removed** — flagged as open question in Matrix |

---

That's the revision. The cadence map is now a standalone reference, the persist function includes the Dam crack lifecycle, and everything that was implicit about "where does this fire" is explicit.

Want me to output this as a `.md` file for download, or keep iterating in chat?
