We now use an AWS EC2 instance to construct a cloud server and run consul and traefik to bypass the campus network firewall restriction.

Because the EC2 instance uses t2.micro which only has 1G memory, the Ollama service runs on a local machine.

In service.py, line 10 CONSUL_AGENT needs to be the server's public IP address, which changes whenever the EC2 instance starts. line 11 OLLAMA_URL needs to be the local machine's public IP address.

Since the service is running on the EC2, the local machines can access the service through the Postman directly.

Go to postman and POST http://{EC2 public IP address:5000/register} to register a service

GET http://{EC2 public IP address:5000/services} to get the current service json list

POST http://{EC2 public IP addresss:5000/forward} with Body 
{
    "service": "my-test-service",
    "message": "Hello from a local machine"
} 
to pass messages to the service
"service" needs to match the registered destination service name
