# Remove $@ if error occurs
.DELETE_ON_ERROR:

# Turn off suffix build rules built into make
.SUFFIXES:

SHELL := /bin/bash
PTGEN := ptgen
.DEFAULT_GOAL := ptgen

# MUST Environment check
ifndef BOARD
  $(error BOARD is not defined)
endif
ifndef SUBTARGET
  $(error SUBTARGET is not defined)
endif
ifndef OUT
  $(error OUT is not defined)
endif

PTGEN_SCRIPT_DIR := common
PTGEN_LAYOUT_DIR := ${BOARD}

MTK_PTGEN_PYTHON := ${PTGEN_SCRIPT_DIR}/default_ptgen.py
MTK_PTGEN_COMMAND := \
	MTK_PLATFORM=${BOARD} \
	MTK_PROJECT=${SUBTARGET} \
	OUT_DIR=${OUT} \
	PL_MODE=${PL_MODE} \
	BOOTING_DEVICE=$(BOOTING_DEVICE) \
	DEVICE_BLOCK_SIZE=$(DEVICE_BLOCK_SIZE) \
	TARGET_CFG_FILE=$(CFG_FILE) \
	python -B $(MTK_PTGEN_PYTHON)

PTGEN_SCRIPT_DEPS := $(shell find $$PTGEN_SCRIPT_DIR -name "*.py")
PTGEN_LAYOUT_DEPS := $(shell find $$PTGEN_LAYOUT_DIR -name "*.csv")
PTGEN_CONFIG_DEPS := $(CFG_FILE)

.PHONY: ptgen
ptgen: $(PTGEN_SCRIPT_DEPS) $(PTGEN_LAYOUT_DEPS) $(PTGEN_CONFIG_DEPS)
	$(eval _result := $(shell $(MTK_PTGEN_COMMAND) >&2; echo $$?))
	@if [ $(_result) -ne 0 ]; then \
		echo 'ptgen error=$(_result): $(MTK_PTGEN_COMMAND)'; \
		exit 1; \
	fi

.PHONY: clean
clean:
	@rm -rf $(OUT)/* 
