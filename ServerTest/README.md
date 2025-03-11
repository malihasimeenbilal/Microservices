trae.zip is the traefik file, user needs to unzip it to a location, then add the unzipped folder to environment path. 

To start the service, in consul/consul.hcl, users need to configure IP addresses. For the server, both bind_addr and retry-join should be the same local IP address. For clients, bind_addr is the local IP address, retry_join is the server machine's IP address.

In service/service.py, line 8 CONSUL_AGENT needs to be server machine's IP address.


To start, in powershell, use "consul agent -config-dir={your consul folder address}" to start consul service. (Server machine first, then client)

Then, in a new powershell, go to service folder, use "docker compose up -d" to start docker service. 

Then, in the service folder, use "python service.py" to start

For both machine, go to postman and POST http://{local IP address:5000/register} to register service

Then server machine GET http://{local IP address:5000/services} to get the current service json list

Machines can also POST http://{Other IP address:5000/forward} with Body {
    "service": "my-test-service",
    "message": "Hello from machine 2"
} to send message to other machine