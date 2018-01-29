# -*- encoding: utf-8 -*-
'''
在配置 Nginx 和 Apache 的时候错误的将目录映射到了 /
主要检测 /etc/passwd
'''

from lib.common import save_user_script_result


def do_check(self, prefix):
	if prefix != "/": return
	#if self.lang != 'java': return
	rules = self._load_rules("./dict/java_web_inf.txt")
	
	rule = rules[0]
	full_url = prefix.rstrip('/') + rule[0]
	url_description = {'prefix': prefix, 'full_url': full_url}
	item = (url_description, rule[1], rule[2], rule[3], rule[4], rule[5], rule[6], rule[7])
	valid_item, status, headers, html_doc = self.apply_rules(item)

	if valid_item:
		for rule in rules:
			full_url = prefix + rule[0]
			self._enqueue_request(prefix, full_url, rule)