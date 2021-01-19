#!/usr/bin/env python
# coding=utf-8
import IPy
import requests
import json
requests.packages.urllib3.disable_warnings()


class ZddiBase():
    def isIp(self, address):
        try:
            IPy.IP(address)
            return True
        except:
            return False

    def sendCmd(self, method, url, params, user, passwd):
        headers = {'Content-type': 'application/json'}
        if method == 'post':
            r = requests.post(url, data=json.dumps(
                params), headers=headers, auth=(user, passwd), verify=False)
        elif method == 'put':
            r = requests.put(url, data=json.dumps(
                params), headers=headers, auth=(user, passwd), verify=False)
        elif method == 'get':
            r = requests.get(url, data=json.dumps(
                params), headers=headers, auth=(user, passwd), verify=False)
        elif method == 'delete':
            r = requests.delete(url, data=json.dumps(
                params), headers=headers, auth=(user, passwd), verify=False)
        else:
            print('http method is illegal')
            raise Exception
        return r
