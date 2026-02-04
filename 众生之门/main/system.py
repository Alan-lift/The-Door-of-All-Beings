import ursina
from log import log

# 1. 退出鼠标控制类（解锁鼠标）
class MouseExitControl:
	def __init__(self):
		log("鼠标控制","退出控制模式")
	
	def execute(self):
		"""解锁鼠标并使其可见"""
		if ursina.mouse.locked:
			ursina.mouse.locked = False
			ursina.mouse.visible = True
			log("鼠标控制器", "鼠标已解锁", explore="可自由移动")
		return True


# 2. 进入鼠标控制类（锁定鼠标）
class MouseEnterControl:
	def __init__(self):
		log("鼠标控制器", "进入控制模式")
	
	def execute(self):
		"""锁定鼠标并隐藏"""
		if not ursina.mouse.locked:
			ursina.mouse.locked = True
			ursina.mouse.visible = False
			log("鼠标控制器", "鼠标已锁定", explore="用于控制视角")
		return True


# 3. 单击屏幕进入控制类
class ScreenClickHandler:
	def __init__(self, mouse_enter_control=None):
		"""
		初始化屏幕点击处理器
		:param mouse_enter_control: MouseEnterControl实例
		"""
		self.mouse_enter_control = mouse_enter_control or MouseEnterControl()
		log("点击处理器", "初始化完成")
	
	def execute(self):
		"""处理屏幕点击事件，进入鼠标控制模式"""
		log("点击处理器", "检测到屏幕点击")
		if self.mouse_enter_control:
			return self.mouse_enter_control.execute()
		return False
	
	def setup_listener(self):
		"""设置鼠标点击监听"""
		# 创建空实体来处理更新
		self.handler = ursina.Entity()
		self.handler.update = self._check_click
	
	def _check_click(self):
		"""每帧检查鼠标点击"""
		if not ursina.mouse.locked:
			# 检查任意鼠标按键是否按下
			if ursina.mouse.left or ursina.mouse.right or ursina.mouse.middle:
				self.execute()


# 4. 按键退出控制类
class KeyExitControl:
	def __init__(self, key='escape', mouse_exit_control=None):
		"""
		初始化按键退出控制器
		:param key: 触发退出的按键（默认为'escape'）
		:param mouse_exit_control: MouseExitControl实例
		"""
		self.key = key
		self.mouse_exit_control = mouse_exit_control or MouseExitControl()
		self.key_pressed = False  # 防止重复触发
		log("按键退出器", "初始化完成", explore=f"退出键：{key}")
	
	def execute(self):
		"""执行按键退出逻辑"""
		log("按键退出器", f"检测到{self.key}键按下")
		if self.mouse_exit_control:
			return self.mouse_exit_control.execute()
		return False
	
	def setup_listener(self):
		"""设置按键监听"""
		self.handler = ursina.Entity()
		self.handler.update = self._check_key
	
	def _check_key(self):
		"""每帧检查按键状态"""
		if ursina.held_keys[self.key]:
			if not self.key_pressed:
				self.execute()
				self.key_pressed = True
		else:
			self.key_pressed = False


# 5. ESC键调用退出，同时设置点击重新进入
def setup_mouse_control_system(
		exit_key='escape',
		mouse_exit_control=None,
		mouse_enter_control=None,
		screen_click_handler=None,
		key_exit_control=None
):
	"""
	设置完整的鼠标控制系统
	:param exit_key: 退出控制模式的按键
	:param mouse_exit_control: 自定义退出控制实例
	:param mouse_enter_control: 自定义进入控制实例
	:param screen_click_handler: 自定义屏幕点击处理器
	:param key_exit_control: 自定义按键退出控制器
	:return: 包含所有控制器的字典
	"""
	
	# 1. 创建基础控制实例
	if mouse_exit_control is None:
		mouse_exit_control = MouseExitControl()
	
	if mouse_enter_control is None:
		mouse_enter_control = MouseEnterControl()
	
	# 2. 设置初始状态
	mouse_enter_control.execute()
	
	# 3. 创建屏幕点击处理器
	if screen_click_handler is None:
		screen_click_handler = ScreenClickHandler(mouse_enter_control)
	screen_click_handler.setup_listener()
	
	# 4. 创建按键退出控制器
	if key_exit_control is None:
		key_exit_control = KeyExitControl(key=exit_key, mouse_exit_control=mouse_exit_control)
	key_exit_control.setup_listener()
	
	# 5. 创建组合控制器来同时监听ESC键和点击
	combo_handler = ursina.Entity()
	combo_handler.update = lambda: None  # 由子组件处理
	
	log("鼠标控制系统","初始化完成")
	log("鼠标控制系统",f"退出控制键: {exit_key}")
	
	return {
		'mouse_exit': mouse_exit_control,
		'mouse_enter': mouse_enter_control,
		'screen_click': screen_click_handler,
		'key_exit': key_exit_control,
		'combo_handler': combo_handler
	}
