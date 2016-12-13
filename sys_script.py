""" Script for gathering host information """


from datetime import datetime
import sys
import os
import optparse
import subprocess

def ram():
    c1 = ['free', '-m']
    p1 = subprocess.Popen(c1, stdout=subprocess.PIPE)
    c2 = ['grep', 'Mem']
    p2 = subprocess.Popen(c2, stdin=p1.stdout, stdout=subprocess.PIPE)
    c3 = ['awk', '{print $4/$2*100}']
    p3 = subprocess.Popen(c3, stdin=p2.stdout, stdout=subprocess.PIPE)
    result = p3.stdout.read()
    return result

def cpu():
    c1 = ['top', '-b', '-n1']
    p1 = subprocess.Popen(c1, stdout=subprocess.PIPE)
    c2 = ['grep', 'Cpu(s)']
    p2 = subprocess.Popen(c2, stdin=p1.stdout, stdout=subprocess.PIPE)
    c3 = ['awk', '{print $2+$4}']
    p3 = subprocess.Popen(c3, stdin=p2.stdout, stdout=subprocess.PIPE)
    result = p3.stdout.read()
    return result

def cur_processes():
    c1 = ['ps', '-c']
    p1 = subprocess.Popen(c1, stdout=subprocess.PIPE)
    c2 = ['grep', '-v', 'PID']
    p2 = subprocess.Popen(c2, stdin=p1.stdout, stdout=subprocess.PIPE)
    c3 = ['wc', '-l']
    p3 = subprocess.Popen(c3, stdin=p2.stdout, stdout=subprocess.PIPE)
    result = p3.stdout.read()
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


