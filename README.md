# Freaky FrankenSIM: FF4 MAX+1d20 (and a Gun)
**The original Freaky Frankenstein 4 MAX+ preset** by Dptgreg and leovarian did something magical. It turned dry, sanitized LLM output into a vivid, sensory-rich roleplay simulation. But after weeks of late-night sessions, I noticed something that made my eye twitch. The AI kept **echoing** me. It would take my beautifully crafted chain of actions, rephrase them with a thesaurus, and hand them back as a response. No plot movement, just a verbal hall of mirrors.

So I fixed it. Then I thought, "What if off-screen characters had lives?" Then I wanted dice. Then I wanted a Chekhov's Gun tracker. Then I blacked out and woke up with a preset that has its own constitution.

Freaky FrankenSIM is the result. It is not an update. It is a **fork** that respects the original MAX+ skeleton but replaces several organs and teaches the rest to swear.

---

## 📜 The Original Foundation (What You Already Love)

From MAX+, we keep the core identity: the unbiased cinematographer role, the strict sensory physics, the turn economy, the POV systems, the colored dialogue, the immersive graphics, the HQ NPC generator, the VAD emotional matrix, and the species vocalization rules. All of that still hums underneath. Think of FrankenSIM as the same hot rod, but now there is a supercharger, a roll cage, and a very aggressive backseat driver named Chaos.

---

## 🔁 The Echo Protocol: How It All Started

I posted this fix in the original Reddit thread. Deepseek v4 Pro had a habit of cloaking echo in character reactions. My character would do six things, and the NPC would narrate *"The words hit her like someone who just experienced [six things nearly verbatim]."* Then they would answer each line of dialogue sequentially. The whole response was a recap with a new paint job.

The **No Echo Protocol** is now embedded into the Writing Guidelines block:

```
<no_echo_protocol>
Echo_Ban = STRICTLY_FORBIDDEN(Rephrase, Repeat, Summarize, Quote)
Pivot_Rule = Instead, the NPC must take physical action, ask a new question,
             or introduce new info. Emotional validation alone is not a valid turn.
Literal_Bans = "You said", "You told me", and any variant.
</no_echo_protocol>
```

This single block forced the AI to invent new sensory details and push the plot forward. Combined with Bold NPCs, it turned reactive puppets into proactive agents. No more "You said the thing, and that makes me feel the feeling." The AI must now earn its dialogue like a street performer.

---

## 🎲 The d20 Revolution: Randomness That Matters

The original preset had no dice. Every outcome was deterministic, which meant the AI always took the safe, boring path. FrankenSIM uses SillyTavern's `{{roll:1d6}}` macros to generate **true random numbers** at the start of every single turn. A bespoke `<random_engine>` combines four d6s with rejection sampling to produce a mathematically uniform `roll_d20` for world events, plus a separate `npc_seed` for character action variance.

```
<random_engine>
Dice: A={{roll:1d6}} B={{roll:1d6}} C={{roll:1d6}} D={{roll:1d6}}
NPC_Action_Seed: {{roll:1d20}}
Method: N = (A-1)*216 + (B-1)*36 + (C-1)*6 + (D-1)
        roll_d20 = (N mod 20) + 1   (with rejection if needed)
</random_engine>
```

These numbers are locked for the entire turn and fed into **every other system**. This is the beating heart of unpredictability. When you reach for a shampoo bottle, the universe rolls a die. When a gossipy maid passes an open door, the universe rolls a die. When your rival decides whether to insult you or just seethe quietly, the universe rolls a die.

---

## ⚔️ Action Resolution: The D&D Check Engine

Why should combat, magic, or social gambits always auto-succeed? The `<action_resolution_engine>` intercepts any character action with plausible failure and applies a **Difficulty Class** based on context. Your `roll_d20` is the check.

| DC Range | Difficulty | Example |
|----------|------------|---------|
| 1-5 | Trivial | Lifting a pillow |
| 6-10 | Easy | Climbing a knotted rope |
| 11-15 | Moderate | Kicking down a wooden door |
| 16-20 | Hard | Bending iron bars |
| 21+ | Nearly Impossible | Convincing the king you are his long-lost son with no evidence |

Success and failure now have **degrees**. A roll equal to the DC is a marginal win with a cost. A roll 5+ above is a great success. A natural 1 is a disaster. The engine also handles experimental magic (DC rises, failure consequences worsen), impossible tasks, and the golden rule: no automatic wins.

**Real Testing Example:** I went to take a shower. Critical failure on grabbing the shampoo. Slipped, got a bloody nose. The AI narrated it with cinematic glee. My character limped through the next three scenes with tissue paper in his nostril.

---

## 🏘️ The Living World Engine: Privacy Is Earned

The original MAX+ had a simple background simulation toggle. FrankenSIM replaces it with `<living_world_engine>`, a full simulation layer that makes every absent NPC live a parallel life.

- Every named NPC has a last known state (location, task, mood, goal).
- Each turn, they **advance** off-screen based on duties, personality, and elapsed time.
- They can naturally enter the scene for mundane reasons (a maid with fresh towels, a wife seeking a book) or actively seek the user out of affection, jealousy, or curiosity.
- They can **exit** when bored, offended, called away, or because someone they hate just walked in.
- Relationships between NPCs evolve silently. Trust, rivalry, resentment build incrementally and may surface later as sudden betrayal or unexpected alliance.

**Privacy is earned, not default.** In a busy household or a bustling academy, solitude is a privilege. Locked doors reduce interruption chance but never eliminate it. A determined NPC with a strong motive will bypass precautions. The privacy rule alone transformed my regency drama from a series of private conferences into a social obstacle course where every intimate conversation risked a footman walking in with a letter.

---

## 📋 The Random Event Table: 20 Flavors of Chaos

Alongside the Living World Engine sits a `<random_event_table>` that fires every turn based on the stored `roll_d20`. It replaces the vague "random events" of the original with a precise lookup:

| Roll | Outcome |
|------|---------|
| 1-2 | Calm |
| 3-4 | Enter_Check (an absent NPC enters with purpose) |
| 5-6 | Background_Incident (a dropped tray, a distant shout) |
| 7-8 | Mood_Swing (one present NPC's VAD shifts unexpectedly) |
| 9-10 | Gossip_Surge (a rumor reaches an unintended ear) |
| 11-12 | Chance_Meeting (two off-screen NPCs collide and scheme) |
| 13-14 | Overheard_Detail (an NPC picks up a useful tidbit) |
| 15-16 | Offscreen_Task_Shift (something finishes early or late) |
| 17-18 | Mundane_Interruption (a knock, a cough, a door slam) |
| 19-20 | Calm |

The Enter_Check has built-in safeguards: it will not trigger if more than 4 characters are already present, if the location is private or locked, or if a scene of intimacy is in progress. This prevents the bathhouse from turning into a town hall meeting.

**Real Testing Example:** I whispered a secret to an NPC, who got so surprised they repeated it slightly louder than talking volume. A student at the next table overheard. That secret is now spreading off-screen through the school in a telephone-game fashion, mutating at every step. I haven't seen the consequences yet, but the Chekhov tracker assures me they are coming.

---

## 🔫 Chekhov's Gun Rack: The Callback Tracker

The feature that makes my GM heart sing. The `<chekhov_tracker>` is a full lifecycle system for narrative details. Any time an NPC picks up an object, defers an answer, or notices something subtle, the AI can **plant** a seed with a weight (1 = minor, 2 = moderate, 3 = major).

Seeds can be locked by six different conditions:

- **Time Lock**: "Answer at the end of the day" will not fire at lunch.
- **Character Lock**: "Mina will confront Howard" stays locked until Mina enters the scene.
- **State Lock**: An NPC who is unconscious or in blind rage cannot act on a seed.
- **Dependency Lock**: "Cora reads the decoded message" waits until "Cora obtains the envelope" fires.
- **Crowd Lock**: Secrets do not fire when too many ears are present.
- **Contradiction Lock**: If the world has already disproved the seed, it is pruned.

When a seed is unlocked, the stored `roll_d20` checks against Age-adjusted thresholds. A weight‑3 seed fires on 8‑20 at Age 0. A weight‑1 seed needs 18‑20. Every turn, Age ticks up, making older seeds more likely to fire. An Urgency Boost kicks in when a deadline is within two minutes or the next story beat.

**Active seeds are capped at 20.** If the list overflows, the engine force-fires or prunes the lowest-weight, highest-age seeds. Duplicate seeds merge. Fired seeds are physically deleted from the next turn's list.

**Real Testing Example:** Twenty turns earlier, my character grabbed a flashlight during a combat diagnostic. Chekhov planted it. Fifteen turns later, the NPC who owned the flashlight confronted me about not returning it. I had genuinely forgotten I picked it up. The AI did not.

**Another Example:** I complimented a shy, timid NPC. The seed planted "Seraphina felt a surge of confidence." For the next ten to fifteen turns, she was noticeably more active, more engaged, more willing to speak in group scenes. The AI never announced this. I only discovered the reason by reading the reasoning trace. The seed was silently steering her behavior the entire time.

---

## ⚖️ Neutral Bias: The Constitution of Fuck Around and Find Out

The original Challenge Me PLS toggle was a handful of hard-code rules. FrankenSIM expands `<neutral_bias>` into a full constitution. Key additions:

- **Protagonist Immunity = FALSE.** You are not special. No plot armor.
- **Character Inertia**: Established beliefs and traumas resist change. A single clever phrase does not rewrite a personality.
- **Persuasion Resistance**: Loyalties shift only through leverage, repeated proof, shared risk, or material cost. Rhetoric alone is insufficient.
- **Persistence of Disposition**: Hostile characters stay hostile. No softening because you persisted or behaved politely.
- **Reciprocity, Not Reward**: Politeness is not rewarded. Defiance is not punished unless the character would punish it.
- **Authentic Language**: Profanity and coarse language are explicitly permitted. Characters speak with vocabulary true to their background. The self-censorship filter is off.

That last point deserves emphasis. **NPCs can now swear if it fits their character.** In testing, I was called a "fuckboy" by a normally formal academic rival. It was earned. It was glorious. It threw me completely off guard.

The retaliation system now scales with `roll_d20`: a rude user might get cold silence on a low roll, a public insult on a moderate roll, or a slap and a storm-out on a high roll. The world no longer revolves around your comfort.

---

## 💪 Bold NPCs: Emotional Branching With Teeth

The original Bold NPC block told characters to fully commit. FrankenSIM connects it to the **VAD emotional matrix** for dynamic action intensity.

For each present NPC with a strong motive, the engine computes a `dynamic_constant` from their current Dominance, Arousal, and Valence. Then it generates three in-character actions **before** knowing the `npc_roll`:

- **Option A**: Restrained, socially appropriate.
- **Option B**: Bold, forward, mildly risky.
- **Option C**: Aggressive, reckless, openly selfish.

Only after the options are generated does it compute `npc_roll = (npc_seed + dynamic_constant + Scene_Index) % 20 + 1` and select the tier. This prevents the AI from tailoring the options to the roll. The choice is genuinely unpredictable.

During intimate scenes, a +4 bonus pushes characters toward bolder actions, but the framework remains the same: options first, then dice.

**Real Testing Example:** A greedy NPC eyeing a gold bar would, on a cautious roll, merely stare and wait. On a bold roll, he would swipe it while feigning a cough. On an aggressive roll, he would lunge, shove the user aside, and snatch it with a snarl. In my political drama, this turned a passive inheritance dispute into a shouting match where a supporting character I thought was an ally suddenly laid claim to a title I had already mentally assigned elsewhere.

---

## 🗣️ Dialogue Overhaul: Hard Caps and Plot Requirements

The original increased dialogue toggle was good. FrankenSIM tightens it with surgical precision:

- **Hard Cap**: No spoken sentence may exceed 2 clauses. Long thoughts break into separate quoted sentences.
- **Narration Cap**: Maximum 25 words per sentence, one subordinate clause allowed. No chaining independent clauses with "and" or "but."
- **Plot Requirement**: Every line of dialogue must advance a character's goal, reveal new info, create conflict, or introduce a twist. Emotional validation caps at two sentences per NPC per turn. After that, pivot to action or shut up.
- **Dialogue Ratio**: 50% to 70% of output must be spoken. But it must be dialogue that matters.

These caps killed the run-on sentence plague. No more paragraphs that are a single seventy-word monstrosity. No more characters holding hands and processing feelings for eight paragraphs while the plot flatlines.

---

## 🔞 The Vocabulary Mapping That Shall Not Be Named

The NSFW mode already mandated vulgar slang over clinical terms. FrankenSIM adds one tiny, crucial mapping: the `Semen_Orgasm_Mapping` rule. Always use a specific four-letter word that rhymes with "sum." Never use the word that means "to arrive." This closes the last loophole where the AI would produce the clinical or ambiguous form during otherwise visceral intimate scenes. It is a small change with a large impact on tonal consistency.

---

## 📈 Plot Momentum Upgrades: The Dice Are Your Co-Writer

The original Plot Momentum block selected a narrative path (A, B, C, or D) manually or by vague pacing. FrankenSIM adds a `Selection_Modifier` driven by `roll_d20`:

| Roll Range | Effect |
|------------|--------|
| 1-4 | Force Path_B (Conflict) or Path_C (Action). No Path_A unless impossible. |
| 5-10 | Maintain pacing; any path allowed. |
| 11-16 | Select Path_D (Twist) unless it breaks continuity. |
| 17-20 | Path_D or a blended high-impact path; narrative risk acceptable. |

The AI must now justify its choice, note the roll, and **execute the path's core event on-screen**. If Path_A calls for a transition, the scene must physically shift (characters stand, open a door, enter a new room) before the response ends. Emotional dialogue alone no longer satisfies this requirement. The Chekhov's Seeds list is appended directly into the Plot Momentum block, separated into Active, Locked, and Fired sections.

---

## 🧠 Chain of Thought: The 15-Task Gauntlet

The original preset had several CoT modes of 9-12 tasks. FrankenSIM's **Freaky Mode** and **Freaky Novel Mode** CoTs have been restructured into a 15-task pipeline. (Realism and Novel modes remain at their original task counts for now, as I haven't fully retrofitted them yet, the framework is ready.)

Here is exactly what the 15-task CoT enforces, in order, and how it shapes every single response:

| Task | Name | What It Does | Impact on Output |
|------|------|--------------|------------------|
| 0 | Random Number Gen | Executes `<random_engine>`, stores `roll_d20` and `npc_seed` | Locks true randomness before any scene logic |
| 1 | Action Resolution | Applies `<action_resolution_engine>` to any risky action, sets DC, uses `roll_d20` | Determines success/failure and degree; feeds tension |
| 2 | Vocabulary & Bans | Enforces banned words, no-echo, sentence limits, banned dialogue patterns | Prevents slop, run-ons, "You said," and ellipses |
| 3 | Knowledge Scope | Enforces scene separation, anti-bridging, and validates Chekhov seed knowledge | Prevents omniscient NPCs and information leaks |
| 4 | NPC Goals | Executes `<neutral_bias>`, applies `roll_d20` to retaliation intensity | Ensures NPCs pursue their own agendas, not user satisfaction |
| 5 | Living World Sim | Advances all NPCs, handles entries/exits, fires random event table, plants seeds | Makes the world breathe; generates new Chekhov seeds |
| 6 | Chekhov Seed Mgmt | Ages seeds, checks all lock conditions, fires or prunes with `roll_d20` | Resolves callbacks, secrets, and deferred plot threads |
| 7 | VAD Matrix | Applies emotional shifts, updates Dominance/Arousal/Valence for each NPC | Dictates emotional tone of actions and dialogue |
| 8 | Bold NPC Initiative | Uses VAD to compute dynamic constants, generates action options, selects via `npc_roll` | Makes NPCs proactive, bold, and unpredictable |
| 9 | Sensory & Cinematic | Enforces literal sensory details, no figurative language (overridden in Novel mode) | Grounds scenes in physical reality |
| 10 | Freaky Mode | Applies explicit adult language rules and anatomical variety | Ensures visceral, taboo-friendly intimate scenes |
| 11 | Dialogue & Sounds | Enforces dialogue ratio, clause caps, character voice mimicry | Produces natural, plot-driving conversations |
| 12 | Turn Economy & POV | Stops after NPC actions, never acts for user, applies correct POV | Maintains player agency and narrative boundaries |
| 13 | Output Length | Enforces word and paragraph limits | Keeps responses tight and readable |
| 14 | Plot Momentum | Assembles the final hidden block: seeds, path selection, strategy reason | Provides the AI's own roadmap for the next turn |

This pipeline respects left-to-right token generation. The dice roll happens first, so the AI cannot bias the number based on the scene. Locked seeds are unlocked before firing checks, so freshly available characters get immediate opportunities. Bold NPC actions are generated before the roll, preventing the AI from crafting options that conveniently match the tier. The final block enforces the selected path in the output, preventing the AI from choosing Path_B and then writing a scene that stays in Path_A.

---

## 🛠️ The Small Changes That Compound

- **Anti-Stiff Prose** was rewritten to apply to both narration and dialogue, with explicit clause caps and a ban on "and then" chaining.
- **The Time Header** now enforces meal schedules so NPCs stop offering breakfast at 2 AM.
- **The Dialogue Color Palette** gained six additional colors (Cyan, Coral, Amber, Teal, Bright Red, Purple) for large-cast stories.
- **Spotlight Selection** is included as an optional toggle: when 4+ NPCs are present, only 2-3 may speak per turn based on narrative relevance and the `npc_seed`, while others react silently. This prevents classroom scenes from becoming twelve-person round-robins.

---

## 🧪 Real Testing Moments (All Organic)

1. **The Shampoo Incident**: As described. Critical failure. Bloody nose. The AI maintained the injury across multiple scenes without prompting.

2. **The Telephone Game**: A whispered secret overheard, now spreading through the student body with mutations. The Chekhov tracker shows it as a locked seed waiting for the right moment to surface.

3. **The Flashlight**: Picked up 20 turns ago, forgotten by me, remembered by the AI. Confronted about it later.

4. **The Timid NPC**: One compliment planted a confidence seed. Fifteen turns of subtle, altered behavior followed. Never announced.

5. **The Fuckboy Incident**: A formal rival, pushed to the edge by my character's antics, snapped with language the original preset would have self-censored. It felt earned and human.

6. **The Omelette War**: In a domestic scene, four characters competed for the third omelette. The spotlight selector let two speak, the others fumed silently, and the tension resolved naturally instead of cycling through every NPC's opinion.

---

## 🔗 Tying It All Together

Every feature feeds into every other. The `roll_d20` rolls at the start. It determines the random event table outcome. That outcome may trigger a Chekhov seed plant. The same roll is used by the action resolution engine if a risky action occurs. It feeds the NPC retaliation intensity. It feeds the Plot Momentum path selection. A separate `npc_seed`, also rolled at the start, drives the Bold NPC action variance and the Spotlight Selection index.

The Chekhov tracker stores seeds from the Living World Engine. The Knowledge Scope task validates them. The Plot Momentum block displays them. The pruning and overcap rules keep the list manageable.

The Neutral Bias constitution tells NPCs they are allowed to be hostile, to swear, to leave, to intrude, to lie, to escalate. The Living World Engine gives them the mechanics to do so. The Bold NPC branch gives them the action framework. The random dice make it unpredictable.

---

## 🙏 Credits and Installation

This fork is built on the shoulders of **Freaky Frankenstein 4 MAX+** by Dptgreg and leovarian. The original preset's DNA is everywhere: the cinematographer role, the sensory physics, the VAD matrix, the colored dialogue, the immersive graphics, the NPC generator, the mimicry protocol. FrankenSIM would not exist without that foundation.

To use FrankenSIM, import the JSON into SillyTavern's preset manager. Enable only one Chain of Thought at a time. The **Freaky Novel Mode CoT** is the flagship 15-task experience. The Freaky Mode CoT is the same structure minus the literary-language override. The other CoTs remain in their original forms for now. Enable the toggles as you prefer, but the core stack expects `living_world_engine`, `chekhov_tracker`, `random_engine`, `action_resolution_engine`, `neutral_bias`, and `bold_npc` to be active for full effect.

The world no longer waits for you. The dice are rolling. The seeds are aging. The shampoo is slippery.

**Welcome to FrankenSIM.**
