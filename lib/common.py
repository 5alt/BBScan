#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
#  Common functions
#

import time
import urlparse
import re
import os


def print_msg(msg):
    print '[%s] %s' % (time.strftime('%H:%M:%S', time.localtime()), msg)


def parse_url(url):
    _ = urlparse.urlparse(url, 'http')
    if not _.netloc:
        _ = urlparse.urlparse('http://' + url, 'http')
    return _.scheme, _.netloc, _.path if _.path else '/'


def decode_response_text(txt, charset=None):
    if charset:
        try:
            return txt.decode(charset)
        except:
            pass

    for _ in ['UTF-8', 'GB2312', 'GBK', 'iso-8859-1', 'big5']:
        try:
            return txt.decode(_)
        except:
            pass

    try:
        return txt.decode('ascii', 'ignore')
    except:
        pass

    raise Exception('Fail to decode response Text')


# calculate depth of a given URL, return tuple (url, depth)
def cal_depth(self, url):
    if url.find('#') >= 0:
        url = url[:url.find('#')]  # cut off fragment
    if url.find('?') >= 0:
        url = url[:url.find('?')]  # cut off query string

    if url.startswith('//'):
        return '', 10000  # //www.baidu.com/index.php

    if not urlparse.urlparse(url, 'http').scheme.startswith('http'):
        return '', 10000  # no HTTP protocol

    if url.lower().startswith('http'):
        _ = urlparse.urlparse(url, 'http')
        if _.netloc == self.host:  # same hostname
            url = _.path
        else:
            return '', 10000  # not the same hostname

    while url.find('//') >= 0:
        url = url.replace('//', '/')

    if not url:
        return '/', 1  # http://www.example.com

    if url[0] != '/':
        url = '/' + url

    url = url[: url.rfind('/') + 1]

    if url.split('/')[-2].find('.') > 0:
        url = '/'.join(url.split('/')[:-2]) + '/'

    depth = url.count('/')
    return url, depth


def save_user_script_result(self, status, url, title):
    self.lock.acquire()
    #print '[+] [%s] %s' % (status, url)
    if url not in self.results:
        self.results[url] = []
    _ = {'status': status, 'url': url, 'title': title}
    self.results[url].append(_)
    self.lock.release()


def get_domain_sub(host):
    if re.search('\d+\.\d+\.\d+\.\d+', host.split(':')[0]):
        return ''
    else:
        return host.split('.')[0]

def check_server(rsp_server):
    if not rsp_server: return 'unknown'

    rsp_server = rsp_server.lower()

    common_server = ['iis', 'tomcat', 'nginx', 'apache', 'tengine', 'express']
    for s in common_server:
        if s in rsp_server:
            return s

    return 'unknown'

def check_lang(base_url, rsp_headers):
    '''
    :param url: 扫描站点的一个url
    :return: php python nodejs unknown
    '''
    # dectect webserver

    # 通过session名比较
    # laravel_session 是laravel的session
    # ci_session 是CI的
    php_session = [('php', 'phpsessid'), ('ci', 'ci_session'), ('cakephp','cakephp'), ('laravel', 'laravel_session')]
    cookies =  rsp_headers.get('set-cookie', '').lower()
    for (n, s) in php_session:
        if s in cookies:
            return 'php', n

    # 通过x-powered-by比较
    rsp_powerby = rsp_headers.get('x-powered-by', '').lower()
    if 'php' in rsp_powerby:
        return 'php', 'php'

    if 'express' in rsp_powerby:
        return 'nodejs', 'express'

    # 不能分辨的最后判断
    if 'nodesess' in cookies:
        return 'nodejs', 'nodejs'
    
    # 区分php java other
    # 通过server比较
    rsp_server = rsp_headers.get('server', '').lower()

    if rsp_server:
        # 有待考证
        python_server = ['tornado', 'wsgi', 'flask', 'django', 'werkzeug', 'gunicorn', 'gevent', 'python']
        for s in python_server:
            if s in rsp_server:
                return 'python', s

        java_server = ['jetty', 'tomcat', 'coyote', 'jboss', 'glassfish', 'wildfly', 'tomee', 'geronimo', 'jonas', 'resin', 'blazix']
        for s in java_server:
            if s in rsp_server:
                return 'java', s

        iis_server = ['iis', 'microsoft'] # asp 没有url重新的情况，上面已经做判断
        for s in iis_server:
            if s in rsp_server:
                return 'aspx', 'unknown'

        r = requests.get(base_url + '/index.php')
        rb = requests.get(base_url)
        # 通过加index.php和不加index.php比较
        if difflib.SequenceMatcher(None, rb.text, r.text).ratio() > 0.9 and r.status_code == rb.status_code:
            return 'php', 'php'

        if 'apache' in rsp_server: # python/nodejs 等一定不是apache，只可能是静态或者java或者php，不管静态
            return 'java', 'unknown'

        # nginx 经常作为cdn，判断出错概率大

    return 'unknown', 'unknown'

def check_lang_url(url):
    parts = urlparse.urlparse(url)
    path = parts.path
    ext = os.path.splitext(path)[1]
    if ext:
        if ext in ['.do', '.action']:
            return 'java'
        if ext in ['.php']:
            return 'php'
        if ext in ['.asp']:
            return 'asp'
        if ext in ['.aspx']:
            return 'aspx'
    return 'unknown'


def check_rewrite(server, lang):
    if lang in ['java', 'python', 'nodejs']:
        return True

    if server not in ['apache', 'nginx', 'tengine', 'iis']:
        return True

    return False
