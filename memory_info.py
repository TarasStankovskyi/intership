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
    filename = options.filename
    return option_dict, filename

def get_arguments_list(options):
    """Function for parsing optparse options"""
    del options['filename']
    args = []
    option_list = ['cpu', 'ram', 'proc']
    for option in options:
        if options[option]:
            args.append(option)
    if len(args) == 0:
        args.extend(option_list)
    return args

def sys_call(args):
    """Function for getting system information"""
    commands = {'ram':"free -m | grep Mem | awk '{print $4/$2*100}'",\
                'cpu':"top -b -n1 | grep 'Cpu(s)' | awk '{print $2+$4}'",\
                'proc':"ps -c | grep -v 'PID'| wc -l"}
    result = {}
    for arg in args:
        if arg in commands:
            result[arg] = subprocess.Popen(commands[arg], shell=True,\
            stdout=subprocess.PIPE).stdout.read()
    return result

def print_result(params, filename=None):
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
    if filename:
        write_into_file(filename, res)
    if not filename:
        print res
    return 1

def write_into_file(filename, result):
    """Write memory info into file"""
    if os.path.exists(filename):
        with open(filename, 'a') as res:
            res.write(result)
    else:
        print "There is not file:'{}' in this directory ".format(filename)

def main():
    """ Function provide information about CPU, RAM usage and processes running  """
    option_dict, filename = get_optparse()
    args = get_arguments_list(option_dict)
    params = sys_call(args)
    print_result(params, filename)


if __name__ == '__main__':
    sys.exit(main())

