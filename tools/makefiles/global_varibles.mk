#可配置参数
export ROOTFSNAME = initramfs.cpio.gz
USER_PROG_NAME := user_prog
USER_PROG_PATH := $(PROJECT_ROOT_PATH)/$(USER_PROG_NAME)
export KERNEL_VERSION := 2.6.26
export OLDMAKE := $(PROJECT_ROOT_PATH)/tools/oldmake
export OLDGCC := $(PROJECT_ROOT_PATH)/tools/oldgcc

#若干目录
export KERNEL_SOURCE_PATH := $(PROJECT_ROOT_PATH)/linux-$(KERNEL_VERSION)
export BZIMAGE_PATH := $(KERNEL_SOURCE_PATH)/arch/x86/boot/bzImage
export VMLINUX_PATH := $(KERNEL_SOURCE_PATH)/vmlinux
export ROOTFS_PATH := $(PROJECT_ROOT_PATH)/$(ROOTFSNAME)
export ROOTFS_DIR_PATH := $(PROJECT_ROOT_PATH)/rootfs

export TOOLS_PATH := $(PROJECT_ROOT_PATH)/tools
# add paths to gdb python environment
export PYTHON_GENERAL_PATH := $(PROJECT_ROOT_PATH)/gdb_scripts
export GDB_PYTHON_INIT := $(PYTHON_GENERAL_PATH)/init.py


#默认运行参数
QEMU := qemu-system-i386
KERNEL_PARAMS := nokaslr console=ttyS0 root=/dev/ram init=/init
QEMU_TEST_FLAGS := -nographic -smp 1 -m 2048
#KERNEL_PARAMS := nokaslr root=/dev/ram init=/init
#QEMU_TEST_FLAGS := -smp 1 -m 256
QEMU_FLAGS := $(QEMU_TEST_FLAGS) -s -S
QEMU_NETWORK_FLAGS := -nic user,model=e1000

# 固定变量
SHELL := /bin/bash
GREEN := \033[1;32m
RESET := \033[0m
# 定义打印命令的函数
define PRINT
  echo -e "$(GREEN)$(1)$(RESET)"
endef
# 定义检查文件是否存在的函数
define ENSURE_FILE
  if [ ! -f $(1) ]; then \
    $(call PRINT, "File $(1) does not exist!"); \
    exit 1; \
  fi
endef
