# Ursina 组件常用参数详解

以下是 Ursina 各个主要组件的常用参数及其含义的表格：

## 1. Entity（实体）组件

| 参数         | 类型       | 默认值         | 含义                                             |
|------------|----------|-------------|------------------------------------------------|
| `model`    | str/Mesh | None        | 3D模型，如 `cube`、`sphere`、`plane`、`quad`或`模型文件路径` |
| `texture`  | str      | None        | 纹理贴图路径或名称                                      |
| `color`    | Color    | color.white | 实体颜色，可包含透明度                                    |
| `position` | Vec3     | (0,0,0)     | 世界坐标系中的位置 (x,y,z)                              |
| `rotation` | Vec3     | (0,0,0)     | 旋转角度 (x,y,z 轴)                                 |
| `scale`    | Vec3     | (1,1,1)     | 缩放比例 (x,y,z 轴)                                 |
| `origin`   | Vec3     | (0,0,0)     | 原点偏移，影响旋转中心                                    |
| `collider` | str      | None        | 碰撞体类型：'box'、'sphere'、'mesh'                    |
| `shader`   | Shader   | None        | 着色器，如 basic_lighting_shader                    |
| `eternal`  | bool     | False       | 是否永久存在（不被自动清理）                                 |
| `ignore`   | bool     | False       | 是否忽略场景管理                                       |
| `parent`   | Entity   | scene       | 父实体                                            |
| `enabled`  | bool     | True        | 是否启用                                           |
| `visible`  | bool     | True        | 是否可见                                           |

## 2. Camera（相机）组件

| 参数                  | 类型     | 默认值     | 含义                  |
|---------------------|--------|---------|---------------------|
| `position`          | Vec3   | (0,0,0) | 相机位置                |
| `rotation`          | Vec3   | (0,0,0) | 相机旋转                |
| `fov`               | float  | 40      | 视野角度（Field of View） |
| `orthographic`      | bool   | False   | 是否正交投影              |
| `orthographic_size` | float  | 6       | 正交投影时的视口大小          |
| `near_plane`        | float  | 0.1     | 近裁剪平面               |
| `far_plane`         | float  | 100     | 远裁剪平面               |
| `clip_plane_near`   | float  | 0.1     | 近裁剪面                |
| `clip_plane_far`    | float  | 100     | 远裁剪面                |
| `ui_size`           | float  | 1       | UI元素的大小缩放           |
| `ui_parent`         | Entity | None    | UI元素的父实体            |

## 3. Light（光源）组件

| 参数                      | 类型    | 默认值         | 含义                                |
|-------------------------|-------|-------------|-----------------------------------|
| `type`                  | str   | 'point'     | 光源类型：'point'、'directional'、'spot' |
| `color`                 | Color | color.white | 光源颜色                              |
| `intensity`             | float | 1           | 光源强度                              |
| `range`                 | float | 10          | 光源影响范围（点光源）                       |
| `shadows`               | bool  | False       | 是否投射阴影                            |
| `shadow_map_resolution` | tuple | (1024,1024) | 阴影贴图分辨率                           |
| `direction`             | Vec3  | (0,-1,0)    | 方向光的方向                            |
| `spot_angle`            | float | 30          | 聚光灯的角度                            |
| `falloff`               | float | 1           | 衰减系数                              |

## 4. UI 组件参数

### 4.1 Button（按钮）

| 参数                | 类型    | 默认值              | 含义      |
|-------------------|-------|------------------|---------|
| `text`            | str   | ''               | 按钮显示的文本 |
| `icon`            | str   | None             | 按钮图标路径  |
| `color`           | Color | color.gray       | 正常状态颜色  |
| `highlight_color` | Color | color.light_gray | 鼠标悬停颜色  |
| `pressed_color`   | Color | color.dark_gray  | 按下状态颜色  |
| `text_color`      | Color | color.black      | 文本颜色    |
| `text_size`       | float | 1                | 文本大小    |
| `scale`           | Vec2  | (0.1,0.05)       | 按钮缩放    |
| `radius`          | float | 0.05             | 圆角半径    |
| `enabled`         | bool  | True             | 是否启用    |

### 4.2 Text（文本）

| 参数            | 类型    | 默认值         | 含义                   |
|---------------|-------|-------------|----------------------|
| `text`        | str   | ''          | 显示的文本内容              |
| `font`        | str   | None        | 字体文件路径               |
| `size`        | float | 0.025       | 文本大小                 |
| `color`       | Color | color.black | 文本颜色                 |
| `background`  | bool  | False       | 是否有背景                |
| `bg_color`    | Color | color.white | 背景颜色                 |
| `origin`      | Vec2  | (0,0)       | 文本对齐方式：(-0.5,0.5)=左上 |
| `wordwrap`    | int   | 0           | 自动换行宽度（字符数）          |
| `line_height` | float | 1           | 行高                   |
| `ignore`      | bool  | False       | 是否忽略场景管理             |

### 4.3 InputField（输入框）

| 参数                   | 类型     | 默认值     | 含义     |
|----------------------|--------|---------|--------|
| `text`               | str    | ''      | 初始文本   |
| `default_text`       | str    | ''      | 默认提示文本 |
| `active`             | bool   | True    | 是否激活   |
| `max_length`         | int    | 24      | 最大输入长度 |
| `character_limit`    | str    | None    | 允许的字符集 |
| `input_field_parent` | Entity | None    | 父实体    |
| `submit_on`          | str    | 'enter' | 提交按键   |
| `clear_on_submit`    | bool   | False   | 提交后清空  |

## 5. Animation（动画）参数

| 参数          | 类型       | 默认值          | 含义                          |
|-------------|----------|--------------|-----------------------------|
| `duration`  | float    | 1            | 动画持续时间（秒）                   |
| `delay`     | float    | 0            | 开始前的延迟时间                    |
| `curve`     | function | curve.linear | 动画曲线函数                      |
| `loop`      | bool     | False        | 是否循环播放                      |
| `ping_pong` | bool     | False        | 是否乒乓式循环                     |
| `interrupt` | str      | 'finish'     | 中断方式：'finish'、'kill'、'stop' |
| `smoothing` | float    | 0            | 平滑系数                        |
| `speed`     | float    | 1            | 播放速度                        |

## 6. Audio（音频）参数

| 参数           | 类型    | 默认值   | 含义           |
|--------------|-------|-------|--------------|
| `file_name`  | str   | ''    | 音频文件路径       |
| `autoplay`   | bool  | True  | 是否自动播放       |
| `loop`       | bool  | False | 是否循环播放       |
| `volume`     | float | 1     | 音量大小（0-1）    |
| `balance`    | float | 0     | 声道平衡（-1左到1右） |
| `pitch`      | float | 1     | 音调           |
| `start_time` | float | 0     | 开始播放时间（秒）    |
| `fade_in`    | float | 0     | 淡入时间（秒）      |
| `fade_out`   | float | 0     | 淡出时间（秒）      |

## 7. Collider（碰撞体）参数

| 参数            | 类型    | 默认值       | 含义                          |
|---------------|-------|-----------|-----------------------------|
| `type`        | str   | 'box'     | 碰撞体类型：'box'、'sphere'、'mesh' |
| `center`      | Vec3  | (0,0,0)   | 碰撞体中心偏移                     |
| `size`        | Vec3  | (1,1,1)   | 碰撞体尺寸（盒体）                   |
| `radius`      | float | 0.5       | 碰撞体半径（球体）                   |
| `visible`     | bool  | False     | 是否显示碰撞体                     |
| `color`       | Color | color.red | 碰撞体显示颜色                     |
| `sensitivity` | float | 0.1       | 碰撞检测灵敏度                     |
| `ignore`      | list  | []        | 忽略碰撞的实体列表                   |

## 8. Mesh（网格）参数

| 参数          | 类型    | 默认值        | 含义                             |
|-------------|-------|------------|--------------------------------|
| `vertices`  | list  | []         | 顶点坐标列表                         |
| `triangles` | list  | []         | 三角形索引列表                        |
| `uvs`       | list  | []         | UV坐标列表                         |
| `normals`   | list  | []         | 法线向量列表                         |
| `colors`    | list  | []         | 顶点颜色列表                         |
| `mode`      | str   | 'triangle' | 渲染模式：'point'、'line'、'triangle' |
| `thickness` | float | 1          | 线框模式下的线宽                       |
| `static`    | bool  | True       | 是否为静态网格                        |

## 9. Window（窗口）参数

| 参数                   | 类型    | 默认值        | 含义        |
|----------------------|-------|------------|-----------|
| `title`              | str   | 'Ursina'   | 窗口标题      |
| `fullscreen`         | bool  | False      | 是否全屏      |
| `borderless`         | bool  | False      | 是否无边框     |
| `size`               | tuple | (1280,720) | 窗口大小（宽,高） |
| `position`           | tuple | None       | 窗口位置（x,y） |
| `vsync`              | bool  | True       | 垂直同步      |
| `show_ursina_splash` | bool  | True       | 是否显示启动画面  |
| `development_mode`   | bool  | True       | 开发模式      |
| `editor_ui_enabled`  | bool  | True       | 是否启用编辑器UI |

## 10. Scene（场景）参数

| 参数                         | 类型    | 默认值         | 含义            |
|----------------------------|-------|-------------|---------------|
| `fog_color`                | Color | color.black | 雾颜色           |
| `fog_density`              | float | 0           | 雾密度           |
| `fog_start`                | float | 10          | 雾开始距离         |
| `fog_end`                  | float | 50          | 雾结束距离         |
| `ambient_light`            | Color | color.black | 环境光颜色         |
| `clear_color`              | Color | color.black | 清除颜色          |
| `reload_shaders_on_change` | bool  | True        | 是否在改变时重新加载着色器 |
| `use_deferred_rendering`   | bool  | False       | 是否使用延迟渲染      |

## 11. Sky（天空盒）参数

| 参数         | 类型     | 默认值           | 含义     |
|------------|--------|---------------|--------|
| `texture`  | str    | 'sky_default' | 天空盒纹理  |
| `scale`    | float  | 100           | 天空盒大小  |
| `rotation` | Vec3   | (0,0,0)       | 天空盒旋转  |
| `color`    | Color  | color.white   | 天空盒颜色  |
| `parent`   | Entity | scene         | 父实体    |
| `eternal`  | bool   | True          | 是否永久存在 |

## 12. 时间相关参数

| 参数                       | 类型    | 默认值 | 含义             |
|--------------------------|-------|-----|----------------|
| `time.dt`                | float | 变化  | 上一帧到当前帧的时间差（秒） |
| `time.time()`            | float | 变化  | 游戏运行总时间（秒）     |
| `application.time_scale` | float | 1   | 时间缩放因子         |
| `application.target_fps` | int   | 60  | 目标帧率           |
| `application.max_fps`    | int   | 0   | 最大帧率（0为无限制）    |

## 使用示例

```python
from ursina import *

app = Ursina()

# 使用表格中的参数创建实体
player = Entity(
    model='cube',
    texture='white_cube',
    position=(0, 2, 0),
    rotation=(45, 45, 45),
    scale=(1, 2, 1),
    color=color.blue,
    collider='box',
    origin=(0, -0.5, 0),  # 将原点调整到底部
    eternal=True
)

# 创建按钮
start_button = Button(
    text='开始游戏',
    color=color.green,
    highlight_color=color.lime,
    scale=(0.3, 0.1),
    position=(0, 0.2),
    text_color=color.white,
    radius=0.05
)

# 创建文本
score_text = Text(
    text='得分: 0',
    position=(-0.85, 0.45),
    size=0.03,
    color=color.yellow,
    background=True,
    bg_color=color.black
)

app.run()
```

这个表格涵盖了 Ursina 中最常用的参数，帮助你快速理解和使用各个组件。在实际开发中，可以根据需要组合使用这些参数来创建复杂的游戏对象和交互效果。




#附件
1. 模型概览表(Entity的model参数)

| 模型名称     | 	形状	 | 默认尺寸   | 	顶点数 | 	三角形数	 | 主要用途        |
|----------|------|--------|------|--------|-------------|
| 'cube'   | 	立方体 | 	1x1x1 | 	8   | 	12    | 	3D物体、建筑、方块 |
| 'sphere' | 	球体	 | 直径1	   | 42	  | 80     | 	球体、行星、头部   |
| 'plane'  | 	平面	 | 1x1    | 	4	  | 2      | 	地面、墙壁、平台   |
| 'quad'	  | 四边形	 | 1x1    | 	4	  | 2      | 	UI、精灵、2D元素 |
