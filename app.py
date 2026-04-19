from flask import Flask, render_template, request, jsonify, send_file
from groq import Groq
from dotenv import load_dotenv
import edge_tts
import asyncio
import os
import uuid

# =========================
# APP
# =========================
app = Flask(__name__)

# =========================
# LOAD ENV
# =========================
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# =========================
# MEMORY FILE
# =========================
MEMORY_FILE = "memory.txt"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        f.write("User name is Ayan\n")
        f.write("Age 19\n")
        f.write("Likes coding\n")

# =========================
# LOAD MEMORY
# =========================
def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

# =========================
# SAVE MEMORY
# =========================
def save_chat(user, bot):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"\nUser: {user}")
        f.write(f"\nAI: {bot}\n")

# =========================
# AI REPLY
# =========================
def ai_reply(msg):

    memory = load_memory()

    try:
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role":"system",
                    "content":f"""
You are Bidwiya.

You are a cute Bengali female AI friend.

User name Ayan.

Known memory:
{memory}

Reply short Bengali style.
Natural sweet talking style.
"""
                },
                {
                    "role":"user",
                    "content":msg
                }
            ],
            temperature=0.8,
            max_tokens=300
        )

        reply = chat.choices[0].message.content

        save_chat(msg, reply)

        return reply

    except Exception as e:
        return "Ami ekhon reply dite parchi na 😔"

# =========================
# EDGE TTS VOICE
# =========================
async def make_voice_async(text, file):
    communicate = edge_tts.Communicate(
        text=text,
        voice="bn-BD-NabanitaNeural"
    )
    await communicate.save(file)

def make_voice(text):
    filename = f"{uuid.uuid4().hex}.mp3"
    asyncio.run(make_voice_async(text, filename))
    return filename

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    msg = data["msg"]

    reply = ai_reply(msg)

    return jsonify({"reply": reply})

@app.route("/voice")
def voice():

    text = request.args.get("text")

    if not text:
        text = "Hello"

    file = make_voice(text)

    return send_file(file, mimetype="audio/mpeg")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
