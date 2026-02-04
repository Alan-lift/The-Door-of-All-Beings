import gc
import json
import os
import sys
import time
import traceback
from typing import *
from typing import Optional

import ursina

import log
import path_right

# ---------------- 路径配置（统一以运行文件为基准） ----------------
RUN_FILE_PATH = sys.argv[0]
RUN_DIR = os.path.dirname(os.path.abspath(RUN_FILE_PATH))
config = os.path.normpath(os.path.join(RUN_DIR, "./config/"))
UserConfig = os.path.normpath(os.path.join(RUN_DIR, "./USERCONFIG/"))


# ---------------- 自定义异常 ----------------
class ConfigPathNotError(Exception):
	"""配置文件无法读取异常"""
	pass


class FontFileIsForgetError(Exception):
	"""字体文件不存在异常"""
	pass


class UserConfigFileError(Exception):
	"""用户配置文件内容错误异常"""
	pass


class JsonParseError(Exception):
	"""JSON配置解析失败异常"""
	pass


# ---------------- 字体路径获取函数 ----------------
def font(head='字体管理器'):
	"""
	从配置文件读取字体路径（所有相对路径以运行文件为基准）
	:return: 有效字体文件绝对路径字符串
	:raise: 各类自定义异常
	"""
	# 1. 拼接配置文件路径
	font_config = os.path.normpath(os.path.join(config, 'font.json'))
	user_font = os.path.normpath(os.path.join(UserConfig, "font.bin"))
	
	# 2. 读取全局字体配置文件（font.json）
	if not path_right.is_file_exists(font_config):
		log.log('error', f'[{head}]',
		        f"ConfigPathNotError\n\tThe config file [{font_config}] cannot be read (file not exists)",
		        error=10)
		raise ConfigPathNotError(f"The config file [{font_config}] cannot be read (file not exists)")
	
	try:
		with open(font_config, "r", encoding="utf-8") as f:
			font_dict: dict = json.load(f)
	except json.JSONDecodeError as e:
		log.log('error', f'[{head}]',
		        f"json.JSONDecodeError\n\tFailed to parse [{font_config}] | JSON error: {str(e)}",
		        error=10)
		raise JsonParseError(f"Failed to parse [{font_config}] | JSON error: {str(e)}")
	except Exception as e:
		log.log('error', f'[{head}]',
		        f"ConfigPathNotError\n\tFailed to read [{font_config}] | Error: {str(e)}",
		        error=10)
		raise ConfigPathNotError(f"Failed to read [{font_config}] | Error: {str(e)}")
	
	# 3. 处理用户字体配置（font.bin）
	path = None
	if path_right.is_file_exists(user_font):
		try:
			with open(user_font, "r", encoding="utf-8") as f:
				f_read = f.read().strip()
		except Exception as e:
			log.log('error', f'[{head}]',
			        f"UserConfigFileError\n\tFailed to read user config [{user_font}] | Error: {str(e)}",
			        error=10)
			raise UserConfigFileError(f"Failed to read user config [{user_font}] | Error: {str(e)}")
		
		if f_read in ['1', '2', '3']:
			if f_read not in font_dict:
				log.log('error', f'[{head}]',
				        f"UserConfigFileError\n\tUser config value [{f_read}] not found in [{font_config}]",
				        error=10)
				raise UserConfigFileError(f"User config value [{f_read}] not found in [{font_config}]")
			path = font_dict[f_read]
			print(f"User selected font path: {path}")
		else:
			log.log('error', f'[{head}]',
			        f"UserConfigFileError\n\tUser config [{user_font}] value is invalid: [{f_read}] (must be '1'/'2'/'3')",
			        error=10)
			raise UserConfigFileError(f"User config [{user_font}] value is invalid: [{f_read}] (must be '1'/'2'/'3')")
	else:
		# 用户配置不存在时，使用默认字体（取font.json中第一个值）
		if not font_dict:
			log.log('error', f'[{head}]',
			        f"ConfigPathNotError\n\tFont config [{font_config}] is empty (no default font)",
			        error=10)
			raise ConfigPathNotError(f"Font config [{font_config}] is empty (no default font)")
		default_key = next(iter(font_dict.keys()))
		path = font_dict[default_key]
		print(f"User config [{user_font}] not found, use default font: {path}")
	
	# 4. 校验并转换为绝对路径（核心：统一以运行文件为基准）
	if not path:
		log.log('error', f'[{head}]',
		        f"FontFileIsForgetError\n\tFont path is empty (no config matched)",
		        error=10)
		raise FontFileIsForgetError("Font path is empty (no config matched)")
	
	# 转换为绝对路径（以运行文件目录为基准）
	abs_font_path = os.path.normpath(os.path.join(RUN_DIR, path)) if not os.path.isabs(path) else path
	if not path_right.is_file_exists(abs_font_path):
		log.log('error', f'[{head}]',
		        f"FontFileIsForgetError\n\tThe font file [{abs_font_path}] does not exist (original path: {path})",
		        error=10)
		raise FontFileIsForgetError(f"The font file [{abs_font_path}] does not exist (original path: {path})")
	
	# 5. 返回有效绝对路径
	return abs_font_path


# ---------------- Text 类（继承Ursina.Text并修复重复创建问题） ----------------
class Text(ursina.Text):
	# 基础配置
	DEFAULT_SIZE = 0.025
	DEFAULT_FONT = 'C:/Users/Alan_/PycharmProjects/众生之门/main/assets/font/msyh.ttc'  # 兜底字体
	START_TAG = '<'
	END_TAG = '>'
	HEAD = 'Text管理器'
	
	def __init__(self,
	             text: str = '',
	             start_tag: Optional[str] = None,
	             end_tag: Optional[str] = None,
	             ignore: bool = True,
	             **kwargs):
		# 初始化核心属性
		self.head = self.HEAD
		self.ID = int(time.time() * 1000)
		self.update_task = None
		self.state = "wait"
		self._destroyed = False
		
		# 处理默认标签
		start_tag = start_tag or self.START_TAG
		end_tag = end_tag or self.END_TAG
		
		# 日志标准化
		init_params = {
			"text": text,
			"start_tag": start_tag,
			"end_tag": end_tag,
			"ignore": ignore,
			"other_kwargs": kwargs
		}
		log.log("info", f"[{self.head}]", f"ID:{self.ID} 开始新建Text组件 | 参数:{init_params}")
		
		try:
			# 获取字体路径
			font_path = self._get_font_path()
			
			# 构建传递给父类的参数
			parent_kwargs = {
				"text": text,
				"start_tag": start_tag,
				"end_tag": end_tag,
				"ignore": ignore,
				"font": font_path,
				"size": self.DEFAULT_SIZE
			}
			
			# 合并额外参数
			for key, value in kwargs.items():
				if key not in parent_kwargs:
					parent_kwargs[key] = value
			
			# 只调用一次父类构造函数
			super().__init__(**parent_kwargs)
			log.log("info", f"[{self.head}]", f"ID:{self.ID} 新建Text组件成功 | 使用字体:{font_path}")
		
		except Exception as e:
			# 如果字体路径获取失败，尝试使用基本参数创建
			log.log("warning", f"[{self.head}]",
			        f"ID:{self.ID} 使用自定义字体失败，尝试使用默认参数 | 错误:{str(e)}")
			
			try:
				# 尝试不带font参数创建
				basic_kwargs = {
					"text": text,
					"start_tag": start_tag,
					"end_tag": end_tag,
					"ignore": ignore,
					"size": self.DEFAULT_SIZE
				}
				basic_kwargs.update(kwargs)
				super().__init__(**basic_kwargs)
			except Exception as e2:
				# 最后尝试：只使用text参数
				log.log("error", f"[{self.head}]",
				        f"ID:{self.ID} 使用默认参数也失败，尝试最小化创建 | 错误:{str(e2)}")
				super().__init__(text=text, **kwargs)
	
	def _get_font_path(self) -> str:
		"""获取字体路径（统一基准+容错+兜底）"""
		try:
			# 调用外部font函数
			font_path = font(head=self.HEAD)
			if not font_path:
				log.log("warning", f"[{self.head}]", f"font()函数返回空路径，使用兜底字体: {self.DEFAULT_FONT}")
				return self.DEFAULT_FONT
			
			# 二次校验：确保路径有效
			if path_right.is_file_exists(font_path):
				log.log("info", f"[{self.head}]", f"字体路径解析成功 | 最终路径:{font_path}")
				return font_path
			else:
				log.log("warning", f"[{self.head}]", f"字体路径无效 [{font_path}]，使用兜底字体: {self.DEFAULT_FONT}")
				return self.DEFAULT_FONT
		
		except Exception as e:
			# 捕获所有异常，使用兜底字体
			log.log("error", f"[{self.head}]",
			        f"调用font()函数失败 | 错误:{traceback.format_exc()}，使用兜底字体: {self.DEFAULT_FONT}", error=2)
			return self.DEFAULT_FONT
	
	def update_text(self, update_text: Callable[[], str], wait_time: int = 0):
		"""动态更新文本（修复：在开始新更新前停止并清理旧任务）"""
		if self._destroyed:
			log.log("error", f"[{self.head}]", f"ID:{self.ID} 实例已销毁，禁止更新文本", error=2)
			return
		
		if not callable(update_text):
			log.log("error", f"[{self.head}]", f"ID:{self.ID} update_text必须是无参可调用函数", error=2)
			return
		
		if wait_time < 0:
			log.log("warning", f"[{self.head}]", f"ID:{self.ID} 等待时间不能为负，已重置为0", error=0)
			wait_time = 0
		
		log.log("info", f"[{self.head}]", f"ID:{self.ID} 设置文本自动更新 | 刷新间隔:{wait_time}ms")
		
		# 关键修复：在开始新任务前，先停止并清理旧任务
		if self.state == "update" and self.update_task is not None:
			log.log("info", f"[{self.head}]", f"ID:{self.ID} 检测到已有更新任务，先停止旧任务")
			self._safe_stop_update_task()
		
		self.state = "update"
		
		def _safe_update():
			if self._destroyed:
				return
			try:
				new_text = update_text()
				self.text = str(new_text)
				log.log("debug", f"[{self.head}]", f"ID:{self.ID} 文本更新成功: {new_text}")
			except Exception as e:
				log.log("error", f"[{self.head}]", f"ID:{self.ID} 文本更新函数执行失败 | 错误:{traceback.format_exc()}",
				        error=3)
		
		if wait_time > 0:
			# 使用Sequence创建循环更新
			self.update_task = ursina.Sequence(
				ursina.Func(_safe_update),
				ursina.Wait(wait_time / 1000),
				loop=True
			)
			self.update_task.start()
			log.log("info", f"[{self.head}]", f"ID:{self.ID} 启动循环更新任务 (Sequence)")
		else:
			# 使用invoke创建立即重复更新
			self.update_task = ursina.invoke(_safe_update, delay=0, repeating=True)
			log.log("info", f"[{self.head}]", f"ID:{self.ID} 启动立即重复更新任务 (invoke)")
	
	def _safe_stop_update_task(self):
		"""安全停止更新任务，清理资源"""
		try:
			if isinstance(self.update_task, ursina.Sequence):
				self.update_task.kill()
				log.log("debug", f"[{self.head}]", f"ID:{self.ID} 已停止Sequence任务")
			elif isinstance(self.update_task, int):
				ursina.invoke.cancel(self.update_task)
				log.log("debug", f"[{self.head}]", f"ID:{self.ID} 已取消invoke任务")
			else:
				log.log("warning", f"[{self.head}]", f"ID:{self.ID} 未知的更新任务类型: {type(self.update_task)}")
		except Exception as e:
			log.log("error", f"[{self.head}]", f"ID:{self.ID} 停止更新任务时出错 | 错误:{traceback.format_exc()}",
			        error=3)
		
		self.update_task = None
	
	def stop(self):
		"""停止文本更新（增强容错）"""
		if self._destroyed:
			log.log("warning", f"[{self.head}]", f"ID:{self.ID} 实例已销毁，无需停止更新", error=0)
			return
		
		if self.state != "update" or self.update_task is None:
			log.log("warning", f"[{self.head}]", f"ID:{self.ID} 无运行中的更新任务", error=0)
			return
		
		try:
			self._safe_stop_update_task()
			self.state = "wait"
			log.log("info", f"[{self.head}]", f"ID:{self.ID} 停止文本更新成功")
		except Exception as e:
			log.log("error", f"[{self.head}]", f"ID:{self.ID} 停止更新任务失败 | 错误:{traceback.format_exc()}",
			        error=3)
	
	def delete(self):
		"""彻底删除Text组件（完善容错）"""
		if self._destroyed:
			log.log("warning", f"[{self.head}]", f"ID:{self.ID} 实例已删除，无需重复操作", error=0)
			return
		
		log.log("info", f"[{self.head}]", f"ID:{self.ID} 开始删除Text组件")
		
		try:
			self.stop()
			ursina.destroy(self)
			self._destroyed = True
			gc.collect()
			log.log("info", f"[{self.head}]", f"ID:{self.ID} 删除Text组件成功")
		
		except Exception as e:
			log.log("error", f"[{self.head}]", f"ID:{self.ID} 删除Text组件失败 | 错误:{traceback.format_exc()}",
			        error=4)
			raise e


# 测试代码 - 模拟您的问题场景
if __name__ == "__main__":
	from ursina import *
	
	app = Ursina()
	window.title = "Text更新测试 - 修复重复创建问题"
	
	# 创建背景
	Entity(model='quad', scale=(2, 2), color=color.dark_gray)
	
	print("=" * 50)
	print("测试：模拟重复调用update_text是否会产生多个文本框")
	
	# 创建文本对象
	text = Text(
		text="初始文本",
		position=(0, 0.2),
		color=color.white,
		scale=2
	)
	print(f"创建Text实例，ID: {text.ID}")
	
	counter = 0
	
	
	def update_func():
		global counter
		counter += 1
		return f"计数: {counter}"
	
	
	# 第一次调用update_text
	print("\n第一次调用update_text...")
	text.update_text(update_func, wait_time=1000)
	
	
	# 模拟5秒后再次调用（模拟重复调用）
	def test_repeat_update():
		print("\n5秒后第二次调用update_text...")
		text.update_text(update_func, wait_time=500)  # 改变更新间隔
		print("注意：这里应该只看到文本更新，而不是创建新文本框")
	
	
	# 5秒后测试重复调用
	invoke(test_repeat_update, delay=5)
	
	# 添加控制说明
	instructions = Text(
		text="测试说明：\n1. 文本应每秒更新一次\n2. 5秒后更新间隔变为500ms\n3. 不应该创建新文本框\n按 Q 停止更新\n按 W 删除文本\n按 ESC 退出",
		position=(0.7, 0.3),
		scale=0.8,
		color=color.yellow
	)
	
	
	def input(key):
		if key == 'q':
			print("\n按 Q - 停止更新")
			text.stop()
		elif key == 'w':
			print("\n按 W - 删除文本")
			text.delete()
		elif key == 'escape':
			print("\n退出程序")
			application.quit()
	
	
	camera.orthographic = True
	camera.fov = 10
	
	print("\n" + "=" * 50)
	print("屏幕上应该显示：白色动态文本(中间) + 黄色说明文本(右侧)")
	print("观察控制台输出，确认没有重复创建Text实例")
	
	app.run()