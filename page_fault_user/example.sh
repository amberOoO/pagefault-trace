# execute from file
#sudo bpftrace -o trace.log page_fault_user.bt -c "$1"

# execute from cmd
sudo bpftrace -q -o trace.log -e 'BEGIN {printf("pid,name,addr,error_code,instruction_ptr,time")} tracepoint:exceptions:page_fault_user {printf("%d,%s,%p,%d,%p,%lu\n",pid,comm,args.address,args.error_code,nsecs());}' -c "$1"

# trace llama.cpp
sudo sh -c 'echo 1 > /proc/sys/vm/drop_caches' && sudo bpftrace -q -o llamacpp.llama8b.trace.$(date +%s).log -e 'BEGIN {printf("pid,name,addr,error_code,instruction_ptr,time\n");} tracepoint:exceptions:page_fault_user {printf("%d,%s,%p,%d,%p,%lu\n",pid,comm,args.address,args.error_code,args.ip,nsecs());}' -c "sudo -u liucp ./main -m models/llama3-8b.gguf -cml"
