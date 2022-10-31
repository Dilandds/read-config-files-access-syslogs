from datetime import datetime, date
from math import inf
import configparser
from operator import attrgetter
import platform
import pwd
import grp

# filewide constants
CONFIG_PATH = 'projectini.ini'
OUTPUT_PATH = 'projectoutput'
OUTPUT_EXT = '.txt'
LOG_PATH = '/var/log/syslog' #should change to syslog if runs on mac
DATE_FORMAT = '%b %d %H:%M:%S'


class User:
    '''A user with uid, name, and groups'''

    def __init__(self, user_id: int, user_name: str, groups: list[str]):
        self.uid = user_id
        self.name = user_name
        self.groups = groups

    def __repr__(self) -> str:
        return f'{self.uid}:{self.name}:{",".join(self.groups)}'


def read_config(file_path: str):
    '''Read the config from the given path and sanitize accounting for missing values.'''
    config = configparser.ConfigParser()
    # default values
    config['BASIC'] = {'outFile': OUTPUT_PATH}
    config['FILTER_ACCOUNTS'] = {
        'sortAccountsReverse': 'False',
        'sortAccountsCriteria': 'name',
        'linesOfAccountsData': '10'
    }
    config['FILTER_LOGS'] = {
        'sortLogsReverse': 'False',
        'logTimeFrom': 'Jan 1 00:00:00',
        'logTimeTo': 'Dec 31 00:00:00',
        'logCriteria': ''
    }
    config.read(file_path)
    # sanitize the config
    sanitized_config = {
        'BASIC': {
            'outFile':
            config['BASIC']['outFile']
            if config['BASIC']['outFile'] else OUTPUT_PATH
        },
        'FILTER_ACCOUNTS': sanitize_account_filters(config),
        'FILTER_LOGS': sanitize_log_filters(config)
    }
    return sanitized_config


def read_logs(log_path: str, config: dict):
    '''Read logs from the log path'''
    # read log lines from the given file
    logs = [
        line.strip() for line in open(log_path, 'r').readlines()
        if line.strip()
    ]
    filtered_logs = []
    # filter logs that match our criteria
    for log in logs:
        try:
            log_date = datetime.strptime(log[:15],
                                         DATE_FORMAT).replace(year=2022)
            if config['logTimeFrom'] <= log_date <= config['logTimeTo']:
                filtered_logs.append(log)
        except Exception as _:
            try:
                filtered_logs[-1] += '\n' + log
            except:
                pass
    # return sorted list according to given criteria
    return sorted([
        log for log in filtered_logs
        if config['logCriteria'].lower() in log.lower()
    ],
                  reverse=config['sortLogsReverse'])


def system_accounts(options: dict):
    '''Returns a list of Users in the system.'''
    users = []
    # for each pwd entry create a User with uid, name, and their groups.
    for pwd_entry in pwd.getpwall():
        users.append(
            User(
                pwd_entry.pw_uid, pwd_entry.pw_name,
                list(
                    set([
                        group.gr_name for group in grp.getgrall()
                        if pwd_entry.pw_name in group.gr_mem
                    ]))))
    users.sort(key=attrgetter(options['sortAccountsCriteria']),
               reverse=options['sortAccountsReverse'])
    return users


def sanitize_account_filters(config: configparser.ConfigParser):
    '''Sanitize FILTER_ACCOUNTS section'''
    options = {}
    # variable type mapping
    options['sortAccountsReverse'] = config['FILTER_ACCOUNTS'][
        'sortAccountsReverse'] == 'True'
    options['sortAccountsCriteria'] = config['FILTER_ACCOUNTS'][
        'sortAccountsCriteria']
    if options['sortAccountsCriteria'] not in ['name', 'uid']:
        print('sortAccountsCriteria invalid. resetting to name.')
        options['sortAccountsCriteria'] = 'name'
    try:
        options['linesOfAccountsData'] = int(
            config['FILTER_ACCOUNTS']['linesOfAccountsData'])
    except:
        if config['FILTER_ACCOUNTS']['linesOfAccountsData'] != 'All':
            print('linesOfAccountsData invalid. resetting to unlimited.')
        options['linesOfAccountsData'] = inf
    return options


def sanitize_log_filters(config: configparser.ConfigParser):
    '''Sanitize FILTER_LOGS section.'''
    options = {}
    # variable type mapping
    options['sortLogsReverse'] = config['FILTER_LOGS'][
        'sortLogsReverse'] == 'True'
    try:
        options['logTimeFrom'] = datetime.strptime(
            config['FILTER_LOGS']['logTimeFrom'],
            DATE_FORMAT).replace(year=date.today().year)
    except:
        options['logTimeFrom'] = datetime.fromtimestamp(0).replace(
            year=date.today().year)
    try:
        options['logTimeTo'] = datetime.strptime(
            config['FILTER_LOGS']['logTimeTo'],
            DATE_FORMAT).replace(year=date.today().year)
    except:
        options['logTimeFrom'] = date.today()
    options['logCriteria'] = config['FILTER_LOGS']['logCriteria']
    return options


def write_data(output_path: str, accounts: list, logs: list):
    '''Write data to the given file'''
    with open(output_path, 'w') as output:
        output.write(platform.node() + '\n')  # computer name
        output.write(date.today().isoformat() + '\n')  # current time
        output.writelines('\n'.join([str(acc)
                                     for acc in accounts]))  # output 1
        output.write('\n\n')
        output.writelines('\n'.join(logs))  # output 2


def main():
    config = read_config(CONFIG_PATH)
    running = True
    # run the main menu
    while running:
        print('\n\n1. System Accounts')
        print('2. System Logs')
        print('3. Generate Report')
        print('0. Exit')
        picked = input('\t: ')
        # act according to user choice
        if picked == '1':
            print(*system_accounts(config['FILTER_ACCOUNTS']), sep='\n')
        elif picked == '2':
            print(*read_logs(LOG_PATH, config['FILTER_LOGS']), sep='\n')
        elif picked == '3':
            write_data(config['BASIC']['outFile'] + OUTPUT_EXT,
                       system_accounts(config['FILTER_ACCOUNTS']),
                       read_logs(LOG_PATH, config['FILTER_LOGS']))
            print(f'\ndata written to {config["BASIC"]["outFile"]}')
        elif picked == '0':
            running = False
        else:
            print('Invalid option')


if __name__ == '__main__':
    main()
