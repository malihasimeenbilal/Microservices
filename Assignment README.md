-open ollama2 and make sure it is running on  port 127.0.0.1:11434
-open docker application 
-open microservice project and run the project 
-run the following command to build a docker image for ollama.py: docker build -t ollama .
-run the microservice called Ollama inside docker: docker run -p 5000:5000 ollama
-Hompage of chatbot is available as we enter the link through docker conatiner 
-open postman use POST and write down the following address "http://127.0.0.1:5000/ask?Content-Type=application" 
（
  Pamas： key: Content-Type, Value: application and 
  Body raw  
  {"prompt": "any question" }
  ) 
-You can obtain the answer from Ollama and it will be displayed in the  Body part of postman .
