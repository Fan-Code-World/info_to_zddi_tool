#!/usr/bin/env python
# coding=utf-8
import csv
import time
import datetime
import IPy
import re
import config
from zddi_interface_ipam import *
from format_config import HandleInfo


# info全局配置项
info_global_conf = {'default_lease_time': '43200',
                    'domain_name_servers': ['10.232.3.202', '10.235.25.161']}


# 日志函数
def loger(log_info):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = now + ' ' + log_info
    print content
    f = file(config.LOG_FILE, 'a')
    f.write(content + '\n')
    f.close()



# 从文件读取网络及自定义属性列表
network_comments = {}
network_file_handle = file(config.IMPORT_DATA_PATH + 'FT_office.csv', 'r')
network_reader = csv.reader(network_file_handle)
for network_line in network_reader:
    network_comments[network_line[0]] = {
        'subnet_mask': network_line[0], 'comment': network_line[1]}
network_file_handle.close()
'''
# 从文件读取固定地址或保留地址的自定义属性列表
ipaddr_comments = {}
ipaddr_file_handle = open(config.IMPORT_DATA_PATH + 'exist_fixed_network.csv', 'r')
ipaddr_reader = csv.reader(ipaddr_file_handle)
for ipaddr_line in ipaddr_reader:
    if ipaddr_comments.has_key(ipaddr_line[0]):
        ipaddr_comments[ipaddr_line[0]][ipaddr_line[1]] = {
            'comment': ipaddr_line[4], 'name':ipaddr_line[3]}
    else:
        ipaddr_comments[ipaddr_line[0]]= {}
        ipaddr_comments[ipaddr_line[0]][ipaddr_line[1]] = {
            'comment': ipaddr_line[4], 'name':ipaddr_line[3]}
#    try: 
#        if ipaddr_comments.has_key(ipaddr_line[0]):
#            #ipaddr_comments[ipaddr_line[0]][ipaddr_line[1]] = {
#            #    'comment': ipaddr_line[4], 'name':ipaddr_line[3]}
#            ipaddr_comments[ipaddr_line[0]][ipaddr_line[1]].append(ipaddr_line[3])
#            ipaddr_comments[ipaddr_line[0]][ipaddr_line[1]].append(ipaddr_line[4])
#        else:
#            ipaddr_comments[ipaddr_line[0]]= {}
#            #ipaddr_comments[ipaddr_line[0]][ipaddr_line[1]] = {
#            #    'comment': ipaddr_line[4], 'name':ipaddr_line[3]}
#            ipaddr_comments[ipaddr_line[0]][ipaddr_line[1]].append(ipaddr_line[3])
#            ipaddr_comments[ipaddr_line[0]][ipaddr_line[1]].append(ipaddr_line[4])
#    except:
#        continue

ipaddr_file_handle.close()
'''

# 从配置文件提取配置字典
info_conf_instance = HandleInfo()
info_conf_file_handle = file(config.IMPORT_DATA_PATH + 'info.conf', 'r')
info_conf_content = info_conf_file_handle.read()  # 把info的配置读成一行字符串
info_conf_file_handle.close()
info_conf = info_conf_instance.analyInfo(info_conf_content.split('}\r\n}\r\n'))

# 创建类实例对象
t1 = NetworkManager(cms_ip=config.CMS_ADDRESS, name_value = config.NAME_VALUE,
                    cms_user=config.CMS_USER, cms_passwd=config.CMS_PASSWD)
t2 = DhcpManager(cms_ip=config.CMS_ADDRESS,
                 cms_user=config.CMS_USER, cms_passwd=config.CMS_PASSWD)


# setup 2:遍历配置字典，创建配置中的网络及网络中包含的资源（地址池、固定地址）
loger("####begin creat network and dhcpresource####")
for subnet in info_conf:
    # setup 2-1:创建网络，创建时匹配网络备注列表，result_network用于判断是否需要创建网络中的dhcp资源
    result_network = True
    network = str(IPy.IP(subnet).make_net(info_conf[subnet]['subnet_mask']))
    try:
        comment = network_comments[network]['comment']
    except:
        comment = 'none'

    return_code = t1.creatNetwork(
        [network], owners=config.NETWORK_OWNERS, attrs=[comment])

    if return_code == 200:
        loger("creat network %s %s success" % (network, comment))
    else:
        loger("creat network %s %s failed and the return_code is %s" %
              (network, comment, return_code))
        result_network = False
    time.sleep(0.3)
    # setup 2-2:创建地址池及固定地址
    # setup 2-2-1:分析提取地址池配置参数
    if info_conf[subnet].has_key('routers'):
        routers = map(lambda x: re.sub(',', '', x),
                      info_conf[subnet]['routers'])
    else:
        routers = []
    if info_conf[subnet].has_key('domain-name-servers'):
    #    domain_name_servers = map(lambda x: re.sub(
    #        ',', '', x), info_conf[subnet]['domain-name-servers'])
    #else:
        domain_name_servers = info_global_conf['domain_name_servers']
    if info_conf[subnet].has_key('acls'):
        acls = map(lambda x: total_acls[x], info_conf[subnet]['acls'])
    else:
        acls = ['any']
    if info_conf[subnet].has_key('default_lease_time'):
        lease_time = info_conf[subnet]['default_lease_time']
    else:
        lease_time = info_global_conf['default_lease_time']
    if info_conf[subnet].has_key('netbios-name-servers'):
        options = [{'space': 'IPv4$DHCP',
                    'name': 'netbios-name-servers;44;array of ip-address',
                    'value': info_conf[subnet]['netbios-name-servers'][0],
                    'vendorid': '',
                    'clientid': '',
                    'force': False}]

    elif info_conf[subnet].has_key('vendor-class-identifier'):
        options = [{'space': 'IPv4$DHCP',
                    'name': 'vendor-class-identifier;60;string',
                    'value': info_conf[subnet]['vendor-class-identifier'][0].replace('"',''),
                   # 'source_match':'option60',
                    'vendorid': '',
                    'clientid': '',
                    'force': False}]

        options.append({'space': 'IPv4$DHCP',
                    'name': 'vendor-encapsulated-options;43;string',
                    'value': info_conf[subnet]['vendor-encapsulated-options'][0].replace('"',''),
                  #  'source_match':'option60',
                    'vendorid': '',
                    'clientid': '',
                    'force': False})
    else :
        options = []
    #如果是IP电话则需要如下option
    options = [{'space': 'IPv4$DHCP',
                'name': 'phone_option;150;array of ip-address',
                'value': '10.227.132.6,10.227.133.6',
                #'source_match':'option60',
                'vendorid': '',
                'clientid': '',
                'force': False}]


    if result_network == True:
        # setup 2-2-2:创建地址池
        if info_conf[subnet].has_key('pools'):
            for j in info_conf[subnet]['pools']:
                return_code = t2.creatDynamicPool(
                    network, config.POOL_OWNER, j[0], j[1], routers, domain_name_servers, lease_time=lease_time, acls=acls, options=options)
                if return_code == 200:
                    loger("creat pool %s-%s of %s success" %
                          (j[0], j[1], network))
                else:
                    loger("creat pool %s-%s of %s failed and the return_code is %s" %
                          (j[0], j[1], network, return_code))
                time.sleep(0.2)
        # setup 2-2-3:创建固定地址
        if info_conf[subnet].has_key('hosts'):
            for k in info_conf[subnet]['hosts']:

                #if ipaddr_comments.has_key(subnet):
                #    if k[0] in ipaddr_comments[subnet]:
                #       comment = list(ipaddr_comments[subnet][k[0]].values())
                comment = ''

                if k[1] == '00:00:00:00:00:00':
                    return_code = t2.creatReservedPool(
                        network, config.POOL_OWNER, k[0], k[0], attrs=[comment])                
                    if return_code == 200:
                        loger("creat Reserved pool %s==>%s of %s success" %
                             (k[0], k[0], network))
                    else:
                        loger("creat Reserved pool %s==>%s of %s failed and the return_code is %s" %
                             (k[0], k[0], network, return_code))
                    time.sleep(0.2)
                else:
                    return_code = t2.creatStaticPool(
                        network, config.POOL_OWNER, k[0], k[1], routers, domain_name_servers, lease_time, options=options, attrs=[comment])
                    if return_code == 200:
                        loger("creat static pool %s==>%s of %s success" %
                             (k[0], k[1], network))
                    else:
                        loger("creat static pool %s==>%s of %s failed and the return_code is %s" %
                             (k[0], k[1], network, return_code))
                    time.sleep(0.2)
