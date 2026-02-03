# 在 Ursina 窗口中添加 UI 界面

是的，Ursina 提供了完整的 UI 系统，可以在窗口中轻松添加各种 UI 界面。以下是详细的 UI 组件使用方法和示例：

## 1. 基础 UI 组件

### 1.1 创建基本 UI

```python
from ursina import *

app = Ursina()

# 创建 UI 面板
panel = Panel(
    scale=(0.8, 0.6),      # 面板大小
    color=color.dark_gray, # 背景颜色
    texture='white_cube',  # 背景纹理
    position=(0, 0, 0)     # 位置
)

# 创建文本标签
title = Text(
    text='游戏菜单',
    origin=(0, 0),
    y=0.35,                # 垂直位置
    scale=2,               # 文本大小
    color=color.white
)

# 创建按钮
start_button = Button(
    text='开始游戏',
    color=color.green,
    highlight_color=color.lime,
    pressed_color=color.dark_green,
    scale=(0.3, 0.1),      # 宽度, 高度
    position=(0, 0.1),     # 位置
    text_color=color.white
)

settings_button = Button(
    text='设置',
    color=color.blue,
    highlight_color=color.light_blue,
    scale=(0.2, 0.08),
    position=(0, -0.05)
)

quit_button = Button(
    text='退出游戏',
    color=color.red,
    highlight_color=color.pink,
    scale=(0.25, 0.09),
    position=(0, -0.2)
)

# 按钮点击事件
def on_start_click():
    print("开始游戏!")
    start_button.text = "游戏中..."
    start_button.color = color.gray

def on_settings_click():
    print("打开设置")
    # 可以在这里添加设置界面

def on_quit_click():
    application.quit()

start_button.on_click = on_start_click
settings_button.on_click = on_settings_click
quit_button.on_click = on_quit_click

app.run()
```

## 2. 完整的游戏 HUD（抬头显示）示例

```python
from ursina import *

app = Ursina()

# 3D游戏世界
player = Entity(model='cube', color=color.blue, scale=(1,2,1), position=(0,1,0))
ground = Entity(model='plane', texture='grass', scale=(20,1,20))

# ============ HUD 界面 ============
class GameHUD:
    def __init__(self):
        # 顶部状态栏
        self.health_bar = Entity(
            parent=camera.ui,
            model='quad',
            color=color.red,
            scale=(0.4, 0.04),
            position=(-0.7, 0.45)
        )
        
        self.health_text = Text(
            text='生命值: 100',
            parent=camera.ui,
            position=(-0.7, 0.4),
            scale=0.8
        )
        
        # 分数显示
        self.score_text = Text(
            text='分数: 0',
            parent=camera.ui,
            position=(0.7, 0.45),
            scale=1,
            color=color.yellow
        )
        
        # 武器信息
        self.weapon_slot = Entity(
            parent=camera.ui,
            model='quad',
            texture='sword_icon',
            scale=(0.08, 0.08),
            position=(-0.85, -0.4),
            color=color.white
        )
        
        self.ammo_text = Text(
            text='弹药: ∞',
            parent=camera.ui,
            position=(-0.85, -0.47),
            scale=0.7
        )
        
        # 小地图框架
        self.minimap_bg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.dark_gray,
            scale=(0.15, 0.15),
            position=(0.85, 0.4)
        )
        
        # 按键提示
        self.key_hint = Text(
            text='WASD:移动  空格:跳跃  F:互动',
            parent=camera.ui,
            position=(0, -0.45),
            scale=0.6,
            color=color.light_gray
        )
        
        # 时间显示
        self.time_text = Text(
            text='时间: 00:00',
            parent=camera.ui,
            position=(0.7, -0.45),
            scale=0.7
        )
        
        self.score = 0
        self.health = 100
        self.time_elapsed = 0
    
    def update(self):
        self.time_elapsed += time.dt
        minutes = int(self.time_elapsed // 60)
        seconds = int(self.time_elapsed % 60)
        self.time_text.text = f'时间: {minutes:02d}:{seconds:02d}'
        
        # 更新生命条
        health_percent = self.health / 100
        self.health_bar.scale_x = 0.4 * health_percent
    
    def add_score(self, points):
        self.score += points
        self.score_text.text = f'分数: {self.score}'
    
    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        self.health_text.text = f'生命值: {self.health}'
        if self.health <= 0:
            self.show_game_over()

# 创建 HUD
hud = GameHUD()

def update():
    hud.update()
    
    # 简单控制
    player.x += held_keys['d'] * time.dt * 3
    player.x -= held_keys['a'] * time.dt * 3
    player.z += held_keys['w'] * time.dt * 3
    player.z -= held_keys['s'] * time.dt * 3
    
    # 空格键加分
    if held_keys['space']:
        hud.add_score(1)

app.run()
```

## 3. 交互式设置菜单

```python
from ursina import *

app = Ursina()

class SettingsMenu:
    def __init__(self):
        # 主面板
        self.panel = Entity(
            parent=camera.ui,
            model='quad',
            color=color.dark_gray,
            scale=(0.7, 0.8),
            position=(0, 0)
        )
        
        # 标题
        self.title = Text(
            parent=camera.ui,
            text='游戏设置',
            scale=2,
            y=0.35,
            color=color.white
        )
        
        # 音量控制滑块
        self.volume_label = Text(
            parent=camera.ui,
            text='音量',
            scale=1.2,
            y=0.15,
            x=-0.2,
            color=color.white
        )
        
        self.volume_slider = Slider(
            parent=camera.ui,
            min=0,
            max=1,
            default=0.5,
            step=0.1,
            x=0.1,
            y=0.15,
            scale=(0.3, 0.03)
        )
        
        self.volume_value = Text(
            parent=camera.ui,
            text='50%',
            scale=0.8,
            y=0.15,
            x=0.3,
            color=color.yellow
        )
        
        # 画质选择
        self.quality_label = Text(
            parent=camera.ui,
            text='画质',
            scale=1.2,
            y=0.05,
            x=-0.2,
            color=color.white
        )
        
        self.quality_dropdown = DropdownMenu(
            parent=camera.ui,
            options=['低', '中', '高', '极高'],
            default='中',
            x=0.1,
            y=0.05,
            scale=(0.3, 0.05)
        )
        
        # 全屏切换
        self.fullscreen_toggle = Button(
            parent=camera.ui,
            text='全屏: 关闭',
            color=color.gray,
            highlight_color=color.light_gray,
            scale=(0.25, 0.06),
            y=-0.05,
            x=-0.1
        )
        
        # 垂直同步切换
        self.vsync_toggle = Button(
            parent=camera.ui,
            text='垂直同步: 开启',
            color=color.blue,
            highlight_color=color.light_blue,
            scale=(0.25, 0.06),
            y=-0.05,
            x=0.2
        )
        
        # 分辨率选择
        self.resolution_label = Text(
            parent=camera.ui,
            text='分辨率',
            scale=1.2,
            y=-0.15,
            x=-0.2,
            color=color.white
        )
        
        self.resolution_buttons = []
        resolutions = ['1280x720', '1920x1080', '2560x1440']
        for i, res in enumerate(resolutions):
            btn = Button(
                parent=camera.ui,
                text=res,
                color=color.dark_gray,
                highlight_color=color.gray,
                scale=(0.15, 0.05),
                y=-0.15,
                x=-0.1 + i * 0.2
            )
            self.resolution_buttons.append(btn)
        
        # 控制按钮
        self.save_button = Button(
            parent=camera.ui,
            text='保存设置',
            color=color.green,
            highlight_color=color.lime,
            scale=(0.2, 0.07),
            y=-0.3,
            x=-0.15
        )
        
        self.cancel_button = Button(
            parent=camera.ui,
            text='取消',
            color=color.red,
            highlight_color=color.pink,
            scale=(0.2, 0.07),
            y=-0.3,
            x=0.15
        )
        
        # 绑定事件
        self.volume_slider.on_value_changed = self.on_volume_change
        self.fullscreen_toggle.on_click = self.toggle_fullscreen
        self.vsync_toggle.on_click = self.toggle_vsync
        self.save_button.on_click = self.save_settings
        self.cancel_button.on_click = self.hide
    
    def on_volume_change(self):
        volume = int(self.volume_slider.value * 100)
        self.volume_value.text = f'{volume}%'
        # 这里可以设置实际音量
    
    def toggle_fullscreen(self):
        window.fullscreen = not window.fullscreen
        self.fullscreen_toggle.text = f'全屏: {"开启" if window.fullscreen else "关闭"}'
    
    def toggle_vsync(self):
        window.vsync = not window.vsync
        self.vsync_toggle.text = f'垂直同步: {"开启" if window.vsync else "关闭"}'
    
    def save_settings(self):
        print("设置已保存!")
        self.hide()
    
    def show(self):
        self.panel.enabled = True
        for child in self.panel.children:
            child.enabled = True
    
    def hide(self):
        self.panel.enabled = False
        for child in self.panel.children:
            child.enabled = False

# 创建主菜单
class MainMenu:
    def __init__(self):
        self.panel = Entity(
            parent=camera.ui,
            model='quad',
            color=color.rgba(0, 0, 0, 200),
            scale=(1, 1),
            position=(0, 0)
        )
        
        self.title = Text(
            parent=camera.ui,
            text='我的游戏',
            scale=3,
            y=0.3,
            color=color.gold
        )
        
        self.start_button = Button(
            parent=camera.ui,
            text='开始游戏',
            color=color.green,
            scale=(0.3, 0.1),
            y=0.1
        )
        
        self.settings_button = Button(
            parent=camera.ui,
            text='设置',
            color=color.blue,
            scale=(0.25, 0.08),
            y=-0.05
        )
        
        self.quit_button = Button(
            parent=camera.ui,
            text='退出游戏',
            color=color.red,
            scale=(0.2, 0.07),
            y=-0.2
        )
        
        self.settings_menu = SettingsMenu()
        self.settings_menu.hide()  # 初始隐藏设置菜单
        
        # 绑定事件
        self.start_button.on_click = self.start_game
        self.settings_button.on_click = self.open_settings
        self.quit_button.on_click = application.quit
    
    def start_game(self):
        print("开始游戏!")
        self.hide()
        # 这里可以开始游戏逻辑
    
    def open_settings(self):
        self.settings_menu.show()
    
    def hide(self):
        self.panel.enabled = False
        for child in self.panel.children:
            child.enabled = False

# 创建主菜单
main_menu = MainMenu()

app.run()
```

## 4. 动态 UI 更新示例

```python
from ursina import *

app = Ursina()

# 创建3D游戏场景
player = Entity(model='cube', color=color.blue, position=(0, 2, -5))
ground = Entity(model='plane', scale=20, color=color.green)
sky = Sky()

# 创建动态UI
class DynamicUI:
    def __init__(self):
        # 显示玩家坐标
        self.coords_text = Text(
            parent=camera.ui,
            text='位置: (0, 2, -5)',
            position=(-0.85, 0.45),
            color=color.white
        )
        
        # 显示帧率
        self.fps_text = Text(
            parent=camera.ui,
            text='FPS: 0',
            position=(-0.85, 0.4),
            color=color.yellow
        )
        
        # 显示按键状态
        self.key_status = Text(
            parent=camera.ui,
            text='按键: 无',
            position=(-0.85, 0.35),
            color=color.light_gray
        )
        
        # 创建任务列表
        self.tasks = []
        task_texts = [
            '找到钥匙',
            '打开宝箱',
            '击败怪物',
            '找到出口'
        ]
        
        for i, task in enumerate(task_texts):
            task_text = Text(
                parent=camera.ui,
                text=f'□ {task}',
                position=(0.7, 0.4 - i * 0.05),
                color=color.gray
            )
            self.tasks.append(task_text)
        
        # 进度条
        self.progress_bg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.dark_gray,
            scale=(0.3, 0.03),
            position=(0, -0.45)
        )
        
        self.progress_fg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.green,
            scale=(0, 0.03),
            position=(-0.15, -0.45)
        )
        
        self.progress_text = Text(
            parent=camera.ui,
            text='进度: 0%',
            position=(0, -0.4),
            color=color.white
        )
        
        self.progress = 0
    
    def update(self):
        # 更新坐标
        self.coords_text.text = f'位置: ({player.x:.1f}, {player.y:.1f}, {player.z:.1f})'
        
        # 更新帧率
        fps = int(1 / time.dt) if time.dt > 0 else 0
        self.fps_text.text = f'FPS: {fps}'
        
        # 更新按键状态
        pressed_keys = [k for k in ['w', 'a', 's', 'd', 'space'] if held_keys[k]]
        if pressed_keys:
            self.key_status.text = f'按键: {", ".join(pressed_keys)}'
        else:
            self.key_status.text = '按键: 无'
        
        # 更新进度条
        if held_keys['p']:  # 按P键增加进度
            self.progress = min(1, self.progress + time.dt * 0.1)
            self.progress_fg.scale_x = 0.3 * self.progress
            self.progress_text.text = f'进度: {int(self.progress * 100)}%'
            
            # 完成任务
            if self.progress >= 0.25 and self.tasks[0].color != color.green:
                self.tasks[0].text = '✓ 找到钥匙'
                self.tasks[0].color = color.green
            if self.progress >= 0.5 and self.tasks[1].color != color.green:
                self.tasks[1].text = '✓ 打开宝箱'
                self.tasks[1].color = color.green
            if self.progress >= 0.75 and self.tasks[2].color != color.green:
                self.tasks[2].text = '✓ 击败怪物'
                self.tasks[2].color = color.green
            if self.progress >= 1.0 and self.tasks[3].color != color.green:
                self.tasks[3].text = '✓ 找到出口'
                self.tasks[3].color = color.green

# 创建动态UI
dynamic_ui = DynamicUI()

def update():
    dynamic_ui.update()
    
    # 简单玩家控制
    player.x += held_keys['d'] * time.dt * 5
    player.x -= held_keys['a'] * time.dt * 5
    player.z += held_keys['w'] * time.dt * 5
    player.z -= held_keys['s'] * time.dt * 5
    
    if held_keys['space']:
        player.y += time.dt * 3
    else:
        player.y = max(0, player.y - time.dt * 3)

app.run()
```

## 5. 重要提示和最佳实践

### 5.1 UI 层级管理
```python
# 使用 parent=camera.ui 确保UI在2D空间
Entity(parent=camera.ui, ...)

# 使用 z 值控制层级
background = Entity(parent=camera.ui, z=1, ...)
button = Entity(parent=camera.ui, z=2, ...)  # 按钮在背景上方
```

### 5.2 响应式设计
```python
# 根据屏幕大小调整UI
def on_resize():
    button.scale = (window.aspect_ratio * 0.1, 0.05)

# 或者使用相对位置
button.position = (0.5 * window.aspect_ratio - 0.1, 0)
```

### 5.3 性能优化
```python
# 1. 批量更新UI
def update_ui_elements():
    # 避免每帧都创建/销毁UI
    pass

# 2. 使用 enabled 属性隐藏UI而非销毁
ui_panel.enabled = False

# 3. 减少UI元素数量
# 合并相关元素，使用图标代替文字等
```

这些示例展示了在 Ursina 中创建各种 UI 界面的方法。你可以根据游戏需求组合使用这些组件，创建出功能丰富、美观的界面。