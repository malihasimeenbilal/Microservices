import requests
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

@app.route("/")
def home():
    return "Hello, this is a Flask Microservice for ollama page"

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

@app.route("/ask", methods=["POST"])
def ask_ollama():
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in request"}), 400

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3.2",
        "prompt": data["prompt"],
        "stream": False
    })

    if response.status_code == 200:
        response_data = response.json()
        return jsonify({"response": response_data.get("response", "No response from model")})
    else:
        return jsonify({"error": f"Request failed with status {response.status_code}"}), response.status_code

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)