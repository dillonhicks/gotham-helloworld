# Echo Example Server


## Up and Running

Shell 1:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
make compile
make runserver
```

- Should have servers listening on:
  - port 8080 - RPC Server (protobuf)
  - port 9090 - Rest Proxy server (json)


Shell 2:
```
make testserver
```
