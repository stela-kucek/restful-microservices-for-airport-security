# ImageAnalysis Service

Get the image from Docker Hub:
```
  docker pull ccuni/image-analysis-service-2020w
```

Run:
```
  docker run -p<yourport>:8080 ccuni/image-analysis-service-2020w
```
or run inside your Docker network:
 ```
  docker run -p<yourport>:8080 --network <my-net> --net-alias image-analysis ccuni/image-analysis-service-2020w
```

Test:
```
  curl http://<yourport>:8080/probe
```
