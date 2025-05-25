from flask import Flask, request, jsonify, render_template 
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")  
def home():
    return render_template("index.html")
from datetime import datetime

@app.route("/checkin", methods=["POST"])
def checkin():
    data = request.get_json()
    mood = data.get("mood")
    journal = data.get("journal")
    timestamp = datetime.utcnow().isoformat()

    log_entry = f"{timestamp} | Mood: {mood} | Journal: {journal}\n"

    # Save to a file (optional)
    with open("checkins.log", "a", encoding="utf-8") as f:
        f.write(log_entry)

    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Haven, a gentle trauma-informed AI."},
            {"role": "user", "content": user_input}
        ]
    )
    return jsonify({"reply": response.choices[0].message["content"]})

if __name__ == "__main__":
    app.run(debug=True)