import ursina
from typing import Optional, Dict, Any
import json
import numpy as np
import os

# 显式获取ursina的time实例
ursina_time = ursina.time


class BlockbenchModel(ursina.Entity):
	def __init__(
			self,
			# ========== 仅保留Blockbench核心参数的显式声明 ==========
			json_path: str,  # Blockbench模型JSON路径（必传）
			texture_path: str,  # 纹理图片路径（必传）
			animation_json_path: Optional[str] = None,  # 独立动画JSON路径（可选）
			animation_speed: float = 1.0,  # 动画播放速度
			# ========== 所有Entity参数通过kwargs传递 ==========
			**kwargs: Any
	):
		# ========== 第一步：强制清理model参数（终极方案） ==========
		# 无论kwargs中是否有model，直接删除，杜绝重复传递
		kwargs.pop('model', None)
		# 暂存动画相关参数（从kwargs中提取）
		self._external_animations = kwargs.pop('animations', None)
		self._external_animation = kwargs.pop('animation', None)
		
		# ========== 第二步：初始化自定义属性 ==========
		self.json_path = json_path
		self.texture_path = texture_path
		self.animation_json_path = animation_json_path
		self.animation_speed = animation_speed
		
		# 核心数据存储
		self.json_data = {}
		self.animation_json_data = {}
		self.meshes = []
		self._parsed_animations = {}
		self.current_animation = None
		self.animation_frame = 0
		self._final_texture = None
		
		# ========== 第三步：安全加载资源 ==========
		self._load_resources()
		
		# 处理纹理（优先使用kwargs中的texture，其次加载指定路径）
		self._final_texture = kwargs.pop('texture', None) or self._load_texture_safely(texture_path)
		# 将处理后的纹理放回kwargs
		if self._final_texture:
			kwargs['texture'] = self._final_texture
		
		# ========== 第四步：初始化父类Entity（仅传递kwargs） ==========
		# 核心：只传递kwargs，不手动传递任何可能冲突的参数
		super().__init__(**kwargs)
		
		# ========== 第五步：解析动画 ==========
		self.parse_animations()
		
		# ========== 第六步：解析模型并创建子网格 ==========
		self.parse_model()
		
		# ========== 第七步：绑定动画更新逻辑 ==========
		self.update = self._update_handler
	
	def _load_texture_safely(self, texture_path: str) -> Optional[ursina.Texture]:
		"""安全加载纹理"""
		if not texture_path or not os.path.exists(texture_path):
			print(f"[BlockbenchModel 警告] 纹理文件不存在: {texture_path}")
			return None
		
		try:
			return ursina.load_texture(texture_path)
		except Exception as e:
			print(f"[BlockbenchModel 错误] 加载纹理失败 {texture_path}: {str(e)}")
			return None
	
	def _load_resources(self):
		"""安全加载JSON资源"""
		# 加载模型JSON
		self.json_data = self._load_json_safely(self.json_path, "模型")
		
		# 加载动画JSON（可选）
		if self.animation_json_path:
			self.animation_json_data = self._load_json_safely(self.animation_json_path, "动画")
	
	def _load_json_safely(self, path: str, file_type: str = "JSON") -> Dict[str, Any]:
		"""安全加载JSON文件，增加格式校验"""
		if not path or not os.path.exists(path):
			print(f"[BlockbenchModel 警告] {file_type}文件不存在: {path}")
			return {}
		
		# 检查文件扩展名
		file_ext = os.path.splitext(path)[1].lower()
		if file_ext not in ['.json', '.bbmodel']:
			print(f"[BlockbenchModel 警告] {file_type}文件格式错误，应为JSON文件（.json/.bbmodel），当前是: {file_ext}")
			return {}
		
		try:
			# 检查是否为二进制文件
			with open(path, 'rb') as f:
				first_bytes = f.read(4)
				binary_signatures = [b'\x89PNG', b'GIF8', b'RIFF', b'glTF']
				for sig in binary_signatures:
					if first_bytes.startswith(sig):
						print(f"[BlockbenchModel 错误] {file_type}文件 {path} 是二进制文件，不是JSON文本")
						return {}
			
			# 读取JSON文件
			with open(path, 'r', encoding='utf-8', errors='replace') as f:
				return json.load(f)
		
		except json.JSONDecodeError:
			print(f"[BlockbenchModel 错误] {file_type}文件 {path} 不是有效的JSON格式")
			return {}
		except UnicodeDecodeError as e:
			print(f"[BlockbenchModel 错误] {file_type}文件 {path} 编码错误（非UTF-8）: {str(e)}")
			try:
				with open(path, 'r', encoding='gbk', errors='replace') as f:
					return json.load(f)
			except:
				return {}
		except Exception as e:
			print(f"[BlockbenchModel 错误] 读取{file_type}文件失败 {path}: {str(e)}")
			return {}
	
	def parse_model(self):
		"""解析Blockbench JSON生成模型子网格"""
		if 'elements' not in self.json_data:
			print(f"[BlockbenchModel 错误] 模型JSON {self.json_path} 中无elements节点")
			return
		
		# 清空原有子网格
		for mesh in self.meshes:
			ursina.destroy(mesh)
		self.meshes.clear()
		
		# 遍历生成立方体
		for element in self.json_data['elements']:
			from_xyz = np.array(element['from']) / 16
			to_xyz = np.array(element['to']) / 16
			size = to_xyz - from_xyz
			
			cube = ursina.Entity(
				parent=self,
				position=from_xyz + size / 2,
				scale=size,
				model='cube',
				texture=self._final_texture,
				color=self.color if hasattr(self, 'color') else ursina.color.white,
				alpha=self.alpha if hasattr(self, 'alpha') else 1.0,
				shader=self.shader if hasattr(self, 'shader') else None,
				material=self.material if hasattr(self, 'material') else None,
				texture_scale=self.texture_scale if hasattr(self, 'texture_scale') else (1, 1),
				texture_offset=self.texture_offset if hasattr(self, 'texture_offset') else (0, 0),
				render_queue=self.render_queue if hasattr(self, 'render_queue') else 0,
				always_on_top=self.always_on_top if hasattr(self, 'always_on_top') else False,
				collider=self.collider if (
							hasattr(self, 'collider') and len(self.json_data['elements']) == 1) else None,
				enabled=self.enabled if hasattr(self, 'enabled') else True
			)
			self.meshes.append(cube)
	
	def parse_animations(self):
		"""解析JSON动画数据"""
		# 优先级：主JSON动画 > 独立动画JSON > 外部传入的animations
		anim_sources = [
			self.json_data,
			self.animation_json_data,
			{'animations': self._external_animations or {}}
		]
		
		for source in anim_sources:
			if 'animations' in source and source['animations']:
				self._parsed_animations = source['animations']
				break
		
		# 更新父类的animations属性
		self.animations = self._parsed_animations
		
		# 自动播放指定动画
		if self._external_animation and self._external_animation in self._parsed_animations:
			self.play_animation(self._external_animation)
	
	def play_animation(self, anim_name: str):
		"""播放指定动画"""
		if anim_name not in self._parsed_animations:
			print(f"[BlockbenchModel 错误] 动画 {anim_name} 不存在")
			return
		
		self.current_animation = anim_name
		self.animation_frame = 0
		print(f"[BlockbenchModel] 开始播放动画: {anim_name}")
	
	def stop_animation(self):
		"""停止当前动画"""
		self.current_animation = None
		self.animation_frame = 0
	
	def _update_handler(self):
		"""动画更新处理器"""
		if not self.current_animation or self.current_animation not in self._parsed_animations:
			return
		
		anim = self._parsed_animations[self.current_animation]
		frame_count = len(anim.get('frames', []))
		
		if frame_count == 0:
			return
		
		# 更新动画帧
		self.animation_frame += ursina_time.dt * self.animation_speed
		anim_length = anim.get('length', 10)
		
		if self.animation_frame >= anim_length:
			if anim.get('loop', True):
				self.animation_frame = 0
			else:
				self.stop_animation()
				return
		
		# 应用帧变换
		frame_ratio = self.animation_frame / anim_length
		frame_index = int(frame_ratio * frame_count) % frame_count
		frame_data = anim['frames'][frame_index]
		
		if 'rotation' in frame_data:
			self.rotation = frame_data['rotation']
		if 'position' in frame_data:
			self.position = np.array(frame_data['position']) / 16
		if 'scale' in frame_data:
			self.scale = np.array(frame_data['scale']) / 16


# -------------------------- 正确使用示例 --------------------------
if __name__ == '__main__':
	app = ursina.Ursina()
	
	# 创建BlockbenchModel（所有Entity参数都放在kwargs中）
	player = BlockbenchModel(
		# Blockbench核心参数（显式声明）
		json_path='character_model.json',  # 你的模型JSON文件
		texture_path='character_texture.png',  # 你的纹理图片
		animation_json_path='character_anim.json',  # 你的动画JSON文件（可选）
		animation_speed=1.2,
		
		# 所有Entity原生参数（通过kwargs传递）
		name='player',
		enabled=True,
		position=(0, 1, 0),
		rotation=(0, 90, 0),
		scale=1.5,
		color=ursina.color.rgba(255, 255, 255, 0.9),
		alpha=0.9,
		parent=ursina.scene,
		shader='lit',
		collider='box',
		eternal=True,
		animations={'idle': {'frames': [], 'length': 5}},
		animation='walk'
	)
	
	# 使用Entity原生方法
	player.look_at(ursina.Vec3(5, 0, 5))
	player.move_forward(2)
	
	
	# 相机控制
	def update():
		ursina.camera.position += ursina.Vec3(
			ursina.held_keys['d'] - ursina.held_keys['a'],
			ursina.held_keys['e'] - ursina.held_keys['q'],
			ursina.held_keys['s'] - ursina.held_keys['w']
		) * ursina_time.dt * 5
	
	
	app.run()