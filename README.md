Hi, yes I was shadowbanned off of Reddit. 

Thankfully there is now a new account made by ***someone*** who types suspiciously like me, has access to FrankenSIM 2.0, and just has to wait 1 day for the automod to cool down on reddit.

Golly gee willikers I don't know who this mysterious u/ok_strategy_2420 is but maybe in a day he woN'T GET BANNED AGAIN

Thanks for all the support.

Here was the post that got me banned:

---

Hi. 27 days ago, I released a very rushed 1.5 update to FrankenSIM. The bugfix update that added 14 features.

And, uh, yeah I certainly added features. Too many features. Honestly, it was so much more of a mess than you all gave me credit for. To the point where I had to stealth patch the dice engine itself just an hour after releasing it because for some reason that broke.

I went to get to work on 2.0 from there, and soon realized that 1.5 was just...not good. It was unstable, slow, token bloated to all hell, and overall just unreliable.

So. I scrapped it entirely. Burnt it to the ground. This is the reason I didn't post any beta builds on Github, because I kept rewriting the entire preset every other day.

But now, after almost a month of pretty constant work, and a solid group of actual beta testers testing this for the past few days, I can now present something I'm personally pretty proud of.

Factions, Alignment, and Aptitude from 1.5 have been dropped completely to hone in the scope. But BOND has absolutely flourished as a result.

There are so many small mechanics here that you might never actually see in action, and that's by design. You will only feel the results of it in the way your characters change and evolve in front of you. Every single block in this preset has been designed to work with each other in a way that can create a specific type of emotional complexity that I've *personally* never seen in a preset before (granted I've only tried like 6 but you know).

There's a lot in this preset. So I will go over the really big selling points.

Also, to the people for some reason saying that it's impossible for the AI to use dice to hurt the player, yeah. I wish that was the case. Then I wouldn't have had to make the ARC Engine. But instead now we have the AI not only blaming, but actively *cheering* the dice for my downfall.

Life is pain.

This is FrankenSIM 2.0.
---

## 👥 NPCs Now Have The Exact Same Relationship Systems As You

In 1.5, NPCs had rudimentary relationships with you. In 2.0, they have the exact same BOND, CRUSH, SIMMER, jealousy, and pair‑flag tracking **with each other**, all off‑screen, all persistent, all invisible to you until the ripples reach the surface.

#### **What this actually means, in practice:**

Two NPCs who share a room can now go from strangers to friends to lovers without you ever interacting with them. They accumulate CRUSH via shared vulnerability, casual touch, quality time, the exact same triggers that would apply if you were in the room. They can cross relationship thresholds off‑screen. They can become a couple, complete with a "couple" flag, and the next time you walk into the cafeteria, they're holding hands and you have zero context.

They can also break up. They can cheat. They can form love triangles that spawn jealousy subsystems. You see none of the mechanics. You just see a cold shoulder, a clipped reply, someone leaving the room when someone else enters, and you have to piece together why.

### **🧠 The State Engine That Makes This Possible**

Every named NPC is always being tracked via a dedicated location tag in the background. The off‑screen simulation knows where everyone is. When two NPCs share a location at the same time, a random encounter roll fires. If they meet, the engine applies CRUSH triggers directly, kindness, compliment, vulnerability, quality time, defense, affection, small gift, trust gesture. Max three per turn, per pair. This happens silently, every turn, whether you're watching or not.
NPCs also now have a SIMMER counter. Slighted? Offended? Someone broke a promise? The simmer ticks up. At seven active simmer seeds from one NPC toward a specific target, the engine forces a conflict escalation, they argue WITH EACH OTHER, not at you. And each night, when the clock crosses midnight, every simmer count above three drains BOND by one. The day's resentments settle in during sleep. By morning, someone likes their coworker a little less. That's not a scripted event. That's accumulated friction.

### **🎭 Jealousy, Love Triangles, and the RIVALRY Flag**

When an NPC with a crush witnesses their target interacting with a rival, or when gossip about that interaction reaches them through the social network, the engine plants a SIMMER seed on the rival and sets a persistent RIVALRY flag. While this flag is active, the jealous NPC's Valence toward the rival drops by one, Arousal ticks up, and they get +1 Bold when the rival is present. They're more performative. More reactive. More likely to stake a claim.

Rivalry expression varies by archetype: possessive types get territorial (frequent casual touch on the target, cold stares at the rival). Analytical types get competitive (pointed observations, proving superiority through competence). Aggressive types go direct (verbal challenges, open disdain). All of them escalate to raised voices only when simmer hits seven and conflict escalation triggers. Before that, it's friction. Not fire.

### **💬 GOSSIP: The World Talks About You (And Each Other)**

Gossip now propagates through BOND social links and shared locations. When a gossip‑worthy event happens, public flirtation, an argument, a lie exposed, an intimate moment witnessed, the engine plants a gossip seed. Every turn, that bullet spreads to one new NPC who shares a social connection or location with someone who already knows. The gossip network is literal. It traces friendships, dorm assignments, shared workplaces.

When gossip reaches someone with a strong bond to the subject OR the subject's known rival, it fires immediately. The hearer reacts per their bond tier, confrontation, jealousy planting, simmer toward the subject, or quiet filing away of the information. The bullet remains in the system, marked resolved, with a complete list of everyone who now knows. The secret is out. The ripple spreads. The user may never even hear about it.

### **🗣️ Character Card Calibration: Why Your NPC Still (mostly) Sounds Like Themself**

All of this, the BOND tiers, the CRUSH accumulation, the simmering resentment, the jealousy spirals, operates inside a strict hierarchy that the preset enforces every single turn. The character card is law. BOND tier sets the behavioral fence: what an NPC can physically do and verbally express. VAD adds emotional intensity and shading *inside* that fence, but never override it.

An NPC with +15 BOND who's shy and reserved will express attraction differently than a boisterous extrovert with the same +15. The shy NPC might press their forehead to yours in silence. The extrovert might shout it from a balcony. Both are valid. Both are in‑character. The preset doesn't flatten them into the same love confession, it filters the same gate through the card's voice.

And when an NPC has to do something the dice demand, attack when they're a pacifist, lie when they're honest, the card still controls the *how*. The pacifist stabs clumsily, cries afterward, drops the weapon. The honest person's lie comes out stilted, their tells obvious even if they don't admit it. The action happens. The voice never breaks. That's the hierarchy in practice.

---

## 🎭 The ARC Engine - 9-Act Narrative Architecture

I told myself I wouldn’t make this the headline feature, because the relationship engine is sexier. But the ARC Engine is the spine that holds the whole thing together.

It’s a dynamic, genre‑aware 9‑act story generator. It assigns a protagonist (sometimes an NPC, sometimes you), defines phase goals, bans resolution in early acts, and forces breathing room. It has its own BAN/ALLOW lists for every phase. Phase 0 cannot resolve anything, only observe, introduce, and foreshadow. Phase 5 allows everything. Phase 8 bans new conflicts entirely and forces closure.

The ARC Engine was born from a bug that I have been chasing since 1.0. A conflict-escalation loop so severe that I had to somehow find a way to force the story to not resolve itself on turn 3. After implementing, though, on Phase 0, the model generated a corruption plotline, a shadow fragment plotline, two made‑up NPCs essential to those plotlines, a backstory arc, a partial conclusion, a pet, and two romance options outside the BOND gate. It was a nuclear meltdown. I have since found the bug, but during the process I hardened the ARC Engine so much that it now is pretty much the main plot driver for 100+ turn narratives. And it works. It works really well, from my testing.

Now? It can generate stories on the fly where YOU aren't the protagonist. You can be the side character, or the witness, or even the comedic relief. Your role is generated upon ARC generation, making your RP have the same pacing as established novels, doesn't matter if it's mundane slice-of-life or an epic. It forces the plot to progress in a new way that I personally very much enjoy.

---

## 👁️ Object Occlusion & The User's POV

The world now has physics. Line of sight requires a clear path and a 120° forward arc. Solid obstructions, tables, counters, booth partitions, another person's torso, nullify vision at any distance. If two NPCs are on the same side of an obstruction from you, they can pass notes, touch, signal, or mouth words without you perceiving it. You find out only if you reposition to clear the obstruction.

Audio is gated the same way. Whispers behind a raised hand, under a table, or turned away halve their range. A conversation behind a closed door is muffled fragments. The reader is tied to the user's physical senses, what you can see, hear, and feel from your exact position. There is no omniscient narrator. No "meanwhile." No bridging. If you walk away mid‑conversation, the dialogue degrades through the audio gradient in real time: full sentences, then fragments, then tone, then warmth, then nothing.

This doesn't just extend to your character, it extends to everyone. The user, the NPCS, and even you, reader.

The narrator is now **physically tied to your character’s senses.** Vision is 120° forward only. Solid objects (tables, counters, other people’s backs) block line of sight. Audio has gradients, normal voice 10‑20m, whispering halved behind a hand or under a surface. Two NPCs on the other side of a booth can pass notes or mouth words without you perceiving them. And you can do the same back. No tells in prose, and they won't know about you either. Unless you're like me and rolled a nat 1 while flirting, and accidentally kicked the shit out of a table leg instead. Then they may know.
If you fall asleep, the prose degrades through the audio gradient in real time. Full dialogue → fragments → single words → sensory only → nothing. The scene ends when your perception fades, not when the NPCs stop talking.

You don’t see everything. You don’t hear everything. The world doesn’t pause when you look away.

---

## Links

**Download:** https://github.com/Ryah/ST-Freaky-D20-Preset/releases/tag/2.0

For Regex, use FF4's Plot Momentum regex. Saves a ton of tokens.

---

See you all soon for 3.0

---

## 🙏 Credits and Installation

This fork is built on the shoulders of **Freaky Frankenstein 4 MAX+** by Dptgreg and leovarian. The original preset's DNA is everywhere: the cinematographer role, the sensory physics, the VAD matrix, the colored dialogue, the immersive graphics, the NPC generator, the mimicry protocol. FrankenSIM would not exist without that foundation.

To use FrankenSIM, import the JSON into SillyTavern's preset manager. Enable only one Chain of Thought at a time. The **Freaky Novel Mode CoT** is the flagship 15-task experience. The Freaky Mode CoT is the same structure minus the literary-language override. The other CoTs remain in their original forms for now. Enable the toggles as you prefer, but the core stack expects `living_world_engine`, `chekhov_tracker`, `random_engine`, `action_resolution_engine`, `neutral_bias`, and `bold_npc` to be active for full effect.

The world no longer waits for you. The dice are rolling. The seeds are aging. The shampoo is slippery.

**Welcome to FrankenSIM.**
