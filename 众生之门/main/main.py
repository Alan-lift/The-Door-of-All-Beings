import time
from ursina.prefabs.first_person_controller import FirstPersonController
import ursina
import system
import _entities
from python_ import print
app = ursina.Ursina()

# 创建文本对象
text = _entities.Text(text="", position=(0, 0), scale=2)
counter = 0

def update_text():
	global counter
	counter += 1
	return  f"count: {counter}"

# 使用Sequence设置循环更新
text.update_text(lambda :f'{time.time()}', 300)

def input(key):
	if key == 'q':
		text.stop()
	if key == 'w':
		text.delete()

system.setup_mouse_control_system()
app.run()