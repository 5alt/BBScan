# -*- encoding: utf-8 -*-
'''
在配置 Nginx 和 Apache 的时候错误的将目录映射到了 home
主要检测bash_history
'''

from lib.common import save_user_script_result


def do_check(self, prefix):
	if prefix != "/": return
	status, headers, html_doc =self._http_request('/.bash_history')
	cur_content_type = headers.get('content-type', '')
	if status == 206 and cur_content_type.find("application/octet-stream") >= 0:
		rules = self._load_rules("./dict/linux_home.txt")
		for rule in rules:
			full_url = prefix + rule[0]
			self._enqueue_request(prefix, full_url, rule)