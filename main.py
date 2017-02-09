import psutil
import sys
import socket
import time

class PricePayToGo:
    def __init__(self):
        pass
    core_requency = 2.59
    coast_cpu_one_hrz = 0.3837
    coast_mem_one_gb = 0.8334
    coast_sata_one_gb = 0.0159
    coast_sas_one_gb = 0.0318
    coast_ssd_one_gb = 0.0649

class Carbon:
    def __init__(self):
        pass
    server = '192.168.110.40'
    port = 2003

def cpu_utilization ():
    cpu = psutil.cpu_times_percent(interval=10)
    cpu_util_percent = cpu.user + cpu.system + cpu.nice + cpu.softirq + cpu.steal
    return cpu_util_percent

def mem_utilization ():
    mem = psutil.virtual_memory()
    mem_util_byte = (mem.total - mem.free)
    return mem_util_byte

def disk_utilization ():
    disk = psutil.disk_partitions()
    disk_util_byte = 0
    for x in disk:
        disk_util_byte = disk_util_byte + psutil.disk_usage(x.mountpoint).total
    return disk_util_byte

def calculator (cpu_met=0, mem_met=0, hdd_met=0):
    if len(sys.argv)  == 1:
        coast_hdd_one_gb = PricePayToGo.coast_sata_one_gb
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'sata':
            coast_hdd_one_gb = PricePayToGo.coast_sata_one_gb
        elif sys.argv[1] == 'sas':
            coast_hdd_one_gb = PricePayToGo.coast_sas_one_gb
        elif sys.argv[1] == 'ssd':
            coast_hdd_one_gb = PricePayToGo.coast_ssd_one_gb
        else:
            print("Unknown argument")
            print("Default argument: sata")
            print("Possible arguments: sata, sas, ssd")
            sys.exit(1)
    else:
        print("Too many arguments")

    cpu_rub_per_10_sec = ((PricePayToGo.core_requency*psutil.cpu_count()/100)*cpu_met)*(PricePayToGo.coast_cpu_one_hrz/(60*60/10))
    mem_rub_per_10_sec = (mem_met/(1024*1024*1024))*(PricePayToGo.coast_mem_one_gb/(60*60/10))
    hdd_rub_per_10_sec = (hdd_met/(1024*1024*1024))*(coast_hdd_one_gb/(60*60/10))
    rub_per_10_sec = cpu_rub_per_10_sec+mem_rub_per_10_sec+hdd_rub_per_10_sec
    return rub_per_10_sec

path="Pay.Hostname." + socket.gethostname()
sock = socket.socket()
sock.connect((Carbon.server, Carbon.port))
while True:
    sock.sendall("%s %.12f %d\n" % (path, calculator(cpu_utilization(), mem_utilization(), disk_utilization()), int(time.time())))
sock.close()
