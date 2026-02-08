import time
from ursina.prefabs.first_person_controller import FirstPersonController
import ursina
import system
import ursina_Text

from python_ import print
app = ursina.Ursina()

# 创建文本对象
text = ursina_Text.Text(text="111", scale=2,)
counter = 0
text.auto_align_text(text)
def update_text():
	global counter
	counter += 1
	return  f"count: {counter}"

# 使用Sequence设置循环更新
text.update_text(lambda :f'{time.time()}', 30)

def input(key):
	if key == 'q':
		text.stop()
	if key == 'w':
		text.delete()

system.setup_mouse_control_system()
app.run()