#!/usr/bin/env python
# coding=utf-8
import re
import json
import config
import IPy


class HandleInfo:
    def analyInfo(self, conf):
        conf_dic = {}
        for i in conf:  # 开始遍历每个subnet
            conf_tmp = map(lambda x: re.sub(';', '', x), i.split(
                '\r\n'))  # 把subet切片,此subnet的配置变成每个元素
            for j in conf_tmp:
                if 'subnet' in j:
                    subnet = j.split()[1]
                    subnet_mask = j.split()[3]
                    conf_dic[subnet] = {}
                    conf_dic[subnet]['subnet_mask'] = subnet_mask
                if 'range' in j and 'infoblox-range' not in j:
                    start_ip = j.split()[1]
                    end_ip = re.sub(';', '', j.split()[2])
                    if 'pools' not in conf_dic[subnet]:
                        conf_dic[subnet]['pools'] = []
                        conf_dic[subnet]['pools'].append((start_ip, end_ip))
                    else:
                        conf_dic[subnet]['pools'].append((start_ip, end_ip))
                if 'host' in j:
                    host_ip = j.split()[1]
                    host_ip_index = conf_tmp.index(j)
                    host_mac = conf_tmp[host_ip_index + 2].split()[2]
                    if 'hosts' not in conf_dic[subnet]:
                        conf_dic[subnet]['hosts'] = []
                        conf_dic[subnet]['hosts'].append((host_ip, host_mac))
                    else:
                        conf_dic[subnet]['hosts'].append((host_ip, host_mac))
                if 'default-lease-time' in j:
                    default_lease_time = j.split()[1]
                    conf_dic[subnet]['default_lease_time'] = default_lease_time
                if 'min-lease-time' in j:
                    min_lease_time = j.split()[1]
                    conf_dic[subnet]['min_lease_time'] = min_lease_time
                if 'max-lease-time' in j:
                    max_lease_time = j.split()[1]
                    conf_dic[subnet]['max_lease_time'] = max_lease_time
                if 'option' in j:
                    option_list = j.split()
                    option_name = option_list[1]
                    option_value = option_list[option_list.index(
                        option_name) + 1:]
                    conf_dic[subnet][option_name] = option_value
                if 'allow members of' in j:
                    acl_name = j.split()[-1].replace('"', '')
                    if 'acls' not in conf_dic[subnet]:
                        conf_dic[subnet]['acls'] = []
                        conf_dic[subnet]['acls'].append(acl_name)
                    else:
                        conf_dic[subnet]['acls'].append(acl_name)
        return conf_dic


if __name__ == '__main__':
    # 把最原始的zp.txt进行初步处理,删除了空行以及一些没有意义的内容
    f = file(config.IMPORT_DATA_PATH + 'info.conf', 'r')
    conf_content = f.read()  # 把info的配置读成一行字符串
    f.close()
    # 把每个subnet的配置切片,每个元素是一行完整字符串,就是这个subnet的所有配置
    conf_content_list = conf_content.split('}\r\n}\r\n')
    t = HandleInfo()
    result = t.analyInfo(conf_content_list)
    
    #输出存在固定地址的网络
    #for subnet in result:
    ##    if result[subnet].has_key('hosts'):
    #        #network = str(IPy.IP(subnet).make_net(result[subnet]['subnet_mask']))
    #        print  subnet

    print json.dumps(result)
