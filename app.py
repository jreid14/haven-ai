
import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from datetime import datetime

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)