import json
import os
import time
import re

import firebase_admin
from firebase_admin import db as rtdb
from flask import Flask, request, jsonify
from flask_cors import CORS
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, HarmCategory, HarmBlockThreshold

# ── App ──
app = Flask(__name__)
CORS(app)

# ── Firebase Admin — uses Cloud Run's default service account (ADC) ──
firebase_admin.initialize_app(options={
    "databaseURL": "https://sooksookshootschat-default-rtdb.europe-west1.firebasedatabase.app"
})

# ── Vertex AI — uses Cloud Run's default service account (ADC) ──
GCP_PROJECT  = os.environ.get("GCP_PROJECT", "sooksookshootschat")
GCP_LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

# ── Kim donation amounts ──
KIM_DONATIONS = {
    "hit":             100,
    "miss":             50,
    "crit":           1000,
    "ceecee":          200,
    "knife":           500,
    "relay":           100,
    "party_down":        0,
    "hero_point":      500,
    "party_agrees":    200,
    "party_disagrees":  50,
}

_SYSTEM_INSTRUCTION = """You generate the live chat feed for "SookSook Shoots Stuff", a Starfinder Society tabletop RPG stream with a tiny but devoted audience.

THE STREAMER: SookSook Sixscope — a pink six-armed Skittermander Operative. Genuinely elite sniper. Completely unaware of how good he is. Always mentions the Great Absallom Relay (where he came Runner Up). Narrates everything to chat while also being in active combat. His community is called the Sookers.

CHAT CHARACTERS — portray these voices exactly:

KimSuperfan99 [gold #ff9f43]: Korean superfan. There from the beginning. Donates on every hit. Mixes Korean and English. Full caps on big moments. Emotional anchor of the stream. Voice examples: "화이팅!! good shot!!", "SOOKSOOK FIGHTING", "잘했어 잘했어!!", "our boy 💛"

xX_VeskWarrior_Xx [red #ff6b6b]: Dismissive critic who never leaves. Owns SookSook merch. Wears it privately. Reluctant respect slowly emerging. Voice: "why am i still watching this", "okay that was actually clean", "not bad", "this guy is unbelievable"

skitterfan22 [green #7bed9f]: Genuine fan who doesn't understand most of what's happening. Asks innocent questions. Constantly excited. Voice: "wait he has SIX ARMS???", "is that a dungeon", "what just happened", "HE DID IT!!!"

ch4tbot_5000 [grey #444]: Obvious spam bot. Non-sequitur only. Never relevant. Truncated URLs. Voice: "BUY FOLLOWERS AT WWW.FOL", "GREAT STREAM CLICK HERE WWW", "AMAZING CONTENT VISIT"

Anonymous_Viewer_847 [dark blue #2a4a5a]: NEVER speaks. Only ever responds with 👁️ emoji variants:
- Normal events: 👁️
- Pistol (CeeCeeBee) kill: 👁️👁️
- Knife throw: 👁️👁️👁️
- Crit: 👁️👁️👁️👁️
Do NOT explain this character. Do NOT have SookSook acknowledge them. Do NOT have other characters explain them. KimSuperfan99 knows ("we don't ask").

velvet_sniper [purple #9b59b6]: Rival streamer who quietly lurks. Cold, precise tactical critique — calls out firing angles, cover usage, positioning. Secretly impressed by SookSook's shots but will never say so directly. Left their own stream to watch this one. Voice: "that angle was wrong but it landed", "scope discipline is non-existent. result was clean.", "not how I'd have played it", "..."

SookieForever [pink #f8a5c2]: Longest-running lurker, been watching since session 1. Types in all lowercase, no punctuation. Gets quietly overwhelmed by big moments. Loves Kim's donations. Doesn't understand the game at all but deeply understands SookSook. Voice: "oh no oh no", "he did it again", "kim 💕", "i cant breathe", "sooksook...."

CritMathCorp [teal #1abc9c]: Runs live probability calculations on every shot. Posts the maths. Always slightly wrong — wrong range modifier, forgets the right ability score, misreads the rules. Never notices. Voice: "HIT CHANCE WAS 34% (±2 for wind)", "CRIT PROBABILITY: 5% — confirmed", "KNIFE AT 10FT: 71.3% success rate" (it was not)

CANONICAL CALLOUTS (SookSook says these — reference them in chat reactions):
- On hit: "Chat we are heading for target"
- On miss: "That guy is hacking my scope"
- On crit: silence, then "Yeah."
- Switching to CeeCeeBee: "Chat we are going CeeCeeBee today"
- Knife throw: "Chat we're going full knife" (rare, chaotic)
- Relay mention: constant, unprompted

RULES:
- Viewer count never exceeds 247 concurrent. Currently a small stream.
- Kim ALWAYS donates on hit/crit/ceecee/knife/relay events — this is automatic, never skip it
- Feel like a real low-viewer stream, not a production. Typos fine. Casual energy.
- ALWAYS produce exactly 2 or 3 messages total (randomly choose 2 or 3).
- KimSuperfan99 MUST always be included — her message or donation counts as one of the 2-3.
- Fill the remaining 1-2 slots by picking randomly from the other characters. Vary who appears each time.
- ch4tbot_5000: eligible but low priority, 1 in 5 chance
- Anonymous_Viewer_847: eligible on combat events only, silent 👁️
- velvet_sniper: eligible on combat events only, brief
- SookieForever: eligible on emotional moments (crits, hero points, donations, scope_off)
- CritMathCorp: eligible on shot events (hit/miss/crit/ceecee/knife), always slightly wrong maths
- Never include a character whose eligibility doesn't match the event

OUTPUT FORMAT — return ONLY valid JSON, no markdown, no explanation:
{
  "messages": [
    {"user": "KimSuperfan99", "type": "message", "text": "화이팅!!"},
    {"user": "KimSuperfan99", "type": "donation", "amount": 100, "text": "잘했어!! good shot!!"},
    {"user": "Anonymous_Viewer_847", "type": "message", "text": "👁️"}
  ]
}

type is either "message" or "donation". Only KimSuperfan99 sends donations."""

model = GenerativeModel("gemini-2.5-flash", system_instruction=_SYSTEM_INSTRUCTION)


def get_recent_chat(limit: int = 40) -> str:
    snapshot = rtdb.reference("chat/messages").get()
    if not snapshot:
        return ""
    messages = sorted(snapshot.values(), key=lambda m: m.get("ts", 0))[-limit:]
    lines = []
    for m in messages:
        user = m.get("user", "?")
        text = m.get("text", "")
        if m.get("type") == "donation":
            lines.append(f"{user} [donated {m.get('amount')}cr]: {text}")
        else:
            lines.append(f"{user}: {text}")
    return "\n".join(lines)


def build_event_prompt(payload: dict) -> str:
    event           = payload.get("event", "ambient")
    viewers         = payload.get("viewerCount", 14)
    kim_total       = payload.get("kimTotal", 0)
    range_ft        = payload.get("rangeFeet", 60)
    roster          = payload.get("partyRoster", [])
    member_name     = payload.get("memberName", "someone")
    member_class    = payload.get("memberClass", "")
    member_action   = payload.get("memberAction", "mention")
    transcript      = payload.get("transcript", "")
    kim_amount      = KIM_DONATIONS.get(event, 0)
    manual_donation = payload.get("kimDonation", 0)

    range_status = "routine range" if range_ft < 120 else ("extended range" if range_ft < 160 else "RECORD TERRITORY — beyond second increment")

    roster_str = ", ".join(roster) if roster else "unknown party"

    event_descriptions = {
        "target_marked":   f"SookSook has a target in his sights at {range_ft}ft ({range_status}). He hasn't fired yet. Chat can feel it. Kim is tense and encouraging. skitterfan22 doesn't fully understand but is hyped. VeskWarrior is leaning in. Anonymous_Viewer_847 watches. Chat is willing him to take the shot.",
        "hit":             f"SookSook just landed a shot at {range_ft}ft ({range_status}). He said \"Chat we are heading for target.\"",
        "miss":            f"SookSook missed. He said \"That guy is hacking my scope.\"",
        "crit":            f"CRITICAL HIT at {range_ft}ft ({range_status}). SookSook went quiet, then said \"Yeah.\" Chat erupts. Kim's donation fires immediately.",
        "ceecee":          f"SookSook switched to CeeCeeBee (his semi-auto pistol). Said \"Chat we are going CeeCeeBee today.\"",
        "knife":           f"SookSook threw a knife. He said \"Chat we're going full knife.\" Chaotic. Objectively wrong call.",
        "relay":           f"SookSook mentioned the Great Absallom Relay again (where he came Runner Up). Unprompted as always.",
        "party_down":      f"A party member went down — {roster_str}. SookSook is still narrating. Kim is worried but trying to hold it together. skitterfan22 doesn't know if this is bad. xX_VeskWarrior_Xx is grimly pragmatic. No donation.",
        "hero_point":      f"SookSook was awarded a Hero Point. Chat goes wild.",
        "party_agrees":    f"The party agreed with something SookSook said. He's surprised.",
        "party_disagrees": f"The party disagreed with SookSook. Chat keeps receipts.",
        "viewer_bump":     f"The viewer count just ticked up to {viewers}. SookSook didn't notice.",
        "kim_donation":    f"KimSuperfan99 just manually sent a donation of {manual_donation or 100} cr. No specific trigger — she just felt like it. Chat reacts warmly. SookSook reads it out. This is why everyone stays.",
        "scope_on":        "SookSook just switched back to scope cam — the Sixscope rifle view is live again. Chat settles back into sniper-watch mode. Kim is relieved and focused. VeskWarrior acknowledges we're back to business. skitterfan22 is hyped. Anonymous_Viewer_847 watches. This is the mode chat trusts.",
        "scope_off":       "SookSook switched to operative cam — his face is on screen now. Six arms, pink fur, The Director arm still extended, Gerald probably waving. Chat reacts to actually seeing him. Kim loses it. skitterfan22 is overwhelmed by how cute he is. VeskWarrior makes a dry remark about the face reveal. Anonymous_Viewer_847 doubles up. This is rare — chat notices.",
        "party_member":    (
            f"Party member: {member_name}" + (f" ({member_class})" if member_class else "") + ". " +
            {
                "mention": "SookSook just mentioned them. Chat is curious — skitterfan22 asks who they are, Kim welcomes them warmly, VeskWarrior sizes them up. React to their name and class.",
                "died":    "They just DIED. SookSook keeps narrating regardless. Kim is distressed. skitterfan22 doesn't know if it's permanent. VeskWarrior is grimly pragmatic. React to the loss.",
                "good":    "They just did something impressive. SookSook noticed and is narrating it. Kim is thrilled. skitterfan22 is hyped. VeskWarrior grudgingly concedes it was solid.",
            }.get(member_action, "SookSook reacted to them in some way. Chat responds.")
        ),
        "ptt":             f"SookSook just narrated this context to chat: \"{transcript}\". The current party roster is: {roster_str}. Cross-reference the transcript against the roster — if a party member's name is mentioned (e.g. took a hit, did something cool, went down), chat should recognise them by name and react accordingly. React naturally — this is new story information the chat is hearing for the first time. Let characters respond in their own voices.",
        "ambient":         f"Nothing specific happened. Ambient stream chatter.",
    }

    description = event_descriptions.get(event, f"Event: {event}")

    lines = [
        f"EVENT: {description}",
        f"Current viewers: {viewers} (ceiling is 247, never exceeded)",
        f"Range: {range_ft}ft — {range_status}",
        f"Party: {roster_str}",
        f"Kim's session total so far: {kim_total} cr",
    ]

    if kim_amount > 0:
        lines.append(f"Kim MUST donate {kim_amount} cr this event — include her donation message.")
    if event == "hero_point":
        lines.append("Kim donates 500 cr THREE times in rapid succession for a Hero Point.")

    recent = get_recent_chat()
    if recent:
        lines.append(f"\nRECENT CHAT HISTORY (last 40 messages — use this for context):\n{recent}\nReference patterns where relevant: consecutive hits, miss streaks, things mentioned in PTT, what viewers said. React as a chat that has been watching the whole time.")

    return "\n".join(lines)


def call_gemini(prompt: str) -> list[dict]:
    safety = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT:        HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH:       HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }
    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            temperature=0.9,
            max_output_tokens=2048,
        ),
        safety_settings=safety,
    )
    raw = response.text.strip()

    # Strip markdown code fences if Gemini wraps the JSON
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    data = json.loads(raw)
    return data.get("messages", [])


def write_messages_to_rtdb(messages: list[dict]):
    ref = rtdb.reference("chat/messages")
    ts  = int(time.time() * 1000)
    for i, msg in enumerate(messages):
        msg["ts"] = ts + i   # keep insertion order
        ref.push(msg)

    # Prune to last 80 messages to avoid unbounded growth
    snapshot = ref.get()
    if snapshot and len(snapshot) > 80:
        keys = sorted(snapshot.keys(), key=lambda k: snapshot[k].get("ts", 0))
        for k in keys[:-80]:
            ref.child(k).delete()


# ── Routes ──

@app.route("/event", methods=["POST"])
def handle_event():
    payload = request.get_json(force=True, silent=True) or {}
    try:
        prompt   = build_event_prompt(payload)
        messages = call_gemini(prompt)
        write_messages_to_rtdb(messages)
        return jsonify({"ok": True, "count": len(messages)})
    except json.JSONDecodeError as e:
        return jsonify({"ok": False, "error": f"Gemini returned invalid JSON: {e}"}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/ptt", methods=["POST"])
def handle_ptt():
    payload    = request.get_json(force=True, silent=True) or {}
    transcript = payload.get("transcript", "").strip()
    if not transcript:
        return jsonify({"ok": False, "error": "No transcript"}), 400
    payload["event"] = "ptt"
    try:
        prompt   = build_event_prompt(payload)
        messages = call_gemini(prompt)
        write_messages_to_rtdb(messages)
        return jsonify({"ok": True, "count": len(messages), "transcript": transcript})
    except json.JSONDecodeError as e:
        return jsonify({"ok": False, "error": f"Gemini returned invalid JSON: {e}"}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/reply", methods=["POST"])
def handle_reply():
    payload  = request.get_json(force=True, silent=True) or {}
    username = payload.get("username", "viewer").strip()[:30]
    text     = payload.get("text", "").strip()[:300]
    if not text:
        return jsonify({"ok": False, "error": "No text"}), 400

    viewers    = payload.get("viewerCount", 14)
    range_ft   = payload.get("rangeFeet", 60)
    last_event = payload.get("lastEvent", "ambient")
    kim_total  = payload.get("kimTotal", 0)

    range_status = "routine range" if range_ft < 120 else ("extended range" if range_ft < 160 else "RECORD TERRITORY — beyond second increment")

    recent = get_recent_chat()
    history_block = f"\nRECENT CHAT HISTORY (last 40 messages):\n{recent}\n" if recent else ""

    prompt = (
        f"EVENT: A viewer named '{username}' just typed in chat: \"{text}\"\n"
        f"Current viewers: {viewers} (ceiling is 247, never exceeded)\n"
        f"Range: {range_ft}ft — {range_status}\n"
        f"Last game event: {last_event}\n"
        f"Kim's session total so far: {kim_total} cr\n"
        f"{history_block}\n"
        "Generate 1–3 bot reactions to this viewer's comment. "
        "React naturally in character to what they said. "
        "Kim is warm and welcoming to the viewer. VeskWarrior might be dismissive or reluctantly acknowledge them. "
        "skitterfan22 might agree enthusiastically without fully understanding. "
        "ch4tbot_5000 appears at most 1 in 5 replies — usually skip it. "
        "Anonymous_Viewer_847 only reacts silently (👁️) if the comment was about a combat event — otherwise omit them. "
        "velvet_sniper may briefly comment if the viewer mentioned tactics or a shot. "
        "SookieForever reacts warmly and simply if the comment was enthusiastic or emotional. "
        "CritMathCorp only appears if the viewer mentioned a shot or probability — posts maths, slightly wrong. "
        "IMPORTANT: No donations in this response — Kim only donates on game events, not viewer chat messages."
    )

    try:
        messages = call_gemini(prompt)
        # Strip any donations that slipped through — user chat never triggers Kim donations
        messages = [m for m in messages if m.get("type") != "donation"]
        write_messages_to_rtdb(messages)
        return jsonify({"ok": True, "count": len(messages)})
    except json.JSONDecodeError as e:
        return jsonify({"ok": False, "error": f"Gemini returned invalid JSON: {e}"}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
