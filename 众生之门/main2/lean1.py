from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight, DirectionalLight, Vec4, Point3
from panda3d.core import TextNode, CardMaker, WindowProperties
import sys
import os


class AnimatedModelViewer(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		
		# 设置窗口属性
		self.setup_window()
		
		# 设置背景色
		self.setBackgroundColor(0.1, 0.15, 0.2, 1)
		
		# 模型和动画管理
		self.actor = None
		self.current_animation = None
		self.animations_list = []
		
		# 加载模型
		self.load_animated_model()
		
		# 设置场景
		self.setup_scene()
		
		# 设置UI
		self.setup_ui()
		
		# 设置控制
		self.setup_controls()
		
		# 开始主循环
		self.start_main_loop()
	
	def setup_window(self):
		"""设置窗口属性"""
		props = WindowProperties()
		props.setTitle("Panda3D 动画模型查看器")
		props.setSize(1200, 800)
		self.win.requestProperties(props)
		
		# 设置帧率显示
		self.setFrameRateMeter(True)
	
	def load_animated_model(self):
		"""加载动画模型"""
		model_path = "./assets/models/netease_models.gltf"
		
		# 尝试不同的模型格式
		formats_to_try = [
			("./assets/models/netease_models.gltf", {"mergeTransforms": 1}),
			("./assets/models/netease_models.glb", {}),
			("./assets/models/netease_models.egg", {}),
			("./assets/models/netease_models.bam", {}),
			("./assets/models/netease_models.fbx", {}),
		]
		
		print("=" * 50)
		print("正在加载动画模型...")
		
		for file_path, kwargs in formats_to_try:
			if os.path.exists(file_path):
				print(f"尝试加载: {file_path}")
				try:
					# 使用Actor类加载模型
					self.actor = Actor(file_path, **kwargs)
					
					if self.actor:
						print(f"✓ 成功加载: {file_path}")
						
						# 获取可用的动画列表
						self.get_available_animations()
						
						# 设置模型位置
						self.actor.reparentTo(self.render)
						self.actor.setPos(0, 20, 0)
						self.actor.setScale(1.5)
						self.actor.setH(180)  # 调整方向
						
						# 播放默认动画
						self.play_animation("idle" if "idle" in self.animations_list else self.animations_list[
							0] if self.animations_list else None)
						return
				
				except Exception as e:
					print(f"✗ 加载失败: {e}")
					continue
		
		# 如果所有格式都失败，创建测试Actor
		print("使用内置测试模型...")
		self.create_test_actor()
	
	def create_test_actor(self):
		"""创建测试用Actor（熊猫模型）"""
		try:
			# 尝试加载Panda3D内置的熊猫模型
			self.actor = Actor("models/panda-model",
			                   {"walk": "models/panda-walk4"})
			self.actor.reparentTo(self.render)
			self.actor.setPos(0, 20, 0)
			self.actor.setScale(0.2)
			
			# 设置动画
			self.animations_list = ["walk"]
			self.play_animation("walk")
			
			# 添加说明
			self.add_status_message("使用内置熊猫模型\n按1-9键切换测试动画")
		
		except:
			# 如果内置模型也不存在，创建最简单的Actor
			print("创建基础测试Actor...")
			self.create_basic_actor()
	
	def create_basic_actor(self):
		"""创建基础的测试Actor"""
		from panda3d.core import AnimBundle, AnimBundleNode
		from panda3d.core import PartBundle, PartGroup
		
		# 创建一个简单的Actor
		self.actor = Actor()
		self.actor.reparentTo(self.render)
		self.actor.setPos(0, 20, 0)
		self.actor.setScale(2)
		
		# 创建一个简单的动画（旋转）
		self.taskMgr.add(self.rotate_actor, "RotateActorTask")
		
		self.animations_list = ["rotate"]
		self.current_animation = "rotate"
		
		self.add_status_message("基础测试Actor\n按R键切换旋转")
	
	def rotate_actor(self, task):
		"""旋转Actor的基本动画"""
		if self.actor:
			self.actor.setH(self.actor.getH() + 1)
		return task.cont
	
	def get_available_animations(self):
		"""获取可用的动画列表"""
		if not self.actor:
			return
		
		try:
			# 获取Actor的所有动画
			anims = self.actor.getAnimNames()
			self.animations_list = list(anims) if anims else []
			
			print(f"找到 {len(self.animations_list)} 个动画:")
			for i, anim in enumerate(self.animations_list, 1):
				print(f"  {i}. {anim}")
				
				# 获取动画帧数信息
				try:
					anim_control = self.actor.getAnimControl(anim)
					if anim_control:
						frames = anim_control.getNumFrames()
						fps = anim_control.getFrameRate()
						print(f"     帧数: {frames}, 帧率: {fps:.1f}")
				except:
					pass
		
		except Exception as e:
			print(f"获取动画列表失败: {e}")
			self.animations_list = []
	
	def play_animation(self, anim_name, loop=True, from_frame=None, to_frame=None):
		"""播放指定动画"""
		if not self.actor or not anim_name:
			return
		
		try:
			# 停止当前动画
			if self.current_animation:
				self.stop_animation()
			
			print(f"播放动画: {anim_name}")
			
			# 设置动画
			if loop:
				self.actor.loop(anim_name)
			else:
				self.actor.play(anim_name)
			
			# 设置播放范围
			anim_control = self.actor.getAnimControl(anim_name)
			if anim_control and (from_frame is not None or to_frame is not None):
				if from_frame is not None:
					anim_control.setPlayRate(from_frame)
				if to_frame is not None:
					pass  # Panda3D中设置结束帧比较复杂
			
			self.current_animation = anim_name
			
			# 更新UI显示
			if hasattr(self, 'anim_text'):
				self.anim_text.setText(f"当前动画: {anim_name}")
		
		except Exception as e:
			print(f"播放动画失败: {e}")
			self.add_status_message(f"无法播放动画: {anim_name}\n错误: {str(e)}")
	
	def stop_animation(self):
		"""停止当前动画"""
		if self.actor and self.current_animation:
			try:
				self.actor.stop(self.current_animation)
				print(f"停止动画: {self.current_animation}")
				self.current_animation = None
			except:
				pass
	
	def setup_scene(self):
		"""设置场景"""
		# 设置灯光
		self.setup_lights()
		
		# 设置相机
		self.setup_camera()
		
		# 设置地面
		self.setup_ground()
	
	def setup_lights(self):
		"""设置灯光系统"""
		# 环境光
		ambient = AmbientLight("ambient_light")
		ambient.setColor(Vec4(0.3, 0.3, 0.3, 1))
		ambient_np = self.render.attachNewNode(ambient)
		self.render.setLight(ambient_np)
		
		# 主方向光
		directional = DirectionalLight("main_light")
		directional.setColor(Vec4(0.8, 0.8, 0.7, 1))
		directional_np = self.render.attachNewNode(directional)
		directional_np.setHpr(45, -60, 0)
		self.render.setLight(directional_np)
		
		# 补光
		fill_light = DirectionalLight("fill_light")
		fill_light.setColor(Vec4(0.3, 0.3, 0.4, 1))
		fill_np = self.render.attachNewNode(fill_light)
		fill_np.setHpr(-45, -30, 0)
		self.render.setLight(fill_np)
		
		# 背光
		back_light = DirectionalLight("back_light")
		back_light.setColor(Vec4(0.2, 0.2, 0.3, 1))
		back_np = self.render.attachNewNode(back_light)
		back_np.setHpr(180, -30, 0)
		self.render.setLight(back_np)
	
	def setup_camera(self):
		"""设置相机"""
		self.disableMouse()
		
		# 初始化相机参数
		self.cam_distance = 25
		self.cam_angle_h = 0
		self.cam_angle_v = 20
		self.target_pos = Point3(0, 20, 0)
		
		# 更新相机位置
		self.update_camera()
		
		# 添加相机控制任务
		self.taskMgr.add(self.camera_control_task, "CameraControlTask")
	
	def update_camera(self):
		"""更新相机位置"""
		import math
		
		# 球面坐标计算
		rad_h = math.radians(self.cam_angle_h)
		rad_v = math.radians(self.cam_angle_v)
		
		x = self.cam_distance * math.sin(rad_h) * math.cos(rad_v)
		y = self.cam_distance * math.cos(rad_h) * math.cos(rad_v)
		z = self.cam_distance * math.sin(rad_v)
		
		# 设置相机位置
		self.camera.setPos(x, y - self.cam_distance, z + 5)
		self.camera.lookAt(self.target_pos)
	
	def camera_control_task(self, task):
		"""相机控制任务"""
		# 这里可以添加平滑相机移动等效果
		return task.cont
	
	def setup_ground(self):
		"""设置地面"""
		cm = CardMaker("ground")
		cm.setFrame(-50, 50, -50, 50)
		
		ground = self.render.attachNewNode(cm.generate())
		ground.setPos(0, 20, -1)
		ground.setColor(0.2, 0.25, 0.3, 1)
		
		# 添加网格
		self.create_ground_grid()
	
	def create_ground_grid(self):
		"""创建地面网格"""
		from panda3d.core import LineSegs
		
		ls = LineSegs()
		ls.setThickness(1)
		ls.setColor(0.3, 0.35, 0.4, 0.5)
		
		# 绘制网格线
		for i in range(-40, 41, 5):
			ls.moveTo(i, -20, 0)
			ls.drawTo(i, 60, 0)
			
			ls.moveTo(-40, i + 20, 0)
			ls.drawTo(40, i + 20, 0)
		
		grid = self.render.attachNewNode(ls.create())
		grid.setZ(-0.5)
	
	def setup_ui(self):
		"""设置用户界面"""
		# 动画信息显示
		self.anim_text = self.create_text_node(
			"当前动画: 无",
			(0.8, 0, 0.9),  # 位置
			0.06,  # 缩放
			(1, 1, 0.8, 1)  # 颜色
		)
		
		# 模型信息显示
		model_info = f"动画数量: {len(self.animations_list)}"
		self.model_text = self.create_text_node(
			model_info,
			(0.8, 0, 0.82),
			0.05,
			(0.8, 0.9, 1, 1)
		)
		
		# 控制说明
		controls = [
			"控制说明:",
			"鼠标拖拽 - 旋转视图",
			"滚轮 - 缩放视图",
			"方向键 - 移动模型",
			"空格键 - 重置模型",
			"R键 - 停止/恢复动画",
			"F键 - 切换线框模式",
			"1-9键 - 切换动画",
			"ESC键 - 退出"
		]
		
		self.control_text = self.create_text_node(
			"\n".join(controls),
			(-1.3, 0, 0.9),
			0.05,
			(0.9, 0.9, 0.7, 1)
		)
		
		# 状态信息
		self.status_text = self.create_text_node(
			"就绪",
			(0, 0, -0.9),
			0.06,
			(1, 0.8, 0.5, 1)
		)
	
	def create_text_node(self, text, pos, scale, color):
		"""创建文本节点"""
		node = TextNode(text[:10])
		node.setText(text)
		node.setTextColor(*color)
		node.setAlign(TextNode.A_left)
		
		np = self.aspect2d.attachNewNode(node)
		np.setScale(scale)
		np.setPos(*pos)
		
		return np
	
	def add_status_message(self, message, duration=3):
		"""添加状态消息"""
		if hasattr(self, 'status_text'):
			self.status_text.node().setText(message)
			
			# 定时清除消息
			def clear_message(task):
				self.status_text.node().setText("就绪")
				return task.done
			
			self.taskMgr.doMethodLater(duration, clear_message, "ClearStatus")
	
	def setup_controls(self):
		"""设置控制"""
		# 退出
		self.accept("escape", self.userExit)
		
		# 模型控制
		self.accept("space", self.reset_model)
		self.accept("r", self.toggle_animation)
		self.accept("f", self.toggle_wireframe)
		
		# 动画切换 (1-9键)
		for i in range(1, 10):
			if i <= len(self.animations_list):
				anim_name = self.animations_list[i - 1]
				self.accept(str(i), self.play_animation, [anim_name])
		
		# 方向键控制模型移动
		self.move_speed = 0.5
		self.move_state = {
			"left": False, "right": False,
			"up": False, "down": False,
			"forward": False, "backward": False
		}
		
		# 绑定方向键
		key_bindings = [
			("arrow_left", "left", True), ("arrow_left-up", "left", False),
			("arrow_right", "right", True), ("arrow_right-up", "right", False),
			("arrow_up", "forward", True), ("arrow_up-up", "forward", False),
			("arrow_down", "backward", True), ("arrow_down-up", "backward", False),
			("w", "up", True), ("w-up", "up", False),
			("s", "down", True), ("s-up", "down", False),
		]
		
		for event, key, state in key_bindings:
			self.accept(event, self.set_move_state, [key, state])
		
		# 相机控制
		self.accept("wheel_up", self.zoom_camera, [1])
		self.accept("wheel_down", self.zoom_camera, [-1])
		
		# 鼠标控制
		self.is_dragging = False
		self.last_mouse_pos = (0, 0)
		
		self.accept("mouse1", self.start_mouse_drag)
		self.accept("mouse1-up", self.stop_mouse_drag)
		
		# 动画控制
		self.accept("a", self.previous_animation)
		self.accept("d", self.next_animation)
		self.accept("q", self.slower_animation)
		self.accept("e", self.faster_animation)
		
		# 添加移动任务
		self.taskMgr.add(self.update_model_movement, "UpdateMovementTask")
	
	def set_move_state(self, key, state):
		"""设置移动状态"""
		self.move_state[key] = state
	
	def update_model_movement(self, task):
		"""更新模型移动"""
		if self.actor:
			pos = self.actor.getPos()
			
			if self.move_state["left"]:
				pos.x -= self.move_speed
			if self.move_state["right"]:
				pos.x += self.move_speed
			if self.move_state["forward"]:
				pos.y += self.move_speed
			if self.move_state["backward"]:
				pos.y -= self.move_speed
			if self.move_state["up"]:
				pos.z += self.move_speed
			if self.move_state["down"]:
				pos.z -= self.move_speed
			
			self.actor.setPos(pos)
			self.target_pos = pos  # 更新相机目标
		
		return task.cont
	
	def start_mouse_drag(self):
		"""开始鼠标拖拽"""
		if self.mouseWatcherNode.hasMouse():
			self.is_dragging = True
			self.last_mouse_pos = (
				self.mouseWatcherNode.getMouseX(),
				self.mouseWatcherNode.getMouseY()
			)
	
	def stop_mouse_drag(self):
		"""停止鼠标拖拽"""
		self.is_dragging = False
	
	def zoom_camera(self, direction):
		"""缩放相机"""
		zoom_speed = 2
		self.cam_distance = max(5, min(50, self.cam_distance - direction * zoom_speed))
		self.update_camera()
	
	def reset_model(self):
		"""重置模型位置和旋转"""
		if self.actor:
			self.actor.setPos(0, 20, 0)
			self.actor.setHpr(180, 0, 0)
			self.target_pos = Point3(0, 20, 0)
			self.add_status_message("模型已重置")
	
	def toggle_animation(self):
		"""切换动画播放状态"""
		if self.actor and self.current_animation:
			try:
				anim_control = self.actor.getAnimControl(self.current_animation)
				if anim_control:
					if anim_control.isPlaying():
						anim_control.stop()
						self.add_status_message(f"停止动画: {self.current_animation}")
					else:
						anim_control.play()
						self.add_status_message(f"继续动画: {self.current_animation}")
			except:
				pass
	
	def toggle_wireframe(self):
		"""切换线框模式"""
		if self.actor:
			current = self.actor.getWireframe()
			self.actor.setWireframe(not current)
			state = "开启" if not current else "关闭"
			self.add_status_message(f"线框模式: {state}")
	
	def previous_animation(self):
		"""切换到上一个动画"""
		if self.animations_list and self.current_animation:
			current_idx = self.animations_list.index(self.current_animation)
			new_idx = (current_idx - 1) % len(self.animations_list)
			self.play_animation(self.animations_list[new_idx])
	
	def next_animation(self):
		"""切换到下一个动画"""
		if self.animations_list and self.current_animation:
			current_idx = self.animations_list.index(self.current_animation)
			new_idx = (current_idx + 1) % len(self.animations_list)
			self.play_animation(self.animations_list[new_idx])
	
	def slower_animation(self):
		"""减慢动画速度"""
		if self.actor and self.current_animation:
			try:
				anim_control = self.actor.getAnimControl(self.current_animation)
				if anim_control:
					current_rate = anim_control.getPlayRate()
					new_rate = max(0.1, current_rate * 0.8)
					anim_control.setPlayRate(new_rate)
					self.add_status_message(f"动画速度: {new_rate:.1f}x")
			except:
				pass
	
	def faster_animation(self):
		"""加快动画速度"""
		if self.actor and self.current_animation:
			try:
				anim_control = self.actor.getAnimControl(self.current_animation)
				if anim_control:
					current_rate = anim_control.getPlayRate()
					new_rate = min(5.0, current_rate * 1.25)
					anim_control.setPlayRate(new_rate)
					self.add_status_message(f"动画速度: {new_rate:.1f}x")
			except:
				pass
	
	def start_main_loop(self):
		"""开始主循环"""
		print("=" * 50)
		print("动画模型查看器已启动")
		print("=" * 50)
		
		# 添加鼠标拖拽更新任务
		self.taskMgr.add(self.update_mouse_drag, "UpdateMouseDragTask")
	
	def update_mouse_drag(self, task):
		"""更新鼠标拖拽"""
		if self.is_dragging and self.mouseWatcherNode.hasMouse():
			current_x = self.mouseWatcherNode.getMouseX()
			current_y = self.mouseWatcherNode.getMouseY()
			
			dx = current_x - self.last_mouse_pos[0]
			dy = current_y - self.last_mouse_pos[1]
			
			# 更新相机角度
			self.cam_angle_h += dx * 100
			self.cam_angle_v = max(-80, min(80, self.cam_angle_v - dy * 50))
			
			self.update_camera()
			
			self.last_mouse_pos = (current_x, current_y)
		
		return task.cont


# 运行应用程序
if __name__ == "__main__":
	try:
		app = AnimatedModelViewer()
		app.run()
	except Exception as e:
		print(f"程序启动失败: {e}")
		import traceback
		
		traceback.print_exc()
		input("按Enter键退出...")