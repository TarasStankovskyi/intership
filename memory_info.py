""" Script for gathering host information """

import time
import sys
import errno
import logging
import optparse
import subprocess


COMMANDS = {'ram':{'format':'RAM usage', 'cmd':"free -m | grep Mem | awk '{print $4/$2*100}'"},
            'cpu':{'format':'CPU usage', 'cmd':"top -b -n1 | grep 'Cpu(s)' | awk '{print $2+$4}'"},
            'proc':{'format':'Processes running', 'cmd':"ps -c | grep -v 'PID'| wc -l"},
            'user':{'format':'Current user', 'cmd':'echo "$USER"'}}


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
    parser.add_option('-u', '--user', dest='user',
                      help='Print current user', default=False, action='store_true')

    options, _ = parser.parse_args()
    return vars(options)


def sys_call(option):
    """Function for getting system information"""
    return subprocess.Popen(COMMANDS[option]['cmd'], shell=True,
                            stdout=subprocess.PIPE).stdout.read()


def get_output(params):
    """Function for result returning"""
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    result = []
    for param in params:
        result.append('  {}:  {}'.format(COMMANDS[param]['format'], params[param]))
    return '{}  {}\n'.format(now, ''.join(result))


def print_result(result, filename=None):
    """Write memory info into file"""
    if filename:
        try:
            with open(filename, 'a') as res:
                res.write(result)
        except  (OSError, IOError) as err:
            logging.exception('Failed to write into file {}: {}'.format(filename, err))
    else:
        print result


def main():
    """ Function provide information about CPU, RAM usage and processes running  """
    logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]#%(levelname)-8s'\
                               '[%(asctime)s] %(message)s', level=logging.DEBUG)
    logging.info('Script started the job')
    options = get_optparse()                   # getting options from optpaarse
    logging.debug("Program's option dict : %s", options)
    args = [key for key, value in options.items() if value and key in COMMANDS]
    logging.debug('Arguments that have True value : %s ', args)
    if not args:
        args = COMMANDS.keys()
    logging.debug('Arguments that have True value : %s ', args)
    params = {}
    logging.info('Operating with options')
    for cmd in args:
        params[cmd] = sys_call(cmd)
    logging.debug('Params : %s', params)
    result = get_output(params)                # formation output
    logging.info('Almsot finished')
    print_result(result, options['filename'])


if __name__ == '__main__':
    sys.exit(main())

