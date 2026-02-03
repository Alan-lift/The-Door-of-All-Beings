import builtins
import gc
import time
import traceback
import weakref
from typing import *
from typing import Callable, Any, Optional, Dict, Union

import ursina
from ursina.shaders import lit_with_shadows_shader

import log


class Entity(ursina.Entity):
	def __init__(
			self,
			# ========== 基础参数 ==========
			name: str = '',
			enabled: bool = True,
			
			# ========== 变换参数 ==========
			position: Union[ursina.Vec3, Tuple[float, float, float], List[float]] = (0, 0, 0),
			rotation: Union[ursina.Vec3, Tuple[float, float, float], List[float]] = (0, 0, 0),
			scale: Union[float, int, ursina.Vec3, Tuple[float, float, float], List[float]] = (1, 1, 1),
			
			# ========== 图形参数 ==========
			model: Union[str, Any] = 'quad',
			texture: Union[str, Any, None] = None,
			color: Union[ursina.Color, Tuple[float, float, float],
			Tuple[float, float, float, float], List[float]] = ursina.color.white,
			alpha: float = 1.0,
			
			# ========== 父子关系 ==========
			parent: Optional[Any] = None,
			children: Optional[List[Any]] = None,
			
			# ========== 材质相关 ==========
			shader: Union[Any, str, None] = None,
			material: Optional[Any] = None,
			
			# ========== 渲染设置 ==========
			texture_scale: Union[ursina.Vec2, Tuple[float, float], List[float]] = (1, 1),
			texture_offset: Union[ursina.Vec2, Tuple[float, float], List[float]] = (0, 0),
			render_queue: int = 0,
			always_on_top: bool = False,
			
			# ========== 碰撞相关 ==========
			collider: Union[str, Any, None] = None,
			ignore: bool = False,
			
			# ========== 动画相关 ==========
			animations: Optional[Dict[str, Any]] = None,
			animation: Optional[Union[str, Dict[str, Any]]] = None,
			
			# ========== 特殊属性 ==========
			eternal: bool = False,
			
			# ========== 额外参数 ==========
			**kwargs: Any
	):
		"""创建一个新的 Entity 实体（封装 Ursina Entity，所有参数挂载到 self 方便类内调用）。

		Args:
			# ---------------- 基础参数 ----------------
			name: 实体的名称，用于标识和调试
				- 类型: str
				- 默认值: ''
				- 保存为: self.name
			enabled: 实体是否启用（可见且可交互）
				- 类型: bool
				- 默认值: True
				- 保存为: self.enabled

			# ---------------- 变换参数 ----------------
			position: 实体在3D空间中的位置
				- 类型: Union[Vec3, Tuple[float, float, float], List[float]]
				- 默认值: (0, 0, 0)
				- 保存为: self.position
			rotation: 实体在3D空间中的旋转角度（欧拉角）
				- 类型: Union[Vec3, Tuple[float, float, float], List[float]]
				- 默认值: (0, 0, 0)
				- 保存为: self.rotation
			scale: 实体的缩放比例，可统一缩放或各轴独立缩放
				- 类型: Union[float, int, Vec3, Tuple[float, float, float], List[float]]
				- 默认值: (1, 1, 1)
				- 保存为: self.scale

			# ---------------- 图形参数 ----------------
			model: 实体使用的3D模型
				- 类型: Union[str, Any]
				- 默认值: 'quad'（四边形）
				- 保存为: self.model
				- 可选值: 'cube', 'sphere', 'plane', 'circle' 或自定义模型路径
			texture: 应用于实体的纹理/贴图
				- 类型: Union[str, Any, None]
				- 默认值: None
				- 保存为: self.texture
				- 说明: 可以是图片文件路径或Texture对象
			color: 实体的基础颜色
				- 类型: Union[Color, Tuple[float, float, float], Tuple[float, float, float, float], List[float]]
				- 默认值: color.white
				- 保存为: self.color
				- 格式: RGB(1,0,0) 或 RGBA(1,0,0,0.5)
			alpha: 实体的透明度（0.0完全透明，1.0完全不透明）
				- 类型: float
				- 默认值: 1.0
				- 保存为: self.alpha

			# ---------------- 父子关系 ----------------
			parent: 实体的父实体，用于建立层级关系
				- 类型: Optional[Any]
				- 默认值: None
				- 保存为: self.parent
			children: 实体的子实体列表
				- 类型: Optional[List[Any]]
				- 默认值: None
				- 保存为: self.children

			# ---------------- 材质相关 ----------------
			shader: 实体使用的着色器程序
				- 类型: Union[Any, str, None]
				- 默认值: None（使用 lit_with_shadows_shader）
				- 保存为: self.shader
			material: 实体使用的材质
				- 类型: Optional[Any]
				- 默认值: None
				- 保存为: self.material

			# ---------------- 渲染设置 ----------------
			texture_scale: 纹理在UV坐标上的缩放
				- 类型: Union[Vec2, Tuple[float, float], List[float]]
				- 默认值: (1, 1)
				- 保存为: self.texture_scale
			texture_offset: 纹理在UV坐标上的偏移
				- 类型: Union[Vec2, Tuple[float, float], List[float]]
				- 默认值: (0, 0)
				- 保存为: self.texture_offset
			render_queue: 渲染顺序编号，数值越大越晚渲染
				- 类型: int
				- 默认值: 0
				- 保存为: self.render_queue
			always_on_top: 是否始终渲染在其他实体之上
				- 类型: bool
				- 默认值: False
				- 保存为: self.always_on_top

			# ---------------- 碰撞相关 ----------------
			collider: 实体的碰撞检测器
				- 类型: Union[str, Any, None]
				- 默认值: None
				- 保存为: self.collider
				- 可选值: 'box', 'sphere', 'mesh' 或 MeshCollider对象
			ignore: 是否忽略碰撞检测
				- 类型: bool
				- 默认值: False
				- 保存为: self.ignore

			# ---------------- 动画相关 ----------------
			animations: 实体可用的动画字典
				- 类型: Optional[Dict[str, Any]]
				- 默认值: None
				- 保存为: self.animations
			animation:播放的动画
			    - 类型:Optional[Union[str, Dict[str, Any]]]
				- 默认值: None
				- 保存为: self.animation

			# ---------------- 特殊属性 ----------------
			eternal: 实体是否永恒存在（不会被场景清除）
				- 类型: bool
				- 默认值: False
				- 保存为: self.eternal

			# ---------------- 额外参数 ----------------
			**kwargs: 额外的自定义属性
				- 类型: Any
				- 说明: 所有额外参数都会作为实例属性保存

		Examples:
			>>> Entity()  # 创建默认白色四边形
			>>> Entity(model='cube', color=ursina.color.red, position=(0,2,-5))
			>>> Entity(name='player', health=100, speed=5.0)  # 添加自定义属性
		"""
		# ========== 第一步：将所有 __init__ 参数挂载到 self 上 ==========
		# 基础参数
		self.name = name
		self.enabled = enabled
		
		# 变换参数
		self.position = position
		self.rotation = rotation
		self.scale = scale
		
		# 图形参数
		self.model = model
		self.texture = texture
		self.color = color
		self.alpha = alpha
		
		# 父子关系
		self.parent = parent
		self.children = children
		
		# 材质相关
		self.shader = shader
		self.material = material
		
		# 渲染设置
		self.texture_scale = texture_scale
		self.texture_offset = texture_offset
		self.render_queue = render_queue
		self.always_on_top = always_on_top
		
		# 碰撞相关
		self.collider = collider
		self.ignore = ignore
		
		# 动画相关
		self.animations = animations
		self.animation = animation
		
		# 特殊属性
		self.eternal = eternal
		
		# 额外参数
		for key, value in kwargs.items():
			setattr(self, key, value)
		
		# ========== 第二步：创建内部实体 self.Entity_model ==========
		# 处理颜色（融合 alpha 透明度）
		processed_color = self.__process_color(self.color, self.alpha)
		# 处理向量参数格式转换（修复切片错误）
		processed_position = self.__convert_to_vec3(self.position)
		processed_rotation = self.__convert_to_vec3(self.rotation)
		processed_scale = self.__convert_scale(self.scale)
		processed_texture_scale = self.__convert_to_vec2(self.texture_scale)
		processed_texture_offset = self.__convert_to_vec2(self.texture_offset)
		# 处理默认着色器
		processed_shader = self.shader if self.shader is not None else lit_with_shadows_shader
		
		self.ID = int(time.time())
		log.log("Entity管理器", "新建Entity实体", f"""实体ID:{self.ID}
参:
\t名称:{self.name}
\t启用:{self.enabled}
\t位置:{processed_position}
\t角度:{processed_rotation}
\t比例:{processed_scale}
\t模型:{self.model}
\t贴图:{self.texture}
\t颜色:{processed_color}
\t父关系:{self.parent}
\t子关系:{self.children}
\t着色器:{processed_shader}
\t材质:{self.material}
\t纹理缩放:{processed_texture_scale}
\t纹理偏移:{processed_texture_offset}
\t渲染编号:{self.render_queue}
\t始终渲染在其他实体之上:{self.always_on_top}
\t碰撞检测器:{self.collider}
\t是否忽略碰撞:{self.ignore}
\t动画字典:{self.animations}
\t动画:{self.animation}
\t是否永恒存在:{self.eternal}""")
		
		# 核心：创建 Ursina 实体并赋值给 self.Entity_model（固定名称，类内调用）
		self.Entity_model = super().__init__(
			name=self.name,
			enabled=self.enabled,
			position=processed_position,
			rotation=processed_rotation,
			scale=processed_scale,
			model=self.model,
			texture=self.texture,
			color=processed_color,
			parent=self.parent,
			shader=processed_shader,
			material=self.material,
			texture_scale=processed_texture_scale,
			texture_offset=processed_texture_offset,
			render_queue=self.render_queue,
			always_on_top=self.always_on_top,
			collider=self.collider,
			animations=self.animations,
			animation=self.animation,
			**kwargs
		)
		log.log("Entity管理器", f"新建Entity成功", f"ID:{self.ID}")
		# ========== 第三步：处理子实体（可选） ==========
		if self.children:
			for child in self.children:
				if hasattr(child, 'Entity_model'):
					child.Entity_model.parent = self.Entity_model
	
	# ========== 私有辅助方法（修复切片错误） ==========
	def __convert_to_vec3(self, value: Any) -> ursina.Vec3:
		"""转换任意类型为 Ursina Vec3（3D向量）【修复切片错误】"""
		if isinstance(value, ursina.Vec3):
			return value
		elif isinstance(value, (tuple, list)):
			# 先处理输入的列表/元组，补全维度后直接创建 Vec3（无切片）
			x = value[0] if len(value) > 0 else 0.0
			y = value[1] if len(value) > 1 else 0.0
			z = value[2] if len(value) > 2 else 0.0
			return ursina.Vec3(x, y, z)
		elif isinstance(value, (int, float)):
			return ursina.Vec3(value, value, value)
		# 默认返回原点
		return ursina.Vec3(0, 0, 0)
	
	def __convert_scale(self, value: Any) -> ursina.Vec3:
		"""处理缩放参数（兼容标量/向量）"""
		if isinstance(value, (int, float)):
			return ursina.Vec3(value, value, value)
		# 复用 Vec3 转换逻辑（已修复切片错误）
		return self.__convert_to_vec3(value)
	
	def __process_color(self, color_value: Any, alpha_value: float) -> ursina.Color:
		"""处理颜色和透明度，确保返回 Ursina Color 类型"""
		# 已有 Color 对象：覆盖透明度
		if isinstance(color_value, ursina.Color):
			return ursina.Color(color_value.r, color_value.g, color_value.b, alpha_value)
		# 元组/列表：兼容 RGB/RGBA
		elif isinstance(color_value, (tuple, list)):
			if len(color_value) >= 3:
				r, g, b = color_value[:3]
				a = color_value[3] if len(color_value) >= 4 else alpha_value
				return ursina.Color(r, g, b, a)
		# 非法类型：返回默认白色（带指定透明度）
		return ursina.Color(1, 1, 1, alpha_value)
	
	def __convert_to_vec2(self, value: Any) -> ursina.Vec2:
		"""转换任意类型为 Ursina Vec2（2D向量）【同步优化逻辑】"""
		if isinstance(value, ursina.Vec2):
			return value
		elif isinstance(value, (tuple, list)):
			# 分步处理，避免切片错误
			x = value[0] if len(value) > 0 else 0.0
			y = value[1] if len(value) > 1 else 0.0
			return ursina.Vec2(x, y)
		elif isinstance(value, (int, float)):
			return ursina.Vec2(value, value)
		# 默认返回 (1,1)（纹理缩放默认值）
		return ursina.Vec2(1, 1)
	
	def move(self, x=None, y=None, z=None):
		if not ((x is None) and (y is None) and (z is None)):
			log.log("Entity管理器", "移动实体", f"ID:{self.ID}")
			
			_x = self.Entity_model.position.x
			_y = self.Entity_model.position.y
			_z = self.Entity_model.position.z
			
			self.Entity_model.position.x = x if x is not None else _x
			self.Entity_model.position.y = y if y is not None else _y
			self.Entity_model.position.z = z if z is not None else _z
			
			log.log("Entity管理器", "移动实体成功", f"""ID:{self.ID}
位置:
\tx:{_x}->{x if x is not None else _x}
\ty:{_y}->{y if y is not None else _y}
\tz:{_z}->{z if z is not None else _z}""")
			return True
		else:
			return self.Entity_model.position
	
	def delete(self):
		log.log("Entity管理器", "启动删除实体任务", f"ID:{self.ID}")
		
		# 容错：如果实体已为空，直接返回
		if self.Entity_model is None or (hasattr(self.Entity_model, 'exists') and not self.Entity_model.exists):
			log.log("error", "Entity管理器所删除的实体不存在", f"ID:{self.ID}", error=1)
			return True
		
		try:
			# 步骤1：清理 Ursina 内置资源（核心）
			# 自动移除渲染、碰撞体、回调等
			log.log("Entity管理器", "删除实体渲染", f"ID:{self.ID}")
			log.log("Entity管理器", "删除实体碰撞体", f"ID:{self.ID}")
			log.log("Entity管理器", "删除实体回调", f"ID:{self.ID}")
			
			ursina.destroy(self.Entity_model)
			
			log.log("Entity管理器", f"删除实体渲染成功", f"ID:{self.ID}")
			log.log("Entity管理器", f"删除实体碰撞体成功", f"ID:{self.ID}")
			log.log("Entity管理器", f"删除实体回调成功", f"ID:{self.ID}")
			
			# 步骤2：自动清理常见的自定义关联资源
			# 1. 音效/音频
			log.log("Entity管理器", "删除实体音频", f"ID:{self.ID}")
			if hasattr(self.Entity_model, 'audio') and self.Entity_model.audio is not None:
				self.Entity_model.audio.stop()
				self.Entity_model.audio = None
			log.log("Entity管理器", f"删除实体音频成功", f"ID:{self.ID}")
			
			# 2. 动画/序列
			log.log("Entity管理器", "删除实体动画", f"ID:{self.ID}")
			if hasattr(self.Entity_model, 'animation') and self.Entity_model.animation is not None:
				self.Entity_model.animation.pause()
				self.Entity_model.animation = None
			log.log("Entity管理器", f"删除实体动画成功", f"ID:{self.ID}")
			
			# 3. 粒子系统
			log.log("Entity管理器", "删除实体粒子", f"ID:{self.ID}")
			if hasattr(self.Entity_model, 'particle_system') and self.Entity_model.particle_system is not None:
				self.Entity_model.particle_system.stop()
				self.Entity_model.particle_system = None
			log.log("Entity管理器", f"删除实体粒子成功", f"ID:{self.ID}")
			
			# 步骤3：清空所有自定义属性（递归置空）
			log.log("Entity管理器", "清空实体所有自定义属性", f"ID:{self.ID}")
			for attr in dir(self.Entity_model):
				# 跳过 Ursina 内置核心属性，只清理自定义属性
				if not attr.startswith('_') and attr not in ['position', 'rotation', 'scale', 'model', 'color']:
					try:
						setattr(self.Entity_model, attr, None)
					except:
						pass
			log.log("Entity管理器", "清空实体所有自定义属性成功", f"ID:{self.ID}")
			
			# 步骤4：触发 Python 垃圾回收（强制释放内存）
			gc.collect()
			
			log.log("Entity管理器", f"删除实体成功", f"ID:{self.ID}")
			return True
		
		except Exception as e:
			log.log("error", f"Entity管理器删除实体错误", f"ID:{self.ID}\n错误:{e}", error=4)
			raise e


class Text(ursina.Text):
	size = .025
	default_font = 'OpenSans-Regular.ttf'
	default_monospace_font = 'VeraMono.ttf'
	default_resolution = 1080 * size * 2
	start_tag = '<'
	end_tag = '>'
	
	def __init__(self,
	             text='',
	             start_tag=start_tag,
	             end_tag=end_tag,
	             ignore=True,
	             **kwargs):
		super().__init__(text=text,
		                 start_tag=start_tag,
		                 end_tag=end_tag,
		                 ignore=ignore,
		                 **kwargs)
	
	def update_text(self, update_text: callable, wait_time: int = 0):
		"""
		动态更新文本内容

		:param update_text: 返回字符串的函数
		:param wait_time: 等待时间（毫秒）
		:return: None
		"""
		if wait_time > 0:
			# 定时更新（间隔大于0）
			def update_action():
				self.text = str(update_text())
			
			ursina.Sequence(
				update_action,
				ursina.Wait(wait_time / 1000),
				loop=True
			).start()
		elif wait_time == 0:
			# 每帧更新
			def update_():
				self.text = str(update_text())
			
			ursina.invoke(update_, delay=0, repeating=True)