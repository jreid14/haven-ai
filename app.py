
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
from datetime import datetime

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/checkin", methods=["POST"])
def checkin():
    data = request.json
    mood = data.get("mood")
    journal = data.get("journal")
    timestamp = datetime.now().isoformat()

    with open("checkins.log", "a") as f:
        f.write(f"{timestamp} | Mood: {mood} | Journal: {journal}\n")

    return jsonify({"message": "Check-in saved successfully."})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    print("Received message:", user_message)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive and emotionally intelligent assistant named Haven."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        print("AI reply:", reply)
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ OpenAI error:", e)
        if "insufficient_quota" in str(e):
            return jsonify({"reply": "Our AI assistant is temporarily unavailable due to API limits. Please try again later."})
        return jsonify({"error": str(e)}), 500
