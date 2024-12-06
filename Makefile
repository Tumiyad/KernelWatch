export PROJECT_ROOT_PATH := $(shell realpath ".")
include $(PROJECT_ROOT_PATH)/tools/makefiles/global_varibles.mk

.PHONY: $(ROOTFSNAME) kernel $(USER_PROG_NAME) macro_expand

# 默认目标
all: help

# 动态生成目标
lab%:
	echo "Running make in ./labs/lab$*/"
	cd ./labs/lab$*/ && $(MAKE)

help:
	@echo "Usage: make NUM"
	@echo "Where NUM is the lab number (e.g., 1, 2, etc.)."


$(ROOTFSNAME):
	cd $(PROJECT_ROOT_PATH)/rootfs && find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../$@

# compile user_prog
$(USER_PROG_NAME):
	$(MAKE) clean -C $(USER_PROG_PATH)
	cd $(USER_PROG_PATH) && $(OLDMAKE)
	$(MAKE) install -C $(USER_PROG_PATH)

kernel:
	cd $(PROJECT_ROOT_PATH)/linux-$(KERNEL_VERSION)/ && $(OLDMAKE)

macro_expand:
ifdef ARG
	python3 $(TOOLS_PATH)/macro_expand.py $(ARG)
else
	$(warning "Usage: make macro_expand ARG="./linux-2.6.26/net/core/skbuff.o"")
	$(error "Error: ARG is not defined. Please provide a value for ARG.")
endif
