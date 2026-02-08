import os
import sys
import time
import traceback
import uuid
from typing import *
from typing import Optional

import ursina

import log

# ---------------- 路径配置（统一以运行文件为基准） ----------------
RUN_FILE_PATH = sys.argv[0]
RUN_DIR = os.path.dirname(os.path.abspath(RUN_FILE_PATH))

AlignDirection = Literal[
    'top_left', 'top_right', 'top_center',
    'bottom_left', 'bottom_right', 'bottom_center',
    'center_left', 'center_right', 'center'
]

# ---------------- 自定义异常（优化命名） ----------------
class FontFileNotFoundError(Exception):
	"""字体文件不存在异常"""
	pass


# ---------------- 路径工具函数 ----------------
def is_file_exists(file_path: str) -> bool:
	"""检查文件是否存在"""
	return os.path.isfile(file_path) and os.path.exists(file_path)


# ---------------- 核心自定义Text类 ----------------
class Text(ursina.Text):
	# 基础配置
	DEFAULT_SIZE = 0.025
	# 兜底字体：使用相对路径（优先找系统默认字体，再用相对路径）
	FALLBACK_FONTS = [
		# 系统通用字体（提高兼容性）
		'Arial.ttf',
		'SimHei.ttf',
		'msyh.ttc',
		# 相对路径兜底
		os.path.normpath(os.path.join(RUN_DIR, "./assets/font/msyh.ttc"))
	]
	START_TAG = '<'
	END_TAG = '>'
	HEAD = 'Text管理器'
	
	def __init__(self,
	             text: str = '',
	             start_tag: Optional[str] = None,
	             end_tag: Optional[str] = None,
	             ignore: bool = True,
	             font: Optional[str] = None,
	             size: Optional[float] = None,
	             **kwargs):
		# 初始化核心属性
		self.head = self.HEAD
		self.ID = str(uuid.uuid4())  # 唯一ID
		self.update_task: Optional[Union[ursina.Sequence, ursina.Invoke]] = None
		self.state = "wait"  # wait:等待状态, update:更新中
		self._destroyed = False  # 标记是否已销毁
		
		# 处理默认标签和尺寸
		start_tag = start_tag or self.START_TAG
		end_tag = end_tag or self.END_TAG
		use_size = size or self.DEFAULT_SIZE
		
		# 日志标准化
		init_params = {
			"text": text,
			"start_tag": start_tag,
			"end_tag": end_tag,
			"ignore": ignore,
			"font": font,
			"size": use_size,
			"other_kwargs": kwargs
		}
		log.log("info", f"[{self.head}]", f"ID:{self.ID} 开始新建DynamicText组件 | 参数:{init_params}")
		
		try:
			# 1. 处理字体路径（核心：公开参数 + 容错兜底）
			font_path = self._resolve_font_path(font)
			
			# 2. 构建传递给父类的参数
			parent_kwargs = {
				"text": text,
				"start_tag": start_tag,
				"end_tag": end_tag,
				"ignore": ignore,
				"font": font_path,
				"size": use_size
			}
			
			# 合并额外参数（覆盖默认值）
			parent_kwargs.update(kwargs)
			
			# 3. 调用父类构造函数
			super().__init__(**parent_kwargs)
			log.log("info", f"[{self.head}]", f"ID:{self.ID} 新建DynamicText组件成功 | 使用字体:{font_path}")
		
		except Exception as e:
			# 终极兜底：不带字体参数创建
			log.log("warning", f"[{self.head}]",
			        f"ID:{self.ID} 使用指定字体失败，尝试使用Ursina默认字体 | 错误:{str(e)}")
			try:
				basic_kwargs = {
					"text": text,
					"start_tag": start_tag,
					"end_tag": end_tag,
					"ignore": ignore,
					"size": use_size
				}
				basic_kwargs.update(kwargs)
				super().__init__(**basic_kwargs)
			except Exception as e2:
				log.log("error", f"[{self.head}]",
				        f"ID:{self.ID} 创建DynamicText组件失败 | 错误:{traceback.format_exc()}", error=4)
				raise e2
	
	def _resolve_font_path(self, font_param: Optional[str]) -> str:
		"""解析字体路径：优先使用传入的font参数，失败则使用兜底字体"""
		# 1. 如果传入了font参数，优先处理
		if font_param:
			# 转换为绝对路径（以运行文件目录为基准）
			abs_font_path = os.path.normpath(os.path.join(RUN_DIR, font_param)) if not os.path.isabs(
				font_param) else font_param
			if is_file_exists(abs_font_path):
				return abs_font_path
			log.log("warning", f"[{self.head}]",
			        f"指定的字体文件不存在 [{abs_font_path}]，尝试使用兜底字体")
		
		# 2. 尝试兜底字体列表
		for fallback_font in self.FALLBACK_FONTS:
			abs_fallback = os.path.normpath(os.path.join(RUN_DIR, fallback_font)) if not os.path.isabs(
				fallback_font) else fallback_font
			if is_file_exists(abs_fallback):
				log.log("info", f"[{self.head}]", f"使用兜底字体: {abs_fallback}")
				return abs_fallback
		
		# 3. 所有兜底都失败，抛出异常
		raise FontFileNotFoundError("所有字体路径（指定参数+兜底列表）均无效，请检查字体文件路径")
	
	def update_text(self, update_func: Callable[[], Optional[str]], update_interval: int = 0) -> None:
		"""
		启动文本自动更新
		:param update_func: 更新函数，无参数，返回需要显示的字符串
		:param update_interval: 更新间隔（毫秒），0表示每一帧自动更新
		"""
		if self._destroyed:
			log.log("error", f"[{self.head}]", f"ID:{self.ID} 实例已销毁，禁止更新文本", error=2)
			return
		
		if not callable(update_func):
			log.log("error", f"[{self.head}]", f"ID:{self.ID} update_func必须是无参可调用函数", error=2)
			return
		
		if update_interval < 0:
			log.log("warning", f"[{self.head}]", f"ID:{self.ID} 等待时间不能为负，已重置为0", error=0)
			update_interval = 0
		
		log.log("info", f"[{self.head}]", f"ID:{self.ID} 设置文本自动更新 | 刷新间隔:{update_interval}ms")
		
		# 停止旧任务（避免重复更新）
		if self.state == "update" and self.update_task is not None:
			log.log("info", f"[{self.head}]", f"ID:{self.ID} 检测到已有更新任务，先停止旧任务")
			self._safe_stop_update_task()
		
		self.state = "update"
		
		def _safe_update():
			"""安全的更新函数（包含异常捕获）"""
			if self._destroyed:
				return
			try:
				new_text = update_func()
				self.text = str(new_text) if new_text is not None else ""
				log.log("debug", f"[{self.head}]", f"ID:{self.ID} 文本更新成功: {self.text}")
			except Exception as e:
				log.log("error", f"[{self.head}]", f"ID:{self.ID} 文本更新函数执行失败 | 错误:{traceback.format_exc()}",
				        error=3)
		
		# 根据更新间隔选择不同的更新方式
		if update_interval > 0:
			# 间隔更新（毫秒转秒）
			self.update_task = ursina.Sequence(
				ursina.Func(_safe_update),
				ursina.Wait(update_interval / 1000),
				loop=True
			)
			self.update_task.start()
			log.log("info", f"[{self.head}]", f"ID:{self.ID} 启动循环更新任务 (间隔{update_interval}ms)")
		else:
			# 每一帧更新
			self.update_task = ursina.invoke(_safe_update, delay=0, repeating=True)
			log.log("info", f"[{self.head}]", f"ID:{self.ID} 启动帧级自动更新任务")
	
	def _safe_stop_update_task(self) -> None:
		"""内部安全停止更新任务的方法"""
		try:
			if isinstance(self.update_task, ursina.Sequence):
				self.update_task.kill()
				log.log("debug", f"[{self.head}]", f"ID:{self.ID} 已停止Sequence更新任务")
			elif isinstance(self.update_task, ursina.Invoke):
				self.update_task.cancel()
				log.log("debug", f"[{self.head}]", f"ID:{self.ID} 已取消Invoke更新任务")
			else:
				log.log("warning", f"[{self.head}]", f"ID:{self.ID} 未知的更新任务类型: {type(self.update_task)}")
		except Exception as e:
			log.log("error", f"[{self.head}]", f"ID:{self.ID} 停止更新任务时出错 | 错误:{traceback.format_exc()}",
			        error=3)
		
		self.update_task = None
	
	def stop(self) -> None:
		"""停止文本自动更新（对外公开方法）"""
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
	
	def delete(self) -> None:
		"""彻底删除DynamicText组件（停止更新+销毁实例）"""
		if self._destroyed:
			log.log("warning", f"[{self.head}]", f"ID:{self.ID} 实例已删除，无需重复操作", error=0)
			return
		
		log.log("info", f"[{self.head}]", f"ID:{self.ID} 开始删除DynamicText组件")
		
		try:
			# 先停止更新
			self.stop()
			# 销毁Ursina实体
			ursina.destroy(self)
			# 标记为已销毁
			self._destroyed = True
			log.log("info", f"[{self.head}]", f"ID:{self.ID} 删除DynamicText组件成功")
		except Exception as e:
			log.log("error", f"[{self.head}]", f"ID:{self.ID} 删除DynamicText组件失败 | 错误:{traceback.format_exc()}",
			        error=4)
			raise e
	
	def auto_align_text(
			self,
			align_direction: AlignDirection = 'top_left',
			offset: ursina.Vec2 = ursina.Vec2(0, 0),
			consider_aspect_ratio: bool = True
	) -> None:
		"""
		自动对齐Text实例到指定的屏幕位置（完全适配Ursina实际结构，无无效导入）
		:param align_direction: 对齐方向（支持9种常用方向）
		:param offset: 偏移量（相对于对齐点的归一化偏移，Vec2(x,y)）
		:param consider_aspect_ratio: 是否适配窗口宽高比（推荐True）
		"""
		# 安全校验：确保Ursina已初始化，window对象存在
		if not hasattr(ursina, 'window'):
			raise RuntimeError("请先初始化Ursina应用（app = Ursina()），再调用auto_align_text")
		
		# 1. 获取全局窗口对象（Ursina唯一正确的方式）
		window_obj = ursina.window
		
		# 2. 计算宽高比（兼容所有Ursina版本）
		if consider_aspect_ratio:
			# 优先级：aspect_ratio属性 → get_aspect_ratio方法 → 手动计算
			if hasattr(window_obj, 'aspect_ratio'):
				aspect_ratio = window_obj.aspect_ratio
			elif hasattr(window_obj, 'get_aspect_ratio'):
				aspect_ratio = window_obj.get_aspect_ratio()
			else:
				aspect_ratio = window_obj.width / window_obj.height
		else:
			aspect_ratio = 1.0
		
		# 3. 对齐方向映射（坐标+锚点）
		position_map = {
			'top_left': (ursina.Vec2(-1 * aspect_ratio, 1), ursina.Vec2(0, 1)),
			'top_right': (ursina.Vec2(1 * aspect_ratio, 1), ursina.Vec2(1, 1)),
			'top_center': (ursina.Vec2(0, 1), ursina.Vec2(0.5, 1)),
			'bottom_left': (ursina.Vec2(-1 * aspect_ratio, -1), ursina.Vec2(0, 0)),
			'bottom_right': (ursina.Vec2(1 * aspect_ratio, -1), ursina.Vec2(1, 0)),
			'bottom_center': (ursina.Vec2(0, -1), ursina.Vec2(0.5, 0)),
			'center_left': (ursina.Vec2(-1 * aspect_ratio, 0), ursina.Vec2(0, 0.5)),
			'center_right': (ursina.Vec2(1 * aspect_ratio, 0), ursina.Vec2(1, 0.5)),
			'center': (ursina.Vec2(0, 0), ursina.Vec2(0.5, 0.5))
		}
		
		# 4. 校验对齐方向合法性
		if align_direction not in position_map:
			raise ValueError(
				f"对齐方向错误！支持：{list(position_map.keys())}，当前传入：{align_direction}"
			)
		
		# 5. 计算目标位置和锚点
		base_pos, origin = position_map[align_direction]
		target_pos = ursina.Vec2(base_pos.x + offset.x, base_pos.y + offset.y)
		
		# 6. 应用到Text实例（核心：坐标+锚点缺一不可）
		self.text.position = target_pos
		self.text.origin = origin
		
		print(f"✅ 文本对齐完成 | 方向：{align_direction} | 坐标：{target_pos} | 锚点：{origin}")