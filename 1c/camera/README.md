# Camera Service

Get the image from Docker Hub:
```
  docker pull ccuni/camera-service-2020w
```

Run:
```
  docker run -p<yourport>:8080 ccuni/camera-service-2020w
```
or run inside your Docker network:
 ```
  docker run -p<yourport>:8080 --network <my-net> --net-alias camera ccuni/camera-service-2020w
```

Test:
```
  curl http://<yourport>:8080/probe
```
