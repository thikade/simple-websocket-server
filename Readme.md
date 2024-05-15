# Simple Websocket Demo for Openshift Router
## About
- Runs a simple Python app deployment containing a trivial websocket *echo*-server 
- Source: https://websockets.readthedocs.io/en/stable/howto/kubernetes.html
- tested with Openshift 4.14
- HTTP/2 is disabled on Openshift router (by default)

## Build
Build the dockerfile and push to some registry. I used: 
```
docker build . -t quay.io/thikade/ws-echo:latest  &&  docker push quay.io/thikade/ws-echo:latest
```

## Deploy
```
oc apply -k server/k8s/
```

## Verify websocket communication
**Either run on your local machine...**
```
$ python -m websockets wss://ws-echo-server.apps.epyc.***
Connected to wss://ws-echo-server.apps.epyc.***.
> hi secure
< hi secure (from your K8s websocket-server :-)
```


**... or run the same Docker image locally:**
```
docker run -ti --rm --name wsclient -h wsclient quay.io/thikade/ws-echo:latest \
   python -m websockets wss://ws-echo-server.apps.epyc.***

Connected to wss://ws-echo-server.apps.epyc.***.
> hi secure
< hi secure (from your K8s websocket-server :-)
```