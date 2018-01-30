# -*- encoding: utf-8 -*-
'''
Nginx 在解析静态文件时，把 web-inf 目录映射进去，若没有做 nginx 相关安全配置或由
于 nginx 自身缺陷影响，将导致通过 nginx 访问到 tomcat 的 web-inf 目录。
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