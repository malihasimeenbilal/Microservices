open ollama2 and make sure it is running on 127.0.0.1:11434
open docker
open our project and enter the root path
run the following command to build a docker image for ollama.py: docker build -t Ollama .
run the microservice called Ollama inside docker: docker run -p 5000:5000 Ollama
open localhost:5000 through docker, you can see the text "Hello, this is a Flask Microservice for Ollama page"
open postman use POST and write down the following address "http://127.0.0.1:5000/ask?Content-Type=application" 
（
  Pamas： key: Content-Type, Value: application and 
  Body raw  
  {"prompt": "any question" }
  ) 
You can obtain the answer from Ollama and it will be displayed in the postman Body part.
