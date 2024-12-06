include $(PROJECT_ROOT_PATH)/tools/makefiles/global_varibles.mk

#lab sepecific varibles
export LAB_PATH := $(PROJECT_ROOT_PATH)/labs/lab$(LAB_NUMBER)
LAB_USER_PROG_PATH := $(LAB_PATH)/$(USER_PROG_NAME)
PYTHON_LAB_PATH := $(LAB_PATH)/gdb_scripts
export PYTHONPATH := $(PYTHON_GENERAL_PATH):$(PYTHON_LAB_PATH)

#TMUX config
export TMUX_SESSION := debugging_session_lab$(LAB_NUMBER)
WINDOW_WIDTH := $$(tput cols)
WINDOW_HEIGHT := $$(($$(tput lines)-1 ))

.PHONY: $(USER_PROG_NAME) $(ROOTFSNAME) kernel



# Debug kernel! Press Ctrl+B and X to exit tmux debug environment.
debug:
	$(call ENSURE_FILE, $(ROOTFS_PATH))
	tmux new-session -d -s $(TMUX_SESSION) -x $(WINDOW_WIDTH) -y $(WINDOW_HEIGHT) -n "kernel_watch"
	tmux list-windows
	tmux split-window -v -l 10%
	tmux split-window -h -t 0


	tmux send-keys -t $(TMUX_SESSION):0.0 "$(QEMU) -kernel $(BZIMAGE_PATH) -initrd $(ROOTFS_PATH) --append \"$(KERNEL_PARAMS)\" $(QEMU_FLAGS) $(QEMU_NETWORK_FLAGS)" C-m
	tmux send-keys -t $(TMUX_SESSION):0.1 "gdb -q -n -x $(TOOLS_PATH)/init.gdb" C-m
	tmux send-keys -t $(TMUX_SESSION):0.1 "init_all $(VMLINUX_PATH) $(KERNEL_SOURCE_PATH) $(GDB_PYTHON_INIT)" C-m
	#sleep 1
	#tmux send-keys -t ${TMUX_SESSION}:0.1 "shell clear" C-m # Clear the screen and make the last executed command to be 'l'
	#tmux send-keys -t $(TMUX_SESSION).0 "      " C-m C-l
	tmux send-keys -t $(TMUX_SESSION):0.2 "$(SHELL) $(LAB_PATH)/commands.bash && exit" C-m
	tmux select-window -t $(TMUX_SESSION):0
	tmux select-pane -t 2
	tmux attach-session -t $(TMUX_SESSION)

# Test if we can successfully boot kernel.
test:
	$(QEMU) -kernel $(BZIMAGE_PATH) -initrd $(ROOTFS_PATH) --append "$(KERNEL_PARAMS)" $(QEMU_TEST_FLAGS) $(QEMU_NETWORK_FLAGS)

kernel:
	cd $(PROJECT_ROOT_PATH)/linux-$(KERNEL_VERSION)/ && $(OLDMAKE)
# compile user_prog
$(USER_PROG_NAME):
	$(MAKE) clean -C $(LAB_USER_PROG_PATH)
	cd $(LAB_USER_PROG_PATH) && $(OLDMAKE)
	$(MAKE) install -C $(LAB_USER_PROG_PATH)
