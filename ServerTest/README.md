We now use consul, traefik, and docker to implement the assignment.

Machine A serves as the server, and machine B serves as the client. Both can register for separate services. 

In service.py, line 10 CONSUL_AGENT needs to be the server's IP address. 

Both machines can access the service through the Postman directly.

Go to postman and POST http://{self IP address:5000/register} to register a service

GET http://{self IP address:5000/services} to get the current service json list

POST http://{self IP addresss:5000/forward} with Body 
{
    "service": {target service name},
    "message": "Hello from a local machine"
} 
to pass messages to the service

POST http://{the other machine's IP addresss:5000/ask} with Body 
{
    "prompt": "Hello"
} 
to talk to Ollama on the other machine and service. 

If the service has no action in 2 minutes, the heartbeat function will deregister this service. 
