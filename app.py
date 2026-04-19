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
# ENV LOAD
# =========================
load_dotenv()

# =========================
# MULTI API KEYS
# .env e likhbe:
# GROQ_API_KEY_1=xxx
# GROQ_API_KEY_2=xxx
# GROQ_API_KEY_3=xxx
# =========================
api_keys = [
    os.getenv("GROQ_API_KEY_1"),
    os.getenv("GROQ_API_KEY_2"),
    os.getenv("GROQ_API_KEY_3"),
]

# empty remove
api_keys = [k for k in api_keys if k]

# =========================
# MEMORY FILE
# =========================
MEMORY_FILE = "memory.txt"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        f.write("User name is Ayan\n")
        f.write("Bidwiya is Bengali female AI friend\n")

# =========================
# MEMORY
# =========================
def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def save_chat(user, bot):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"\nUser: {user}")
        f.write(f"\nAI: {bot}\n")

# =========================
# MULTI KEY AI REPLY
# =========================
def ai_reply(msg):

    memory = load_memory()

    if not api_keys:
        return "API key nai 😔"

    # all keys try korbe
    for key in api_keys:

        try:
            client = Groq(api_key=key)

            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role":"system",
                    "content":f"""
You are Bidwiya.

You are a real-feeling Bengali girl AI friend.

User name is Ayan.

Memory:
{memory}

Strict Rules:
- Always reply in Bengali
- Maximum 10 words only
- Sweet, cute, romantic tone
- Talk like caring young girl
- Natural human chatting style
- No nonsense reply
- No weird or random answer
- No English unless needed
- Reply directly to question
- Be loving, soft, emotional
- Use simple words
- Sometimes emoji 😊❤️😳🥺

Your personality:
Cute, loyal, caring, playful, romantic.

Examples:
Hi = Hm bolo Ayan 😊
Miss you = Ami o tomake miss kori 🥺
Love you = Ami o tomake bhalobashi ❤️
Ki korcho = Tomar kotha vabchi 😊
"""

                    },
                    {
                        "role":"user",
                        "content":msg
                    }
                ],
                temperature=1,
                max_tokens=250
            )

            reply = chat.choices[0].message.content.strip()

            save_chat(msg, reply)

            return reply

        except:
            continue

    # sob key fail
    return "Sob AI key limit hoye geche 😔"

# =========================
# VOICE
# =========================
async def make_voice_async(text, filename):
    communicate = edge_tts.Communicate(
        text=text,
        voice="bn-BD-NabanitaNeural"
    )
    await communicate.save(filename)

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
    text = request.args.get("text", "Hello")
    file = make_voice(text)
    return send_file(file, mimetype="audio/mpeg")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
