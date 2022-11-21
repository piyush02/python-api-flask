## API App Deployment on Kubernetes

## Prerequisites

- Dokcer steps executed and image is pushed on docker hub (docker/Dockerfile)
- minikube/kubernetes cluster

## Manifest file

## NameSpace:
  - devops-task namespace is created for api app deployment
## Secret:
  - Execute docker_secret.sh script for creating docker registory secret
## Deployment:
  - Api app is created in devops-task namespace 
  - APi endpoint expose to 31000 port via service NodePort
  - ENV varibale is set for port 5000
 
## Serivce:
  - Service resource deployed to access the API app running inside container from outside.
  - targetPrt is set to 5000 in container
  
 ##Usage
 
 #Steps:
 - cd to kubernetes directory
 - kubectl apply -f namespace.yaml
 - bash docker_secret.sh
 - kubectl apply -f python_api_flask.yaml
 
 ## Kubectl command to check status 
 - command to check pod is running or not
    - kubectl get pod -n devops-task
 - command to check pod logs for troubleshooting
    - kubectl logs pod-name -n devops-task
 - command to check service
    - kubectl get service -n devops-task
 - Endpoint of the API app 
    - nodeip:nodeport(30080)
 
 ## minkube comand for Mac M1
 - kubectl get service api-service -n devops-task 
 
 <img width="1040" alt="image" src="https://user-images.githubusercontent.com/6249054/202996730-f7985a71-c028-448a-9693-8a2e696443d8.png">

<img width="479" alt="image" src="https://user-images.githubusercontent.com/6249054/202996848-7d136d92-0f50-4b67-b7bf-4040bc58f9c6.png">

![image](https://user-images.githubusercontent.com/6249054/202997052-10ad94ae-5173-499f-9ad9-286bd9b99800.png)

 
  
