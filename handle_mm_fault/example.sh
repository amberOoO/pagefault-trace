BEGIN {printf("pid,name,addr,flags,time\n")} kprobe:handle_mm_fault{printf("%d,%s,%p,%lu,%lu,%lu\n", pid, comm, arg1, arg2, nsecs(), retval);}

# execute from cmd
sudo bpftrace -q -o trace.log -e 'BEGIN {printf("pid,name,addr,flags,time\n")} kprobe:handle_mm_fault{printf("%d,%s,%p,%lu,%lu,%lu\n", pid, comm, arg1, arg2, nsecs(), retval);}' -c "$1"

# trace llama.cpp
sudo sh -c 'echo 1 > /proc/sys/vm/drop_caches' && sudo bpftrace -q -o llamacpp.llama8b.trace.$(date +%s).log -e 'BEGIN {printf("pid,name,addr,flags,time\n")} kprobe:handle_mm_fault{printf("%d,%s,%p,%lu,%lu,%lu\n", pid, comm, arg1, arg2, nsecs(), retval);}' -c "sudo -u liucp /home/liucp/Documents/gitRepos/llama.cpp/main -m /home/liucp/Documents/gitRepos/llama.cpp/models/llama3-8b.gguf -cml"
