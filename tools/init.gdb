# gdb_script.gdb

set height 1000
set architecture i386
set print pretty on
define init_all
    file $arg0
    directory $arg1
    source $arg2
    target remote localhost:1234
    continue
end
define split
    layout split
end


