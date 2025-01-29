import requests
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
port = int(os.environ.get('PORT', 2000))


@app.route("/")
def home():
    return "Hello, this is a Flask Microservice"

OLLAMA_URL = "http://localhost:11434/api/generate"
@app.route("/ask", methods=["POST"])
def ask_ollama():
    # Get the user input from the request
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in request"}), 400

    # Send the request to Ollama
    response = requests.post(OLLAMA_URL, json={
        "model": "llama2",  # Make sure llama2 or your chosen model is available
        "prompt": data["prompt"],
        "stream": False
    })

    # Handle the response from Ollama
    if response.status_code == 200:
        response_data = response.json()
        return jsonify({"response": response_data.get("response", "No response from model")})
    else:
        return jsonify({"error": f"Request failed with status {response.status_code}"}), response.status_code

if __name__ == "__main__":
    app.run(debug=True, port=2000)
