from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import *
import system
import _entities
app = Ursina()

# 创建文本对象
text = _entities.Text(text="初始值: 0", position=(-0.5, 0.4), scale=2)
counter = 0

def update_text():
    global counter
    counter += 1
    return  f"计数: {counter}"

# 使用Sequence设置循环更新
text.update_text(update_text, 300)

system.setup_mouse_control_system()
app.run()