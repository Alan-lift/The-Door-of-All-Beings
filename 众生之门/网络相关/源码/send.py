import argparse
import json
import socket
import sys
import time
import log
import 加密

TIMEOUT = 2
head = "网络连接器"

def print(*args):
	pass

global_config = {
    'server_address': '',      # IP地址
    'port': 9999,          # 端口号
    'message': '',             # 消息内容
    'explor': 'No explor',            # 扩展信息
	'back':9999
}

class main:
	def __init__(self):
		self.sock = None
		self.ip = self.get_local_ip()
		self.init_socket()
	
	def init_socket(self):
		"""初始化套接字（支持重连）"""
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.sock.settimeout(TIMEOUT)
			log.log(head, "套接字创建成功")
		except Exception as e:
			log.log("error", f"[{head}]",f"创建UDP套接字失败：{str(e)}")
			self.sock = None
	
	def send_data(self, data, SERVER_ADDR):
		"""发送数据（JSON格式）"""
		if not self.sock:
			log.log("error", f"[{head}]","套接字未初始化，发送失败", error=10)
			return False
		try:
			# 转换为JSON字符串发送（替代字符串化字典）
			json_data = json.dumps(data, ensure_ascii=False)
			self.sock.sendto(json_data.encode('utf-8'), SERVER_ADDR)
			print("发送", f"向{SERVER_ADDR}发送：{json_data}")
			return True
		except Exception as e:
			log.log("error",f'[{head}]', f"发送数据失败：{str(e)}")
			return False
	
	def get_local_ip(self):
		"""获取本地IP地址（用于发送给服务器）"""
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(('8.8.8.8', 80))
			self.ip = s.getsockname()[0]
			s.close()
			print(f'获取IP:{self.ip}')
			log.log(head, '获取本地IP成功')
			return self.ip
		except Exception as e:
			log.log("error", f"[{head}]",f"获取本地IP失败：{str(e)}", error=10)
			return False
	
	def send(self):
		try:
			to = (global_config['server_address'], global_config['port'])
			if self.ip != False:
				to_ = 加密.加密(str(to))
				self.send_data({
					'head': 'from Out Pet App',
					'version': '4.0.0',
					'time': int(time.time() / 100),
					'IP': self.ip,
					'message': global_config['message'],
					'explor': global_config['explor'],
					"to": to_,
					"back": global_config['back']
				},
					to)
				log.log(head, "发送信息成功")
		except Exception as e:
			log.log('error', f"[{head}]", explore=e,error=10 )
			sys.exit(1)
		sys.exit(0)

def parse_arguments_strict():
	"""带验证的参数解析"""
	
	def validate_port(value):
		"""验证端口号是否有效"""
		port = int(value)
		if not 1 <= port <= 65535:
			raise argparse.ArgumentTypeError(f"端口号必须在 1-65535 之间")
		return port
	
	def validate_ip(value):
		"""简单验证IP地址格式"""
		if not value.replace('.', '').isdigit():
			raise argparse.ArgumentTypeError(f"无效的IP地址格式")
		parts = value.split('.')
		if len(parts) != 4:
			raise argparse.ArgumentTypeError(f"IP地址必须有4个部分")
		return value
	
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-i', '--ip',
	                    type=validate_ip,
	                    required=True,
	                    help='服务器IP地址 (例如: 192.168.1.100)')
	
	parser.add_argument('-p', '--port',
	                    type=validate_port,
	                    required=False,
	                    help='服务器端口号 (1-65535)')
	
	parser.add_argument('-m', '--message',
	                    required=True,
	                    help='消息内容')
	
	parser.add_argument('-e', '--explor',
	                    required=False,
	                    help='扩展信息')
	parser.add_argument('-b', '--back',
	                    type=validate_port,
	                    required=False,
	                    help='返回端口')
	
	try:
		args = parser.parse_args()
		
		# 保存到全局变量
		global_config['server_address'] = args.ip
		global_config['port'] = args.port if args.port else 9999
		global_config['message'] = args.message
		global_config['explor'] = args.explor if args.explor else 'No explor'
		global_config['back'] = args.back if args.back else 9999
		
		print(global_config)
		log.log(head, f"解读网络信息成功", f"{global_config}")
		return True
	
	except SystemExit:
		# 参数错误，程序退出
		sys.exit(1)

if __name__ == '__main__':
	parse_arguments_strict()
	main().send()