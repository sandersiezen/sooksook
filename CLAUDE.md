# SookSook Shoots Stuff — Claude Code Context

## What This Project Is
A fake live stream overlay and controller app for a Starfinder Society tabletop RPG character named SookSook Sixscope. Used as a prop at the gaming table. Driven by Vertex AI (Gemini) for dynamic chat generation.

## Full Project Brief
See `SOOKSOOK.md` for complete context including:
- Character background and psychology
- Full weapon loadout with canonical names
- Chat character voices and donation rules
- Controller button spec
- Design system (colours, fonts, aesthetic)
- Asset pipeline status
- Vertex AI system prompt
- Character arc level 1-10

## Stack
- **Hosting:** Firebase
- **Backend:** Google Cloud Run
- **AI:** Vertex AI (Gemini)
- **Transcription:** Local Whisper (PTT mode)
- **Camera filter:** MediaPipe face mesh / Snap Camera Lens Studio
- **Frontend:** Vanilla HTML/CSS/JS
- **IDE:** PyCharm with Claude Code

## Two Apps
1. **Viewer Screen** (`viewer/`) — Stream overlay displayed on table for all players. Starfinder sci-fi Kick.com aesthetic.
2. **Controller Screen** (`controller/`) — Hidden mobile interface for the player. Large tap buttons. PTT. Range input.

## Design System (quick ref)
```css
--cyan: #00e5ff;
--slate: #0a1520;
--gold-kim: #ff9f43;
```
Fonts: Orbitron (headers) + Share Tech Mono (data) + Exo 2 (body)
Reference: `sooksook-stream.html` (existing overlay mockup)

## Critical Rules
- Viewer count NEVER exceeds 247 concurrent. Hard ceiling. Always.
- Runner Up medal must be visible on viewer screen at all times.
- Kim donates on every hit event. Auto-trigger.
- Anonymous_Viewer_847 only ever responds with 👁️ variants. Never explain.
- All Vertex calls via Cloud Run. Never expose API keys to frontend.
- Viewer count increments by non-round numbers (3, 7, 11 etc). Never round numbers.

## Current Status
- [x] Stream overlay HTML mockup complete (sooksook-stream.html)
- [ ] Controller screen app
- [ ] Viewer screen app (dynamic version of mockup)
- [ ] Cloud Run Vertex AI backend
- [ ] PTT transcription pipeline
- [ ] Skittermander face filter (colleague handling asset)

## Aesthetic Reference
Dark sci-fi. Cyan neon on slate. Holographic grid. Scanlines on camera feeds. Everything looks like a ship's comms panel. Orbitron font everywhere important. The stream is bad quality on purpose. SIG: LOW is accurate not aesthetic.
