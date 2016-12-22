""" Script for gathering host information """


import sys
import errno
import logging
import optparse
import subprocess
import logging.handlers


COMMANDS = {'ram':{'format':'RAM usage', 'cmd':"free -m | grep Mem | awk '{print $4/$2*100}'"},
            'cpu':{'format':'CPU usage', 'cmd':"top -b -n1 | grep 'Cpu(s)' | awk '{print $2+$4}'"},
            'proc':{'format':'Processes running', 'cmd':"ps -c | grep -v 'PID'| wc -l"},
            'user':{'format':'Current user', 'cmd':'echo "$USER"'}}

FORMATTER = logging.Formatter('Line : %(lineno)d - %(asctime)s -'\
                                  '%(name)s - %(levelname)s - %(message)s')

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
    result = []
    for param in params:
        result.append('  {}:  {}'.format(COMMANDS[param]['format'], params[param]))
    return '\n{}'.format(''.join(result))


def print_result(result, filename=None):
    """Write memory info into file or print in stdout"""
    file_handler = logging.getLogger(__name__)
    file_handler.setLevel(logging.INFO)
    fh = logging.FileHandler('{}.log'.format(filename))

    fh.setFormatter(FORMATTER)
    file_handler.propagate = False
    file_handler.addHandler(fh)

    console = logging.getLogger('main')
    console.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(FORMATTER)
    console.propagate = False
    console.addHandler(ch)

    if filename:
        try:
            file_handler.info(result)
        except  (OSError, IOError) as err:
            logging.exception('Failed to write into file : {}'.format(err))
    else:
        console.info(result)


def main():
    """ Function provide information about CPU, RAM usage and processes running  """
    log_handler = logging.getLogger('memory_info')
    log_handler.setLevel(logging.INFO)
    lh = logging.handlers.SysLogHandler(address='/dev/log',
                                        facility=logging.handlers.SysLogHandler.LOG_LOCAL7)
    lh.setFormatter(FORMATTER)
    log_handler.propagate = False
    log_handler.addHandler(lh)

    log_handler.info('Script started the job')
    options = get_optparse()                   # getting options from optpaarse
    log_handler.debug("Program's option dict : %s", options)
    args = [key for key, value in options.items() if value and key in COMMANDS]
    log_handler.debug('Arguments that have True value : %s ', args)
    if not args:
        args = COMMANDS.keys()
    log_handler.debug('Arguments that have True value : %s ', args)
    params = {}
    log_handler.info('Operating with options')
    for cmd in args:
        log_handler.debug('%s is running', cmd)
        params[cmd] = sys_call(cmd)
    log_handler.debug('Params : %s', params)
    result = get_output(params)                # formation output
    log_handler.info('Almsot finished')
    print_result(result, options['filename'])


if __name__ == '__main__':
    sys.exit(main())

