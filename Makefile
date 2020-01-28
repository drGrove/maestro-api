SHELL := /bin/bash
PIP_ENV := $(shell pipenv --venv || true)
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
_VERSION ?= $(shell echo $$(./scripts/gen_version.sh))
_PREFIX ?= $(shell echo $${PREFIX:+$$PREFIX\_})
VERSION ?= $(shell echo $(_PREFIX)$(_VERSION))
DOCKER_REGISTRY_PATH := docker.io
PACKAGE := maestro-api
TAG := latest
NAMESPACE := default

# Check that given variables are set and all have non-empty values,
# die with an error otherwise.
#
# Params:
#   1. Variable name(s) to test.
#   2. (optional) Error message to print.
.PHONY: check_defined
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

ifeq ($(OS),Windows_NT)
    UNAME := Windows
else
    UNAME := $(shell uname -s)
endif

.PHONY: shell
shell:
	@pipenv shell

.PHONY: setup
setup:
	@pipenv --three install --dev

.PHONY: run
run:
	@pipenv run python3 wsgi.py

.PHONY: pipenv-lock
pipenv-lock:
	@pipenv update
	@pipenv lock -r > requirements.txt

.PHONY: format
format:
	@pipenv run black ./**/*.py

.PHONY: lint
lint:
	@pipenv run black **/*.py --check
	@pipenv run flake8 ./**/*.py

.PHONY: test
test: setup
	-@$(PIP_ENV)/bin/coverage run -m unittest -v

.PHONY: test-by-name
test-by-name:
	-@$(PIP_ENV)/bin/coverage run -m unittest $(TEST) -v

.PHONY: coverage
coverage:
	@$(PIP_ENV)/bin/coverage report -m

.PHONY: build-image
build-image:
	$(call check_defined, PACKAGE)
	@docker build \
		--tag $(DOCKER_REGISTRY_PATH)/$(PACKAGE):$(VERSION) \
		$(ARGS) \
		.

.PHONY: tag-image-latest
tag-image-latest:
ifeq ("${BRANCH}", "master")
ifeq ("${CI}", "")
	@echo "This should only be run in CI"
else
	$(call check_defined, PACKAGE)
	@docker tag $(DOCKER_REGISTRY_PATH)/$(PACKAGE):$(VERSION) $(DOCKER_REGISTRY_PATH)/$(PACKAGE):$(PREFIX)master
	@docker push $(DOCKER_REGISTRY_PATH)/$(PACKAGE):$(PREFIX)master
endif
endif

.PHONY: push-image
push-image:
	$(call check_defined, PACKAGE)
	docker push $(DOCKER_REGISTRY_PATH)/$(PACKAGE):$(VERSION)

.PHONY: postgres
postgres:
	@docker run -d \
		-p 5432:5432 \
		-e POSTGRES_USER=postgres \
		-e POSTGRES_PASSWORD=postgres \
		-e POSTGRES_DB=maestro \
		postgres

.PHONY: clean
clean:
	@rm -r $(PIP_ENV)
