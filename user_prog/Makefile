# 变量定义
PROJECT_ROOT_PATH ?= $(shell realpath "..")
ROOTFSNAME ?= initramfs.cpio.gz
ROOTFS_DIR_PATH ?= $(PROJECT_ROOT_PATH)/rootfs

CC = gcc
CFLAGS = -Wall -g -std=gnu99 -static -m32 #-save-temps

# 查找所有源文件并生成目标文件名
SRC_FILES = $(shell find . -name '*.c')
TARGETS = $(SRC_FILES:.c=)


# 默认目标
all: $(TARGETS)

# 编译目标
%: %.c
	$(CC) $(CFLAGS) -o $@ $<

# 清理生成的文件
clean:
	rm -f $(TARGETS) *.i *.s *.o

install: $(TARGETS)
	cp $(TARGETS) $(ROOTFS_DIR_PATH)
	cd $(PROJECT_ROOT_PATH) && make $(ROOTFSNAME)
test:
	$(shell echo $(TARGETS))

.PHONY: all clean install tesl
