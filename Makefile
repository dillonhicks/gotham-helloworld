BUILD_VARS=

CONFIG_DIR ?= $(PWD)/config
BUILD_VARS+=CONFIG_DIR=$(CONFIG_DIR)

PROTOS_DIR ?= $(PWD)/protos
BUILD_VARS+=PROTOS_DIR=$(PROTOS_DIR)

BUILD_DIR ?= $(PWD)/build
BUILD_VARS+=BUILD_DIR=$(BUILD_DIR)


all:
	$(error You must explicitly use 'make compile')


compile:
	@echo === Build Variables ===
	@echo $(BUILD_VARS) | xargs -n1 echo
	@echo =======================
	@echo

	docker run --rm \
		-v $(CONFIG_DIR):/app/config \
	  	-v $(PROTOS_DIR):/app/protos \
	  	-v $(BUILD_DIR):/app/build \
	  	-t dillonhicks/gotham:latest


runserver:
	PYTHONPATH=$(BUILD_DIR)/python/echoexample \
		python server.py --with-proxy-server

testserver:
	curl http://localhost:9090/v1/echo/Sir/Good%20Day
	@echo
