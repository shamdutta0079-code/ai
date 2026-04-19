from flask import Flask, render_template, request, jsonify, send_file
from groq import Groq
from dotenv import load_dotenv
from gtts import gTTS
import os, uuid

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MEMORY_FILE = "memory.txt"

if not os.path.exists(MEMORY_FILE):
    open(MEMORY_FILE,"w",encoding="utf-8").write("User name Ayan\n")

def load_memory():
    return open(MEMORY_FILE,"r",encoding="utf-8").read()

def save_chat(u,b):
    with open(MEMORY_FILE,"a",encoding="utf-8") as f:
        f.write(f"\nUser:{u}\nAI:{b}\n")

def ai_reply(msg):

    memory = load_memory()

    try:
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role":"system",
                    "content":f"""
You are Bidwiya Bengali AI.
User is Ayan.

Memory:
{memory}

Reply short Bengali style.
"""
                },
                {
                    "role":"user",
                    "content":msg
                }
            ]
        )

        reply = chat.choices[0].message.content
        save_chat(msg,reply)
        return reply

    except:
        return "AI Error"

def voice_make(text):
    name = f"{uuid.uuid4().hex}.mp3"
    gTTS(text=text,lang="bn").save(name)
    return name

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat",methods=["POST"])
def chat():
    msg = request.json["msg"]
    reply = ai_reply(msg)
    return jsonify({"reply":reply})

@app.route("/voice")
def voice():
    text = request.args.get("text")
    file = voice_make(text)
    return send_file(file,mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)