# -*- coding: utf-8 -*-
# Copyright (c) 2015 hustlibraco
# MIT license
# 
import json
import urllib2
import zlib
import re
import subprocess
import time
import msvcrt

def main():
    try:
        url = 'http://www.ishadowsocks.com'
        headers = { 
            'Host':'www.ishadowsocks.com',
            'Connection':'keep-alive',
            'Cache-Control':'max-age=0',
            'Accept': 'text/html, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
            'DNT':'1',
            'Referer': 'http://www.ishadowsocks.com',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6'
        }
        req = urllib2.Request(url, headers=headers)
        res = urllib2.urlopen(req)
        html = res.read()
        if res.info().get("Content-Encoding") == "gzip":
            html = zlib.decompress(html, 16+zlib.MAX_WBITS)
        pattern = r'''<div class="col-lg-12 text-center">
                    <h4>服务器地址:([.\w]+)</h4>
                    <h4>端口:(\d+)</h4>
<h4>密码:(.+)</h4>
                    <h4>加密方式:(.+)</h4>
                    <h4>状态:<font color="green">(.+)</font></h4>
                    <h4><font color="red">注意：每6小时更换一次密码</font></h4>
                </div>'''
        m = re.search(pattern, html)
        if not m:
            print '没有取到配置'
            return
        config = m.groups() # ('us.ssserver.pw', '8989', '70668631', 'aes-256-cfb', '\xe6\xad\xa3\xe5\xb8\xb8')
        try:
            ssconfig = json.load(open("gui-config.json"))
            for i in ssconfig['configs']:
                if i['remarks'] == 'ishadowsocks':              
                    i['server'] = unicode(config[0])
                    i['server_port'] = int(config[1])
                    i['password'] = unicode(config[2])
                    i['method'] = unicode(config[3])
                    break
        except IOError:
            # 配置文件不存在，新建配置
            config = {
                'server': unicode(config[0]), 
                'server_port': int(config[1]), 
                'password': unicode(config[2]), 
                'method': unicode(config[3]),
                'remarks': u'ishadowsocks'
            }
            ssconfig = {
                "index": 0, 
                "localPort": 1080, 
                "shareOverLan": False, 
                "global": False, 
                "enabled": True, 
                "useOnlinePac": False, 
                "pacUrl": None, 
                "isDefault": False,
                "configs":[config]
            }
        
        json.dump(ssconfig, open("gui-config.json","w"))
        start = time.time()
        subprocess.call('Ss.exe')
        print 'Shadowsocks running time:%ss' % (time.time() - start)
        msvcrt.getch()

    except Exception, e:
        raise e

if __name__ == '__main__':
    main()
