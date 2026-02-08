# Panda3D 核心功能概览表

以下是 Panda3D 游戏引擎的主要模块、类和函数概览：

| 模块/类别      | 类/函数名                     | 用途                 | 基本用法示例                                           |
|------------|---------------------------|--------------------|--------------------------------------------------|
| **核心引擎**   | `ShowBase`                | 游戏主类，管理窗口、场景图等     | `from direct.showbase.ShowBase import ShowBase`  |
|            | `DirectStart`             | 快速启动 Panda3D 的快捷方式 | `from direct.showbase import DirectStart`        |
| **场景图**    | `NodePath`                | 3D 对象在场景图中的句柄      | `model = loader.loadModel("model.egg")`          |
|            | `PandaNode`               | 场景图节点基类            | `node = PandaNode("myNode")`                     |
| **模型加载**   | `Loader`                  | 加载模型、纹理等资源         | `model = loader.loadModel("models/environment")` |
|            | `ModelRoot`               | 加载的模型根节点           | 通常通过 `loader.loadModel()` 获取                     |
| **几何体**    | `GeomNode`                | 包含几何数据的节点          | `geom_node = GeomNode("geometry")`               |
|            | `Geom`, `GeomVertexData`  | 定义顶点、法线、UV等数据      | 用于程序化生成几何体                                       |
| **相机**     | `Camera`                  | 相机对象               | `camera = Camera("mainCam")`                     |
|            | `PerspectiveLens`         | 透视投影镜头             | `lens = PerspectiveLens()`                       |
| **灯光**     | `DirectionalLight`        | 方向光                | `dlight = DirectionalLight("dlight")`            |
|            | `AmbientLight`            | 环境光                | `alight = AmbientLight("alight")`                |
|            | `PointLight`              | 点光源                | `plight = PointLight("plight")`                  |
|            | `Spotlight`               | 聚光灯                | `slight = Spotlight("slight")`                   |
| **纹理**     | `Texture`                 | 纹理对象               | `tex = loader.loadTexture("textures/wood.png")`  |
|            | `TextureStage`            | 纹理阶段，用于多纹理         | `ts = TextureStage("ts")`                        |
| **渲染**     | `RenderState`             | 渲染状态（材质、混合等）       | 控制对象的渲染方式                                        |
|            | `Material`                | 材质属性（漫反射、高光等）      | `mat = Material()`                               |
| **输入**     | `accept()`                | 注册键盘/鼠标事件处理        | `self.accept("escape", sys.exit)`                |
|            | `ignore()`                | 取消事件监听             | `self.ignore("space")`                           |
|            | `mouseWatcherNode`        | 鼠标状态跟踪             | `if base.mouseWatcherNode.hasMouse():`           |
| **任务管理**   | `taskMgr`                 | 任务管理器              | `taskMgr.add(self.update, "update")`             |
|            | `Task`                    | 任务对象               | 包含任务执行逻辑                                         |
| **碰撞检测**   | `CollisionTraverser`      | 碰撞遍历器              | `self.cTrav = CollisionTraverser()`              |
|            | `CollisionHandler`        | 碰撞处理器基类            |                                                  |
|            | `CollisionHandlerQueue`   | 队列碰撞处理器            | `handler = CollisionHandlerQueue()`              |
|            | `CollisionNode`           | 碰撞节点               | `cnode = CollisionNode("collider")`              |
|            | `CollisionSphere`         | 球体碰撞体              | `cs = CollisionSphere(0, 0, 0, 1)`               |
|            | `CollisionRay`            | 射线碰撞体              | `cray = CollisionRay()`                          |
| **2D GUI** | `DirectGui`               | 2D GUI 系统          | `from direct.gui.DirectGui import *`             |
|            | `DirectFrame`             | GUI 框架容器           | `frame = DirectFrame()`                          |
|            | `DirectButton`            | 按钮控件               | `btn = DirectButton(command=myFunc)`             |
|            | `DirectLabel`             | 标签控件               | `lbl = DirectLabel(text="Hello")`                |
| **音效**     | `AudioSound`              | 音效对象               | `sound = loader.loadSfx("sound.wav")`            |
|            | `AudioManager`            | 音频管理器              | 管理音频系统和资源                                        |
| **粒子系统**   | `ParticleSystem`          | 粒子系统               | 创建粒子效果                                           |
|            | `ParticleSystemManager`   | 粒子系统管理器            | 管理多个粒子系统                                         |
| **数学**     | `Vec3`, `Vec4`            | 3D/4D 向量           | `pos = Vec3(0, 0, 0)`                            |
|            | `Point3`                  | 3D 点               | `point = Point3(1, 2, 3)`                        |
|            | `Mat4`                    | 4x4 矩阵             | `mat = Mat4.translate_mat(1, 0, 0)`              |
|            | `Quat`                    | 四元数                | `quat = Quat()`                                  |
| **动画**     | `Actor`                   | 带动画的模型             | `actor = Actor("models/character")`              |
|            | `AnimControl`             | 动画控制器              | `anim = actor.getAnimControl("walk")`            |
|            | `PartBundle`              | 动画骨骼捆绑             | 用于复杂角色动画                                         |
| **后期处理**   | `CardMaker`               | 创建矩形卡片             | `cm = CardMaker("card")`                         |
|            | `FilterManager`           | 滤镜管理器              | 实现屏幕空间效果                                         |
| **物理**     | `PhysicsWorld`            | 物理世界               | 模拟刚体物理（通过 Bullet 插件）                             |
|            | `BulletWorld`             | Bullet 物理世界        | `from panda3d.bullet import BulletWorld`         |
| **网络**     | `ConnectionManager`       | 网络连接管理器            | 用于多人游戏网络通信                                       |
|            | `QueuedConnectionManager` | 队列连接管理器            | 处理网络消息队列                                         |

## 基础示例代码

```python
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # 加载模型
        self.model = self.loader.loadModel("models/environment")
        self.model.reparentTo(self.render)
        self.model.setScale(0.1, 0.1, 0.1)
        self.model.setPos(-8, 42, 0)
        
        # 设置相机
        self.disableMouse()
        self.camera.setPos(0, -10, 0)
        
        # 键盘控制
        self.accept("escape", self.userExit)
        self.accept("arrow_up", self.move_forward)
        
        # 任务循环
        self.taskMgr.add(self.update, "update")
    
    def move_forward(self):
        self.camera.setY(self.camera, 1)
    
    def update(self, task):
        # 每帧执行的逻辑
        return task.cont

game = MyGame()
game.run()
```

## 主要模块说明

1. **direct.showbase** - 核心引擎框架
2. **panda3d.core** - 核心功能模块（数学、渲染、场景图等）
3. **direct.gui** - 2D GUI 系统
4. **direct.actor** - 角色动画系统
5. **panda3d.bullet** - Bullet 物理引擎集成
6. **direct.task** - 任务管理系统
7. **direct.interval** - 动画间隔系统

## 注意事项

- Panda3D 采用右手法则坐标系：X 向右，Y 向前，Z 向上
- 场景图采用父节点-子节点层级结构
- 大多数操作通过 `NodePath` 对象进行，而非直接操作节点
- 引擎同时支持 Python 和 C++ API，但 Python API 更常用

此表格涵盖了 Panda3D 的主要功能，但实际引擎包含更多类和函数。建议查阅官方文档获取完整信息：https://docs.panda3d.org/







#
#






# Panda3D 核心模块与函数参考

以下是 Panda3D 主要模块、类和函数的表格概览：

## 核心模块概览

| 模块名称          | 主要功能     | 常用类/函数                                |
|---------------|----------|---------------------------------------|
| `DirectStart` | 快速启动3D应用 | `run()`                               |
| `ShowBase`    | 主框架类     | `ShowBase`, `WindowProperties`        |
| `NodePath`    | 场景图节点操作  | `NodePath`, `ModelNode`               |
| `Actor`       | 角色动画     | `Actor`, `AnimControl`                |
| `Loader`      | 资源加载     | `Loader.loadModel()`, `loadTexture()` |
| `Camera`      | 摄像机控制    | `Camera`, `PerspectiveLens`           |
| `Light`       | 光照系统     | `AmbientLight`, `DirectionalLight`    |
| `TextNode`    | 文字渲染     | `TextNode`, `OnscreenText`            |
| `Collision`   | 碰撞检测     | `CollisionTraverser`, `CollisionNode` |
| `Physics`     | 物理引擎     | `PhysicsWorld`, `PhysicsBody`         |

## ShowBase 核心类方法

| 类别   | 方法/属性              | 描述      |
|------|--------------------|---------|
| 窗口管理 | `openWindow()`     | 打开显示窗口  |
|      | `windowProperties` | 窗口属性对象  |
| 场景图  | `render`           | 根渲染节点   |
|      | `camera`           | 主摄像机    |
|      | `makeCamera()`     | 创建新摄像机  |
| 任务管理 | `taskMgr`          | 任务管理器   |
|      | `addTask()`        | 添加任务    |
| 输入处理 | `mouseWatcherNode` | 鼠标监听    |
|      | `buttonThrowers`   | 按钮事件处理器 |

## NodePath 常用方法

| 方法类型  | 方法名称                    | 描述             |
|-------|-------------------------|----------------|
| 变换操作  | `setPos(x, y, z)`       | 设置位置           |
|       | `setHpr(h, p, r)`       | 设置旋转（航向、俯仰、横滚） |
|       | `setScale(s)`           | 设置缩放           |
|       | `lookAt(target)`        | 看向目标           |
| 父子关系  | `reparentTo(parent)`    | 重新设置父节点        |
|       | `detachNode()`          | 从父节点分离         |
|       | `getChildren()`         | 获取子节点列表        |
| 节点操作  | `attachNewNode(name)`   | 附加新节点          |
|       | `find(path)`            | 查找节点           |
|       | `show()` / `hide()`     | 显示/隐藏节点        |
| 着色与材质 | `setColor(r, g, b, a)`  | 设置颜色           |
|       | `setTexture(texture)`   | 设置纹理           |
|       | `setMaterial(material)` | 设置材质           |

## 模型与资源加载

| 类/函数                   | 描述     | 示例                                       |
|------------------------|--------|------------------------------------------|
| `Loader.loadModel()`   | 加载3D模型 | `loader.loadModel('models/model.egg')`   |
| `Loader.loadTexture()` | 加载纹理   | `loader.loadTexture('textures/tex.png')` |
| `Loader.loadFont()`    | 加载字体   | `loader.loadFont('fonts/font.ttf')`      |
| `ModelPool`            | 模型池    | `ModelPool.loadModel()`                  |
| `TexturePool`          | 纹理池    | `TexturePool.loadTexture()`              |

## 摄像机与视角控制

| 类/方法               | 描述      | 示例                          |
|--------------------|---------|-----------------------------|
| `Camera`           | 摄像机对象   | `camera = Camera('main')`   |
| `PerspectiveLens`  | 透视镜头    | `lens = PerspectiveLens()`  |
| `OrthographicLens` | 正交镜头    | `lens = OrthographicLens()` |
| `setPos()`         | 设置摄像机位置 | `camera.setPos(0, -10, 0)`  |
| `setLens()`        | 设置镜头    | `camera.setLens(lens)`      |

## 光照系统

| 光照类型 | 类                   | 描述         |
|------|---------------------|------------|
| 环境光  | `AmbientLight`      | 均匀照亮所有方向   |
| 定向光  | `DirectionalLight`  | 平行光（如太阳光）  |
| 点光源  | `PointLight`        | 从一点向所有方向发光 |
| 聚光灯  | `Spotlight`         | 锥形光        |
| 用法   | `render.setLight()` | 将光照应用到场景   |

## 碰撞检测系统

| 组件   | 类/方法                     | 描述       |
|------|--------------------------|----------|
| 碰撞器  | `CollisionSphere`        | 球体碰撞器    |
|      | `CollisionBox`           | 盒子碰撞器    |
|      | `CollisionRay`           | 射线碰撞器    |
| 碰撞节点 | `CollisionNode`          | 包含碰撞器的节点 |
| 遍历器  | `CollisionTraverser`     | 遍历碰撞检测   |
| 处理器  | `CollisionHandlerQueue`  | 队列处理器    |
|      | `CollisionHandlerPusher` | 推开处理器    |

## 物理引擎（Bullet）

| 类                       | 描述   | 常用方法            |
|-------------------------|------|-----------------|
| `BulletWorld`           | 物理世界 | `doPhysics(dt)` |
| `BulletRigidBodyNode`   | 刚体节点 | `setMass(mass)` |
| `BulletBoxShape`        | 盒子形状 |                 |
| `BulletSphereShape`     | 球体形状 |                 |
| `BulletConvexHullShape` | 凸包形状 |                 |

## GUI 系统

| 组件  | 类              | 描述    |
|-----|----------------|-------|
| 文本  | `OnscreenText` | 屏幕文字  |
|     | `DirectLabel`  | 标签控件  |
| 按钮  | `DirectButton` | 按钮控件  |
| 输入框 | `DirectEntry`  | 文本输入框 |
| 对话框 | `DirectDialog` | 对话框   |
| 框架  | `DirectFrame`  | 容器框架  |

## 任务与事件系统

| 系统   | 类/方法                      | 描述   |
|------|---------------------------|------|
| 任务管理 | `Task`                    | 任务对象 |
|      | `TaskManager.add()`       | 添加任务 |
|      | `taskMgr.doMethodLater()` | 延迟执行 |
| 事件处理 | `Messenger`               | 消息系统 |
|      | `accept(event, handler)`  | 接受事件 |
|      | `ignore(event)`           | 忽略事件 |
|      | `send(event, args)`       | 发送事件 |

## 音频系统

| 类/方法               | 描述    | 示例                            |
|--------------------|-------|-------------------------------|
| `AudioSound`       | 音频对象  |                               |
| `AudioManager`     | 音频管理器 |                               |
| `base.loadMusic()` | 加载音乐  | `base.loadMusic('music.ogg')` |
| `base.playMusic()` | 播放音乐  |                               |
| `setLoop()`        | 设置循环  | `sound.setLoop(True)`         |
| `setVolume()`      | 设置音量  | `sound.setVolume(0.5)`        |

## 粒子系统

| 组件    | 类                        | 描述      |
|-------|--------------------------|---------|
| 粒子系统  | `ParticleSystem`         | 粒子系统    |
| 粒子发射器 | `PointEmitter`           | 点发射器    |
|       | `RectangleEmitter`       | 矩形发射器   |
| 粒子工厂  | `SpriteParticleRenderer` | 精灵粒子渲染器 |

## 着色器系统

| 类/方法                   | 描述    | 示例                            |
|------------------------|-------|-------------------------------|
| `Shader`               | 着色器对象 |                               |
| `Shader.load()`        | 加载着色器 | `Shader.load(Shader.SL_GLSL)` |
| `NodePath.setShader()` | 应用着色器 | `model.setShader(shader)`     |
| `ShaderAttrib`         | 着色器属性 |                               |

## 常用工具函数

| 模块             | 函数               | 描述    |
|----------------|------------------|-------|
| `panda3d.core` | `LVector3`       | 3D向量类 |
|                | `LPoint3`        | 3D点类  |
|                | `LColor`         | 颜色类   |
| `panda3d.core` | `TransformState` | 变换状态  |
| `mathutil`     | `Mat4`           | 4x4矩阵 |
| `panda3d.core` | `ClockObject`    | 计时器   |

## 基本使用示例

```python
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # 加载模型
        self.model = self.loader.loadModel("models/environment")
        self.model.reparentTo(self.render)
        self.model.setScale(0.25, 0.25, 0.25)
        self.model.setPos(-8, 42, 0)
        
        # 设置摄像机
        self.disableMouse()
        self.camera.setPos(0, -10, 0)
        
        # 添加任务
        self.taskMgr.add(self.update, "update")
    
    def update(self, task):
        # 更新逻辑
        dt = globalClock.getDt()
        # ... 更新代码
        return task.cont

app = MyApp()
app.run()
```

这个表格涵盖了 Panda3D 的主要功能和类。请注意，Panda3D 是一个功能丰富的引擎，实际使用时建议参考官方文档和示例代码获取更详细的信息。