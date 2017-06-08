__author__ = 'klyang'
import libvirt
import sys
from collections import Counter
import subprocess

CPU_DEDICATED = -1
CPU_SHARE = -2

"""
input range data as 0-7
and output a list as [0,1,2,3,4,5,6,7]
"""
def expand_range_tolist(rangedata):
    datalist = []
    start,end = rangedata.split("-")
    end=int(end)+1
    datalist=range(int(start),int(end))
    return datalist

"""
get system numa cpu topology
return list the index is matched for numa node id
index data as the cpus
as [[0,2,3],[2,3,4]]
"""
def get_numa_cpumap_system():
    cpumaps=[]
    data = subprocess.check_output(["lscpu"])
    if data != None:
        data = data.split("\n") #transfer data to list
        numadata = [s for s in data if "NUMA" in s]
        if len(numadata) != 0:
            for numanode in numadata[1:]:
                nodecpumaps =[]
                tmplist = numanode.split(":")
                if len(tmplist) >=2:
                    tmpdata = tmplist[-1]
                    tmpdatalist = tmpdata.split(",")
                    if len(tmpdatalist) !=0:
                        for val in tmpdatalist:
                            if "-" in val:
                                rangedata = expand_range_tolist(val)
                            else:
                                rangedata = list(val)

                            nodecpumaps = nodecpumaps+rangedata

                if len(nodecpumaps) != 0:
                    cpumaps.append(nodecpumaps)

    return cpumaps

def get_numanodeid_bycpuid(cpuid,cpumaps):
    nodeid = 0
    for nodemaps in cpumaps:
        if cpuid in nodemaps:
            return nodeid
        else:
            nodeid+=1

    return nodeid

CPUMAPS=get_numa_cpumap_system()


"""
cala used pcpus in the host of a vm
data based on input vcpus obj
"""
def calc_dompcpuids_byvcpusobj(vcpus):
    pcpus=[]
    if vcpus != None:
        cpus = vcpus[0]
        for cpu in cpus:
            print ("vcpu %d pcpu %d nodeid %d"
                   %(cpu[0],cpu[-1],get_numanodeid_bycpuid(cpu[-1],CPUMAPS)))
            pcpus.append(cpu[-1])

    return pcpus

"""
check and return
if the vm used dedicated cpu policy
"""
def check_cpu_dedicated_byvcpuobj(vcpus):
    if vcpus != None:
        cpumaps = vcpus[1]
        cpunum = len(cpumaps)
        trueNum = 0
        for cpumap in cpumaps:
            cnt = Counter(cpumap)
            trueNum += cnt[True]

        if cpunum == trueNum:
            return CPU_DEDICATED

    return CPU_SHARE


try:
    conn = libvirt.openReadOnly(None)
except libvirt.libvirtError:
    print("Failed to connect to the hypervisor")
    sys.exit(1)

hostTotalCpus=conn.getCPUMap()[0]
print("Host Total CPU Num %d "%hostTotalCpus)

hostCpuMapSet=set(range(hostTotalCpus))

vmids = conn.listDomainsID() #fetch the running vms
pcpus=[]
pcpuset=set()
if len(vmids)!=0:
    for vmid in vmids:
        tmpcpus=[]
        dom = conn.lookupByID(vmid)
        vcpuinfo = dom.vcpus()
        print("VM: %s"% dom.name())
        tmpcpus=calc_dompcpuids_byvcpusobj(vcpuinfo)
        if len(tmpcpus) !=0:
            pcpuset = pcpuset|set(tmpcpus)

        cpupolicy = check_cpu_dedicated_byvcpuobj(vcpuinfo)
        if cpupolicy == CPU_DEDICATED:
            print("CPU DEDICATED!")

        print("\r\n")

print("total pcpuused info %s" % pcpuset)

freeCpu = hostCpuMapSet-pcpuset
print("free host cpus %s " % freeCpu)


conn.close()
exit(0)
