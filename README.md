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
    - see: gotham-helloworld/server.py
  - port 9090 - Rest Proxy server (json)
    - see: gotham-helloworld/build/pyhon/echoexample/echoexampl/bin/rest-proxy-server.go


Shell 2:
```
make testserver
```


## What is it?


There is not a lot tooling to make working with protocol buffers in
python easy. This repository uses the a docker image created from the
(gotham)[https://github.com/dillonhicks/gotham] that contains a
toolchain for building all of the protobuf artifacts into a python
package by mounting this repos source, config, and build directories
into the running container.


After a successful `make compile` the build directory should contain:

- Generated go source for the protocol buffers and rest proxy server
  for all of the services contained in the protos directory.

- A python package with:
  - pb generated python files for protocol buffer message
  - The grpc
