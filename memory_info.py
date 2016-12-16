""" Script for gathering host information """

import time
import sys
import optparse
import subprocess


OPTION_LIST = ['cpu', 'ram', 'proc']
COMMANDS = {'ram':"free -m | grep Mem | awk '{print $4/$2*100}'",
            'cpu':"top -b -n1 | grep 'Cpu(s)' | awk '{print $2+$4}'",
            'proc':"ps -c | grep -v 'PID'| wc -l"}


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
    return vars(options)


def sys_call(option):
    """Function for getting system information"""
    return subprocess.Popen(COMMANDS[option], shell=True,
                            stdout=subprocess.PIPE).stdout.read()


def get_output(params):
    """Function for result returning"""
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    result = []
    if 'cpu' in params:
        result.append('  CPU usage: {}'.format(params['cpu']))
    if 'ram' in params:
        result.append('  RAM usage: {}'.format(params['ram']))
    if 'proc' in params:
        result.append('  Processes running: {}'.format(params['proc']))
    if not result:
        result.append('  CPU usage: {}  Current number of processes running'\
                      ': {}  RAM usage: {}\n'.format(params['cpu'],\
                      params['proc'], params['ram']))
    return  '{}  {}'.format(now, ''.join(result) +'\n')


def print_result(result, filename=None):
    """Write memory info into file"""
    if filename:
        with open(filename, 'a') as res:
            res.write(result)
    else:
        print result


def main():
    """ Function provide information about CPU, RAM usage and processes running  """
    options = get_optparse()                   # getting options from optpaarse
    args = [key for key, value in options.items() if value and key in OPTION_LIST]
    if not args:
        args = OPTION_LIST
    params = {}
    for cmd in args:
        params[cmd] = sys_call(cmd)
    result = get_output(params)                # formation output
    print_result(result, options['filename'])


if __name__ == '__main__':
    sys.exit(main())

