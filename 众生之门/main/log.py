import time
import os
import python_

encoding='utf-8'


def log(title, message, explore="No explore", ip='xxxx', error: int = 1):
	"""
	:param title: 日志标题
	:param message: 日志内容
	:param explore: 日志扩展内容
	:param ip: 日志来自的程序位置编码
	:param error: 如果有错误那么错误等级(1最轻,可以忽略;10最严重)
	:return: None
	"""
	if title == 'error':
		title = f'{title} -- {error}'
	temp_text = f'''
[{title}]
\tdate:
\t\t{time.strftime("%Y-%m-%d %H:%M:%S")}
\t\t{time.strftime("%A-->%a")}
\t\t{time.strftime("%m=%B-->%b")}
\t\t{time.time()}
\tmessage:
\t\t{message}
\texplore:
\t\t{explore}
\tip:
\t\t{ip}
'''
	python_.print(temp_text)
