""" Script for gathering host information """


import time as t
import os
import sys
import optparse
import subprocess

def get_current_ram():
    """Getting current RAM usage using subprocess library"""
    result = subprocess.Popen("free -m | grep Mem | awk '{print $4/$2*100}'", shell=True,\
             stdout=subprocess.PIPE)
    return  result.stdout.read()

def get_current_cpu():
    """Getting current CPU usage using subprocess library"""
    result = subprocess.Popen("top -b -n1 | grep 'Cpu(s)' | awk '{print $2+$4}'",shell=True,\
             stdout=subprocess.PIPE)
    return result.stdout.read()


def get_processes_count():
    """Getting number of current process running"""
    result = subprocess.Popen("ps -c | grep -v 'PID'| wc -l",shell=True,stdout=subprocess.PIPE)
    return result.stdout.read()

def write_into_file(filename, result):
    """Write memory info into file"""
    if os.path.exists(filename):
        with open(filename, 'a') as res:
            res.write(result)
    else:
        print "There is not file:'{}' in this directory ".format(filename)

def main():
    """ Function provide information about CPU, RAM usage and processes running  """
    usage = "Usage: %prog -s path to file -a append iformation to existing file "
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-c', '--cpu', dest='cpu',
                      help='Print current CPU usage', default=False, action='store_true')
    parser.add_option('-r', '--ram', dest='ram',
                      help='Print current RAM usage', default=False, action='store_true')
    parser.add_option('-p', '--processes', dest='proc',
                      help='Print current number of processes running',
                      default=False, action='store_true')
    parser.add_option('-s', '--file', dest='filename', help='Path to file', default=False)

    options, _ = parser.parse_args()

    cur_ram = get_current_ram()
    cur_cpu = get_current_cpu()
    processes = get_processes_count()
    time = t.strftime("%Y-%m-%d %H:%M:%S")

    result = [str(time)]

    if options.cpu:
        result.append('\tCPU usage: ' + str(cur_cpu))
    if options.ram:
        result.append('\tRAM usage: ' + str(cur_ram))
    if options.proc:
        result.append('\tProcesses running: ' + str(processes))
    if len(result) == 1:
        result.append('CPU usage:{}\tCurrent number of processes running'\
                      ':{}\tRAM usage :{}\n'.format(cur_cpu, processes, cur_ram))

    res = '\t'.join(result) +'\n'

    filename = options.filename

    if filename:
        write_into_file(filename, res)
    if not filename:
        print res

if __name__ == '__main__':
    sys.exit(main())

