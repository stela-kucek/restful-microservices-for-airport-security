## Assignment 1c
This subproject comprises eight RESTful services which make up a simulated and simplified Airport Security System. 

### Requirements
Docker

### Setup
This assignment's solution can be setup and run with Docker:
- within this repository, run `docker-compose up`

### Testing
Access the CPanel via browser at [http://localhost:3800](http://localhost:3800)

From there you can:
- See a list of cameras
- Update configurations for available cameras
- View existing configurations via http://localhost:3800/cameras/<id>/config
- Start streaming with available cameras (defaults to 5 frames, 1 sec delay)
- See a list of persons from sections
- See a list of known persons from alerts

Alternatively, communicate with the camera service directly via postman:
- POST
- http://localhost:3100/stream?toggle=on
- body(JSON):
 ````JSON
    {
        "destination": "http://collector:80/frame",
        "max-frames": 1, 
        "delay": 0.1
    }
 ````
See the documentation file for a detailed description of the communication flow from this initial point.