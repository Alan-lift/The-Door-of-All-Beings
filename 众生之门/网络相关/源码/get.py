import argparse
import ipaddress as ipaq
import json
import os
import socket
import sys
import time

import log
import 加密

listen_port = 9999
listen_host = ''
wait = 30
head = "网络连接器"
ip_file = './IP_Errors.json'
message_file = './Message.json'

class main:
	def __init__(self):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind((listen_host, listen_port))
		self.server_socket.settimeout(wait)
		self.ip_file = ip_file
		self.message_file = message_file
		# 初始化黑名单文件（避免首次读取报错）
		self._init_ip_file()
		self.get()
	
	def _init_ip_file(self):
		"""初始化IP黑名单文件"""
		if not os.path.exists(self.ip_file):
			log.log(head, "初始化黑名单")
			with open(self.ip_file, 'w') as f:
				f.write(json.dumps([]))
	
	def get(self):
		# 改为循环而非递归，避免栈溢出
		while True:
			try:
				data, client_addr = self.server_socket.recvfrom(1024)
				client_ip = client_addr[0]
				log.log(head, f'{client_addr}想要连接')
				# 1. 客户端IP在黑名单，直接跳过
				if self.is_ip_in_blacklist(client_ip):
					log.log(head, f"{client_ip}在黑名单中")
					continue
				
				# 2. 数据解码
				data = data.decode('utf-8', errors='ignore')
				print(f"收到数据：{data}")
				
				# 3. 解析JSON
				try:
					data: dict = json.loads(data)
				except json.decoder.JSONDecodeError:
					print("JSON解析失败，跳过")
					continue
				
				# 4. 校验必填字段
				required_fields = ['head', 'version', 'time', 'IP', 'message', "explor", "to", "back"]
				if not all(field in data for field in required_fields):
					log.log(head, f"{client_ip}的信息缺少必要字段")
					continue
				
				# 5. 加密验证
				temp = str((self.get_ip(), listen_port))
				if not 加密.验证(temp, data['to']):
					log.log(head, f'{client_ip}的信息加密验证失败')
					continue
				
				# 6. 时间戳校验
				if data['time'] != int(time.time() / 100):
					log.log(head, f'{client_ip}的信息时间戳错误')
					continue
				
				# 7. 消息中的IP不在黑名单 且 版本号正确，才保存
				if not self.is_ip_in_blacklist(data['IP']) and data['version'] == '4.0.0':
					print('即将写入')
					self.Message(message=data['message'],
					             client_ip=client_ip,
					             explor=data['explor'],
					             back=data['back'])
				else:
					log.log(head, f'{client_ip}的信息在黑名单 或 版本号不正确')
					
			except socket.timeout:
				# 超时后继续循环，而非递归
				continue
			except KeyboardInterrupt:
				# 捕获Ctrl+C，优雅退出
				print("\n服务器退出")
				self.server_socket.close()
				sys.exit(0)
			except Exception as e:
				# 捕获其他异常，避免程序崩溃
				print(f"处理数据出错：{e}")
				continue
	
	@staticmethod
	def is_valid_ip(ip_str):
		try:
			ipaq.ip_address(ip_str)
			return True
		except ValueError:
			return False
	
	def is_ip_in_blacklist(self, ip):
		# 先验证IP格式，非法IP直接视为不在黑名单
		if not self.is_valid_ip(ip):
			return False
		
		try:
			with open(self.ip_file, 'r') as f:
				ips = json.loads(f.read())
			return ip in ips
		except Exception as e:
			print(f"读取黑名单失败：{e}")
			return False
	
	def Message(self, message, explor, client_ip, back):
		text = {'message': message, 'explor': explor, 'client_ip': client_ip, 'back': back}
		print(f"尝试保存消息：{text}")
		
		# 确保消息文件所在目录存在（比如目录被删除的情况）
		msg_dir = os.path.dirname(self.message_file)
		if msg_dir and not os.path.exists(msg_dir):
			os.makedirs(msg_dir, exist_ok=True)
			print(f"创建消息文件目录：{msg_dir}")
		
		try:
			# 方案：先读取（若文件不存在/损坏则初始化），再写入
			data_list = []
			# 1. 读取原有数据（容错）
			if os.path.exists(self.message_file):
				try:
					with open(self.message_file, 'r', encoding='utf-8') as f:
						content = f.read().strip()
						if content:  # 非空才解析
							data_list = json.loads(content)
						else:
							data_list = []
				except json.JSONDecodeError as e:
					print(f"Message.json格式损坏，重置为空列表：{e}")
					data_list = []
				except PermissionError:
					print(f"权限不足：无法读取{self.message_file}")
					return
				except Exception as e:
					print(f"读取Message.json失败：{type(e).__name__} - {e}")
					return
			
			# 2. 追加新数据
			data_list.append(text)
			
			# 3. 写入文件（用w模式，避免r+的指针问题）
			try:
				with open(self.message_file, 'w', encoding='utf-8') as f:
					# ensure_ascii=False：支持中文；indent=2：格式化，便于查看
					json.dump(data_list, f, ensure_ascii=False, indent=2)
				print(f"✅ 消息写入成功，当前累计{len(data_list)}条")
			except PermissionError:
				print(f"❌ 权限不足：无法写入{self.message_file}（请检查文件是否被占用/目录权限）")
			except OSError as e:
				print(f"❌ 系统错误：{e}（可能磁盘满/路径不存在）")
			except Exception as e:
				print(f"❌ 写入Message.json失败：{type(e).__name__} - {e}")
		
		except Exception as e:
			print(f"❌ 处理消息时总异常：{type(e).__name__} - {e}")
	
	def get_ip(self):
		"""获取本地IP，增加异常处理"""
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(('8.8.8.8', 80))
			ip = s.getsockname()[0]
			s.close()
			return ip
		except Exception as e:
			print(f"获取本地IP失败：{e}")
			return '0.0.0.0'

True_False=False
def _():
	global listen_port
	global True_False
	global message_file
	
	def validate_port(value):
		"""验证端口号是否有效"""
		port = int(value)
		if not 1 <= port <= 65535:
			raise argparse.ArgumentTypeError(f"必须在 1-65535 之间")
		return port
	
	def path(value):
		# 1. 基础校验：非字符串/空路径直接判定为不合法
		if not isinstance(path, str) or path.strip() == "":
			raise argparse.ArgumentTypeError(f"路径不能为空或非字符串类型: {path}")
		
		try:
			# 2. 规范化路径（处理相对路径、../、./ 等）
			normalized_path = os.path.normpath(path)
			
			# 3. 检查操作系统非法字符（Windows特有）
			if sys.platform == 'win32':
				illegal_chars = '<>:"/\\|?*'
				if any(char in normalized_path for char in illegal_chars):
					raise argparse.ArgumentTypeError(
						f"Windows路径包含非法字符 ({illegal_chars}): {normalized_path}"
					)
			
			# 4. 提取文件的父目录路径
			parent_dir = os.path.dirname(normalized_path)
			
			# 5. 父目录不存在则创建（递归创建多级目录）
			if parent_dir and not os.path.exists(parent_dir):
				os.makedirs(parent_dir, exist_ok=True)
			
			# 6. 返回规范化后的合法路径
			return normalized_path
		
		except argparse.ArgumentTypeError:
			# 主动抛出的参数错误直接向上传递
			raise
		except (ValueError, TypeError, OSError) as e:
			# 其他路径相关异常包装为ArgumentTypeError
			raise argparse.ArgumentTypeError(f"路径语法不合法: {path}, 错误原因: {str(e)}")
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--port',
	                    type=validate_port,
	                    required=False,
	                    help='服务器端口号 (1-65535)')
	parser.add_argument('-P', '--Print',
	                    type=bool,
	                    required=False,
	                    help='')
	parser.add_argument('-f', '--file',
	                    type=path,
	                    required=False,
	                    help='保存地址')
	args = parser.parse_args()
	listen_port = args.port if args.port else 9999
	True_False = args.Print if args.Print else False
	message_file = args.file if args.file else './Message.json'

if __name__ == '__main__':
	_()
	if not True_False:
		def print(*args):
			pass
	main()