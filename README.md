# numa
this project is to record any useful tools for debug the info under linux env

nodeestats.py is for info all running vms memory status:

eg:

python nodestats.py

NUMA stats
NUMA nodes:     0       1
MemTotal:       130677  131072
MemFree:        104184  105046
Domain 'instance-00000053':

        Overall memory: 2048 MiB nodes 0
        Node 0: 2048 MiB nodes 0
Domain 'instance-00000055':
        Overall memory: 2048 MiB
Domain 'instance-00000058':
        Overall memory: 2048 MiB nodes 0
        Node 0: 2048 MiB nodes 0


vcpustats.py is for info about all running vm cpu info:

eg:

python vcpustats.py

Host Total CPU Num 32 
VM: instance-00000055
vcpu 0 pcpu 8 nodeid 1


VM: instance-00000053
vcpu 0 pcpu 0 nodeid 0
vcpu 1 pcpu 0 nodeid 0


VM: instance-00000058
vcpu 0 pcpu 0 nodeid 0
vcpu 1 pcpu 16 nodeid 0
CPU DEDICATED!


total pcpuused info set([8, 0, 16])
free host cpus set([1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]) 