#!/usr/bin/python3
import json
import requests
import os
import sys
import getopt
import csv


def main():
    shard = ''
    username = ''
    password = ''
    localpath = ''
    workspacepath = ''
    releasefile = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs:u:p:lwf',
                                   ['shard=', 'username=', 'password=', 'localpath=', 'workspacepath=', 'releasefile='])
    except getopt.GetoptError:
        print(
            'delete.py -u <username> -p <password> -s <shard> -l <localpath> -w <workspacepath> -f <releasefile>)')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print (
                'delete.py -u <username> -p <password> -s <shard> -l <localpath> -w <workspacepath> -f <releasefile>')
            sys.exit()
        elif opt in ('-s', '--shard'):
            shard = arg
        elif opt in ('-u', '--username'):
            username = arg
        elif opt in ('-p', '--password'):
            password = arg
        elif opt in ('-l', '--localpath'):
            localpath = arg
        elif opt in ('-w', '--workspacepath'):
            workspacepath = arg
        elif opt in ('-f', '--releasefile'):
            releasefile = arg

    print ('-s is ' + shard)
    print ('-u is ' + username)
    print ('-l is ' + localpath)
    print ('-w is ' + workspacepath)
    print ('-f is ' + releasefile)

    delete_file(shard, username, password)



def delete(shard, username, password):

    print('Importing file:' + fullpath + ' to Workspace path:' + fullworkspacepath)
    files = {'content': open(fullpath, 'rb')}
    values = {'path': fullworkspacepath, 'language': sourcetype, 'overwrite': 'true', 'format': 'SOURCE'}
    resp = requests.post('https://' + shard + '.cloud.databricks.com/api/2.0/workspace/import', files=files,
                         data=values, auth=(username, password))
    print(resp.text)


if __name__ == '__main__':
    main()
