""" Script for gathering host information """


import time as t
import os
import sys
import optparse
import subprocess

def get_current_ram():
    """Getting current RAM usage using subprocess library"""
    command_1 = ['free', '-m']
    process_1 = subprocess.Popen(command_1, stdout=subprocess.PIPE)
    command_2 = ['grep', 'Mem']
    process_2 = subprocess.Popen(command_2, stdin=process_1.stdout, stdout=subprocess.PIPE)
    command_3 = ['awk', '{print $4/$2*100}']
    process_3 = subprocess.Popen(command_3, stdin=process_2.stdout, stdout=subprocess.PIPE)
    result = process_3.stdout.read()
    return result

def get_current_cpu():
    """Getting current CPU usage using subprocess library"""
    command_1 = ['top', '-b', '-n1']
    process_1 = subprocess.Popen(command_1, stdout=subprocess.PIPE)
    command_2 = ['grep', 'Cpu(s)']
    process_2 = subprocess.Popen(command_2, stdin=process_1.stdout, stdout=subprocess.PIPE)
    command_3 = ['awk', '{print $2+$4}']
    process_3 = subprocess.Popen(command_3, stdin=process_2.stdout, stdout=subprocess.PIPE)
    result = process_3.stdout.read()
    return result

def get_processes_count():
    """Getting number of current process running"""
    command_1 = ['ps', '-c']
    process_1 = subprocess.Popen(command_1, stdout=subprocess.PIPE)
    command_2 = ['grep', '-v', 'PID']
    process_2 = subprocess.Popen(command_2, stdin=process_1.stdout, stdout=subprocess.PIPE)
    command_3 = ['wc', '-l']
    process_3 = subprocess.Popen(command_3, stdin=process_2.stdout, stdout=subprocess.PIPE)
    result = process_3.stdout.read()
    return result

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
    print res

    filename = options.filename
    if filename:
        write_into_file(result=res, filename=filename)


if __name__ == '__main__':
    sys.exit(main())

