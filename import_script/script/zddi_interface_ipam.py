#!/usr/bin/env python
# coding=utf-8
import json
from zddi_base import ZddiBase


# 提供zddi网络管理部分的常用操作方法


class NetworkManager(ZddiBase):
    def __init__(self, cms_ip='192.168.1.1', name_value = '默认组', cms_user='admin', cms_passwd='admin', lang='zh'):
        if self.isIp(cms_ip):
            self.__cms_ip = cms_ip
        else:
            print('cms_ip is illegal')
            raise Exception
        self.__name_value = name_value
        self.__cms_user = cms_user
        self.__cms_passwd = cms_passwd
        self.__cms_lang = lang

    def creatNetwork(self, networks, owners, attrs=[]):
        url = 'https://%s:20120/multi-networks' % (self.__cms_ip)
        params = {'networks': networks,
                  'owners': owners,
                  'current_user': self.__cms_user,
                  'templates': '0',
                  'name_value': self.__name_value,  
                  'lang': self.__cms_lang,
                  'uuid': 'uuid',
                  'comment': ''}
        if len(attrs) != 0:
            for i in range(1, len(attrs) + 1):
                params['key_' + str(i+5)] = attrs[i - 1]
        return self.sendCmd('post', url, params, self.__cms_user, self.__cms_passwd).status_code

    def updateNetwork(self, networks, attrs=[]):
        url = 'https://%s:20120/networks' % (self.__cms_ip)
        params = {'ids': networks,
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        if len(attrs) != 0:
            for i in range(1, len(attrs) + 1):
                params['key_' + str(i)] = attrs[i - 1]
        return self.sendCmd('put', url, params, self.__cms_user, self.__cms_passwd).status_code

    def updateNetworkOwner(self, networks, owners=[]):
        url = 'https://%s:20120/networks/owners' % (self.__cms_ip)
        params = {'ids': networks,
                  'owners': owners,
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        return self.sendCmd('put', url, params, self.__cms_user, self.__cms_passwd).status_code

    def deleteNetwork(self, networks):
        url = 'https://%s:20120/networks' % (self.__cms_ip)
        params = {'ids': networks,
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        return self.sendCmd('delete', url, params, self.__cms_user, self.__cms_passwd).status_code

    def getLeafNetworks(self):
        url = 'https://%s:20120/leaf-networks' % (self.__cms_ip)
        params = {'current_user': self.__cms_user}
        return self.sendCmd('get', url, params, self.__cms_user, self.__cms_passwd).json()

    def getNetworkInfo(self, network):
        url = 'https://%s:20120/networks/%s' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {'current_user': self.__cms_user}
        return self.sendCmd('get', url, params, self.__cms_user, self.__cms_passwd).json()

    def getNetworkAddressInfos(self, network):
        url = 'https://%s:20120/networks/%s/addressinfos' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {'current_user': self.__cms_user}
        return self.sendCmd('get', url, params, self.__cms_user, self.__cms_passwd).json()

# 提供zddi mac管理的常用操作方法


class MacManager(ZddiBase):
    def __init__(self, cms_ip='192.168.1.1', cms_user='admin', cms_passwd='admin', lang='zh'):
        if self.isIp(cms_ip):
            self.__cms_ip = cms_ip
        else:
            print('cms_ip is not a ip address')
            raise Exception
        self.__cms_user = cms_user
        self.__cms_passwd = cms_passwd
        self.__cms_lang = lang

    def creatMacInfo(self, mac, nic_port=[], attrs=[]):
        url = 'https://%s:20120/mac-informations' % (self.__cms_ip)
        params = {'MAC': mac,
                  'nic_port': nic_port,
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid',
                  'comment': ''}
        if len(attrs) != 0:
            for i in range(1, len(attrs) + 1):
                params['key_' + str(i)] = attrs[i - 1]
        return self.sendCmd('post', url, params, self.__cms_user, self.__cms_passwd).status_code

    def updateMacInfo(self, macs, nic_port=[], attrs=[]):
        url = 'https://%s:20120/mac-informations' % (self.__cms_ip)
        params = {'ids': macs,
                  'nic_port': nic_port,
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        if len(attrs) != 0:
            for i in range(1, len(attrs) + 1):
                params['key_' + str(i)] = attrs[i - 1]
        return self.sendCmd('put', url, params, self.__cms_user, self.__cms_passwd).status_code

    def deleteMacInfo(self, macs):
        url = 'https://%s:20120/mac-informations' % (self.__cms_ip)
        params = {'ids': macs,
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        return self.sendCmd('delete', url, params, self.__cms_user, self.__cms_passwd).status_code

    def getMacsInfo(self):
        url = 'https://%s:20120/mac-informations' % (self.__cms_ip)
        params = {'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        return self.sendCmd('get', url, params, self.__cms_user, self.__cms_passwd).json()


# 提供zddi地址池管理常用操作方法


class DhcpManager(ZddiBase):
    def __init__(self, cms_ip='192.168.1.1', cms_user='admin', cms_passwd='admin', lang='zh'):
        if self.isIp(cms_ip):
            self.__cms_ip = cms_ip
        else:
            print('cms_ip is not a ip address')
            raise Exception
        self.__cms_user = cms_user
        self.__cms_passwd = cms_passwd
        self.__cms_lang = lang

    def creatDynamicPool(self, network, owner, ip_start, ip_end, routers, domain_name_servers,  lease_time='43200', domain_name='', acls=['any'], bootp_switch='yes', attrs=[], options=[]):
        url = 'https://%s:20120/networks/%s/dhcp-resources' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {'owner': owner,
                  'current_user': self.__cms_user,
                  'type': 'dynamic',
                  'ip_start': ip_start,
                  'ip_end': ip_end,
                  'default_lease_time': lease_time,
                  'default_lease_time_unit': '1',
                  'max_lease_time': lease_time,
                  'max_lease_time_unit': '1',
                  'min_lease_time': str(int(lease_time) - 1),
                  'min_lease_time_unit': '1',
                  'domain_name_servers': domain_name_servers,
                  'routers': routers,
                  'domain_name': domain_name,
                  'auto_bind': 'no',
                  'bootp': bootp_switch,
                  'acls': acls,
                  'options': options,
                  'max_value': lease_time,
                  'max_unit': '1',
                  'def_value': lease_time,
                  'def_unit': '1',
                  'min_value': str(int(lease_time) - 1),
                  'min_unit': '1',
                  'inherit_default_lease_time': 'no',
                  'inherit_max_lease_time': 'no',
                  'inherit_min_lease_time': 'no',
                  'inherit_domain_name_servers': 'no',
                  'inherit_routers': 'no',
                  'inherit_domain_name': 'no',
                  'inherit_options': 'no',
                  'inherit_acls': 'no',
                  'inherit_auto_bind': 'no',
                  'inherit_bootp': 'no',
                  'lang': self.__cms_lang,
                  'uuid': 'uuid',
                  'comment': ''}
        if len(attrs) != 0:
            for i in range(1, len(attrs) + 1):
                params['key_' + str(i)] = attrs[i - 1]
        return self.sendCmd('post', url, params, self.__cms_user, self.__cms_passwd).status_code

    def updateDynamicPool(self, network, ip_start, ip_end, routers, domain_name_servers,  lease_time='43200', domain_name='', acls=['any'], bootp_switch='yes', attrs=[], options=[]):
        url = 'https://%s:20120/networks/%s/dhcp-resources' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {'ids': [ip_start + '-' + ip_end],
                  'current_user': self.__cms_user,
                  'type': 'dynamic',
                  'ip_start': ip_start,
                  'ip_end': ip_end,
                  'default_lease_time': lease_time,
                  'default_lease_time_unit': '1',
                  'max_lease_time': lease_time,
                  'max_lease_time_unit': '1',
                  'min_lease_time': str(int(lease_time) - 1),
                  'min_lease_time_unit': '1',
                  'domain_name_servers': domain_name_servers,
                  'routers': routers,
                  'domain_name': domain_name,
                  'auto_bind': 'no',
                  'bootp': bootp_switch,
                  'acls': acls,
                  'options': options,
                  'max_value': lease_time,
                  'max_unit': '1',
                  'def_value': lease_time,
                  'def_unit': '1',
                  'min_value': str(int(lease_time) - 1),
                  'min_unit': '1',
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        if len(attrs) != 0:
            for i in range(1, len(attrs) + 1):
                params['key_' + str(i)] = attrs[i - 1]
        return self.sendCmd('put', url, params, self.__cms_user, self.__cms_passwd).status_code

    def creatStaticPool(self, network, owner, ip_address, mac_address, routers, domain_name_servers,  lease_time='43200', domain_name='', attrs=[], options=[]):
        url = 'https://%s:20120/networks/%s/dhcp-resources' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {'owner': owner,
                  'current_user': self.__cms_user,
                  'type': 'static',
                  'ip_start': ip_address,
                  'hardware_ethernet': mac_address,
                  'default_lease_time': lease_time,
                  'default_lease_time_unit': '1',
                  'max_lease_time': lease_time,
                  'max_lease_time_unit': '1',
                  'min_lease_time': str(int(lease_time) - 1),
                  'min_lease_time_unit': '1',
                  'domain_name_servers': domain_name_servers,
                  'routers': routers,
                  'domain_name': domain_name,
                  'auto_bind': 'no',
                  'bootp': 'yes',
                  'options': options,
                  'max_value': lease_time,
                  'max_unit': '1',
                  'def_value': lease_time,
                  'def_unit': '1',
                  'min_value': str(int(lease_time) - 1),
                  'min_unit': '1',
                  'inherit_default_lease_time': 'no',
                  'inherit_max_lease_time': 'no',
                  'inherit_min_lease_time': 'no',
                  'inherit_domain_name_servers': 'no',
                  'inherit_routers': 'no',
                  'inherit_domain_name': 'no',
                  'inherit_options': 'no',
                  'lang': self.__cms_lang,
                  'uuid': 'uuid',
                  'comment': ''}
        if len(attrs) != 0:
            for i in range(1, len(attrs) + 1):
                params['key_' + str(i+5)] = attrs[i - 1]
        return self.sendCmd('post', url, params, self.__cms_user, self.__cms_passwd).status_code

    def updateStaticPool(self, network, ip_address, mac_address, routers, domain_name_servers,  lease_time='43200', domain_name='', attrs=[], options=[]):
        url = 'https://%s:20120/networks/%s/dhcp-resources' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {'ids': [ip_address + '-' + ip_address],
                  'current_user': self.__cms_user,
                  'type': 'static',
                  'hardware_ethernet': mac_address,
                  'default_lease_time': lease_time,
                  'default_lease_time_unit': '1',
                  'max_lease_time': lease_time,
                  'max_lease_time_unit': '1',
                  'min_lease_time': str(int(lease_time) - 1),
                  'min_lease_time_unit': '1',
                  'domain_name_servers': domain_name_servers,
                  'routers': routers,
                  'domain_name': domain_name,
                  'auto_bind': 'no',
                  'bootp': 'yes',
                  'options': options,
                  'max_value': lease_time,
                  'max_unit': '1',
                  'def_value': lease_time,
                  'def_unit': '1',
                  'min_value': str(int(lease_time) - 1),
                  'min_unit': '1',
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        if len(attrs) != 0:
            for i in range(1, len(attrs) + 1):
                params['key_' + str(i)] = attrs[i - 1]
        return self.sendCmd('put', url, params, self.__cms_user, self.__cms_passwd).status_code

    def creatReservedPool(self, network, owner, ip_start, ip_end, attrs=[]):
        url = 'https://%s:20120/networks/%s/dhcp-resources' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {'owner': owner,
                  'current_user': self.__cms_user,
                  'type': 'reservation',
                  'ip_start': ip_start,
                  'ip_end': ip_end,
                  'routers': [],
                  'domain_name_servers': [],
                  'options': [],
                  'lang': self.__cms_lang,
                  'uuid': 'uuid',
                  'comment': ''}
        if len(attrs) != 0:
            for i in range(1, len(attrs) + 1):
                params['key_' + str(i+5)] = attrs[i - 1]
        return self.sendCmd('post', url, params, self.__cms_user, self.__cms_passwd).status_code

    def updateReservedPool(self, network, ip_start, ip_end, attrs=[]):
        url = 'https://%s:20120/networks/%s/dhcp-resources' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {'routers': [],
                  'domain_name_servers': [],
                  'options': [],
                  'type': 'reservation',
                  'ids': [ip_start + '-' + ip_end],
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        if len(attrs) != 0:
            for i in range(1, len(attrs) + 1):
                params['key_' + str(i)] = attrs[i - 1]
        return self.sendCmd('put', url, params, self.__cms_user, self.__cms_passwd).status_code

    def getDhcpPools(self, network):
        url = 'https://%s:20120/networks/%s/dhcp-resources' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        return self.sendCmd('get', url, params, self.__cms_user, self.__cms_passwd).json()

    def deletePools(self, ids):
        url = 'https://%s:20120/networks/%s/dhcp-resources' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {'ids': ids,
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        return self.sendCmd('delete', url, params, self.__cms_user, self.__cms_passwd).status_code

    def updatePoolsOwner(self, ids, owner):
        url = 'https://%s:20120/networks/%s/dhcp-resources/owners' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {'ids': ids,
                  'owner': owner,
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        return self.sendCmd('put', url, params, self.__cms_user, self.__cms_passwd).status_code

    def updatePoolMsgpush(self, network, ids, urls, ip_switch='yes', mac_switch='yes', client_hostname_switch='yes', vci_switch='yes', fgr_switch='yes', remain_lease_switch='yes', portal_switch='no', fgr_name_switch='yes', manufacturer_switch='other'):
        url = 'https://%s:20120/networks/%s/dhcp-resources/msgpush' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {"msgpush": {'enabled': 'yes',
                              'ip': ip_switch,
                              'mac': mac_switch,
                              'client_hostname': client_hostname_switch,
                              'vci': vci_switch,
                              'fgr': fgr_switch,
                              'remain_lease': remain_lease_switch,
                              'portal': portal_switch,
                              'fgr_name': fgr_name_switch,
                              'manufacturer': manufacturer_switch,
                              'urls': urls},
                  'ids': ids,
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        return self.sendCmd('put', url, params, self.__cms_user, self.__cms_passwd).status_code

    def offPoolMsgpush(self, network, ids):
        url = 'https://%s:20120/networks/%s/dhcp-resources/msgpush' % (
            self.__cms_ip, network.replace("/", "$"))
        params = {"msgpush": {'enabled': 'no'},
                  'ids': ids,
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid'}
        return self.sendCmd('put', url, params, self.__cms_user, self.__cms_passwd).status_code

    def creatAcl(self, acl_name, acl_type='macs'):
        url = 'https://%s:20120/dhcp-acls' % (self.__cms_ip)
        params = {'name': acl_name,
                  'type': acl_type,
                  'current_user': self.__cms_user,
                  'lang': self.__cms_lang,
                  'uuid': 'uuid',
                  'comment': ''}
        return self.sendCmd('post', url, params, self.__cms_user, self.__cms_passwd).status_code


if __name__ == '__main__':
    t1 = NetworkManager(cms_ip='10.1.112.94')
    t2 = MacManager(cms_ip='10.1.112.94')
    t3 = DhcpManager(cms_ip='10.1.112.94')
    # 测试网络管理部分方法
    print t1.creatNetwork(['192.168.1.0/24', '192.168.2.0/24', '192.168.3.0/24', '192.168.4.0/24', '192.168.5.0/24'], ['local.master'], attrs=['1', '1'])
    #print t1.updateNetwork(['192.168.1.0/24'], attrs=['2', '2'])
    #print t1.updateNetworkOwner(['192.168.1.0/24', '192.168.2.0/24'], ['local.master', 'local.slave'])
    #print t1.deleteNetwork(['192.168.5.0/24'])
    #print t1.getLeafNetworks()
    #print t1.getNetworkInfo('192.168.1.0/24')
    # 测试mac管理部分方法
    print t2.creatMacInfo('11:11:11:11:11:11', nic_port=['g0/0/1'], attrs=['1'])
    #print t2.updateMacInfo(['11:11:11:11:11:11'], nic_port=['g0/1/1'], attrs=['11'])
    #print t2.deleteMacInfo(['11:11:11:11:11:11'])
    #print t2.getMacsInfo()
    # 测试dhcp管理部分方法
    print t3.creatReservedPool('192.168.1.0/24','local.master', '192.168.1.2', '192.168.1.9')
    #print t3.creatDynamicPool('192.168.1.0/24', 'local.master', '192.168.1.2', '192.168.1.9', ['192.168.1.1'], ['114.114.114.114', '8.8.8.8'], lease_time='1800', attrs=['1', '1'])
    #print t3.updateDynamicPool('192.168.1.0/24', '192.168.1.2', '192.168.1.9', ['192.168.1.254'], ['223.5.5.5'], lease_time='3600', attrs=['2', '2'])
