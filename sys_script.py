""" Script for gathering host information """


from datetime import datetime
import sys
import os
import optparse
import subprocess

def ram():
    """Getting current RAM usage using subprocess library"""
    command_1 = ['free', '-m']
    process_1 = subprocess.Popen(command_1, stdout=subprocess.PIPE)
    command_2 = ['grep', 'Mem']
    process_2 = subprocess.Popen(command_2, stdin=process_1.stdout, stdout=subprocess.PIPE)
    command_3 = ['awk', '{print $4/$2*100}']
    process_3 = subprocess.Popen(command_3, stdin=process_2.stdout, stdout=subprocess.PIPE)
    result = process_3.stdout.read()
    return result

def cpu():
    """Getting current CPU usage using subprocess library"""
    command_1 = ['top', '-b', '-n1']
    process_1 = subprocess.Popen(command_1, stdout=subprocess.PIPE)
    command_2 = ['grep', 'Cpu(s)']
    process_2 = subprocess.Popen(command_2, stdin=process_1.stdout, stdout=subprocess.PIPE)
    command_3 = ['awk', '{print $2+$4}']
    process_3 = subprocess.Popen(command_3, stdin=process_2.stdout, stdout=subprocess.PIPE)
    result = process_3.stdout.read()
    return result

def cur_processes():
    """Getting number of current process running"""
    command_1 = ['ps', '-c']
    process_1 = subprocess.Popen(command_1, stdout=subprocess.PIPE)
    command_2 = ['grep', '-v', 'PID']
    process_2 = subprocess.Popen(command_2, stdin=process_1.stdout, stdout=subprocess.PIPE)
    command_3 = ['wc', '-l']
    process_3 = subprocess.Popen(command_3, stdin=process_2.stdout, stdout=subprocess.PIPE)
    result = process_3.stdout.read()
    return result

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
    parser.add_option('-a', '--append', dest='app',
                      help='Append current info to existing file',
                      default=False, action='store_true')
    parser.add_option('-s', '--file', dest='filename', help='Path to file', default=False)

    options, _ = parser.parse_args()

    cur_ram = ram()
    cur_cpu = cpu()
    processes = cur_processes()
    time = datetime.now()

    print cur_cpu

    count = 0
    stdout = str(time)

    if options.cpu:
        count += 1
        stdout += '\tCPU usage: ' + str(cur_cpu)
    if options.ram:
        count += 1
        stdout += '\tRAM usage: ' + str(cur_ram)
    if options.proc:
        count += 1
        stdout += '\tProcesses running: ' + str(processes)
    if count > 0:
        print stdout +'\n'
    else:
        print '{0}\tCPU usage:{1}\tCurrent number of processes running'\
              ':{2}\tRAM usage :{3}\n'.format(time, cur_cpu, processes, cur_ram)

    filename = options.filename
    app = options.app

    if filename and os.path.isfile(filename) or app:
        with open(filename, 'a') as res:
            if count > 0:
                res.write(stdout + '\n')
            else:
                res.write('{0}\tCPU usage:{1}\tCurrent number of processes running'\
                          ':{2}\t RAM usage :{3}\n'.format(time, cur_cpu, processes, cur_ram))


if __name__ == '__main__':
    sys.exit(main())


