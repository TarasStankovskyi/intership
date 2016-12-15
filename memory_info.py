""" Script for gathering host information """


import time as t
import os
import sys
import optparse
import subprocess


def get_optparse():
    """Function for optparse option"""
    usage = "Usage: %prog -s path to file -a append iformation to existing file "
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-c', '--cpu', dest='cpu',
                      help='Print current CPU usage', default=False, action='store_true')
    parser.add_option('-r', '--ram', dest='ram',
                      help='Print current RAM usage', default=False, action='store_true')
    parser.add_option('-p', '--processes', dest='proc',
                      help='Print current number of processes running',
                      default=False, action='store_true')
    parser.add_option('-s', '--file', dest='filename', help='Path to file', default=None)

    options, _ = parser.parse_args()
    option_dict = vars(options)
    return option_dict

def sys_call(options):
    """Function for getting system information"""
    option_list = ['cpu', 'ram', 'proc']
    result = {}
    args = []
    commands = {'ram':"free -m | grep Mem | awk '{print $4/$2*100}'",\
                'cpu':"top -b -n1 | grep 'Cpu(s)' | awk '{print $2+$4}'",\
                'proc':"ps -c | grep -v 'PID'| wc -l"}

    del options['filename']
    [args.append(option) for option in options if options[option]]
    if len(args) == 0:
        args.extend(option_list)
    for arg in args:
        if arg in commands:
            result[arg] = subprocess.Popen(commands[arg], shell=True,\
            stdout=subprocess.PIPE).stdout.read()
    return result

def get_output(params):
    """Function for result returning"""
    time = t.strftime("%Y-%m-%d %H:%M:%S")
    result = [time]
    if 'cpu' in params:
        result.append(' CPU usage: {}'.format(params['cpu']))
    if 'ram' in params:
        result.append(' RAM usage: {}'.format(params['ram']))
    if 'proc' in params:
        result.append(' Processes running: {}'.format(params['proc']))
    if len(result) == 1:
        result.append('CPU usage:{}\tCurrent number of processes running'\
                      ':{}\tRAM usage :{}\n'.format(params['cpu'],\
                      params['proc'], params['ram']))
    res = ' '.join(result) +'\n'
    return res

def print_result(result, filename=None):
    """Write memory info into file"""
    if filename:
        with open(filename, 'a') as res:
            res.write(result)
    if not filename:
        print result

def main():
    """ Function provide information about CPU, RAM usage and processes running  """
    args = get_optparse()                   # getting options from optpaarse
    filename = args['filename']
    params = sys_call(args)                 # processing selected options
    result = get_output(params)             # formation output
    print_result(result, filename)


if __name__ == '__main__':
    sys.exit(main())

