#!/usr/bin/python
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


def log_results(result, filename=None):
    """Write memory info into file or print in stdout"""
    if filename:
        logger = get_logger('memory_info_results', handler_type='file', filename=filename)
        try:
            logger.info(result)
        except (OSError, IOError) as err:
            logger.exception('Failed to write into file {}: {}'.format(filename, err))
    else:
        logger = get_logger('memory_info_results', 'stream')
        logger.info(result)


def get_logger(name, handler_type='stream', level=logging.INFO, propagate=False, filename=None):
    opt = {'stream': logging.StreamHandler(),
           'file': logging.FileHandler('{}.log'.format(filename)),
           'syslog': logging.handlers.SysLogHandler(address='/dev/log',
                                             facility=logging.handlers.SysLogHandler.LOG_LOCAL7)}
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = propagate
    if handler_type in opt:
        log = opt[handler_type]
        log.setFormatter(FORMATTER)
        logger.addHandler(log)
    return logger


def main():
    """ Function provide information about CPU, RAM usage and processes running """
    sys_log = get_logger('memory_info', 'syslog')
    sys_log.info('Script started the job')
    options = get_optparse()                   # getting options from optpaarse
    sys_log.debug("Program's option dict : %s", options)
    args = [key for key, value in options.items() if value and key in COMMANDS]
    sys_log.debug('Arguments that have True value : %s ', args)
    if not args:
        args = COMMANDS.keys()
    sys_log.debug('Arguments that have True value : %s ', args)
    params = {}
    sys_log.info('Operating with options')
    for cmd in args:
        sys_log.debug('%s is running', cmd)
        params[cmd] = sys_call(cmd)
    sys_log.debug('Params : %s', params)
    result = get_output(params)                # formation output
    sys_log.info('Almsot finished')

    log_results(result, options['filename'])

if __name__ == '__main__':
    sys.exit(main())

