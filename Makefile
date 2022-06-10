########################
#       Load Env       #
########################
cnf ?= config.env
include $(cnf)

########################
#     Detected OS      #
########################
ifeq ($(OS), Windows_NT)
	DETECTED_OS := Windows
	WORKING_DIR := $(shell cd)
else
	DETECTED_OS := $(shell sh -c 'uname -s 2>/dev/null || echo not')
	WORKING_DIR := $(shell pwd)
endif


########################
# Fetch Container Info #
########################
CONTAINER_ID := $(shell docker ps -qf "name=$(CONTAINER_NAME)")


########################
#     Display Info     #
########################
$(info ========== Info ==========)
$(info Working Directory: $(WORKING_DIR))
$(info Detected OS: $(DETECTED_OS))
$(info ContainerID: $(CONTAINER_ID))
$(info Image Name: $(IMAGE_NAME))
$(info Image Version: $(IMAGE_VERSION))
$(info Container Name: $(CONTAINER_NAME))
$(info ==========================)

########################
#        Setting       #
########################
.PHONY: help
.DEFAULT_GOAL := help

help: ## This help message
ifeq ($(DETECTED_OS), Windows)
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "%-30s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
else
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
endif

up:  ## Start Runtime
	docker compose up -d

down:  ## Close Runtime
	docker compose down -d

build:  ## Build docker runtime
	docker build -t $(IMAGE_NAME):$(IMAGE_VERSION) .

rebuild:  ## Build docker runtime without cache
	docker build -t $(IMAGE_NAME):$(IMAGE_VERSION) --no-cache .

run-dev: ## Start dev runtime
	docker run --name $(CONTAINER_NAME) --rm -it $(IMAGE_NAME):$(IMAGE_VERSION)

commit-dev: ## Commit current container status
	docker commit $(CONTAINER_ID) $(IMAGE_NAME):$(IMAGE_VERSION)

pytest: ## PyTest
	docker run --name $(CONTAINER_NAME) --rm -it $(IMAGE_NAME):$(IMAGE_VERSION) pytest
