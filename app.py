from flask import Flask, request, jsonify, render_template 
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")  "comment"
def home():
    return render_template("index.html")

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