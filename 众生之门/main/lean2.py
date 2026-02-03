from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from game import *
import os


class FBXWorld:
	def __init__(self):
		print("=" * 60)
		print("FBX模型加载器")
		print("=" * 60)
		
		# 检查文件
		model_path = './assets/models/netease_models.fbx'
		texture_path = './assets/textures/kris_tailnexa - 纹理.png'
		
		print(f"模型文件: {model_path}")
		print(f"  存在: {os.path.exists(model_path)}")
		if os.path.exists(model_path):
			print(f"  大小: {os.path.getsize(model_path) / 1024:.1f} KB")
		
		print(f"纹理文件: {texture_path}")
		print(f"  存在: {os.path.exists(texture_path)}")
		
		# 创建应用
		app = Ursina(title='FBX模型展示')
		
		# 创建场景
		self.create_scene()
		
		# 加载FBX模型（带贴图）
		self.load_fbx_model(model_path, texture_path)
		
		# 添加玩家
		self.create_player()
		
		# 添加UI
		self.create_ui()
		
		app.run()
	
	def create_scene(self):
		"""创建场景"""
		# 地面
		self.ground = Entity(
			model='plane',
			scale=200,
			position=(0, 0, 0),
			collider='box',
			texture='grass',
			texture_scale=(100, 100)
		)
		
		# 天空
		Sky(color=color.rgb(135, 206, 235))
		
		# 光照
		scene.ambient_color = color.rgb(180, 180, 180)
		DirectionalLight()
	
	def load_fbx_model(self, model_path, texture_path):
		"""加载FBX模型"""
		print("\n正在加载FBX模型...")
		
		if not os.path.exists(model_path):
			print("❌ FBX文件不存在")
			self.create_fallback_model()
			return
		
		try:
			# 尝试不同缩放比例
			scale_options = [0.1, 0.5, 1, 2, 5, 10, 20]
			
			for scale_val in scale_options:
				print(f"尝试缩放: {scale_val}倍...")
				
				try:
					# 加载模型
					self.model = Entity(
						model=model_path,
						position=(0, 0, 0),
						scale=scale_val,
						eternal=True
					)
					
					# 尝试应用贴图
					if os.path.exists(texture_path):
						try:
							self.model.texture = texture_path
							print(f"✅ 应用贴图: {os.path.basename(texture_path)}")
						except:
							print("⚠️  贴图应用失败，使用颜色")
							self.model.color = color.white
					else:
						print("⚠️  贴图文件不存在，使用白色")
						self.model.color = color.white
					
					print(f"✅ FBX模型加载成功！")
					print(f"  缩放: {self.model.scale}")
					print(f"  位置: {self.model.position}")
					
					# 检查模型属性
					self.check_model_properties()
					
					# 添加碰撞体
					self.add_model_collider(scale_val)
					
					# 添加模型标记
					self.add_model_marker()
					
					# 尝试播放动画（如果FBX包含）
					self.try_play_animation()
					
					break  # 成功加载
				
				except Exception as e:
					print(f"缩放 {scale_val} 失败: {str(e)[:80]}")
					continue
			
			if not hasattr(self, 'model'):
				print("❌ 所有缩放都失败")
				self.create_fallback_model()
		
		except Exception as e:
			print(f"❌ FBX加载失败: {e}")
			self.create_fallback_model()
	
	def check_model_properties(self):
		"""检查模型属性"""
		try:
			if hasattr(self.model.model, 'vertices'):
				vertex_count = len(self.model.model.vertices)
				print(f"  顶点数: {vertex_count:,}")
			
			if hasattr(self.model.model, 'triangles'):
				triangle_count = len(self.model.model.triangles) // 3
				print(f"  三角面数: {triangle_count:,}")
		
		except:
			pass
	
	def add_model_collider(self, scale_val):
		"""添加碰撞体"""
		try:
			self.model.collider = 'mesh'
			print("  添加网格碰撞体")
		except:
			try:
				# 如果网格碰撞体失败，使用盒子碰撞体
				collider_size = scale_val * 2
				self.model.collider = BoxCollider(
					self.model,
					center=Vec3(0, collider_size / 2, 0),
					size=Vec3(collider_size, collider_size, collider_size)
				)
				print(f"  添加盒子碰撞体，大小: {collider_size}")
			except:
				print("  碰撞体添加失败")
	
	def add_model_marker(self):
		"""添加模型标记"""
		# 在模型上方添加标记
		if hasattr(self, 'model'):
			marker_height = max(self.model.scale_y * 1.5, 10)
			
			self.marker = Entity(
				model='cube',
				color=color.red,
				position=(0, marker_height, 0),
				scale=2
			)
			
			self.marker_text = Text(
				text='模型位置',
				position=(0, marker_height + 3, 0),
				scale=1.5,
				color=color.yellow,
				background=True
			)
	
	def try_play_animation(self):
		"""尝试播放动画"""
		try:
			# 检查模型是否有动画
			if hasattr(self.model.model, 'animations') and self.model.model.animations:
				print(f"发现 {len(self.model.model.animations)} 个动画")
				
				# 创建动画控制器
				self.model.animator = Animator()
				
				# 尝试播放第一个动画
				if len(self.model.model.animations) > 0:
					self.model.animator.state = self.model.model.animations[0]
					print("  播放动画")
		
		except Exception as e:
			print(f"动画设置失败: {e}")
	
	def create_fallback_model(self):
		"""创建备用模型"""
		print("\n创建备用模型...")
		
		self.model = Entity(
			model='cube',
			color=color.cyan,
			position=(0, 5, 0),
			scale=(10, 15, 10),
			texture='brick'
		)
		
		# 添加旋转动画
		self.model.animate_rotation((0, 360, 0), duration=10, loop=True)
		
		print("备用模型创建完成")
	
	def create_player(self):
		"""创建玩家"""
		print("\n创建玩家...")
		
		# 根据模型大小调整起始距离
		start_distance = 30
		if hasattr(self, 'model'):
			model_size = max(self.model.scale)
			start_distance = max(model_size * 3, 30)
		
		self.player = FirstPersonController(
			position=(0, 2, -start_distance),
			speed=8,
			jump_height=2,
			mouse_sensitivity=Vec2(40, 40)
		)
		
		self.player.cursor.visible = False
		
		print(f"✅ 玩家创建完成")
		print(f"  起始位置: {self.player.position}")
		print(f"  距离模型: {start_distance}")
	
	def create_ui(self):
		"""创建UI"""
		# 状态显示
		self.status_text = Text(
			text='FBX模型测试',
			position=(-0.9, 0.45),
			scale=1.2,
			color=color.white,
			background=True
		)
		
		# 控制说明
		controls = [
			'WASD - 移动',
			'空格 - 跳跃',
			'鼠标 - 视角',
			'ESC - 显示/隐藏鼠标',
			'F - 飞行模式'
		]
		
		for i, text in enumerate(controls):
			Text(
				text=text,
				position=(-0.9, 0.40 - i * 0.04),
				scale=1.0,
				color=color.light_gray
			)
	
	def update(self):
		"""每帧更新"""
		if hasattr(self, 'player'):
			# 更新窗口标题
			fps = int(1 / time.dt) if time.dt > 0 else 0
			window.title = f'FBX模型 | FPS: {fps}'
			
			# 更新状态
			pos = self.player.position
			status = f'位置: X:{pos.x:.1f} Y:{pos.y:.1f} Z:{pos.z:.1f}'
			
			if hasattr(self, 'model'):
				distance = (pos - self.model.position).length()
				status += f'\n距离模型: {distance:.1f}'
			
			self.status_text.text = status
	
	def input(self, key):
		"""处理输入"""
		# 飞行模式
		if key == 'f' and hasattr(self, 'player'):
			self.player.gravity = 0 if self.player.gravity != 0 else 1
			mode = "飞行" if self.player.gravity == 0 else "行走"
			print(f"切换为: {mode}模式")
		
		# 重置位置
		if key == 'r' and hasattr(self, 'player'):
			self.player.position = (0, 2, -30)
			print("位置重置")


# 运行FBX世界
if __name__ == '__main__':
	# 初始化鼠标控制器
	setup_mouse_control_system()
	
	# 创建FBX世界
	world = FBXWorld()