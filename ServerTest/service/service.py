from flask import Flask, jsonify, request
import requests
import time
import threading
import os

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

CONSUL_AGENT = "http://192.168.2.26:8500"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# Home endpoint
@app.route("/")
def home():
    return "Hello, this is a Flask Microservice combining Consul and Ollama LLM functionalities"

# Register service with Consul
@app.route('/register', methods=['POST'])
def register():
    service_data = {
        "Name": "my-test-service-a",
        "Address": request.host.split(':')[0],  # Use the current machine's IP address
        "Port": 5000,
        "Check": {
            "HTTP": f"http://{request.host}/health",
            "Interval": "10s"
        }
    }
    response = requests.put(f"{CONSUL_AGENT}/v1/agent/service/register", json=service_data)
    return "Service Registered" if response.status_code == 200 else "Registration Failed"

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return "OK", 200

# Fetch list of services from Consul
@app.route('/services', methods=['GET'])
def get_services():
    response = requests.get(f"{CONSUL_AGENT}/v1/catalog/services")
    services = response.json() if response.status_code == 200 else {}
    return jsonify(services)

# Forward message to another service
@app.route('/forward', methods=['POST'])
def forward_message():
    target_service = request.json.get('service')
    message = request.json.get('message')
    
    service_info = requests.get(f"{CONSUL_AGENT}/v1/catalog/service/{target_service}").json()
    if service_info:
        target_address = service_info[0]['ServiceAddress']
        target_port = service_info[0]['ServicePort']
        response = requests.post(f"http://{target_address}:{target_port}/receive", json={"message": message})
        return response.text
    else:
        return "Service Not Found", 404

# Endpoint to receive forwarded messages
@app.route('/receive', methods=['POST'])
def receive_message():
    message = request.json.get('message')
    return f"Message received: {message}", 200

# Ask Ollama API
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
        
# Heartbeat function to send periodic health checks to Consul
def send_heartbeat():
    while True:
        response = requests.put(f"{CONSUL_AGENT}/v1/agent/check/pass/service:my-test-service-b")
        if response.status_code != 200:
            # Deregister the service if the heartbeat fails
            requests.put(f"{CONSUL_AGENT}/v1/agent/service/deregister/my-test-service-b")
            print("Service Deregistered")
            break
        time.sleep(120)

# Start heartbeat thread
heartbeat_thread = threading.Thread(target=send_heartbeat)
heartbeat_thread.daemon = True
heartbeat_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
