## Assignment 1a
A simple REST web service that uses Google Vision API to detect objects in images. 
The service allows users to upload a base64-encoded image in a JSON object, and sends it for object detection using Google Cloud Vision REST API. 
The service then forwards the response from the remote service back to the user.

### Requirements
- python3+
- py-pip3 
- flask
- requests

### Setup
`pip3 install flask`

`pip3 install requests`
 
### Run
`python3 service_1a.py`

### Test
Once the service is up and running, the functionality can be tested with the following commands:

- `curl http://localhost:80`

    --> should return a simple greeting

- `curl -X POST -H "Content-Type: application/json" -d @user_input1.json http://localhost:80/frame`

    --> should automatically forward the request to the default destination (Google Cloud Vision) and return its response in JSON format
    
- `curl -X POST -H "Content-Type: application/json" -d @user_input2.json http://localhost:80/frame`
   
    --> should forward the request to the specified destination

### _Optional task_
Convert image to base64 and output in JSON as:
````JSON
{
    "image": "<base64-encoded-image>"
}
````
#### _Test_
`curl -X POST -H "Content-Type: image/jpeg" -d @img/puppy.jpg http://localhost:80/convert
`

---------------
## Assignment 1b
An additional REST web service that communicates with the service from Assignment 1a. 
The service allows users to upload a base64-encoded image in a JSON object, and sends it for object detection using Google Cloud Vision REST API. 
The service then forwards the response from service-1a back to the user.

### Requirements
Docker

### Setup
This assignment's solution can be setup and run with Docker:
- within this repository, run `docker-compose up`
 
### Test
Once the service network is up and running, the functionality can be tested with the following commands:

- `curl http://localhost:8080` (service1a)

   `curl http://localhost:8081` (service1b)

    --> should return a simple greeting

- `curl -X POST -H "Content-Type: application/json" -d @user_input1.json http://localhost:8081/frame`

    `curl -X POST -H "Content-Type: application/json" -d @user_input1.json http://localhost:8080/frame`
    
    --> in user_input1.json, the destination is not specified
    --> service1b forwards the request to service1a, 
    service1a forwards the request to GCV and returns the response to service1b, 
    and finally, service1b returns the result to the user
    
- `curl -X POST -H "Content-Type: application/json" -d @user_input2.json http://localhost:8081/frame`

    `curl -X POST -H "Content-Type: application/json" -d @user_input2.json http://localhost:8080/frame`
   
    --> in user_input2.json, the destination is specified with service1a URL
    --> service1b forwards to request to service1a
    --> service1a will forward the request to GCV if the specified destination 
    is its own address, and attempt to forward the request to any other destination that is specified

### _Optional task_
Test service1a by sending the same image request a defined number of times and return the
elapsed time from first to fulfillment of last request in a JSON response:
````JSON
{
    "time": "<elapsed time>"
}
````
#### _Test_
`curl -X POST -H "Content-Type: application/json" -d @user_input3.json http://localhost:8081/test
`
