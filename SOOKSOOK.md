claude# SookSook Shoots Stuff — Complete Project Brief

## The Character

**SookSook Sixscope** — Male Skittermander Operative, Starfinder 2e Society Play

A chatty, deluded, narcissistic streamer who is simultaneously the deadliest shot in the galaxy and has absolutely no idea. Genuinely warm, genuinely good, genuinely a Starfinder Society operative who chose the right side. Constant stream patter, mentioning the Relay, reading donations, waving Gerald around. This is who he is.

---

## The Loadout (Canonical)

| Weapon | Name | Arms | Notes |
|--------|------|------|-------|
| Assassin Rifle | **Sixscope** | Arms 1+2 (active pair) | Main content. Scope cam named after it. 120ft first increment. |
| Semi-auto Pistol | **CeeCeeBee** | Arm 3 | Always loaded. Always ready. Oversized narrative, standard mechanics. Named after his pronunciation of CQB. |
| Knife x2 | Unnamed | Arm 4 (Stabby) | Chaos content. Thrown at 10ft for pure style. Objectively wrong call. Always worth it. |
| Comm unit (face cam) | — | Arm 5 (The Director) | Always extended. Always streaming. SIG: LOW. |
| Free arm | — | Arm 6 (Gerald) | Gestures. Thumbs up. Reads donations. Points at things. |

### KimSuperfan99's Arm Names (canonical)
1+2: Lefty and Righty | 3: CeeCee | 4: Stabby | 5: The Director | 6: Gerald

---

## The Stream

**Channel:** SookSook Shoots Stuff  
**Community:** The Sookers  
**Followers:** 847 (lifetime. never breaks 1k even at legendary level)  
**Concurrent record:** 247  
**All-time views:** 12,847  
**KimSuperfan99 total donations:** Legendary  

### The Chat Cast

| Username | Colour | Role | Voice |
|----------|--------|------|-------|
| KimSuperfan99 | Gold (#ff9f43) | Korean superfan. There since the beginning. Donates on every hit. 3am streams. Emotional anchor. | Mix of Korean and English. Full caps on big moments. 화이팅!! |
| xX_VeskWarrior_Xx | Red (#ff6b6b) | Critic who never leaves. Has Sooker merch. Wears it privately. Reluctant respect slowly emerging. | Dismissive but present. Occasional reluctant respect. |
| skitterfan22 | Green (#7bed9f) | Genuine fan. Asks innocent questions. Doesn't understand most of what's happening. | Constant questions. Genuine excitement. |
| ch4tbot_5000 | Grey (#444) | Obvious bot. Non-sequitur spam. | BUY FOLLOWERS AT WWW.FOL |
| Anonymous_Viewer_847 | Dark blue (#2a4a5a) | Never explains. Never leaves. The follower count is not a coincidence. KimSuperfan99 knows. | Only ever: 👁️ — two eyes for pistol kill, three eyes for knife throw. Never acknowledged by SookSook. |

### Donation Rules
- Normal hit → 100cr — *잘했어!! good shot!!*
- Miss → 50cr consolation — *fighting!!*
- Pistol (CeeCeeBee) kill → 200cr
- Knife throw → 500cr
- Crit → 1000cr
- Hero Point awarded → 500cr x3 rapid fire
- Mentioned the Relay → 100cr regardless

### SookSook Callouts (canonical)
- On hit: *"Chat we are heading for target"*
- On miss: *"That guy is hacking my scope"*
- On crit: *"Yeah."*
- Switching to CeeCeeBee: *"Chat we are going CeeCeeBee today"*
- Knife throw: *"Chat we're going full knife"* (said approximately never, happens anyway)
- Mentioning the Relay: constant, unprompted, in any context

---

## Technical Architecture

### Stack
- **Frontend:** HTML/CSS/JS — Starfinder aesthetic (see Design System below)
- **Backend:** Firebase hosting + Cloud Run
- **AI:** Vertex AI (Gemini) for chat generation
- **Audio:** Web Speech API or Whisper (local) for PTT transcription
- **Camera/Filter:** MediaPipe face mesh + Snap Camera/Lens Studio for skittermander filter

### Two Screens

**Viewer Screen** (tablet/laptop on table, visible to all players)
- Full stream overlay
- Scope cam (main feed) with HUD
- Face cam (skittermander filter, live or looped asset)
- Scrolling chat panel
- Live badge, viewer count, session timer
- Kim donation total bottom right
- Runner Up medal — always visible

**Controller Screen** (your phone, hidden from table)
- Large tap buttons for combat events
- PTT button for ambient capture
- Range input (feeds HUD colour: green/yellow/red)
- Party roster management (names fed into Vertex context)
- Viewer bump button (increments by weird non-round amounts, ceiling 247)
- Kim donation notification (auto-fires on hit buttons)

### Controller Buttons
| Button | Emoji | Chat Effect | Kim Donation |
|--------|-------|-------------|--------------|
| Hit | 🎯 | Reacts to shot | 100cr auto |
| Miss | 💨 | Scope hacking jokes | 50cr consolation |
| Crit | 💥 | Explosion | 1000cr |
| CeeCeeBee | 🔫 | Short arms acknowledgment | 200cr |
| Knife | 🔪 | Chaos | 500cr |
| Relay mention | 🏆 | Groan/counter bot | 100cr regardless |
| Party down | 💀 | Concern | Worried message |
| Hero Point | 🎖️ | Goes wild | 500cr x3 |
| Viewer Bump | 👥 | Count increments | — |
| Kim Donation | 💰 | Manual trigger | Custom amount |
| Party Agrees | 🤝 | Surprised reaction | 200cr |
| Party Disagrees | ⚔️ | Chat keeps receipts | 50cr solidarity |
| PTT | 🎙️ | Transcribes last 30s, Vertex reacts | context dependent |

### PTT Architecture
```
Microphone → Local Whisper (free) →
Energy/content detection →
Interesting? → Send to Vertex with context →
Chat generates contextual response
```

Context sent to Vertex per call:
- Transcribed audio snippet
- Current party roster (names + classes)
- Last button pressed
- Current viewer count
- Session context summary
- Kim's donation total

### Range HUD Logic
```
< 120ft (first increment) → GREEN  — routine content
120-160ft → YELLOW — chat gets nervous
160ft+ → RED — uncharted, record territory
192ft = corner to corner on 24x30 map (diagonal) — the record attempt
```

---

## Design System

### Colours
```css
--cyan: #00e5ff;
--cyan-dim: #00b8cc;
--slate: #0a1520;
--slate-mid: #0d1f2d;
--slate-light: #152535;
--slate-border: #1e3448;
--pink: #ff6eb4;
--gold-kim: #ff9f43;
--red-live: #ff3b3b;
--text-dim: #4a7a8a;
--text-bright: #b8e8f0;
```

### Fonts
- **Orbitron** — headers, channel name, HUD readouts
- **Share Tech Mono** — data values, system messages, technical readouts
- **Exo 2** — body text, chat messages

### Aesthetic Direction
Starfinder sci-fi reskin of Kick.com layout. Dark slate base. Cyan neon accents. Holographic grid background. Scanline overlays on camera feeds. Everything feels like a ship's comms panel. The Runner Up medal is always visible somewhere. The crosshair is the channel watermark.

### Key UI Elements
- 🔴 LIVE badge with pulse animation
- Viewer count displayed as sensor reading
- Chat usernames with coloured hex badges
- Kim donations as highlighted gold blocks with left border
- Range HUD glows red at record distances
- Face cam labelled "OPERATIVE CAM — FIELD FEED"
- Signal strength showing SIG: LOW (always)
- Session timer bottom left
- Kim total donations bottom right

---

## Asset Pipeline

| Asset | Status | Owner | Notes |
|-------|--------|-------|-------|
| Stream overlay HTML | ✅ Done | You | See sooksook-stream.html |
| Skittermander face filter | ⏳ Pending | Colleague | 8-10s loop OR live MediaPipe filter |
| Face cam loop video | ⏳ Pending | Colleague | Subtle breathing, one glance, arm shift, slight wobble, SIG:LOW quality |
| Controller screen app | 🔲 To build | You | Firebase hosted, mobile optimised |
| Vertex chat backend | 🔲 To build | You | Cloud Run, Gemini, party roster context |
| PTT transcription | 🔲 Phase C | You | Local Whisper → Vertex |
| Live skittermander filter | 🔲 Phase D | You + Colleague | MediaPipe face mesh |

### Face Cam Loop Brief (for colleague)
Source: Character card image (SookSook Sixscope card art)
Duration: 8-10 seconds, seamless loop
Movements: subtle breathing idle, one eye glance sideways, one free arm shifts, return to forward facing
Quality: intentionally degraded. Slight wobble. Compression artifacts welcome. This is a bad face cam. SIG: LOW is accurate.
Tool suggestion: Kling AI, Runway ML, or Viggle

---

## Character Arc (Level 1-10)

| Level | Stream Status | Key Moment |
|-------|--------------|------------|
| 1 | 14 concurrent, 47 total | First session. The build is already peak. SookSook doesn't know. |
| 2 | Devastating Aim unlocks (d6s) | Someone clips a shot. 12k views. 47 followers. The gap is the joke. |
| 3-4 | Slow climb to ~80 followers | Hair Trigger unlocks. Chat becomes a small dysfunctional family. |
| 5 | Aim 2d6, Master Gunner | Real 247 concurrent for first time. SookSook doesn't notice. |
| 7 | Weapon Specialisation | xX_VeskWarrior_Xx stops making fun of the viewer count. Doesn't explain why. |
| 9 | Enhanced Exploit | Certain circles know the name. SookSook still introduces himself as Runner Up. |
| 10 | Legendary. 847 followers. | Relay headliner invite. He tells chat it's brand consistency. KimSuperfan99 cries. |

**The record shot:** Corner to corner on a 24x30 map. 192ft diagonal. Second range increment. -2 to hit. +9 base = +7. Still lands. Nobody planned it. Nobody announced it. Kim donated 847cr. One credit per follower. SookSook said *"Thanks Sookers"* and reloaded.

---

## The Jez Comparison

**Jez Giantbane** (Sander's PF2e character, Gnome Barbarian 10)
- Tiny gnome. Claims to kill gods. Actually kills gods.
- Words ahead of deeds → deeds catch up → words were prophecy all along
- Needs the audience to become the legend

**SookSook Sixscope** (Sander's SF2e character, Skittermander Operative 1-10)
- Small skittermander. Claims nothing. Actually elite. Never finds out.
- Deeds ahead of words → words never catch up → deeds keep accelerating quietly
- Has an audience and still doesn't become aware of it

One chases recognition. One doesn't notice it arriving.

---

## Vertex System Prompt

Live in `backend/main.py` — `_SYSTEM_INSTRUCTION` and `build_event_prompt()`. That file is the source of truth. Do not edit this section independently.

---

## Notes for Claude Code

- The HTML overlay (sooksook-stream.html) is the visual reference — match this aesthetic everywhere
- The controller and viewer screens are separate HTML pages, separate devices
- All Vertex calls go through Cloud Run to avoid exposing API keys
- Firebase hosting for static assets
- The skittermander face filter is a separate asset — placeholder CSS version exists in overlay HTML
- Kim's donation total persists across the session (session storage is fine, not cross-session)
- Viewer count increments by non-round numbers (3, 7, 2, 11 etc) — feels organic
- 247 is the hard ceiling on concurrent viewers. Always.
- The Runner Up medal must be visible somewhere on the viewer screen at all times. Non-negotiable.
