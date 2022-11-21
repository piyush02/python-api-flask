## API App dockerization 

Below commands to build and push the api app image to docker hub

Prerequisites copy Dockerfile to main directory (i.e task directory) and execute below commands.

- docker login -u username
- docker build -t piyush02/flask:v1 .
- docker push piyush02/flask:v1 

Below command to run localy 
- docker run -d -p 5000:5000 piyush02/flask:v1
