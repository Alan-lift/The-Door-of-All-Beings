import os
import time

encoding='utf-8'

def log(title:str, message, explore="No explore", ip='xxxx', error: int = 1):
	"""
	:param title: 日志标题
	:param message: 日志内容
	:param explore: 日志扩展内容
	:param ip: 日志来自的程序位置编码
	:param error: 如果有错误那么错误等级(1最轻,可以忽略;10最严重)
	:return: None
	"""
	if title.upper() == 'ERROR':
		title = f'{title.upper()} -- {error}'
	else:
		title = title.upper()
	
	temp_text =f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] [{title}] [{ip}] [{message}] \n{explore}'
	
	try:
		with open(f'./logs/{time.strftime("%Y-%m-%d")}.log', 'a', encoding=encoding) as f:
			f.write(temp_text)
			f.flush()
	except FileNotFoundError:
		os.mkdir('./logs')
		with open(f'./logs/{time.strftime("%Y-%m-%d")}.log', 'a', encoding=encoding) as f:
			f.write(temp_text)
			f.flush()

