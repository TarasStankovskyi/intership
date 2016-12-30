#!/usr/bin/python
""" Script for gathering host information """

import os
import sys
import logging
import optparse
import subprocess
import ConfigParser
import logging.config


COMMANDS = {'ram':{'format':'RAM usage', 'cmd':"free -m | grep Mem | awk '{print $4/$2*100}'"},
            'cpu':{'format':'CPU usage', 'cmd':"top -b -n1 | grep 'Cpu(s)' | awk '{print $2+$4}'"},
            'proc':{'format':'Processes running', 'cmd':"ps -c | grep -v 'PID'| wc -l"},
            'user':{'format':'Current user', 'cmd':'echo "$USER"'}}

FORMATTER = logging.Formatter('Line : %(lineno)d - %(asctime)s -'\
                                  '%(name)s - %(levelname)s - %(message)s')


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


def log_results(result, logger):
    """Write memory info into file or print in stdout"""
    try:
        logger.info(result)
    except (OSError, IOError) as err:
        logger.exception('Failed to log result {}'.format(err))


def get_config_options(filename):
    "Function return dictionary with all options from configuration file"
    config = ConfigParser.ConfigParser()
    config.read(filename)
    conf_options = {}
    for section in config.sections():
        conf_options[section] = {}
        for option in config.options(section):
            conf_options[section][option] = config.get(section, option)
    return conf_options


def main():
    """ Function provide information about CPU, RAM usage and processes running """
    parser = optparse.OptionParser()
    parser.add_option('-s', '--file', dest='filename', help='Path to file', default=None)
    options, _ = parser.parse_args()
    if not options.filename:
        raise IOError("Path to config required")

    conf_options = get_config_options(options.filename)
    logging.config.fileConfig(conf_options['logging']['config_file'])
    logger = logging.getLogger(conf_options['logging'].get('logger', 'stream'))
    logger.debug('Get options from configuration file')
    logger.info('Script started the job')

    options = {option : eval(conf_options['commands'][option]) for option in conf_options['commands']\
              if conf_options['commands'][option] in ('True','False')}

    logger.debug("Program's option dict : %s", options)
    args = [key for key, value in options.items() if value and key in COMMANDS]\
           or COMMANDS.keys()
    params = {arg : sys_call(arg) for arg in args}
    result = get_output(params)
    logger.info('Formatting output')
    log_results(result, logger)
    logger.info('Finished')

if __name__ == '__main__':
    sys.exit(main())

