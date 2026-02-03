# 《众生之门》联机版开发计划文档
## 面向学生开发者的渐进式开发方案

---

## 一、项目概况与调整

### 项目调整说明
**目标定位**：考虑到学生开发者的实际情况（课程压力、时间有限、技术经验不足），本项目调整为：
- **开发周期**：24周（6个月）→ 延长至32周（8个月）
- **团队规模**：3-5人学生团队
- **开发强度**：每周10-15小时有效开发时间
- **技术难度**：采用渐进式学习，避免复杂技术栈

### 开发原则
1. **先单机后联机**：先完成单机可玩版本，再添加联机功能
2. **模块化开发**：每个系统独立可测试
3. **文档驱动**：所有功能先设计文档再编码
4. **每周会议**：周日晚上进行进度同步和问题讨论

---

## 二、详细时间轴（32周计划）

### 阶段一：基础建设与学习（第1-8周）

#### **第1-2周：环境搭建与团队熟悉**
```python
# week1-2/setup_guide.py
"""
目标：让所有团队成员完成开发环境配置
任务分解：
1. 基础环境安装（每人必须完成）
   - Python 3.9+ 安装
   - Git 安装与配置
   - VS Code 或 PyCharm 安装
   
2. 学习基础框架
   - Ursina Engine 官方教程完成
   - 理解实体-组件系统
   - 完成3个小练习：
     a. 移动一个立方体
     b. 实现简单的第一人称视角
     c. 加载外部模型
   
3. 团队协作规范
   - Git工作流培训
   - 代码规范制定
   - 项目目录结构共识
"""

# 团队练习项目：每个人的第一个Ursina程序
from ursina import *

app = Ursina()

class TeamMember(Entity):
    def __init__(self, name, model='cube', color=color.random_color()):
        super().__init__(
            model=model,
            color=color,
            scale=0.5,
            position=(random.uniform(-5,5), random.uniform(-5,5), random.uniform(-5,5))
        )
        self.name = name
        self.speed = random.uniform(1, 3)
        
    def update(self):
        self.rotation_y += self.speed * time.dt

# 每个成员创建自己的角色
members = ['Alice', 'Bob', 'Charlie', 'Diana', 'Ethan']
for name in members:
    TeamMember(name)

app.run()
```

**学习资料清单**：
- [ ] Ursina官方教程：https://www.ursinaengine.org/
- [ ] Git基础教程：https://www.atlassian.com/git/tutorials
- [ ] Python游戏开发基础（可选书籍）
- [ ] 团队共享文档模板（Notion或腾讯文档）

---

#### **第3-4周：单机基础原型（无需网络）**
```python
# week3-4/singleplayer_prototype.py
"""
目标：创建可玩的单机基础版本，确定核心玩法
功能清单：
1. 基础角色控制器（移动、跳跃、视角）
2. 简单地形生成
3. 基础交互系统（拾取物品）
4. 简单UI显示（生命值、能量值）
"""

class SimplePlayerController(Entity):
    """简化的单机玩家控制器"""
    def __init__(self):
        super().__init__(
            model='cube',
            color=color.orange,
            scale=(0.8, 1.8, 0.8),
            collider='box'
        )
        self.speed = 5
        self.jump_height = 8
        self.health = 100
        self.spirit_energy = 100
        
        # 简单的输入处理
        self.keys = {
            'forward': 'w',
            'backward': 's',
            'left': 'a',
            'right': 'd',
            'jump': 'space',
            'interact': 'e'
        }
        
    def update(self):
        # 移动输入
        move_direction = Vec3(0, 0, 0)
        
        if held_keys[self.keys['forward']]:
            move_direction += self.forward
        if held_keys[self.keys['backward']]:
            move_direction -= self.forward
        if held_keys[self.keys['left']]:
            move_direction -= self.right
        if held_keys[self.keys['right']]:
            move_direction += self.right
            
        # 应用移动
        if move_direction.length() > 0:
            self.position += move_direction.normalized() * self.speed * time.dt
            
        # 跳跃
        if held_keys[self.keys['jump']] and self.grounded:
            self.animate_position(
                self.position + (0, self.jump_height, 0),
                duration=0.5,
                curve=curve.out_expo
            )

class SimpleWorld:
    """简化世界生成器"""
    def __init__(self, size=10):
        self.size = size
        self.terrain = []
        self.interactables = []
        
    def generate(self):
        # 地面
        ground = Entity(
            model='plane',
            texture='white_cube',
            scale=(self.size, 1, self.size),
            color=color.green.tint(-0.3)
        )
        self.terrain.append(ground)
        
        # 随机障碍物
        for _ in range(20):
            obstacle = Entity(
                model='cube',
                position=(
                    random.uniform(-self.size/2, self.size/2),
                    0.5,
                    random.uniform(-self.size/2, self.size/2)
                ),
                scale=(random.uniform(0.5, 2), 1, random.uniform(0.5, 2)),
                color=color.gray,
                collider='box'
            )
            self.terrain.append(obstacle)
            
        # 可拾取物品
        for _ in range(10):
            item = CollectibleItem(
                position=(
                    random.uniform(-self.size/2, self.size/2),
                    1,
                    random.uniform(-self.size/2, self.size/2)
                )
            )
            self.interactables.append(item)
            
class CollectibleItem(Entity):
    """可收集物品"""
    def __init__(self, position):
        super().__init__(
            model='sphere',
            color=color.yellow,
            position=position,
            scale=0.5,
            collider='sphere'
        )
        self.rotation_speed = random.uniform(30, 90)
        self.bob_height = 0.2
        self.bob_speed = random.uniform(1, 3)
        self.original_y = position[1]
        
    def update(self):
        # 旋转和上下浮动
        self.rotation_y += self.rotation_speed * time.dt
        self.y = self.original_y + math.sin(time.time() * self.bob_speed) * self.bob_height
        
    def collect(self):
        """被收集时的效果"""
        self.animate_scale((0, 0, 0), duration=0.3)
        destroy(self, delay=0.3)
```

**团队分工建议**：
- **A同学**：角色控制器、动画系统
- **B同学**：世界生成、环境美术
- **C同学**：UI系统、音效集成
- **D同学**：物品系统、交互逻辑

---

#### **第5-6周：灵质系统基础（单机版）**
```python
# week5-6/spirit_system_single.py
"""
目标：实现完整的灵质能力系统（单机）
设计原则：简单但可扩展
"""

class SpiritAbility:
    """灵质能力基类"""
    def __init__(self, name, element, cost, cooldown, icon):
        self.name = name
        self.element = element  # 'wood', 'metal', 'spatial'
        self.cost = cost
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.icon = icon
        self.level = 1
        
    def can_use(self, player):
        """检查是否可以使用"""
        return (
            player.spirit_energy >= self.cost and 
            self.current_cooldown <= 0
        )
        
    def use(self, player, target_position=None):
        """使用能力（抽象方法）"""
        raise NotImplementedError
        
    def update(self):
        """更新冷却"""
        if self.current_cooldown > 0:
            self.current_cooldown -= time.dt
            
    def start_cooldown(self):
        """开始冷却"""
        self.current_cooldown = self.cooldown

class WoodVineAbility(SpiritAbility):
    """木系：藤蔓"""
    def __init__(self):
        super().__init__(
            name="藤蔓缠绕",
            element="wood",
            cost=20,
            cooldown=3,
            icon="vine_icon"
        )
        self.vine_length = 5
        self.vine_duration = 2
        
    def use(self, player, target_position=None):
        if not self.can_use(player):
            return False
            
        # 消耗能量
        player.spirit_energy -= self.cost
        
        # 如果没有指定目标，使用玩家前方
        if not target_position:
            target_position = player.position + player.forward * 3
            
        # 创建藤蔓
        vine = Vine(
            start_position=player.position,
            end_position=target_position,
            duration=self.vine_duration
        )
        
        self.start_cooldown()
        return True

class Vine(Entity):
    """藤蔓效果"""
    def __init__(self, start_position, end_position, duration=2):
        super().__init__()
        
        # 计算方向和长度
        direction = end_position - start_position
        length = direction.length()
        direction = direction.normalized()
        
        # 创建藤蔓主体
        self.model = 'cube'
        self.color = color.green.tint(-0.2)
        self.position = start_position + direction * (length / 2)
        self.scale = (0.2, length, 0.2)
        self.look_at(end_position)
        
        # 添加叶子装饰
        leaf_count = int(length)
        for i in range(leaf_count):
            leaf_pos = start_position + direction * (i * length / leaf_count)
            leaf_pos += Vec3(
                random.uniform(-0.3, 0.3),
                random.uniform(-0.3, 0.3),
                random.uniform(-0.3, 0.3)
            )
            
            leaf = Entity(
                model='sphere',
                color=color.green,
                position=leaf_pos,
                scale=random.uniform(0.2, 0.4)
            )
            leaf.animate_scale((0, 0, 0), duration=duration, delay=duration)
            
        # 自动销毁
        self.animate_scale((0, 0, 0), duration=duration)
        destroy(self, delay=duration)

class SpiritHUD:
    """灵质系统UI"""
    def __init__(self, player):
        self.player = player
        self.abilities = []
        self.ui_elements = {}
        
        # 创建能量条
        self.create_spirit_bar()
        self.create_ability_bar()
        
    def create_spirit_bar(self):
        """创建灵质能量条"""
        # 背景
        bg = Entity(
            model='quad',
            color=color.dark_gray,
            parent=camera.ui,
            scale=(0.3, 0.03),
            position=(-0.7, -0.4)
        )
        
        # 能量条
        bar = Entity(
            model='quad',
            color=color.cyan,
            parent=bg,
            scale=(1, 1),
            position=(0, 0)
        )
        
        self.ui_elements['spirit_bar'] = bar
        
    def update(self):
        """更新UI"""
        # 更新能量条
        spirit_ratio = self.player.spirit_energy / self.player.max_spirit
        self.ui_elements['spirit_bar'].scale_x = max(0, spirit_ratio)
```

**学习重点**：
1. 面向对象设计（继承、多态）
2. 特效系统实现
3. UI与游戏逻辑分离

---

#### **第7-8周：数据持久化与设置系统**
```python
# week7-8/save_system.py
"""
目标：实现游戏设置和存档系统
功能：
1. 游戏设置（分辨率、音量、按键绑定）
2. 本地存档系统
3. 玩家进度保存
"""

import json
import os
from dataclasses import dataclass, asdict

@dataclass
class GameSettings:
    """游戏设置数据类"""
    # 视频设置
    resolution: tuple = (1280, 720)
    fullscreen: bool = False
    vsync: bool = True
    graphics_quality: str = "medium"  # low, medium, high
    
    # 音频设置
    master_volume: float = 0.8
    bgm_volume: float = 0.7
    sfx_volume: float = 0.8
    
    # 控制设置
    keybindings: dict = None
    
    def __post_init__(self):
        if self.keybindings is None:
            self.keybindings = {
                'move_forward': 'w',
                'move_backward': 's',
                'move_left': 'a',
                'move_right': 'd',
                'jump': 'space',
                'interact': 'e',
                'ability_1': '1',
                'ability_2': '2',
                'ability_3': '3',
                'inventory': 'tab',
                'menu': 'escape'
            }
            
@dataclass
class SaveData:
    """存档数据类"""
    player_name: str = "玩家"
    player_level: int = 1
    experience: int = 0
    play_time: float = 0.0
    world_seed: int = 0
    last_position: tuple = (0, 0, 0)
    unlocked_abilities: list = None
    completed_quests: list = None
    inventory_items: list = None
    
    def __post_init__(self):
        if self.unlocked_abilities is None:
            self.unlocked_abilities = []
        if self.completed_quests is None:
            self.completed_quests = []
        if self.inventory_items is None:
            self.inventory_items = []

class SaveSystem:
    """存档管理系统"""
    def __init__(self):
        self.save_dir = "saves"
        self.settings_file = "settings.json"
        self.current_save_slot = 0
        self.max_save_slots = 5
        
        # 确保目录存在
        os.makedirs(self.save_dir, exist_ok=True)
        
    def load_settings(self):
        """加载游戏设置"""
        settings_path = os.path.join(self.save_dir, self.settings_file)
        
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return GameSettings(**data)
            except:
                print("设置文件损坏，使用默认设置")
                
        return GameSettings()
        
    def save_settings(self, settings):
        """保存游戏设置"""
        settings_path = os.path.join(self.save_dir, self.settings_file)
        
        try:
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(settings), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存设置失败: {e}")
            return False
            
    def save_game(self, slot, save_data):
        """保存游戏进度"""
        if slot < 0 or slot >= self.max_save_slots:
            return False
            
        save_path = os.path.join(self.save_dir, f"save_{slot}.json")
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(save_data), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存游戏失败: {e}")
            return False
            
    def load_game(self, slot):
        """加载游戏进度"""
        if slot < 0 or slot >= self.max_save_slots:
            return None
            
        save_path = os.path.join(self.save_dir, f"save_{slot}.json")
        
        if not os.path.exists(save_path):
            return None
            
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return SaveData(**data)
        except:
            print(f"存档文件损坏: {save_path}")
            return None

class SettingsMenu:
    """设置菜单界面"""
    def __init__(self):
        self.save_system = SaveSystem()
        self.settings = self.save_system.load_settings()
        self.menu_elements = {}
        
    def show(self):
        """显示设置菜单"""
        # 创建背景
        bg = Entity(
            model='quad',
            color=color.black66,
            parent=camera.ui,
            scale=(1.5, 1.0),
            position=(0, 0)
        )
        
        # 标题
        title = Text(
            text="设置",
            parent=camera.ui,
            position=(0, 0.4),
            scale=2,
            color=color.white
        )
        
        # 创建设置选项
        self.create_video_settings(bg)
        self.create_audio_settings(bg)
        self.create_control_settings(bg)
        
        # 保存按钮
        save_btn = Button(
            text="保存设置",
            parent=camera.ui,
            position=(0, -0.4),
            scale=(0.2, 0.05),
            on_click=self.save_and_close
        )
        
        self.menu_elements['background'] = bg
        self.menu_elements['title'] = title
        self.menu_elements['save_button'] = save_btn
        
    def create_video_settings(self, parent):
        """创建视频设置"""
        # 分辨率选择
        resolutions = [(1280, 720), (1366, 768), (1920, 1080)]
        
        res_label = Text(
            text="分辨率:",
            parent=parent,
            position=(-0.4, 0.2),
            scale=1.5
        )
        
        # 更多设置选项...
        
    def save_and_close(self):
        """保存设置并关闭菜单"""
        self.save_system.save_settings(self.settings)
        
        # 应用设置
        self.apply_settings()
        
        # 销毁菜单元素
        for element in self.menu_elements.values():
            destroy(element)
        self.menu_elements.clear()
```

**重要概念学习**：
1. JSON数据序列化
2. 数据类（dataclass）使用
3. 文件系统操作
4. 配置管理设计模式

---

### 阶段二：联机系统学习与实现（第9-16周）

#### **第9-10周：网络编程基础学习**
```python
# week9-10/network_basics.py
"""
目标：学习网络编程基础概念
学习路径：
1. Python socket 编程基础
2. 简单的客户端-服务器通信
3. 了解游戏网络同步的基本概念

重要：这部分是理论学习，不直接集成到游戏中
"""

# 示例1：最简单的TCP服务器和客户端
# server.py
import socket
import threading

class SimpleGameServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.clients = []
        self.running = False
        
    def start(self):
        """启动服务器"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"服务器启动在 {self.host}:{self.port}")
        
        # 接受连接
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.start()
        
    def accept_connections(self):
        """接受客户端连接"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"新连接: {address}")
                
                # 处理客户端
                client_handler = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_handler.start()
                
                self.clients.append((client_socket, address))
                
            except Exception as e:
                print(f"接受连接时出错: {e}")
                
    def handle_client(self, client_socket, address):
        """处理客户端消息"""
        while self.running:
            try:
                # 接收数据
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                print(f"来自 {address} 的消息: {data}")
                
                # 广播给所有客户端
                self.broadcast(f"{address}: {data}", exclude=client_socket)
                
            except Exception as e:
                print(f"处理客户端 {address} 时出错: {e}")
                break
                
        # 清理
        client_socket.close()
        self.clients = [c for c in self.clients if c[0] != client_socket]
        print(f"客户端 {address} 断开连接")
        
    def broadcast(self, message, exclude=None):
        """广播消息给所有客户端"""
        for client_socket, address in self.clients:
            if client_socket != exclude:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    pass
                    
    def stop(self):
        """停止服务器"""
        self.running = False
        for client_socket, _ in self.clients:
            client_socket.close()
        self.server_socket.close()

# client.py
class SimpleGameClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        
    def connect(self):
        """连接到服务器"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.running = True
        
        # 启动接收线程
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
        
        print("已连接到服务器")
        
    def receive_messages(self):
        """接收服务器消息"""
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    print(f"服务器: {message}")
            except:
                break
                
    def send_message(self, message):
        """发送消息到服务器"""
        try:
            self.socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"发送消息失败: {e}")
            
    def disconnect(self):
        """断开连接"""
        self.running = False
        if self.socket:
            self.socket.close()

# 使用示例
if __name__ == "__main__":
    # 在第一个终端运行服务器
    # server = SimpleGameServer()
    # server.start()
    
    # 在第二个终端运行客户端
    client = SimpleGameClient()
    client.connect()
    client.send_message("Hello, Server!")
```

**网络学习资料**：
- [ ] Python Socket 编程官方文档
- [ ] 《网络游戏核心技术与实战》第1-3章
- [ ] UDP vs TCP 区别和应用场景
- [ ] 游戏同步技术：状态同步 vs 帧同步

---

#### **第11-12周：简单联机原型（局域网）**
```python
# week11-12/local_network_prototype.py
"""
目标：实现局域网内的简单联机功能
功能：
1. 发现局域网内可用的服务器
2. 玩家位置同步
3. 简单聊天功能
4. 玩家加入/离开通知

设计：采用P2P（对等网络）架构，简化服务器需求
"""

import socket
import threading
import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, List

@dataclass
class NetworkPlayer:
    """网络玩家数据"""
    player_id: str
    username: str
    position: tuple
    rotation: tuple
    health: int
    last_update: float

class NetworkManager:
    """网络管理器 - 简化的P2P实现"""
    def __init__(self, username, is_host=False):
        self.username = username
        self.is_host = is_host
        self.player_id = self.generate_id()
        
        # 网络配置
        self.udp_port = 7777
        self.broadcast_port = 7778
        self.broadcast_address = '255.255.255.255'
        
        # 玩家列表
        self.players: Dict[str, NetworkPlayer] = {}
        self.players[self.player_id] = NetworkPlayer(
            player_id=self.player_id,
            username=username,
            position=(0, 0, 0),
            rotation=(0, 0, 0),
            health=100,
            last_update=time.time()
        )
        
        # 网络状态
        self.running = False
        self.socket = None
        
    def generate_id(self):
        """生成玩家ID"""
        import hashlib
        import uuid
        return hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:8]
        
    def start(self):
        """启动网络功能"""
        self.running = True
        
        # 创建UDP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', self.udp_port))
        self.socket.settimeout(0.1)
        
        # 启动接收线程
        receive_thread = threading.Thread(target=self.receive_loop)
        receive_thread.start()
        
        # 如果是主机，定期广播服务器存在
        if self.is_host:
            broadcast_thread = threading.Thread(target=self.broadcast_server)
            broadcast_thread.start()
        else:
            # 客户端，尝试发现服务器
            self.discover_servers()
            
    def discover_servers(self):
        """发现局域网内的服务器"""
        discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # 发送发现请求
        message = json.dumps({
            'type': 'discovery',
            'username': self.username,
            'player_id': self.player_id
        })
        
        discovery_socket.sendto(
            message.encode('utf-8'),
            (self.broadcast_address, self.broadcast_port)
        )
        discovery_socket.close()
        
    def broadcast_server(self):
        """广播服务器存在"""
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        while self.running:
            message = json.dumps({
                'type': 'server_info',
                'hostname': socket.gethostname(),
                'player_count': len(self.players),
                'max_players': 4
            })
            
            try:
                broadcast_socket.sendto(
                    message.encode('utf-8'),
                    (self.broadcast_address, self.broadcast_port)
                )
            except:
                pass
                
            time.sleep(2)  # 每2秒广播一次
            
        broadcast_socket.close()
        
    def receive_loop(self):
        """接收消息循环"""
        while self.running:
            try:
                data, address = self.socket.recvfrom(4096)
                self.process_message(data, address)
            except socket.timeout:
                continue
            except Exception as e:
                print(f"接收消息错误: {e}")
                
    def process_message(self, data, address):
        """处理接收到的消息"""
        try:
            message = json.loads(data.decode('utf-8'))
            msg_type = message.get('type')
            
            if msg_type == 'player_update':
                self.handle_player_update(message, address)
            elif msg_type == 'player_join':
                self.handle_player_join(message, address)
            elif msg_type == 'player_leave':
                self.handle_player_leave(message)
            elif msg_type == 'chat_message':
                self.handle_chat_message(message)
                
        except json.JSONDecodeError:
            print("收到无效的JSON数据")
            
    def send_player_update(self, position, rotation, health):
        """发送玩家状态更新"""
        update_data = {
            'type': 'player_update',
            'player_id': self.player_id,
            'username': self.username,
            'position': position,
            'rotation': rotation,
            'health': health,
            'timestamp': time.time()
        }
        
        # 发送给所有已知玩家
        for player_id, player in self.players.items():
            if player_id != self.player_id:
                self.send_to_player(player_id, update_data)
                
    def send_to_player(self, player_id, data):
        """发送数据给指定玩家"""
        # 在实际实现中，这里需要知道玩家的IP地址
        # 简化版：广播给局域网
        message = json.dumps(data)
        for addr in self.get_broadcast_addresses():
            try:
                self.socket.sendto(message.encode('utf-8'), (addr, self.udp_port))
            except:
                pass
                
    def get_broadcast_addresses(self):
        """获取广播地址列表"""
        # 简化实现：返回几个常见的局域网广播地址
        return ['255.255.255.255', '192.168.1.255', '10.0.0.255']
        
    def stop(self):
        """停止网络功能"""
        self.running = False
        if self.socket:
            self.socket.close()

class NetworkedPlayer(Entity):
    """网络化的玩家实体"""
    def __init__(self, player_data, is_local=False):
        super().__init__(
            model='cube' if is_local else 'sphere',
            color=color.orange if is_local else color.blue,
            scale=(0.8, 1.8, 0.8),
            position=player_data.position
        )
        
        self.player_id = player_data.player_id
        self.username = player_data.username
        self.is_local = is_local
        self.health = player_data.health
        self.last_update = player_data.last_update
        
        # 显示玩家名
        self.name_tag = Text(
            text=self.username,
            parent=self,
            position=(0, 1.5, 0),
            scale=0.5,
            billboard=True
        )
        
    def update_from_network(self, player_data):
        """从网络数据更新状态"""
        self.position = player_data.position
        self.rotation = player_data.rotation
        self.health = player_data.health
        self.last_update = player_data.last_update
        
        # 平滑插值
        self.animate_position(self.position, duration=0.1)
```

**关键学习点**：
1. UDP广播和发现机制
2. P2P网络架构
3. 玩家状态同步
4. 局域网通信优化

---

#### **第13-14周：权威服务器设计（可选，如果决定使用服务器）**
```python
# week13-14/dedicated_server.py
"""
目标：设计并实现一个简单的权威服务器
注意：这部分是可选的，如果团队决定不使用专用服务器，可以跳过
"""

import asyncio
import websockets
import json
from typing import Dict, Set
from enum import Enum

class MessageType(Enum):
    """消息类型枚举"""
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    PLAYER_UPDATE = "player_update"
    WORLD_STATE = "world_state"
    CHAT_MESSAGE = "chat_message"
    GAME_EVENT = "game_event"

class GameServer:
    """游戏服务器"""
    def __init__(self, host='0.0.0.0', port=8765):
        self.host = host
        self.port = port
        self.connected_clients: Set[websockets.WebSocketServerProtocol] = set()
        self.players: Dict[str, dict] = {}
        self.world_state = {}
        
    async def start(self):
        """启动服务器"""
        print(f"启动游戏服务器在 {self.host}:{self.port}")
        
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # 永远运行
            
    async def handle_client(self, websocket, path):
        """处理客户端连接"""
        client_id = id(websocket)
        self.connected_clients.add(websocket)
        
        try:
            # 发送欢迎消息
            welcome_msg = {
                'type': MessageType.CONNECT.value,
                'client_id': client_id,
                'message': '欢迎连接到游戏服务器'
            }
            await websocket.send(json.dumps(welcome_msg))
            
            # 处理客户端消息
            async for message in websocket:
                await self.process_client_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            print(f"客户端 {client_id} 断开连接")
        finally:
            # 清理
            self.connected_clients.remove(websocket)
            if str(client_id) in self.players:
                del self.players[str(client_id)]
                
            # 通知其他玩家
            await self.broadcast_player_left(client_id)
            
    async def process_client_message(self, websocket, message):
        """处理客户端消息"""
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            
            if msg_type == MessageType.PLAYER_UPDATE.value:
                await self.handle_player_update(websocket, data)
            elif msg_type == MessageType.CHAT_MESSAGE.value:
                await self.handle_chat_message(websocket, data)
            elif msg_type == MessageType.GAME_EVENT.value:
                await self.handle_game_event(websocket, data)
                
        except json.JSONDecodeError:
            print("收到无效的JSON数据")
            
    async def handle_player_update(self, websocket, data):
        """处理玩家状态更新"""
        client_id = id(websocket)
        player_data = data.get('data', {})
        
        # 更新玩家状态
        self.players[str(client_id)] = {
            **player_data,
            'last_update': asyncio.get_event_loop().time(),
            'client_id': client_id
        }
        
        # 广播给所有客户端
        broadcast_msg = {
            'type': MessageType.WORLD_STATE.value,
            'players': self.players
        }
        
        await self.broadcast(json.dumps(broadcast_msg))
        
    async def handle_chat_message(self, websocket, data):
        """处理聊天消息"""
        client_id = id(websocket)
        message = data.get('message', '')
        sender = self.players.get(str(client_id), {}).get('username', 'Unknown')
        
        # 广播聊天消息
        chat_msg = {
            'type': MessageType.CHAT_MESSAGE.value,
            'sender': sender,
            'message': message,
            'timestamp': asyncio.get_event_loop().time()
        }
        
        await self.broadcast(json.dumps(chat_msg))
        
    async def broadcast(self, message, exclude=None):
        """广播消息给所有客户端"""
        if not self.connected_clients:
            return
            
        tasks = []
        for client in self.connected_clients:
            if client != exclude:
                tasks.append(client.send(message))
                
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
    async def broadcast_player_left(self, client_id):
        """广播玩家离开"""
        leave_msg = {
            'type': MessageType.DISCONNECT.value,
            'client_id': client_id
        }
        
        await self.broadcast(json.dumps(leave_msg))

class WebSocketClient:
    """WebSocket客户端"""
    def __init__(self, server_url='ws://localhost:8765'):
        self.server_url = server_url
        self.websocket = None
        self.connected = False
        
    async def connect(self, username):
        """连接到服务器"""
        try:
            self.websocket = await websockets.connect(self.server_url)
            self.connected = True
            
            # 发送连接信息
            connect_msg = {
                'type': MessageType.CONNECT.value,
                'username': username
            }
            await self.websocket.send(json.dumps(connect_msg))
            
            # 启动接收循环
            asyncio.create_task(self.receive_messages())
            
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False
            
    async def send_player_update(self, player_data):
        """发送玩家状态更新"""
        if not self.connected:
            return
            
        msg = {
            'type': MessageType.PLAYER_UPDATE.value,
            'data': player_data
        }
        
        try:
            await self.websocket.send(json.dumps(msg))
        except Exception as e:
            print(f"发送更新失败: {e}")
            self.connected = False
            
    async def receive_messages(self):
        """接收服务器消息"""
        while self.connected:
            try:
                message = await self.websocket.recv()
                await self.handle_server_message(message)
            except websockets.exceptions.ConnectionClosed:
                print("与服务器的连接已关闭")
                self.connected = False
                break
            except Exception as e:
                print(f"接收消息错误: {e}")
                break
```

**服务器方案选择**：
1. **完全P2P（推荐给学生项目）**：无需服务器，玩家直连
2. **监听服务器**：一个玩家作为主机，其他连接
3. **专用服务器（复杂）**：需要额外服务器运行

---

#### **第15-16周：联机游戏逻辑整合**
```python
# week15-16/online_integration.py
"""
目标：将联机功能整合到单机游戏中
步骤：
1. 创建联机大厅
2. 实现玩家同步
3. 添加联机聊天
4. 处理联机游戏事件
"""

class OnlineLobby:
    """联机大厅"""
    def __init__(self):
        self.network_manager = None
        self.local_player = None
        self.remote_players = {}
        self.lobby_state = "disconnected"  # disconnected, searching, connected
        
        # UI元素
        self.ui_elements = {}
        
    def show_lobby_menu(self):
        """显示联机大厅菜单"""
        # 创建背景
        bg = Entity(
            model='quad',
            color=color.black66,
            parent=camera.ui,
            scale=(1.2, 0.8),
            position=(0, 0)
        )
        
        # 标题
        title = Text(
            text="联机大厅",
            parent=camera.ui,
            position=(0, 0.3),
            scale=2,
            color=color.white
        )
        
        # 连接状态
        status_text = Text(
            text=self.get_status_text(),
            parent=camera.ui,
            position=(0, 0.1),
            scale=1.2,
            color=self.get_status_color()
        )
        
        # 按钮
        button_y = -0.1
        buttons = [
            ("创建房间", self.create_room, (0, button_y)),
            ("加入房间", self.join_room, (0, button_y - 0.15)),
            ("快速加入", self.quick_join, (0, button_y - 0.3)),
            ("返回", self.close_lobby, (0, button_y - 0.45))
        ]
        
        for text, callback, pos in buttons:
            btn = Button(
                text=text,
                parent=camera.ui,
                position=pos,
                scale=(0.25, 0.06),
                on_click=callback
            )
            
        self.ui_elements.update({
            'background': bg,
            'title': title,
            'status': status_text
        })
        
    def get_status_text(self):
        """获取连接状态文本"""
        status_map = {
            "disconnected": "未连接",
            "searching": "搜索房间中...",
            "connected": "已连接"
        }
        return status_map.get(self.lobby_state, "未知状态")
        
    def get_status_color(self):
        """获取状态颜色"""
        color_map = {
            "disconnected": color.red,
            "searching": color.yellow,
            "connected": color.green
        }
        return color_map.get(self.lobby_state, color.white)
        
    def create_room(self):
        """创建房间"""
        if self.lobby_state != "disconnected":
            return
            
        # 获取用户名
        username = self.get_username()
        if not username:
            return
            
        # 启动网络管理器（作为主机）
        self.network_manager = NetworkManager(username=username, is_host=True)
        self.network_manager.start()
        
        # 创建本地玩家
        self.local_player = LocalPlayer(username)
        
        self.lobby_state = "connected"
        self.update_status()
        
        # 关闭大厅，进入游戏
        self.enter_game()
        
    def join_room(self):
        """加入房间"""
        # 显示房间列表
        self.show_room_list()
        
    def quick_join(self):
        """快速加入"""
        if self.lobby_state != "disconnected":
            return
            
        username = self.get_username()
        if not username:
            return
            
        # 启动网络管理器（作为客户端）
        self.network_manager = NetworkManager(username=username, is_host=False)
        self.network_manager.start()
        
        self.lobby_state = "searching"
        self.update_status()
        
        # 尝试发现服务器
        self.network_manager.discover_servers()
        
    def show_room_list(self):
        """显示房间列表"""
        # 清空现有UI
        self.clear_lobby_ui()
        
        # 创建房间列表
        rooms = self.discover_rooms()  # 假设这个方法能发现房间
        
        if not rooms:
            no_rooms_text = Text(
                text="未发现可用房间",
                parent=camera.ui,
                position=(0, 0),
                scale=1.5,
                color=color.red
            )
            self.ui_elements['no_rooms'] = no_rooms_text
            return
            
        # 显示房间列表
        room_list = []
        for i, room in enumerate(rooms):
            room_text = f"{room['name']} ({room['players']}/{room['max_players']})"
            
            text_entity = Text(
                text=room_text,
                parent=camera.ui,
                position=(0, 0.2 - i * 0.1),
                scale=1.2
            )
            
            # 点击加入
            def join_room_callback(room_info=room):
                self.join_specific_room(room_info)
                
            text_entity.on_click = join_room_callback
            room_list.append(text_entity)
            
        self.ui_elements['room_list'] = room_list
        
    def enter_game(self):
        """进入联机游戏"""
        # 关闭大厅UI
        self.clear_lobby_ui()
        
        # 创建联机游戏世界
        online_world = OnlineWorld(self.network_manager)
        online_world.start()
        
    def update_status(self):
        """更新状态显示"""
        if 'status' in self.ui_elements:
            self.ui_elements['status'].text = self.get_status_text()
            self.ui_elements['status'].color = self.get_status_color()

class OnlineWorld:
    """联机游戏世界"""
    def __init__(self, network_manager):
        self.network_manager = network_manager
        self.players = {}
        self.world_entities = []
        
    def start(self):
        """开始联机游戏"""
        # 创建世界
        self.create_world()
        
        # 创建本地玩家
        self.create_local_player()
        
        # 启动网络同步
        self.start_network_sync()
        
    def create_world(self):
        """创建游戏世界"""
        # 地面
        ground = Entity(
            model='plane',
            texture='grass',
            scale=(50, 1, 50),
            color=color.green.tint(-0.3)
        )
        self.world_entities.append(ground)
        
        # 一些障碍物
        for _ in range(20):
            obstacle = Entity(
                model='cube',
                position=(
                    random.uniform(-20, 20),
                    0.5,
                    random.uniform(-20, 20)
                ),
                scale=(1, random.uniform(1, 3), 1),
                color=color.gray,
                collider='box'
            )
            self.world_entities.append(obstacle)
            
    def create_local_player(self):
        """创建本地玩家"""
        player_data = self.network_manager.players[self.network_manager.player_id]
        
        player = LocalOnlinePlayer(
            player_data=player_data,
            network_manager=self.network_manager
        )
        
        self.players[self.network_manager.player_id] = player
        camera.parent = player
        
    def start_network_sync(self):
        """启动网络同步"""
        def sync_loop():
            while True:
                # 发送本地玩家状态
                if self.network_manager.player_id in self.players:
                    local_player = self.players[self.network_manager.player_id]
                    
                    self.network_manager.send_player_update(
                        position=local_player.position,
                        rotation=local_player.rotation,
                        health=local_player.health
                    )
                    
                # 更新远程玩家
                self.update_remote_players()
                
                # 等待下一帧
                time.sleep(0.033)  # 30fps
                
        sync_thread = threading.Thread(target=sync_loop)
        sync_thread.daemon = True
        sync_thread.start()

class LocalOnlinePlayer(Entity):
    """本地联机玩家"""
    def __init__(self, player_data, network_manager):
        super().__init__(
            model='cube',
            color=color.orange,
            scale=(0.8, 1.8, 0.8),
            position=player_data.position,
            collider='box'
        )
        
        self.player_data = player_data
        self.network_manager = network_manager
        self.speed = 5
        self.health = 100
        
        # 第一人称控制器
        mouse.locked = True
        camera.parent = self
        camera.position = (0, 1.5, 0)
        
    def update(self):
        # 移动控制
        self.move()
        
        # 鼠标视角
        self.rotate_camera()
        
    def move(self):
        """移动控制"""
        move_direction = Vec3(0, 0, 0)
        
        if held_keys['w']:
            move_direction += self.forward
        if held_keys['s']:
            move_direction -= self.forward
        if held_keys['a']:
            move_direction -= self.right
        if held_keys['d']:
            move_direction += self.right
            
        if move_direction.length() > 0:
            self.position += move_direction.normalized() * self.speed * time.dt
            
        # 跳跃
        if held_keys['space'] and self.grounded:
            self.animate_position(
                self.position + (0, 3, 0),
                duration=0.5,
                curve=curve.out_expo
            )
            
    def rotate_camera(self):
        """旋转视角"""
        self.rotation_y += mouse.velocity[0] * 40
        camera.rotation_x -= mouse.velocity[1] * 40
        camera.rotation_x = clamp(camera.rotation_x, -90, 90)
```

**整合要点**：
1. 保持单机代码的完整性
2. 联机功能作为可选模块
3. 清晰的UI状态切换
4. 良好的错误处理

---

### 阶段三：无服务器联机方案（第17-20周）

#### **第17-18周：完善的P2P联机系统**
```python
# week17-18/advanced_p2p.py
"""
目标：实现完整可靠的P2P联机系统
功能：
1. NAT穿透（使用STUN/简单的UDP打洞）
2. 可靠的消息传递（类似TCP over UDP）
3. 玩家预测和补偿
4. 断线重连
"""

import struct
import hashlib
import pickle
from collections import deque
from enum import IntEnum

class MessageType(IntEnum):
    """消息类型（使用整数以提高效率）"""
    HEARTBEAT = 0
    PLAYER_STATE = 1
    WORLD_STATE = 2
    CHAT = 3
    GAME_EVENT = 4
    RELIABLE = 5  # 可靠消息
    ACK = 6       # 确认消息

class ReliableMessage:
    """可靠消息封装"""
    def __init__(self, msg_type, data, sequence_id):
        self.msg_type = msg_type
        self.data = data
        self.sequence_id = sequence_id
        self.timestamp = time.time()
        self.retries = 0
        self.max_retries = 3
        
    def pack(self):
        """打包消息"""
        header = struct.pack('!BII', self.msg_type, self.sequence_id, int(self.timestamp))
        body = pickle.dumps(self.data)
        checksum = hashlib.md5(body).digest()[:4]
        
        return header + checksum + body
        
    @classmethod
    def unpack(cls, data):
        """解包消息"""
        if len(data) < 13:  # header + checksum
            return None
            
        header = data[:9]
        checksum = data[9:13]
        body = data[13:]
        
        if hashlib.md5(body).digest()[:4] != checksum:
            return None
            
        msg_type, seq_id, timestamp = struct.unpack('!BII', header)
        
        try:
            data_obj = pickle.loads(body)
        except:
            return None
            
        return cls(msg_type, data_obj, seq_id)

class P2PNetworkManager:
    """高级P2P网络管理器"""
    def __init__(self, username, is_host=False):
        self.username = username
        self.is_host = is_host
        self.peer_id = self.generate_peer_id()
        
        # 连接管理
        self.peers = {}  # peer_id -> (address, last_seen)
        self.connections = {}  # peer_id -> connection_state
        
        # 消息队列
        self.outgoing_queue = deque()
        self.incoming_queue = deque()
        self.reliable_messages = {}  # sequence_id -> ReliableMessage
        self.next_sequence_id = 0
        
        # 预测和补偿
        self.player_states = {}  # peer_id -> predicted_state
        self.state_history = {}  # peer_id -> [state_history]
        
        # NAT穿透
        self.stun_servers = [
            ('stun.l.google.com', 19302),
            ('stun1.l.google.com', 19302),
            ('stun2.l.google.com', 19302)
        ]
        
        # 网络统计
        self.stats = {
            'sent_packets': 0,
            'received_packets': 0,
            'lost_packets': 0,
            'avg_latency': 0
        }
        
    def generate_peer_id(self):
        """生成对等节点ID"""
        return hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()[:16]
        
    def start(self):
        """启动P2P网络"""
        # 创建UDP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', 0))  # 任意端口
        self.socket.settimeout(0.01)
        
        # 获取本地IP和端口
        self.local_address = self.socket.getsockname()
        
        # 尝试NAT穿透
        if not self.is_host:
            self.perform_nat_traversal()
            
        # 启动网络线程
        self.running = True
        self.receive_thread = threading.Thread(target=self.receive_loop)
        self.send_thread = threading.Thread(target=self.send_loop)
        self.heartbeat_thread = threading.Thread(target=self.heartbeat_loop)
        
        self.receive_thread.start()
        self.send_thread.start()
        self.heartbeat_thread.start()
        
    def perform_nat_traversal(self):
        """执行NAT穿透"""
        # 简单的UDP打洞
        # 在实际项目中，这里需要实现完整的STUN协议
        # 简化版：直接尝试连接主机
        
        if not self.is_host and hasattr(self, 'host_address'):
            # 向主机发送连接请求
            self.send_connect_request(self.host_address)
            
    def send_connect_request(self, host_address):
        """发送连接请求"""
        connect_msg = {
            'type': 'connect_request',
            'peer_id': self.peer_id,
            'username': self.username,
            'public_address': self.local_address
        }
        
        self.send_reliable(MessageType.RELIABLE, connect_msg, host_address)
        
    def send_reliable(self, msg_type, data, address):
        """发送可靠消息"""
        seq_id = self.get_next_sequence_id()
        message = ReliableMessage(msg_type, data, seq_id)
        
        # 添加到可靠消息队列
        self.reliable_messages[seq_id] = {
            'message': message,
            'address': address,
            'last_sent': 0,
            'acked': False
        }
        
    def receive_loop(self):
        """接收循环"""
        buffer_size = 4096
        
        while self.running:
            try:
                data, address = self.socket.recvfrom(buffer_size)
                self.process_incoming_data(data, address)
                self.stats['received_packets'] += 1
                
            except socket.timeout:
                continue
            except Exception as e:
                print(f"接收错误: {e}")
                
    def process_incoming_data(self, data, address):
        """处理接收到的数据"""
        # 尝试解包为可靠消息
        reliable_msg = ReliableMessage.unpack(data)
        
        if reliable_msg:
            self.process_reliable_message(reliable_msg, address)
        else:
            # 普通消息
            self.process_regular_message(data, address)
            
    def process_reliable_message(self, message, address):
        """处理可靠消息"""
        # 发送确认
        ack_msg = ReliableMessage(MessageType.ACK, message.sequence_id, 0)
        self.socket.sendto(ack_msg.pack(), address)
        
        # 处理消息内容
        if message.msg_type == MessageType.CONNECT_REQUEST:
            self.handle_connect_request(message.data, address)
        elif message.msg_type == MessageType.PLAYER_STATE:
            self.handle_player_state(message.data, address)
            
    def send_loop(self):
        """发送循环"""
        send_interval = 0.033  # 30fps
        
        while self.running:
            # 发送待处理的消息
            self.flush_outgoing_queue()
            
            # 重传未确认的可靠消息
            self.retry_reliable_messages()
            
            time.sleep(send_interval)
            
    def flush_outgoing_queue(self):
        """发送队列中的消息"""
        while self.outgoing_queue:
            message, address = self.outgoing_queue.popleft()
            try:
                self.socket.sendto(message, address)
                self.stats['sent_packets'] += 1
            except Exception as e:
                print(f"发送失败: {e}")
                
    def retry_reliable_messages(self):
        """重传未确认的可靠消息"""
        current_time = time.time()
        to_remove = []
        
        for seq_id, msg_info in self.reliable_messages.items():
            if msg_info['acked']:
                continue
                
            if current_time - msg_info['last_sent'] > 0.1:  # 100ms重传间隔
                if msg_info['retries'] < msg_info['message'].max_retries:
                    # 重传
                    self.socket.sendto(msg_info['message'].pack(), msg_info['address'])
                    msg_info['last_sent'] = current_time
                    msg_info['retries'] += 1
                else:
                    # 重试次数用完
                    to_remove.append(seq_id)
                    self.stats['lost_packets'] += 1
                    
        for seq_id in to_remove:
            del self.reliable_messages[seq_id]
            
    def heartbeat_loop(self):
        """心跳循环"""
        while self.running:
            self.send_heartbeat()
            time.sleep(5)  # 5秒一次
            
    def send_heartbeat(self):
        """发送心跳"""
        heartbeat_msg = ReliableMessage(MessageType.HEARTBEAT, {}, 0)
        
        for peer_id, peer_info in self.peers.items():
            self.socket.sendto(heartbeat_msg.pack(), peer_info['address'])
            
    def add_peer(self, peer_id, address):
        """添加对等节点"""
        self.peers[peer_id] = {
            'address': address,
            'last_seen': time.time(),
            'latency': 0
        }
        self.connections[peer_id] = 'connected'
        
        print(f"添加对等节点: {peer_id} @ {address}")
        
    def remove_peer(self, peer_id):
        """移除对等节点"""
        if peer_id in self.peers:
            del self.peers[peer_id]
        if peer_id in self.connections:
            del self.connections[peer_id]
            
        print(f"移除对等节点: {peer_id}")
        
    def update_player_state(self, player_state):
        """更新玩家状态并发送"""
        # 本地预测
        self.predict_local_state(player_state)
        
        # 发送给所有对等节点
        for peer_id in self.peers:
            self.send_player_state(player_state, self.peers[peer_id]['address'])
            
    def predict_local_state(self, state):
        """本地状态预测"""
        # 保存历史状态用于补偿
        if self.peer_id not in self.state_history:
            self.state_history[self.peer_id] = deque(maxlen=10)
            
        self.state_history[self.peer_id].append({
            'state': state.copy(),
            'timestamp': time.time()
        })
        
    def reconcile_state(self, peer_id, received_state, received_time):
        """状态协调（补偿）"""
        if peer_id not in self.state_history:
            return received_state
            
        # 查找最接近的历史状态
        history = self.state_history[peer_id]
        if not history:
            return received_state
            
        # 计算延迟补偿
        latency = self.peers.get(peer_id, {}).get('latency', 0)
        target_time = received_time - latency
        
        # 插值找到最佳状态
        best_state = None
        for i, record in enumerate(history):
            if record['timestamp'] <= target_time:
                best_state = record['state']
            else:
                # 进行插值
                if i > 0:
                    prev = history[i-1]
                    next = record
                    
                    alpha = (target_time - prev['timestamp']) / (next['timestamp'] - prev['timestamp'])
                    best_state = self.interpolate_states(prev['state'], next['state'], alpha)
                break
                
        return best_state if best_state else received_state
        
    def interpolate_states(self, state1, state2, alpha):
        """状态插值"""
        interpolated = {}
        for key in state1:
            if isinstance(state1[key], (int, float)):
                interpolated[key] = state1[key] + (state2[key] - state1[key]) * alpha
            else:
                interpolated[key] = state2[key]  # 非数值类型直接使用最新
                
        return interpolated
```

**P2P关键技术**：
1. **UDP打洞**：通过第三方服务器帮助建立连接
2. **状态预测**：客户端预测其他玩家位置
3. **延迟补偿**：服务器权威状态和客户端显示的平衡
4. **可靠消息**：在UDP上实现可靠传输

---

#### **第19-20周：联机游戏内容设计**
```python
# week19-20/online_game_content.py
"""
目标：设计适合联机游玩的游戏内容
原则：
1. 简单易上手，但有一定深度
2. 鼓励玩家合作
3. 支持2-4人游玩
4. 单局时间控制在15-30分钟
"""

class OnlineGameMode:
    """联机游戏模式基类"""
    def __init__(self, name, min_players=2, max_players=4):
        self.name = name
        self.min_players = min_players
        self.max_players = max_players
        self.players = []
        self.state = "waiting"  # waiting, playing, finished
        self.start_time = 0
        self.duration = 0
        
    def can_start(self):
        """检查是否可以开始游戏"""
        return len(self.players) >= self.min_players
        
    def start(self):
        """开始游戏"""
        if not self.can_start():
            return False
            
        self.state = "playing"
        self.start_time = time.time()
        return True
        
    def update(self):
        """更新游戏状态"""
        if self.state != "playing":
            return
            
        self.duration = time.time() - self.start_time
        
        # 检查游戏结束条件
        if self.check_win_condition():
            self.end_game()
            
    def check_win_condition(self):
        """检查获胜条件（子类实现）"""
        raise NotImplementedError
        
    def end_game(self):
        """结束游戏"""
        self.state = "finished"
        self.calculate_results()
        
    def calculate_results(self):
        """计算结果（子类实现）"""
        raise NotImplementedError

class SpiritCollectionMode(OnlineGameMode):
    """灵质收集模式 - 合作收集灵质"""
    def __init__(self):
        super().__init__(name="灵质收集", min_players=2, max_players=4)
        
        # 游戏参数
        self.target_spirit = 100  # 需要收集的总灵质量
        self.current_spirit = 0
        self.spirit_nodes = []
        self.danger_zones = []
        
        # 计时器
        self.time_limit = 300  # 5分钟
        self.warning_time = 60  # 最后1分钟警告
        
    def setup_world(self):
        """设置游戏世界"""
        # 生成灵质节点
        for _ in range(20):
            node = SpiritNode()
            self.spirit_nodes.append(node)
            
        # 生成危险区域
        for _ in range(5):
            zone = DangerZone()
            self.danger_zones.append(zone)
            
    def update(self):
        super().update()
        
        # 检查时间限制
        if self.duration >= self.time_limit:
            self.end_game()
            
        # 更新灵质节点
        for node in self.spirit_nodes:
            node.update()
            
        # 更新危险区域
        for zone in self.danger_zones:
            zone.update()
            
    def player_collect_spirit(self, player, amount):
        """玩家收集灵质"""
        self.current_spirit += amount
        player.collected_spirit += amount
        
        # 检查是否达到目标
        if self.current_spirit >= self.target_spirit:
            self.end_game()
            
    def check_win_condition(self):
        """检查获胜条件"""
        # 收集足够灵质或时间用完
        if self.current_spirit >= self.target_spirit:
            return True
        elif self.duration >= self.time_limit:
            return True
        return False
        
    def calculate_results(self):
        """计算结果"""
        success = self.current_spirit >= self.target_spirit
        
        results = {
            'success': success,
            'total_spirit': self.current_spirit,
            'target_spirit': self.target_spirit,
            'time_used': self.duration,
            'player_stats': []
        }
        
        # 玩家统计
        for player in self.players:
            results['player_stats'].append({
                'username': player.username,
                'collected_spirit': player.collected_spirit,
                'abilities_used': player.abilities_used,
                'damage_taken': player.damage_taken
            })
            
        return results

class SpiritNode(Entity):
    """灵质节点"""
    def __init__(self):
        super().__init__(
            model='sphere',
            color=color.cyan,
            position=(
                random.uniform(-20, 20),
                1,
                random.uniform(-20, 20)
            ),
            scale=random.uniform(0.5, 1.5)
        )
        
        self.spirit_amount = random.randint(10, 30)
        self.respawn_time = random.uniform(10, 30)
        self.collected = False
        self.collect_time = 0
        
        # 动画
        self.bob_speed = random.uniform(0.5, 2)
        self.bob_height = random.uniform(0.2, 0.5)
        self.original_y = self.y
        self.rotation_speed = random.uniform(30, 90)
        
    def update(self):
        if not self.collected:
            # 浮动和旋转
            self.y = self.original_y + math.sin(time.time() * self.bob_speed) * self.bob_height
            self.rotation_y += self.rotation_speed * time.dt
        else:
            # 重生计时
            if time.time() - self.collect_time > self.respawn_time:
                self.respawn()
                
    def collect(self, player):
        """被收集"""
        if self.collected:
            return 0
            
        self.collected = True
        self.collect_time = time.time()
        
        # 收集动画
        self.animate_scale((0, 0, 0), duration=0.3)
        
        return self.spirit_amount
        
    def respawn(self):
        """重生"""
        self.collected = False
        self.scale = random.uniform(0.5, 1.5)
        self.animate_scale(self.scale, duration=0.5)

class DangerZone(Entity):
    """危险区域"""
    def __init__(self):
        super().__init__(
            model='cylinder',
            color=color.red.tint(-0.3),
            position=(
                random.uniform(-20, 20),
                0,
                random.uniform(-20, 20)
            ),
            scale=(random.uniform(3, 8), 0.2, random.uniform(3, 8)),
            alpha=0.3
        )
        
        self.damage_per_second = 5
        self.active = True
        self.pulse_speed = 2
        
    def update(self):
        if self.active:
            # 脉动效果
            pulse = math.sin(time.time() * self.pulse_speed) * 0.1 + 0.9
            self.scale_x = self.scale_x * pulse
            self.scale_z = self.scale_z * pulse
            
    def check_player(self, player):
        """检查玩家是否在区域内"""
        distance_xz = distance((self.x, self.z), (player.x, player.z))
        return distance_xz < self.scale_x
        
    def apply_damage(self, player):
        """对玩家造成伤害"""
        if self.active and self.check_player(player):
            player.take_damage(self.damage_per_second * time.dt)
            return True
        return False

class SpiritArenaMode(OnlineGameMode):
    """灵质竞技场 - PvP对战模式"""
    def __init__(self):
        super().__init__(name="灵质竞技场", min_players=2, max_players=4)
        
        # 竞技场参数
        self.arena_size = (40, 40)
        self.kill_limit = 10
        self.time_limit = 300  # 5分钟
        
        # 玩家统计
        self.player_kills = {}
        self.player_deaths = {}
        
        # 竞技场元素
        self.power_ups = []
        self.obstacles = []
        
    def setup_arena(self):
        """设置竞技场"""
        # 竞技场地板
        arena_floor = Entity(
            model='plane',
            texture='white_cube',
            scale=(self.arena_size[0], 1, self.arena_size[1]),
            color=color.gray.tint(0.2),
            position=(0, 0, 0)
        )
        
        # 边界墙
        self.create_boundary_walls()
        
        # 障碍物
        self.create_obstacles()
        
        # 生成能量强化
        self.spawn_power_ups()
        
    def create_boundary_walls(self):
        """创建边界墙"""
        wall_height = 5
        wall_thickness = 1
        
        # 四个方向的墙
        walls = [
            # 北墙
            Entity(
                model='cube',
                position=(0, wall_height/2, -self.arena_size[1]/2),
                scale=(self.arena_size[0] + wall_thickness*2, wall_height, wall_thickness),
                color=color.dark_gray,
                collider='box'
            ),
            # 南墙
            Entity(
                model='cube',
                position=(0, wall_height/2, self.arena_size[1]/2),
                scale=(self.arena_size[0] + wall_thickness*2, wall_height, wall_thickness),
                color=color.dark_gray,
                collider='box'
            ),
            # 东墙
            Entity(
                model='cube',
                position=(-self.arena_size[0]/2, wall_height/2, 0),
                scale=(wall_thickness, wall_height, self.arena_size[1] + wall_thickness*2),
                color=color.dark_gray,
                collider='box'
            ),
            # 西墙
            Entity(
                model='cube',
                position=(self.arena_size[0]/2, wall_height/2, 0),
                scale=(wall_thickness, wall_height, self.arena_size[1] + wall_thickness*2),
                color=color.dark_gray,
                collider='box'
            )
        ]
        
        self.obstacles.extend(walls)
        
    def create_obstacles(self):
        """创建障碍物"""
        obstacle_count = 8
        
        for _ in range(obstacle_count):
            obstacle = Entity(
                model='cube',
                position=(
                    random.uniform(-self.arena_size[0]/2 + 5, self.arena_size[0]/2 - 5),
                    1,
                    random.uniform(-self.arena_size[1]/2 + 5, self.arena_size[1]/2 - 5)
                ),
                scale=(
                    random.uniform(2, 6),
                    random.uniform(2, 4),
                    random.uniform(2, 6)
                ),
                color=color.gray.tint(random.uniform(-0.3, 0.3)),
                collider='box'
            )
            self.obstacles.append(obstacle)
            
    def spawn_power_ups(self):
        """生成能量强化"""
        power_up_types = [
            ('speed_boost', color.yellow, 0.3),
            ('damage_boost', color.red, 0.3),
            ('defense_boost', color.blue, 0.3),
            ('spirit_regen', color.cyan, 0.3)
        ]
        
        for power_type, power_color, spawn_chance in power_up_types:
            if random.random() < spawn_chance:
                power_up = PowerUp(
                    power_type=power_type,
                    color=power_color,
                    position=(
                        random.uniform(-self.arena_size[0]/2 + 3, self.arena_size[0]/2 - 3),
                        0.5,
                        random.uniform(-self.arena_size[1]/2 + 3, self.arena_size[1]/2 - 3)
                    )
                )
                self.power_ups.append(power_up)
                
    def player_killed(self, killer, victim):
        """玩家击杀"""
        if killer not in self.player_kills:
            self.player_kills[killer] = 0
        if victim not in self.player_deaths:
            self.player_deaths[victim] = 0
            
        self.player_kills[killer] += 1
        self.player_deaths[victim] += 1
        
        # 检查是否达到击杀限制
        if self.player_kills[killer] >= self.kill_limit:
            self.end_game()
            
    def check_win_condition(self):
        """检查获胜条件"""
        # 检查是否有人达到击杀限制
        for player, kills in self.player_kills.items():
            if kills >= self.kill_limit:
                return True
                
        # 检查时间限制
        if self.duration >= self.time_limit:
            return True
            
        return False
        
    def calculate_results(self):
        """计算结果"""
        # 找到获胜者
        winner = None
        max_kills = 0
        
        for player, kills in self.player_kills.items():
            if kills > max_kills:
                max_kills = kills
                winner = player
                
        results = {
            'winner': winner,
            'max_kills': max_kills,
            'time_used': self.duration,
            'player_stats': []
        }
        
        # 玩家统计
        for player in self.players:
            kills = self.player_kills.get(player, 0)
            deaths = self.player_deaths.get(player, 0)
            
            kdr = kills / max(deaths, 1)
            
            results['player_stats'].append({
                'username': player.username,
                'kills': kills,
                'deaths': deaths,
                'kdr': kdr
            })
            
        return results

class PowerUp(Entity):
    """能量强化"""
    def __init__(self, power_type, color, position):
        super().__init__(
            model='sphere',
            color=color,
            position=position,
            scale=0.8
        )
        
        self.power_type = power_type
        self.active = True
        self.duration = 10  # 效果持续时间
        self.respawn_time = 30  # 重生时间
        
        # 动画
        self.rotation_speed = random.uniform(45, 90)
        self.bob_speed = random.uniform(1, 2)
        self.bob_height = 0.3
        self.original_y = self.y
        
    def update(self):
        if self.active:
            # 旋转和浮动
            self.rotation_y += self.rotation_speed * time.dt
            self.y = self.original_y + math.sin(time.time() * self.bob_speed) * self.bob_height
            
    def collect(self, player):
        """被收集"""
        if not self.active:
            return False
            
        self.active = False
        self.visible = False
        
        # 应用效果
        self.apply_effect(player)
        
        # 安排重生
        invoke(self.respawn, delay=self.respawn_time)
        
        return True
        
    def apply_effect(self, player):
        """应用强化效果"""
        effects = {
            'speed_boost': lambda p: setattr(p, 'speed_multiplier', 1.5),
            'damage_boost': lambda p: setattr(p, 'damage_multiplier', 1.5),
            'defense_boost': lambda p: setattr(p, 'defense_multiplier', 0.5),
            'spirit_regen': lambda p: setattr(p, 'spirit_regen_multiplier', 2.0)
        }
        
        if self.power_type in effects:
            effects[self.power_type](player)
            
            # 设置效果超时
            def remove_effect():
                setattr(player, self.power_type.split('_')[0] + '_multiplier', 1.0)
                
            invoke(remove_effect, delay=self.duration)
            
    def respawn(self):
        """重生"""
        self.active = True
        self.visible = True
        self.animate_scale(0.8, duration=0.5)
```

**联机游戏模式设计要点**：
1. **简单规则**：易于理解，快速上手
2. **明确目标**：清晰的胜利条件
3. **团队互动**：鼓励合作或竞争
4. **时间控制**：单局时间适中
5. **回放价值**：支持多次游玩

---

### 阶段四：完善与测试（第21-32周）

#### **第21-24周：联机游戏平衡与优化**
```python
# week21-24/game_balancing.py
"""
目标：平衡游戏数值，优化联机体验
工作内容：
1. 角色能力平衡
2. 游戏难度调整
3. 网络延迟优化
4. 性能调优
"""

class GameBalancer:
    """游戏平衡器"""
    def __init__(self):
        # 能力平衡数据
        self.ability_data = {
            'wood_vine': {
                'base_damage': 20,
                'cooldown': 3.0,
                'spirit_cost': 15,
                'range': 5.0,
                'scaling': {
                    'damage_per_level': 5,
                    'cooldown_reduction_per_level': 0.1
                }
            },
            'spatial_teleport': {
                'base_range': 10.0,
                'cooldown': 5.0,
                'spirit_cost': 25,
                'scaling': {
                    'range_per_level': 2,
                    'cooldown_reduction_per_level': 0.2
                }
            },
            # 更多能力...
        }
        
        # 角色平衡数据
        self.character_stats = {
            'default': {
                'base_health': 100,
                'base_spirit': 100,
                'base_speed': 5.0,
                'health_per_level': 20,
                'spirit_per_level': 15
            }
        }
        
        # 游戏模式平衡
        self.game_mode_settings = {
            'spirit_collection': {
                'target_spirit_per_player': 25,
                'time_limit_per_player': 75,  # 秒
                'spirit_node_respawn_multiplier': 1.0
            },
            'spirit_arena': {
                'kill_limit_per_player': 3,
                'time_limit': 300,
                'power_up_spawn_interval': 30
            }
        }
        
    def calculate_ability_stats(self, ability_name, level=1):
        """计算能力属性"""
        if ability_name not in self.ability_data:
            return None
            
        data = self.ability_data[ability_name]
        stats = data.copy()
        
        # 应用等级缩放
        scaling = data.get('scaling', {})
        
        if 'damage_per_level' in scaling:
            stats['damage'] = data.get('base_damage', 0) + scaling['damage_per_level'] * (level - 1)
            
        if 'cooldown_reduction_per_level' in scaling:
            cooldown_reduction = scaling['cooldown_reduction_per_level'] * (level - 1)
            stats['cooldown'] = max(0.5, data['cooldown'] - cooldown_reduction)
            
        return stats
        
    def adjust_for_player_count(self, game_mode, player_count):
        """根据玩家数量调整游戏设置"""
        settings = self.game_mode_settings.get(game_mode, {}).copy()
        
        if game_mode == 'spirit_collection':
            # 每个玩家需要收集25灵质
            settings['target_spirit'] = settings.get('target_spirit_per_player', 25) * player_count
            # 每增加一个玩家增加75秒时间
            settings['time_limit'] = 60 + settings.get('time_limit_per_player', 75) * player_count
            
        elif game_mode == 'spirit_arena':
            # 击杀限制 = 3 * (玩家数 - 1)
            settings['kill_limit'] = settings.get('kill_limit_per_player', 3) * (player_count - 1)
            
        return settings
        
    def balance_network_settings(self, avg_latency, player_count):
        """根据网络条件平衡设置"""
        # 网络延迟补偿
        if avg_latency < 50:
            # 良好网络
            interpolation_delay = 0.1
            extrapolation_amount = 0.5
        elif avg_latency < 150:
            # 中等网络
            interpolation_delay = 0.15
            extrapolation_amount = 0.3
        else:
            # 较差网络
            interpolation_delay = 0.2
            extrapolation_amount = 0.1
            
        # 根据玩家数量调整更新频率
        update_interval = 0.033  # 30fps
        
        if player_count > 4:
            update_interval = 0.05  # 20fps
        elif player_count > 8:
            update_interval = 0.1  # 10fps
            
        return {
            'interpolation_delay': interpolation_delay,
            'extrapolation_amount': extrapolation_amount,
            'update_interval': update_interval,
            'max_prediction_frames': 2
        }

class PerformanceOptimizer:
    """性能优化器"""
    def __init__(self):
        self.quality_presets = {
            'low': {
                'texture_quality': 0.5,
                'shadow_quality': 0,
                'particle_count': 10,
                'draw_distance': 30,
                'lod_distance': 10
            },
            'medium': {
                'texture_quality': 0.75,
                'shadow_quality': 1,
                'particle_count': 25,
                'draw_distance': 50,
                'lod_distance': 20
            },
            'high': {
                'texture_quality': 1.0,
                'shadow_quality': 2,
                'particle_count': 50,
                'draw_distance': 100,
                'lod_distance': 40
            }
        }
        
    def auto_detect_settings(self):
        """自动检测硬件并推荐设置"""
        import psutil
        import platform
        
        # 获取系统信息
        cpu_count = psutil.cpu_count()
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # 简单的硬件评级
        if cpu_count >= 8 and memory_gb >= 16:
            return 'high'
        elif cpu_count >= 4 and memory_gb >= 8:
            return 'medium'
        else:
            return 'low'
            
    def apply_quality_settings(self, quality_level):
        """应用质量设置"""
        if quality_level not in self.quality_presets:
            quality_level = 'medium'
            
        settings = self.quality_presets[quality_level]
        
        # 应用设置
        window.size = (1280, 720) if quality_level == 'low' else (1920, 1080)
        
        # 这里应该有更多的图形设置应用代码
        # 例如：调整材质质量、阴影设置等
        
        return settings
```

**平衡与优化工作**：
1. **数值测试**：每个能力都要测试平衡性
2. **难度曲线**：确保游戏难度适中
3. **网络测试**：在不同网络条件下测试
4. **性能测试**：在不同硬件上测试

---

#### **第25-28周：完整联机游戏测试**

**测试计划**：
```python
# week25-28/testing_plan.py
"""
测试阶段详细计划
第一阶段：内部测试（第25周）
  1. 功能测试 - 确保所有功能正常工作
  2. 平衡测试 - 调整游戏数值
  3. 性能测试 - 在不同设备上测试
  
第二阶段：小范围公测（第26-27周）
  1. 邀请10-20名玩家进行测试
  2. 收集反馈和建议
  3. 修复发现的bug
  
第三阶段：公开测试（第28周）
  1. 发布公开测试版
  2. 收集更广泛的反馈
  3. 准备正式发布
"""

class GameTester:
    """游戏测试器"""
    def __init__(self):
        self.test_cases = self.load_test_cases()
        self.bug_reports = []
        self.performance_logs = []
        
    def run_network_tests(self):
        """运行网络测试"""
        tests = [
            self.test_latency_tolerance,
            self.test_packet_loss_recovery,
            self.test_connection_stability,
            self.test_multiplayer_sync
        ]
        
        results = {}
        for test in tests:
            test_name = test.__name__
            print(f"正在运行测试: {test_name}")
            
            try:
                result = test()
                results[test_name] = result
                print(f"  ✓ {test_name}: {result}")
            except Exception as e:
                results[test_name] = f"失败: {str(e)}"
                print(f"  ✗ {test_name}: {e}")
                self.bug_reports.append({
                    'test': test_name,
                    'error': str(e),
                    'severity': 'high'
                })
                
        return results
        
    def test_latency_tolerance(self):
        """测试延迟容忍度"""
        # 模拟不同延迟
        test_delays = [50, 100, 200, 300, 500]  # 毫秒
        
        results = {}
        for delay in test_delays:
            # 模拟延迟
            success = self.simulate_latency(delay)
            results[f"{delay}ms"] = "通过" if success else "失败"
            
        return results
        
    def test_multiplayer_sync(self):
        """测试多人同步"""
        # 模拟2-4个玩家
        player_counts = [2, 3, 4]
        
        results = {}
        for count in player_counts:
            # 创建虚拟玩家
            players = self.create_virtual_players(count)
            
            # 运行模拟
            sync_errors = self.simulate_gameplay(players, duration=60)
            
            if sync_errors < 0.1:  # 小于10%的同步错误
                results[f"{count}_players"] = "良好"
            elif sync_errors < 0.3:
                results[f"{count}_players"] = "可接受"
            else:
                results[f"{count}_players"] = "需要改进"
                
        return results
        
    def collect_player_feedback(self, feedback_form):
        """收集玩家反馈"""
        # 建议的反馈项目
        feedback_categories = {
            'gameplay': [
                "游戏是否有趣？",
                "操作是否流畅？",
                "游戏难度是否合适？",
                "最满意的地方？",
                "最需要改进的地方？"
            ],
            'network': [
                "联机是否稳定？",
                "延迟是否可接受？",
                "是否有掉线问题？",
                "匹配系统是否好用？"
            ],
            'balance': [
                "角色能力是否平衡？",
                "游戏模式是否公平？",
                "有没有过于强大的策略？"
            ],
            'performance': [
                "游戏运行是否流畅？",
                "是否有卡顿现象？",
                "加载时间是否合理？"
            ]
        }
        
        feedback_results = {}
        for category, questions in feedback_categories.items():
            feedback_results[category] = {}
            for question in questions:
                # 在实际实现中，这里会收集玩家的回答
                pass
                
        return feedback_results
```

**测试清单**：
- [ ] 单人游戏所有功能
- [ ] 联机连接和匹配
- [ ] 所有游戏模式
- [ ] 角色能力和平衡
- [ ] 游戏性能和稳定性
- [ ] 用户界面和体验

---

#### **第29-32周：最终完善与发布准备**

**发布清单**：
```python
# week29-32/release_checklist.py
"""
最终发布检查清单
"""

class ReleaseManager:
    """发布管理器"""
    def __init__(self, version='1.0.0'):
        self.version = version
        self.checklist = {
            '代码质量': [
                '所有TODO标记已处理',
                '代码注释完整',
                '无调试代码残留',
                '错误处理完善',
                '代码风格统一'
            ],
            '游戏内容': [
                '所有游戏模式可玩',
                '教程完整易懂',
                '游戏平衡性良好',
                '无重大bug',
                '所有文本已本地化'
            ],
            '联机功能': [
                '连接稳定可靠',
                '匹配系统工作正常',
                '网络同步准确',
                '支持断线重连',
                '有合理的超时处理'
            ],
            '用户体验': [
                'UI/UX设计合理',
                '控制设置可自定义',
                '音效音乐完整',
                '画面流畅稳定',
                '有适当的反馈提示'
            ],
            '性能优化': [
                '内存使用合理',
                'CPU占用适中',
                '网络流量优化',
                '加载时间可接受',
                '支持多种硬件'
            ],
            '发布准备': [
                '安装包制作完成',
                '文档准备齐全',
                '宣传材料准备',
                '发布平台账号注册',
                '社区支持准备'
            ]
        }
        
    def run_preflight_check(self):
        """运行发布前检查"""
        results = {}
        
        for category, items in self.checklist.items():
            results[category] = {}
            for item in items:
                # 在实际实现中，这里会检查每个项目
                status = self.check_item(item)
                results[category][item] = status
                
        return results
        
    def create_release_build(self, platform):
        """创建发布构建"""
        build_script = f"""
#!/bin/bash
# 构建脚本示例
        
echo "正在构建 {platform} 版本..."
        
# 清理旧的构建
rm -rf build/{platform}
mkdir -p build/{platform}
        
# 复制游戏文件
cp -r game/ build/{platform}/
cp -r assets/ build/{platform}/
cp main.py build/{platform}/
        
# 处理平台特定设置
if [ "{platform}" == "windows" ]; then
    # 创建Windows可执行文件
    pyinstaller --onefile --windowed main.py
    mv dist/main.exe build/{platform}/众生之门.exe
    
elif [ "{platform}" == "mac" ]; then
    # 创建macOS应用包
    # ...
    
elif [ "{platform}" == "linux" ]; then
    # 创建Linux可执行文件
    chmod +x build/{platform}/main.py
    # ...
fi
        
echo "构建完成！"
        """
        
        # 执行构建脚本
        import subprocess
        result = subprocess.run(['bash', '-c', build_script], 
                              capture_output=True, text=True)
        
        return result.returncode == 0
        
    def create_installer(self, platform):
        """创建安装程序"""
        if platform == 'windows':
            return self.create_windows_installer()
        elif platform == 'mac':
            return self.create_mac_dmg()
        elif platform == 'linux':
            return self.create_linux_package()
            
    def create_windows_installer(self):
        """创建Windows安装程序"""
        # 使用NSIS或Inno Setup
        # 这里只是一个示例
        
        nsis_script = f"""
!include "MUI2.nsh"
        
!define APP_NAME "众生之门"
!define APP_VERSION "{self.version}"
!define APP_PUBLISHER "学生开发组"
!define APP_WEBSITE "https://github.com/your-repo"
        
Name "${{APP_NAME}}"
OutFile "build/众生之门_Setup_v{self.version}.exe"
InstallDir "$PROGRAMFILES64\\${{APP_NAME}}"
RequestExecutionLevel admin
        
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
        
!insertmacro MUI_LANGUAGE "SimpChinese"
        
Section "主程序"
  SetOutPath "$INSTDIR"
  File /r "build/windows/*"
SectionEnd
        
Section "开始菜单快捷方式"
  CreateDirectory "$SMPROGRAMS\\${{APP_NAME}}"
  CreateShortcut "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk" "$INSTDIR\\众生之门.exe"
SectionEnd
        
Section "桌面快捷方式"
  CreateShortCut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\众生之门.exe"
SectionEnd
        """
        
        with open('installer.nsi', 'w', encoding='utf-8') as f:
            f.write(nsis_script)
            
        # 执行NSIS编译
        import subprocess
        result = subprocess.run(['makensis', 'installer.nsi'], 
                              capture_output=True, text=True)
        
        return result.returncode == 0
```

**最终任务**：
1. **代码整理**：清理所有调试代码
2. **文档编写**：用户手册、技术文档
3. **宣传材料**：截图、预告片、游戏介绍
4. **社区建设**：Discord服务器、社交媒体账号
5. **发布上线**：上传到发布平台

---

## 三、无服务器备用方案详解

### 方案一：局域网直连（最简单）
```python
# 局域网发现和连接
class LANConnection:
    """局域网连接方案"""
    def __init__(self):
        self.use_upnp = False  # 可选的UPnP端口转发
        self.broadcast_port = 7777
        self.game_port = 7778
        
    def create_host(self):
        """创建主机"""
        # 1. 绑定端口
        # 2. 广播服务器信息
        # 3. 等待客户端连接
        
    def connect_to_host(self, host_ip):
        """连接到主机"""
        # 1. 发送连接请求
        # 2. 建立P2P连接
        # 3. 开始游戏
```

### 方案二：使用免费的中转服务器
```python
# 使用免费的WebSocket服务中转
class RelayServerConnection:
    """中继服务器连接"""
    def __init__(self):
        self.relay_servers = [
            'wss://free-relay-server-1.com',
            'wss://free-relay-server-2.com'
        ]
        
    def connect_via_relay(self):
        """通过中继服务器连接"""
        # 所有玩家连接到同一个中继服务器
        # 中继服务器转发消息
        # 不需要NAT穿透
```

### 方案三：完全P2P（WebRTC技术）
```python
# 使用WebRTC实现真正的P2P
class WebRTCConnection:
    """WebRTC连接"""
    def __init__(self):
        self.use_stun = True
        self.stun_servers = [
            'stun:stun.l.google.com:19302',
            'stun:stun1.l.google.com:19302'
        ]
        
        self.use_turn = False  # TURN服务器需要自己搭建
        
    def establish_p2p(self, peer_id):
        """建立P2P连接"""
        # 1. 交换SDP和ICE候选
        # 2. 建立直接连接
        # 3. 开始数据传输
```

**推荐学生项目使用方案**：
1. **首选**：局域网直连 + 简单的互联网P2P
2. **备选**：使用免费的WebSocket中继
3. **进阶**：WebRTC（技术较复杂）

---

## 四、团队协作建议

### 开发流程：
1. **每周会议**：周日晚上，每人汇报进度
2. **代码审查**：互相review代码，学习最佳实践
3. **版本控制**：使用Git，每个功能一个分支
4. **任务管理**：使用Trello或Notion管理任务

### 学习支持：
1. **技术分享会**：每周一人分享学习心得
2. **结对编程**：复杂功能两人一起实现
3. **在线资源**：利用B站、慕课网等学习平台

### 时间管理：
1. **学期中**：每周保证10小时开发时间
2. **寒暑假**：集中开发，每周30-40小时
3. **考试周**：暂停开发，专注学习

---

## 五、成功标准

### 最低目标（完成即可发布）：
- [ ] 可玩的单机版本
- [ ] 2-4人局域网联机
- [ ] 2种游戏模式
- [ ] 基础的角色能力系统
- [ ] 稳定的性能表现

### 理想目标：
- [ ] 支持互联网联机
- [ ] 4种以上游戏模式
- [ ] 完整的角色成长系统
- [ ] 社区功能和排行榜
- [ ] 可扩展的内容框架

### 超预期目标：
- [ ] 跨平台支持
- [ ] Steam/Epic平台发布
- [ ] 创意工坊支持
- [ ] 电子竞技潜力

---

## 六、风险评估与应对

### 高风险：
1. **技术难度过高**
   - 应对：优先实现核心功能，简化非核心
   - 使用成熟框架，避免造轮子
   
2. **时间不足**
   - 应对：制定合理计划，优先完成MVP
   - 寒暑假集中开发
   
3. **团队成员退出**
   - 应对：文档化所有工作，功能模块化
   - 确保至少2人了解关键系统

### 中风险：
1. **美术资源缺乏**
   - 应对：使用免费资源，简化美术要求
   - 程序生成部分内容
   
2. **网络问题复杂**
   - 应对：提供多种联机方案
   - 优先保证局域网稳定性

### 低风险：
1. **功能需求变化**
   - 应对：保持代码灵活性
   - 定期与潜在玩家沟通

---

这份计划文档专门为学生开发者设计，考虑到了学习曲线和时间限制。关键是保持灵活性，优先实现核心功能，逐步增加复杂度。记住，完成比完美更重要，先做出一个可玩的版本，再逐步完善。

祝你们开发顺利，享受游戏开发的乐趣！