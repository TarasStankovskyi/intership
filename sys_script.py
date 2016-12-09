import os
import psutil
from datetime import datetime
import optparse
import sys

def info():
    usage = "Usage: %prog -s path to file -a append iformation to existing file "
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-c', '--cpu', dest='cpu', help='Print current CPU usage', default=False, action='store_true')
    parser.add_option('-r', '--ram', dest='ram', help='Print current RAM usage', default=False, action='store_true')
    parser.add_option('-p', '--processes', dest='proc', help='Print current number of processes running', default=False, action='store_true')
    parser.add_option('-a', '--append', dest='app', help='Append current info to existing file',  default=False, action='store_true')
    parser.add_option('-s', '--file', dest ='filename', help='Path to file', default=False)
    
    options, _ = parser.parse_args()

    cur_ram = psutil.virtual_memory()
    cur_cpu = psutil.cpu_percent(1)
    processes = len(psutil.pids())
    time = datetime.now()

    cpu = options.cpu
    ram = options.ram
    proc = options.proc
    filename = options.filename
    app = options.app

    if os.path.isfile(filename) and app:
        with open(filename, 'a') as res:
            if cpu and proc:
                res.write('<{0}>  <Current CPU : {1}> <Current number of processes running : {2}> <Current RAM : {3}>\n'.format(time, cpu,processes, ram))
            
            elif cpu and ram:
                res.write('<{0}>  <Current CPU : {1}> <Current RAM : {2}>\n'.format(time, cpu, ram))
            
            elif proc and ram:
                res.write('<{0}>  <Current number of processes running : {1}> <Current RAM : {2}>\n'.format(time, processes, cur_ram))
            
            elif cpu:
                res.write('<{0}>  <Current CPU : {1}>\n'.format(time, cur_cpu))
            
            elif ram:
                res.write('<{0}>  <Current RAM : {1}>\n'.format(time, cur_ram))
            
            elif proc:
                res.write('<{0}>  <Current number of processes running : {1}>\n'.format(time, processes))
             
            else:
                res.write('<{0}>  <Current CPU : {1}> <Current number of processes running : {2}> <Current RAM : {3}>\n'.format(time, cur_cpu,processes, cur_ram))

    elif filename and not app:
        with open(filename, 'w') as res:
            if cpu and proc:
                res.write('<{0}>  <Current CPU : {1}> <Current number of processes running : {2}> <Current RAM : {3}>\n'.format(time, cpu,processes, ram))

            elif cpu and ram:
                res.write('<{0}>  <Current CPU : {1}> <Current RAM : {2}>\n'.format(time, cpu, ram))
            
            elif proc and ram:
                res.write('<{0}>  <Current number of processes running : {1}> <Current RAM : {2}>\n'.format(time, processes, cur_ram))

            elif cpu:
                res.write('<{0}>  <Current CPU : {1}>\n'.format(time, cur_cpu))

            elif ram:
                res.write('<{0}>  <Current RAM : {1}>\n'.format(time, cur_ram))

            elif proc:
                res.write('<{0}>  <Current number of processes running : {1}>\n'.format(time, processes))

            else:
                res.write('<{0}>  <Current CPU : {1}> <Current number of processes running : {2}> <Current RAM : {3}>\n'.format(time, cur_cpu,processes, cur_ram))

    if cpu and proc:
        print '<{0}>  <Current CPU : {1}> <Current number of processes running : {2}>\n'.format(time, cur_cpu, processes)
        return 1

    elif cpu and ram:
        print '<{0}>  <Current CPU : {1}>  <Current RAM : {2}>\n'.format(time, cur_cpu, cur_ram)
        return 1

    elif proc and ram:
        print '<{0}>  <Current number of processes running : {1}> <Current RAM : {2}>\n'.format(time, processes, cur_ram)
        return 1

    elif cpu:
        print '<{0}>  <Current CPU : {1}>\n'.format(time, cur_cpu)
        return 1

    elif ram:
        print '<{0}>  <Current RAM : {1}>\n'.format(time, cur_ram)
        return 1

    elif proc:
        print '<{0}>  <Current number of processes running : {1}>\n'.format(time, processes)
        return 1

    else:
        print '<{0}>  <Current CPU : {1}> <Current number of processes running : {2}> <Current RAM : {3}>\n'.format(time, cur_cpu,processes, cur_ram)
        return 1


    
if __name__ == '__main__':
    info()


