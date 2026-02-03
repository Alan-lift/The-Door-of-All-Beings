# 《众生之门》3D游戏开发详细计划文档

## 一、项目概述
**项目名称**：《众生之门 - 灵域探险》
**开发周期**：16周（4个月）
**目标平台**：Windows/macOS
**技术栈**：Python 3.9+ + Ursina Engine + Blender

## 二、详细时间轴与里程碑

### 阶段一：基础构建（第1-4周）
#### **第1周：环境搭建与原型验证**
**目标**：完成开发环境配置和基础场景
```python
# week1/prototype.py - 基础场景原型
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# 基础世界
class BasicWorld:
    def __init__(self):
        self.generate_terrain()
        self.create_skybox()
        
    def generate_terrain(self):
        """生成基础地形"""
        self.ground = Entity(
            model='plane',
            texture='grass',
            scale=(50, 1, 50),
            collider='box'
        )
        
        # 测试树木
        for i in range(5):
            Tree(position=(random.uniform(-20,20), 0, random.uniform(-20,20)))
            
    def create_skybox(self):
        Sky(color=color.rgb(135, 206, 235))

# 简单树木类
class Tree(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            model='cube',
            color=color.brown,
            position=position,
            scale=(0.5, 3, 0.5)
        )
        self.leaves = Entity(
            model='sphere',
            color=color.green.tint(-0.1),
            position=position + (0, 2, 0),
            scale=2,
            parent=self
        )

world = BasicWorld()
player = FirstPersonController()
player.position = (0, 2, 0)

app.run()
```

**需要素材**：
- [ ] 基础草地质地贴图 (1024x1024 PNG)
- [ ] 天空盒6面贴图 (2048x2048 PNG)
- [ ] 临时树木模型 (Blender源文件)

**详细计划**：
- 完成Ursina环境安装
- 创建可移动的第一人称控制器
- 实现基础地形生成
- 建立Git仓库

---

#### **第2周：角色系统基础**
**目标**：实现小黑角色控制器和基础动画
```python
# week2/character_system.py
from ursina import *
from ursina.animation import Animator

class XiaoHeiCharacter(Entity):
    def __init__(self):
        super().__init__(
            model='assets/models/xiaohei.fbx',  # 需要准备的基础模型
            texture='assets/textures/xiaohei.png',
            collider='box',
            scale=0.5
        )
        self.speed = 5
        self.spirit_energy = 100
        self.max_spirit = 100
        
        # 动画控制器
        self.animator = Animator({
            'idle': self.idle_animation,
            'walk': self.walk_animation,
            'run': self.run_animation,
            'jump': self.jump_animation
        })
        
        # 移动控制
        self.move_direction = Vec3(0, 0, 0)
        
    def update(self):
        self.handle_input()
        self.apply_movement()
        self.update_animation()
        
    def handle_input(self):
        self.move_direction = Vec3(0, 0, 0)
        
        if held_keys['w']:
            self.move_direction += self.forward
        if held_keys['s']:
            self.move_direction -= self.forward
        if held_keys['a']:
            self.move_direction -= self.right
        if held_keys['d']:
            self.move_direction += self.right
            
        if held_keys['space'] and self.grounded:
            self.move_direction.y = 8  # 跳跃
            
    def apply_movement(self):
        if self.move_direction.length() > 0:
            self.position += self.move_direction.normalized() * self.speed * time.dt
            self.look_at(self.position + self.move_direction)
```

**需要素材**：
- [ ] 小黑基础3D模型 (FBX格式)
- [ ] 角色贴图 (2048x2048 PNG带透明通道)
- [ ] 行走/跑步/跳跃动画 (FBX动画文件)
- [ ] UI图标集 (32x32 PNG icons)

---

#### **第3周：灵质系统基础**
**目标**：实现基础灵质能量和简单能力
```python
# week3/spirit_system.py
class SpiritSystem:
    def __init__(self, player):
        self.player = player
        self.abilities = []
        self.active_ability = None
        self.spirit_particles = []
        
    def add_ability(self, ability_data):
        """添加新能力"""
        ability = Ability(
            name=ability_data['name'],
            element=ability_data['element'],
            cost=ability_data['cost'],
            cooldown=ability_data['cooldown'],
            icon=ability_data['icon']
        )
        self.abilities.append(ability)
        
    def use_ability(self, index, target=None):
        """使用能力"""
        if index >= len(self.abilities):
            return False
            
        ability = self.abilities[index]
        
        if self.player.spirit_energy < ability.cost:
            return False
            
        if ability.cooldown_remaining > 0:
            return False
            
        # 消耗能量
        self.player.spirit_energy -= ability.cost
        
        # 执行能力
        if ability.element == 'wood':
            return self.use_wood_ability(ability, target)
        elif ability.element == 'spatial':
            return self.use_spatial_ability(ability, target)
            
        ability.start_cooldown()
        return True
        
    def use_wood_ability(self, ability, target):
        """木系能力：藤蔓生长"""
        if not target:
            target = self.player.position + self.player.forward * 3
            
        # 创建藤蔓
        vine = Vine(
            start_pos=self.player.position,
            end_pos=target,
            growth_speed=ability.power
        )
        
        # 粒子效果
        self.create_spirit_particles(
            position=self.player.position,
            count=20,
            color=color.green.tint(0.3),
            lifetime=1.0
        )
        
        return vine

class Ability:
    def __init__(self, name, element, cost, cooldown, icon):
        self.name = name
        self.element = element
        self.cost = cost
        self.cooldown = cooldown
        self.cooldown_remaining = 0
        self.icon = icon
        self.level = 1
        
    def update(self):
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= time.dt
            
    def start_cooldown(self):
        self.cooldown_remaining = self.cooldown
        
class Vine(Entity):
    """藤蔓实体"""
    def __init__(self, start_pos, end_pos, growth_speed=2):
        super().__init__()
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.growth_speed = growth_speed
        self.current_length = 0
        self.max_length = distance(start_pos, end_pos)
        
        self.model = 'cube'
        self.color = color.green
        self.position = start_pos
        
        invoke(self.grow, delay=0.1)
        
    def grow(self):
        if self.current_length < self.max_length:
            self.current_length += self.growth_speed * time.dt
            self.scale_y = self.current_length
            self.look_at(self.end_pos)
            invoke(self.grow, delay=0.01)
```

**需要素材**：
- [ ] 灵质粒子特效贴图 (512x512带透明PNG)
- [ ] 能力图标 (64x64 PNG)
- [ ] 技能音效 (WAV格式)：藤蔓生长、空间撕裂
- [ ] 能力特效模型 (简单的FBX模型)

---

#### **第4周：世界生成系统**
**目标**：实现分块式地形和基础生态
```python
# week4/world_generator.py
class WorldGenerator:
    def __init__(self):
        self.chunk_size = 32
        self.chunks = {}
        self.active_chunks = []
        self.player_position = (0, 0, 0)
        
    def update(self, player_position):
        """更新玩家周围区块"""
        self.player_position = player_position
        chunk_x = int(player_position.x // self.chunk_size)
        chunk_z = int(player_position.z // self.chunk_size)
        
        # 卸载远离的区块
        self.unload_distant_chunks(chunk_x, chunk_z)
        
        # 加载新的区块
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                chunk_key = (chunk_x + dx, chunk_z + dz)
                if chunk_key not in self.chunks:
                    self.load_chunk(chunk_key[0], chunk_key[1])
                    
    def load_chunk(self, x, z):
        """加载一个区块"""
        chunk_key = (x, z)
        chunk_entities = []
        
        # 生成地形
        heightmap = self.generate_heightmap(x, z)
        terrain = self.create_terrain(x, z, heightmap)
        chunk_entities.append(terrain)
        
        # 生成植被
        vegetation = self.generate_vegetation(x, z, heightmap)
        chunk_entities.extend(vegetation)
        
        # 生成建筑和物品
        structures = self.generate_structures(x, z)
        chunk_entities.extend(structures)
        
        self.chunks[chunk_key] = chunk_entities
        self.active_chunks.append(chunk_key)
        
    def generate_heightmap(self, x, z):
        """生成高度图（Perlin噪声）"""
        import noise
        scale = 50.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        
        heightmap = []
        for i in range(self.chunk_size):
            row = []
            for j in range(self.chunk_size):
                world_x = x * self.chunk_size + i
                world_z = z * self.chunk_size + j
                
                # 基础地形
                height = noise.pnoise2(
                    world_x/scale, 
                    world_z/scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=1024,
                    repeaty=1024,
                    base=42
                )
                
                # 添加山脉和河流特征
                if height > 0.3:
                    height *= 1.5  # 山脉
                elif height < -0.2:
                    height *= 0.2  # 河流
                    
                row.append(height * 20)  # 缩放高度
            heightmap.append(row)
            
        return heightmap
        
    def create_terrain(self, x, z, heightmap):
        """创建地形网格"""
        terrain = Entity()
        
        # 创建网格顶点
        vertices = []
        uvs = []
        
        for i in range(self.chunk_size):
            for j in range(self.chunk_size):
                world_x = x * self.chunk_size + i
                world_z = z * self.chunk_size + j
                
                vertices.append(Vec3(i, heightmap[i][j], j))
                uvs.append((i/self.chunk_size, j/self.chunk_size))
                
        # 创建三角形
        triangles = []
        for i in range(self.chunk_size - 1):
            for j in range(self.chunk_size - 1):
                # 两个三角形组成一个网格面
                a = i * self.chunk_size + j
                b = (i+1) * self.chunk_size + j
                c = i * self.chunk_size + (j+1)
                d = (i+1) * self.chunk_size + (j+1)
                
                triangles.extend([a, b, c, b, d, c])
                
        # 创建Mesh
        terrain.model = Mesh(
            vertices=vertices,
            triangles=triangles,
            uvs=uvs,
            mode='triangle'
        )
        terrain.texture = 'assets/textures/terrain_atlas.png'
        terrain.position = (x * self.chunk_size, 0, z * self.chunk_size)
        terrain.collider = 'mesh'
        
        return terrain
        
    def generate_vegetation(self, x, z, heightmap):
        """生成植被"""
        vegetation = []
        
        # 密度图
        vegetation_density = 0.1
        
        for i in range(self.chunk_size):
            for j in range(self.chunk_size):
                if random.random() < vegetation_density:
                    height = heightmap[i][j]
                    
                    # 根据高度选择植被类型
                    if height > 15:
                        # 高山植物
                        pass
                    elif height > 0:
                        # 森林
                        if random.random() < 0.3:
                            tree = self.create_tree(
                                x * self.chunk_size + i + random.uniform(-0.5, 0.5),
                                z * self.chunk_size + j + random.uniform(-0.5, 0.5),
                                height
                            )
                            vegetation.append(tree)
                    else:
                        # 水边植物
                        pass
                        
        return vegetation
```

**需要素材**：
- [ ] 地形纹理集 (2048x2048 PNG包含多种地形)
- [ ] 多种树木模型 (3-5种树木FBX)
- [ ] 岩石和石头模型
- [ ] 水体纹理和材质

---

### 阶段二：核心系统（第5-8周）

#### **第5周：交互系统与NPC基础**
**目标**：实现对话、任务和NPC AI
```python
# week5/interaction_system.py
class InteractionSystem:
    def __init__(self):
        self.nearby_interactables = []
        self.current_dialogue = None
        self.dialogue_ui = DialogueUI()
        
    def update(self, player):
        """检测附近的交互对象"""
        self.nearby_interactables = []
        
        for entity in scene.entities:
            if hasattr(entity, 'interactable') and entity.interactable:
                distance = distance_xz(player.position, entity.position)
                if distance < entity.interaction_range:
                    self.nearby_interactables.append(entity)
                    
        # 显示交互提示
        if self.nearby_interactables:
            self.show_interaction_hint(self.nearby_interactables[0])
            
    def interact(self):
        """执行交互"""
        if not self.nearby_interactables:
            return
            
        target = self.nearby_interactables[0]
        
        if isinstance(target, NPC):
            self.start_dialogue(target)
        elif isinstance(target, QuestItem):
            self.collect_item(target)
        elif isinstance(target, Door):
            self.open_door(target)
            
class NPC(Entity):
    def __init__(self, name, faction, dialogue_tree):
        super().__init__()
        self.name = name
        self.faction = faction
        self.dialogue_tree = dialogue_tree
        self.current_dialogue_node = 'greeting'
        self.quests = []
        self.interactable = True
        self.interaction_range = 3
        
        # AI状态机
        self.state = 'idle'
        self.patrol_points = []
        self.current_patrol_index = 0
        
    def start_dialogue(self, player):
        """开始对话"""
        dialogue_data = self.dialogue_tree.get(self.current_dialogue_node)
        
        if not dialogue_data:
            return
            
        dialogue_ui = DialogueUI()
        dialogue_ui.show_dialogue(
            speaker=self.name,
            text=dialogue_data['text'],
            choices=dialogue_data.get('choices', []),
            on_choice_selected=self.on_choice_selected
        )
        
    def on_choice_selected(self, choice_index):
        """处理对话选择"""
        current_node = self.dialogue_tree[self.current_dialogue_node]
        
        if choice_index < len(current_node.get('choices', [])):
            next_node = current_node['choices'][choice_index]['next_node']
            self.current_dialogue_node = next_node
            
            # 检查是否触发任务
            if 'quest' in self.dialogue_tree.get(next_node, {}):
                quest_data = self.dialogue_tree[next_node]['quest']
                QuestManager.assign_quest(quest_data)
```

**需要素材**：
- [ ] NPC角色模型 (人类、妖精、动物)
- [ ] 对话UI界面素材 (PNG切片)
- [ ] 任务图标和标记
- [ ] 音效：对话提示音、物品拾取音

---

#### **第6周：任务系统与进度追踪**
```python
# week6/quest_system.py
class QuestSystem:
    def __init__(self):
        self.active_quests = []
        self.completed_quests = []
        self.quest_log = {}
        
    class Quest:
        def __init__(self, id, title, description, objectives, rewards):
            self.id = id
            self.title = title
            self.description = description
            self.objectives = objectives  # [{type: 'collect', target: 'item_id', amount: 3}]
            self.current_objectives = [0] * len(objectives)
            self.rewards = rewards
            self.state = 'active'  # active, completed, failed
            
        def update_objective(self, objective_type, target, amount=1):
            """更新任务目标进度"""
            for i, obj in enumerate(self.objectives):
                if obj['type'] == objective_type and obj['target'] == target:
                    self.current_objectives[i] += amount
                    
                    if self.current_objectives[i] >= obj['amount']:
                        self.check_completion()
                        
        def check_completion(self):
            """检查任务是否完成"""
            for i, obj in enumerate(self.objectives):
                if self.current_objectives[i] < obj['amount']:
                    return False
                    
            self.state = 'completed'
            self.give_rewards()
            QuestSystem.complete_quest(self.id)
            return True
            
        def give_rewards(self):
            """发放任务奖励"""
            player = scene.player
            
            if 'experience' in self.rewards:
                player.gain_experience(self.rewards['experience'])
                
            if 'items' in self.rewards:
                for item in self.rewards['items']:
                    Inventory.add_item(item)
                    
            if 'abilities' in self.rewards:
                for ability in self.rewards['abilities']:
                    player.spirit_system.add_ability(ability)
                    
# 示例任务定义
QUEST_DATABASE = {
    'first_meeting': {
        'id': 'first_meeting',
        'title': '初入灵域',
        'description': '遇见灵域向导，了解基础规则',
        'objectives': [
            {'type': 'talk', 'target': 'guide_npc', 'amount': 1},
            {'type': 'collect', 'target': 'spirit_essence', 'amount': 5}
        ],
        'rewards': {
            'experience': 100,
            'items': ['basic_spirit_crystal'],
            'abilities': ['wood_vine']
        }
    },
    'forest_guardian': {
        'id': 'forest_guardian',
        'title': '森林守护者',
        'description': '帮助森林守护者修复被破坏的灵脉',
        'objectives': [
            {'type': 'defeat', 'target': 'corrupted_spirit', 'amount': 3},
            {'type': 'activate', 'target': 'spirit_node', 'amount': 2}
        ],
        'rewards': {
            'experience': 300,
            'abilities': ['wood_heal']
        }
    }
}
```

**需要素材**：
- [ ] 任务UI界面 (完整的界面设计)
- [ ] 任务物品模型 (不同种类的灵质结晶)
- [ ] 任务完成特效
- [ ] 经验值增加动画效果

---

#### **第7周：战斗系统与敌人AI**
```python
# week7/combat_system.py
class CombatSystem:
    def __init__(self):
        self.enemies = []
        self.combat_mode = False
        
    class Enemy(Entity):
        def __init__(self, enemy_type, level, position):
            super().__init__(
                model=f'assets/models/enemies/{enemy_type}.fbx',
                position=position,
                collider='box'
            )
            self.enemy_type = enemy_type
            self.level = level
            self.health = 100 * level
            self.max_health = self.health
            self.attack_damage = 10 * level
            self.attack_range = 2
            self.aggro_range = 10
            self.detection_range = 15
            self.target = None
            
            # AI状态
            self.state = 'patrol'  # patrol, chase, attack, flee
            self.patrol_path = []
            self.attack_cooldown = 0
            
        def update(self):
            player = scene.player
            
            # 检测玩家
            distance_to_player = distance(self.position, player.position)
            
            if distance_to_player < self.detection_range:
                self.target = player
                
                if distance_to_player < self.attack_range:
                    self.state = 'attack'
                    self.attack()
                elif distance_to_player < self.aggro_range:
                    self.state = 'chase'
                    self.chase_player()
                else:
                    self.state = 'patrol'
                    self.patrol()
            else:
                self.target = None
                self.state = 'patrol'
                self.patrol()
                
        def chase_player(self):
            if not self.target:
                return
                
            direction = (self.target.position - self.position).normalized()
            self.position += direction * 3 * time.dt
            self.look_at(self.target.position)
            
        def attack(self):
            if self.attack_cooldown > 0:
                self.attack_cooldown -= time.dt
                return
                
            if distance(self.position, self.target.position) <= self.attack_range:
                # 造成伤害
                self.target.take_damage(self.attack_damage)
                
                # 攻击特效
                self.play_attack_animation()
                self.create_attack_particles()
                
                self.attack_cooldown = 2.0  # 2秒攻击间隔
                
        def take_damage(self, damage, damage_type=None):
            """受到伤害"""
            # 根据伤害类型计算抗性
            damage_multiplier = 1.0
            
            if damage_type == 'wood' and self.enemy_type == 'corrupted_spirit':
                damage_multiplier = 1.5  # 木系对腐蚀灵体有加成
                
            actual_damage = damage * damage_multiplier
            self.health -= actual_damage
            
            # 显示伤害数字
            DamageNumber(actual_damage, self.position + (0, 2, 0))
            
            # 受伤效果
            self.blink_red()
            
            if self.health <= 0:
                self.die()
                
        def die(self):
            """敌人死亡"""
            # 掉落物品
            self.drop_loot()
            
            # 死亡动画
            self.animate_scale((0.1, 0.1, 0.1), duration=0.5)
            
            # 延迟销毁
            invoke(self.destroy, delay=0.5)
            
            # 通知任务系统
            QuestSystem.enemy_defeated(self.enemy_type)
```

**需要素材**：
- [ ] 敌人模型集合 (3-5种敌人类型)
- [ ] 攻击特效粒子
- [ ] 伤害数字字体和动画
- [ ] 敌人AI配置文件 (JSON格式)

---

#### **第8周：物品与装备系统**
```python
# week8/inventory_system.py
class InventorySystem:
    def __init__(self):
        self.items = []
        self.max_slots = 20
        self.equipped_items = {
            'weapon': None,
            'armor': None,
            'accessory': None
        }
        
    class Item:
        def __init__(self, item_id, name, item_type, stats, icon):
            self.id = item_id
            self.name = name
            self.type = item_type  # weapon, armor, consumable, material
            self.stats = stats
            self.icon = icon
            self.quantity = 1
            self.max_stack = 1
            
    def add_item(self, item_id, quantity=1):
        """添加物品到背包"""
        item_data = ITEM_DATABASE[item_id]
        
        # 检查是否可堆叠
        if item_data['max_stack'] > 1:
            # 寻找已有堆叠
            for item in self.items:
                if item.id == item_id and item.quantity < item.max_stack:
                    space_left = item.max_stack - item.quantity
                    add_amount = min(quantity, space_left)
                    item.quantity += add_amount
                    quantity -= add_amount
                    
                    if quantity <= 0:
                        return True
                        
        # 添加新物品
        while quantity > 0 and len(self.items) < self.max_slots:
            new_item = InventorySystem.Item(
                item_id=item_id,
                name=item_data['name'],
                item_type=item_data['type'],
                stats=item_data['stats'],
                icon=item_data['icon']
            )
            new_item.max_stack = item_data['max_stack']
            new_item.quantity = min(quantity, item_data['max_stack'])
            
            self.items.append(new_item)
            quantity -= new_item.quantity
            
        return quantity == 0
        
    def equip_item(self, item_slot):
        """装备物品"""
        if item_slot >= len(self.items):
            return
            
        item = self.items[item_slot]
        
        if item.type in ['weapon', 'armor', 'accessory']:
            # 卸下当前装备
            if self.equipped_items[item.type]:
                self.unequip_item(item.type)
                
            # 装备新物品
            self.equipped_items[item.type] = item
            self.apply_item_stats(item)
            
            # 从背包移除
            if item.quantity == 1:
                self.items.pop(item_slot)
            else:
                item.quantity -= 1
                
    def apply_item_stats(self, item):
        """应用物品属性"""
        player = scene.player
        
        if 'attack' in item.stats:
            player.attack_power += item.stats['attack']
        if 'defense' in item.stats:
            player.defense += item.stats['defense']
        if 'spirit_regen' in item.stats:
            player.spirit_regen_rate += item.stats['spirit_regen']
            
# 物品数据库
ITEM_DATABASE = {
    'wooden_staff': {
        'name': '木制法杖',
        'type': 'weapon',
        'stats': {'attack': 15, 'wood_power': 10},
        'icon': 'staff_icon',
        'max_stack': 1,
        'description': '蕴含自然灵力的法杖，增强木系能力'
    },
    'spirit_robe': {
        'name': '灵质长袍',
        'type': 'armor',
        'stats': {'defense': 20, 'spirit_regen': 5},
        'icon': 'robe_icon',
        'max_stack': 1,
        'description': '用灵丝编织的长袍，提升灵力恢复'
    },
    'healing_herb': {
        'name': '治愈草药',
        'type': 'consumable',
        'stats': {'heal': 50},
        'icon': 'herb_icon',
        'max_stack': 20,
        'description': '普通草药，可以恢复少量生命'
    }
}
```

**需要素材**：
- [ ] 物品图标全集 (64x64 PNG icons)
- [ ] 装备模型 (法杖、长袍等3D模型)
- [ ] 背包UI界面
- [ ] 物品描述文本数据

---

### 阶段三：内容填充（第9-12周）

#### **第9周：区域设计 - 起始森林**
**目标**：创建完整的起始区域
```python
# week9/starting_forest.py
class StartingForest:
    def __init__(self):
        self.name = "新手森林"
        self.size = (400, 400)  # 400x400单位
        self.regions = {
            'tutorial_grove': {
                'position': (0, 0, 0),
                'size': (50, 50),
                'features': ['training_dummies', 'guide_npc', 'spirit_pond']
            },
            'whispering_woods': {
                'position': (100, 0, 0),
                'size': (100, 150),
                'features': ['mystical_trees', 'hidden_paths', 'friendly_spirits']
            },
            'ancient_ruins': {
                'position': (-80, 0, 120),
                'size': (80, 80),
                'features': ['broken_pillars', 'spirit_altar', 'first_boss']
            }
        }
        
    def generate(self):
        """生成起始森林"""
        # 地形
        self.create_terrain()
        
        # 区域
        for region_name, region_data in self.regions.items():
            self.generate_region(region_name, region_data)
            
        # 路径连接
        self.connect_regions()
        
        # 动态元素
        self.add_dynamic_elements()
        
    def generate_region(self, region_name, region_data):
        """生成特定区域"""
        if region_name == 'tutorial_grove':
            self.create_tutorial_grove(region_data)
        elif region_name == 'whispering_woods':
            self.create_whispering_woods(region_data)
        elif region_name == 'ancient_ruins':
            self.create_ancient_ruins(region_data)
            
    def create_tutorial_grove(self, region_data):
        """创建教程林地区"""
        # 中心空地
        self.create_clearing(region_data['position'], 20)
        
        # 训练假人
        for i in range(3):
            dummy = TrainingDummy(
                position=(
                    region_data['position'][0] + random.uniform(-15, 15),
                    0,
                    region_data['position'][2] + random.uniform(-15, 15)
                )
            )
            
        # 向导NPC
        guide = NPC(
            name="老树精",
            faction="neutral",
            dialogue_tree=TUTORIAL_DIALOGUE,
            position=region_data['position']
        )
        
        # 灵质池塘
        pond = SpiritPond(
            position=(
                region_data['position'][0] + 10,
                0,
                region_data['position'][2] - 10
            )
        )
```

**需要素材**：
- [ ] 森林主题环境模型 (树木、岩石、地面杂物)
- [ ] 遗迹建筑模型
- [ ] 灵质池塘特效
- [ ] 区域背景音乐 (WAV/OGG格式)

---

#### **第10周：区域设计 - 元素领域**
**目标**：创建木、金、空间三个元素领域
```python
# week10/elemental_realms.py
class ElementalRealm:
    def __init__(self, element_type):
        self.element = element_type
        self.colors = self.get_realm_colors()
        self.atmosphere = self.create_atmosphere()
        self.challenges = []
        
    def get_realm_colors(self):
        """获取领域颜色主题"""
        color_schemes = {
            'wood': {
                'primary': color.rgb(76, 175, 80),
                'secondary': color.rgb(139, 195, 74),
                'accent': color.rgb(255, 193, 7),
                'ambient': color.rgb(200, 230, 200)
            },
            'metal': {
                'primary': color.rgb(158, 158, 158),
                'secondary': color.rgb(97, 97, 97),
                'accent': color.rgb(255, 215, 0),
                'ambient': color.rgb(180, 180, 200)
            },
            'spatial': {
                'primary': color.rgb(103, 58, 183),
                'secondary': color.rgb(156, 39, 176),
                'accent': color.rgb(0, 188, 212),
                'ambient': color.rgb(150, 150, 255, 100)
            }
        }
        return color_schemes[self.element]
        
    def create_atmosphere(self):
        """创建领域氛围"""
        atmosphere = Entity()
        
        # 天空颜色
        atmosphere.sky_color = self.colors['ambient']
        
        # 雾效
        if self.element == 'spatial':
            atmosphere.fog_color = self.colors['primary']
            atmosphere.fog_density = 0.03
        elif self.element == 'wood':
            atmosphere.fog_color = color.rgb(100, 150, 100, 150)
            atmosphere.fog_density = 0.02
            
        # 粒子效果
        atmosphere.particles = self.create_realm_particles()
        
        return atmosphere
        
    def create_realm_particles(self):
        """创建领域特有粒子"""
        particles = []
        
        if self.element == 'wood':
            # 飘落的树叶
            for _ in range(50):
                leaf = Particle(
                    model='quad',
                    texture='leaf_particle.png',
                    position=(
                        random.uniform(-100, 100),
                        random.uniform(10, 30),
                        random.uniform(-100, 100)
                    ),
                    scale=0.3,
                    color=self.colors['secondary'],
                    rotation=random.uniform(0, 360)
                )
                leaf.animate_y(
                    leaf.y - 40,
                    duration=random.uniform(3, 8),
                    curve=curve.linear,
                    loop=True
                )
                particles.append(leaf)
                
        elif self.element == 'spatial':
            # 漂浮的空间碎片
            for _ in range(30):
                fragment = Particle(
                    model='cube',
                    color=self.colors['accent'],
                    position=(
                        random.uniform(-80, 80),
                        random.uniform(5, 20),
                        random.uniform(-80, 80)
                    ),
                    scale=random.uniform(0.2, 0.5),
                    alpha=0.7
                )
                fragment.animate_rotation(
                    Vec3(
                        random.uniform(0, 360),
                        random.uniform(0, 360),
                        random.uniform(0, 360)
                    ),
                    duration=random.uniform(5, 10),
                    loop=True
                )
                particles.append(fragment)
                
        return particles
```

**需要素材**：
- [ ] 元素领域专属模型 (三种风格)
- [ ] 粒子特效贴图 (树叶、金属碎片、空间碎片)
- [ ] 元素领域背景音乐
- [ ] 环境音效 (风吹、金属回响、空间震动)

---

#### **第11周：剧情任务线设计**
**目标**：设计完整的主线剧情和支线任务
```python
# week11/storyline.py
class StorylineManager:
    def __init__(self):
        self.main_quests = []
        self.side_quests = []
        self.current_chapter = 0
        self.story_progress = {}
        
    class Chapter:
        def __init__(self, chapter_number, title, quests, cutscene=None):
            self.number = chapter_number
            self.title = title
            self.quests = quests
            self.cutscene = cutscene
            self.completed = False
            
    def setup_storyline(self):
        """设置完整剧情线"""
        self.main_quests = [
            self.Chapter(
                1,
                "灵域初醒",
                ['first_meeting', 'spirit_training', 'forest_threat'],
                cutscene='opening_cutscene'
            ),
            self.Chapter(
                2,
                "元素试炼",
                ['wood_trial', 'metal_trial', 'spatial_trial'],
                cutscene='element_intro'
            ),
            self.Chapter(
                3,
                "破碎的平衡",
                ['corruption_source', 'ancient_secret', 'guardian_alliance'],
                cutscene='corruption_reveal'
            ),
            self.Chapter(
                4,
                "众生之门",
                ['final_preparation', 'gate_ritual', 'true_purpose'],
                cutscene='ending_cutscene'
            )
        ]
        
        self.side_quests = [
            # 森林区域支线
            {'id': 'lost_spirit', 'region': 'starting_forest', 'min_level': 2},
            {'id': 'herbalist_request', 'region': 'starting_forest', 'min_level': 3},
            
            # 元素领域支线
            {'id': 'wood_grove_protection', 'region': 'wood_realm', 'min_level': 5},
            {'id': 'metal_forge_restoration', 'region': 'metal_realm', 'min_level': 6},
            {'id': 'spatial_puzzle', 'region': 'spatial_realm', 'min_level': 7},
            
            # 角色相关支线
            {'id': 'npcs_backstory', 'requirements': ['friendship_level'], 'min_level': 8}
        ]
        
    def start_chapter(self, chapter_number):
        """开始新章节"""
        if chapter_number < len(self.main_quests):
            chapter = self.main_quests[chapter_number]
            self.current_chapter = chapter_number
            
            # 播放章节开场动画
            if chapter.cutscene:
                self.play_cutscene(chapter.cutscene)
                
            # 激活章节第一个任务
            if chapter.quests:
                QuestSystem.activate_quest(chapter.quests[0])
                
    def complete_quest(self, quest_id):
        """完成任务并推进剧情"""
        # 检查是否是主线任务
        current_chapter = self.main_quests[self.current_chapter]
        
        if quest_id in current_chapter.quests:
            quest_index = current_chapter.quests.index(quest_id)
            
            # 如果是当前章节最后一个任务
            if quest_index == len(current_chapter.quests) - 1:
                self.complete_chapter(self.current_chapter)
            else:
                # 激活下一个任务
                next_quest = current_chapter.quests[quest_index + 1]
                QuestSystem.activate_quest(next_quest)
                
    def complete_chapter(self, chapter_number):
        """完成章节"""
        chapter = self.main_quests[chapter_number]
        chapter.completed = True
        
        # 章节奖励
        self.give_chapter_rewards(chapter_number)
        
        # 解锁新区域
        self.unlock_new_regions(chapter_number)
        
        # 如果还有下一章，开始下一章
        if chapter_number + 1 < len(self.main_quests):
            self.start_chapter(chapter_number + 1)
        else:
            # 游戏通关
            self.end_game()
            
    def give_chapter_rewards(self, chapter_number):
        """发放章节奖励"""
        rewards = {
            0: {'experience': 500, 'ability': 'double_jump'},
            1: {'experience': 1000, 'ability': 'elemental_fusion'},
            2: {'experience': 2000, 'title': '灵域守护者'},
            3: {'experience': 5000, 'ending': 'true_ending'}
        }
        
        if chapter_number in rewards:
            reward = rewards[chapter_number]
            player = scene.player
            
            if 'experience' in reward:
                player.gain_experience(reward['experience'])
                
            if 'ability' in reward:
                player.spirit_system.add_ability(reward['ability'])
                
            if 'title' in reward:
                player.title = reward['title']
                
            # 显示奖励提示
            RewardNotification.show(reward)
```

**需要素材**：
- [ ] 剧情对话文本 (完整剧本)
- [ ] 过场动画脚本和镜头设计
- [ ] 章节插图 (1920x1080 PNG)
- [ ] 配音脚本 (如果需要)

---

#### **第12周：能力成长系统**
```python
# week12/progression_system.py
class ProgressionSystem:
    def __init__(self):
        self.player_level = 1
        self.experience = 0
        self.ability_points = 0
        self.skill_trees = {}
        self.unlocked_abilities = []
        
    def setup_skill_trees(self):
        """设置技能树"""
        self.skill_trees = {
            'wood': {
                'name': '木系专精',
                'icon': 'wood_tree_icon',
                'nodes': {
                    'basic_vine': {
                        'name': '基础藤蔓',
                        'description': '召唤藤蔓束缚敌人',
                        'cost': 1,
                        'prerequisites': [],
                        'effects': {'vine_damage': 10, 'vine_duration': 3}
                    },
                    'vine_whip': {
                        'name': '藤蔓鞭挞',
                        'description': '用藤蔓抽打前方敌人',
                        'cost': 2,
                        'prerequisites': ['basic_vine'],
                        'effects': {'vine_range': 5, 'vine_damage': 25}
                    },
                    'healing_grove': {
                        'name': '治愈之森',
                        'description': '召唤治愈领域恢复生命',
                        'cost': 3,
                        'prerequisites': ['basic_vine'],
                        'effects': {'heal_per_second': 10, 'area_radius': 8}
                    }
                }
            },
            'spatial': {
                'name': '空间掌控',
                'icon': 'spatial_tree_icon',
                'nodes': {
                    'short_teleport': {
                        'name': '短距瞬移',
                        'description': '向前方短距离瞬移',
                        'cost': 1,
                        'prerequisites': [],
                        'effects': {'teleport_distance': 10}
                    },
                    'spatial_cut': {
                        'name': '空间切割',
                        'description': '制造空间裂缝攻击敌人',
                        'cost': 2,
                        'prerequisites': ['short_teleport'],
                        'effects': {'cut_damage': 30, 'cut_range': 15}
                    },
                    'dimension_pocket': {
                        'name': '维度口袋',
                        'description': '创建小型存储空间',
                        'cost': 3,
                        'prerequisites': ['short_teleport'],
                        'effects': {'extra_inventory_slots': 10}
                    }
                }
            }
        }
        
    def gain_experience(self, amount):
        """获得经验"""
        self.experience += amount
        
        # 检查升级
        while self.experience >= self.get_next_level_xp():
            self.level_up()
            
    def get_next_level_xp(self):
        """获取下一级所需经验"""
        # 指数增长公式
        base_xp = 100
        multiplier = 1.5
        return int(base_xp * (multiplier ** (self.player_level - 1)))
        
    def level_up(self):
        """升级"""
        self.player_level += 1
        self.ability_points += 1
        
        # 升级效果
        player = scene.player
        player.max_health += 20
        player.health = player.max_health
        player.max_spirit += 15
        player.spirit_energy = player.max_spirit
        
        # 升级特效
        self.play_level_up_effects()
        
        # 解锁新能力（每5级）
        if self.player_level % 5 == 0:
            self.unlock_new_ability_slot()
            
    def unlock_skill_node(self, tree_name, node_name):
        """解锁技能节点"""
        tree = self.skill_trees.get(tree_name)
        if not tree:
            return False
            
        node = tree['nodes'].get(node_name)
        if not node:
            return False
            
        # 检查前置条件
        for prereq in node['prerequisites']:
            if prereq not in self.unlocked_abilities:
                return False
                
        # 检查技能点
        if self.ability_points < node['cost']:
            return False
            
        # 解锁节点
        self.ability_points -= node['cost']
        self.unlocked_abilities.append(f"{tree_name}:{node_name}")
        
        # 应用效果
        self.apply_node_effects(tree_name, node_name, node['effects'])
        
        return True
        
    def apply_node_effects(self, tree_name, node_name, effects):
        """应用技能节点效果"""
        player = scene.player
        
        if tree_name == 'wood':
            if node_name == 'vine_whip':
                player.spirit_system.get_ability('wood_vine').damage = effects['vine_damage']
                player.spirit_system.get_ability('wood_vine').range = effects['vine_range']
            elif node_name == 'healing_grove':
                player.spirit_system.add_ability('wood_heal_area')
                
        elif tree_name == 'spatial':
            if node_name == 'spatial_cut':
                player.spirit_system.add_ability('spatial_cut')
```

**需要素材**：
- [ ] 技能树UI界面
- [ ] 技能图标全集
- [ ] 升级特效和音效
- [ ] 技能描述文本

---

### 阶段四：优化完善（第13-16周）

#### **第13周：性能优化**
```python
# week13/optimization.py
class PerformanceOptimizer:
    def __init__(self):
        self.draw_calls = 0
        self.triangle_count = 0
        self.fps = 60
        self.optimization_settings = {
            'lod_enabled': True,
            'culling_enabled': True,
            'texture_atlas': True,
            'instance_rendering': True
        }
        
    def apply_optimizations(self):
        """应用性能优化"""
        # 1. 细节层次(LOD)
        if self.optimization_settings['lod_enabled']:
            self.setup_lod_system()
            
        # 2. 视锥体剔除
        if self.optimization_settings['culling_enabled']:
            self.enable_frustum_culling()
            
        # 3. 纹理图集
        if self.optimization_settings['texture_atlas']:
            self.create_texture_atlases()
            
        # 4. 实例化渲染
        if self.optimization_settings['instance_rendering']:
            self.enable_instance_rendering()
            
        # 5. 动态批处理
        self.enable_dynamic_batching()
        
    def setup_lod_system(self):
        """设置LOD系统"""
        LOD_LEVELS = {
            'high': {'distance': 0, 'multiplier': 1.0},
            'medium': {'distance': 20, 'multiplier': 0.5},
            'low': {'distance': 50, 'multiplier': 0.2}
        }
        
        for entity in scene.entities:
            if hasattr(entity, 'lod_models'):
                entity.lod_handler = LODHandler(entity, LOD_LEVELS)
                
    class LODHandler:
        def __init__(self, entity, lod_settings):
            self.entity = entity
            self.lod_settings = lod_settings
            self.current_lod = 'high'
            
        def update(self, camera_position):
            distance = distance(self.entity.position, camera_position)
            
            new_lod = 'high'
            if distance > self.lod_settings['low']['distance']:
                new_lod = 'low'
            elif distance > self.lod_settings['medium']['distance']:
                new_lod = 'medium'
                
            if new_lod != self.current_lod:
                self.switch_lod(new_lod)
                
        def switch_lod(self, lod_level):
            self.current_lod = lod_level
            model_data = self.entity.lod_models[lod_level]
            
            self.entity.model = model_data['model']
            if 'texture' in model_data:
                self.entity.texture = model_data['texture']
                
    def enable_frustum_culling(self):
        """启用视锥体剔除"""
        camera = scene.camera
        
        def update_entity_visibility(entity):
            if hasattr(entity, 'always_visible') and entity.always_visible:
                entity.visible = True
                return
                
            # 检查是否在视锥体内
            is_visible = camera.frustum.contains(entity.world_position)
            entity.visible = is_visible
            
            # 递归处理子物体
            if hasattr(entity, 'children'):
                for child in entity.children:
                    update_entity_visibility(child)
                    
        # 应用到所有实体
        for entity in scene.entities:
            if not hasattr(entity, 'custom_visibility'):
                entity.custom_visibility = True
                entity.update = lambda e=entity: update_entity_visibility(e)
                
    def create_texture_atlases(self):
        """创建纹理图集"""
        atlases = {
            'terrain': {
                'size': (2048, 2048),
                'textures': ['grass', 'dirt', 'rock', 'sand', 'snow']
            },
            'characters': {
                'size': (1024, 1024),
                'textures': ['player_diffuse', 'npc_diffuse', 'enemy_diffuse']
            },
            'ui': {
                'size': (512, 512),
                'textures': ['icons', 'buttons', 'frames']
            }
        }
        
        for atlas_name, atlas_data in atlases.items():
            atlas = TextureAtlas(
                size=atlas_data['size'],
                textures=atlas_data['textures']
            )
            
            # 更新材质引用
            self.update_material_references(atlas_name, atlas)
```

**优化措施**：
1. **模型优化**：减少多边形数量，使用法线贴图
2. **纹理优化**：压缩纹理尺寸，使用BC/DXT压缩
3. **代码优化**：避免每帧创建对象，使用对象池
4. **内存管理**：及时卸载不用的资源

---

#### **第14周：音效与音乐系统**
```python
# week14/audio_system.py
class AudioSystem:
    def __init__(self):
        self.bgm_volume = 0.7
        self.sfx_volume = 0.8
        self.current_bgm = None
        self.audio_pool = AudioPool()
        
    class AudioPool:
        """音频池，复用音频对象"""
        def __init__(self):
            self.pool = {}
            self.max_instances = 10
            
        def play(self, audio_clip, position=None, volume=1.0, loop=False):
            # 从池中获取或创建音频对象
            pass
            
    def play_bgm(self, track_name, fade_duration=2):
        """播放背景音乐"""
        if self.current_bgm:
            self.fade_out_bgm(fade_duration)
            
        bgm_file = f'assets/audio/bgm/{track_name}.ogg'
        self.current_bgm = Audio(bgm_file, loop=True, volume=0)
        self.current_bgm.play()
        
        # 淡入效果
        self.current_bgm.animate_volume(self.bgm_volume, duration=fade_duration)
        
    def play_sfx(self, sfx_name, position=None, volume=None):
        """播放音效"""
        if volume is None:
            volume = self.sfx_volume
            
        sfx_file = f'assets/audio/sfx/{sfx_name}.wav'
        
        if position:
            # 3D音效
            audio = self.audio_pool.play_3d(sfx_file, position, volume)
        else:
            # 2D音效
            audio = self.audio_pool.play(sfx_file, volume)
            
        return audio
        
    def play_ambient(self, region_name):
        """播放环境音效"""
        ambient_sounds = {
            'forest': ['wind_light', 'birds_chirping', 'leaves_rustling'],
            'cave': ['dripping_water', 'echo_ambient', 'cave_wind'],
            'realm_wood': ['magic_hum', 'wood_creaking', 'spirit_whispers']
        }
        
        if region_name in ambient_sounds:
            sounds = ambient_sounds[region_name]
            
            # 随机播放环境音效
            for sound in sounds:
                delay = random.uniform(0, 10)
                invoke(lambda s=sound: self.play_sfx(s, volume=0.3), delay=delay)
                
    def setup_audio_events(self):
        """设置音频事件"""
        # 玩家相关
        player = scene.player
        
        # 脚步声
        player.footstep_sounds = {
            'grass': ['footstep_grass1', 'footstep_grass2'],
            'stone': ['footstep_stone1', 'footstep_stone2'],
            'wood': ['footstep_wood1', 'footstep_wood2']
        }
        
        # 能力音效
        ability_sounds = {
            'wood_vine': 'vine_growth',
            'wood_heal': 'healing_melody',
            'spatial_teleport': 'teleport_whoosh',
            'metal_shield': 'shield_activate'
        }
        
        # UI音效
        ui_sounds = {
            'button_click': 'ui_click',
            'menu_open': 'menu_open',
            'item_pickup': 'item_pickup',
            'quest_complete': 'quest_complete_jingle'
        }
```

**需要素材**：
- [ ] 背景音乐 (5-8首，各区域主题)
- [ ] 音效全集 (UI、能力、环境、战斗)
- [ ] 角色语音 (打招呼、战斗语音)
- [ ] 环境氛围音 (森林、洞穴、城市)

---

#### **第15周：UI/UX完善与本地化**
```python
# week15/ui_system.py
class UISystem:
    def __init__(self):
        self.current_screen = 'game'
        self.ui_elements = {}
        self.hud = HUD()
        self.menus = {}
        
    class HUD:
        def __init__(self):
            self.health_bar = HealthBar()
            self.spirit_bar = SpiritBar()
            self.minimap = Minimap()
            self.quest_tracker = QuestTracker()
            self.ability_bar = AbilityBar()
            
        def update(self, player):
            self.health_bar.value = player.health / player.max_health
            self.spirit_bar.value = player.spirit_energy / player.max_spirit
            self.minimap.update_player_position(player.position)
            
    def create_main_menu(self):
        """创建主菜单"""
        menu_background = Entity(
            model='quad',
            texture='assets/ui/main_menu_bg.png',
            scale=(16, 9),
            parent=camera.ui
        )
        
        buttons = [
            {
                'text': '开始游戏',
                'position': (0, 0.1),
                'on_click': self.start_new_game
            },
            {
                'text': '继续游戏',
                'position': (0, -0.1),
                'on_click': self.continue_game
            },
            {
                'text': '设置',
                'position': (0, -0.3),
                'on_click': self.open_settings
            },
            {
                'text': '退出游戏',
                'position': (0, -0.5),
                'on_click': application.quit
            }
        ]
        
        for btn_data in buttons:
            button = Button(
                text=btn_data['text'],
                position=btn_data['position'],
                scale=(0.3, 0.1),
                parent=camera.ui,
                on_click=btn_data['on_click']
            )
            
    def create_pause_menu(self):
        """创建暂停菜单"""
        pass
        
    def create_inventory_ui(self):
        """创建背包UI"""
        inventory_window = Window(
            title='背包',
            size=(0.8, 0.8),
            position=(0, 0),
            parent=camera.ui,
            draggable=False
        )
        
        # 物品格子
        slot_size = 0.08
        margin = 0.02
        columns = 5
        rows = 4
        
        for row in range(rows):
            for col in range(columns):
                slot = ItemSlot(
                    position=(
                        -0.4 + col * (slot_size + margin),
                        0.3 - row * (slot_size + margin)
                    ),
                    size=slot_size
                )
                
    class Localization:
        """本地化系统"""
        def __init__(self):
            self.languages = {
                'zh_CN': self.load_language('zh_CN'),
                'en_US': self.load_language('en_US'),
                'ja_JP': self.load_language('ja_JP')
            }
            self.current_language = 'zh_CN'
            
        def load_language(self, lang_code):
            """加载语言文件"""
            with open(f'assets/localization/{lang_code}.json', 'r', encoding='utf-8') as f:
                return json.load(f)
                
        def get_text(self, key, **kwargs):
            """获取本地化文本"""
            text = self.languages[self.current_language].get(key, key)
            
            # 替换参数
            if kwargs:
                try:
                    text = text.format(**kwargs)
                except:
                    pass
                    
            return text
            
        def switch_language(self, lang_code):
            """切换语言"""
            if lang_code in self.languages:
                self.current_language = lang_code
                self.update_all_ui_text()
```

**需要素材**：
- [ ] UI界面设计图 (所有界面)
- [ ] 字体文件 (支持中文、英文)
- [ ] UI音效 (按钮点击、菜单切换)
- [ ] 本地化文本文件 (JSON格式)

---

#### **第16周：测试、打包与发布**
```python
# week16/testing_deployment.py
class GameTester:
    def __init__(self):
        self.test_cases = []
        self.bug_reports = []
        self.performance_data = {}
        
    def run_automated_tests(self):
        """运行自动化测试"""
        tests = [
            self.test_player_movement,
            self.test_combat_system,
            self.test_save_load,
            self.test_quest_progression,
            self.test_performance
        ]
        
        for test_func in tests:
            try:
                result = test_func()
                print(f"{test_func.__name__}: {result}")
            except Exception as e:
                print(f"{test_func.__name__} FAILED: {e}")
                self.bug_reports.append({
                    'test': test_func.__name__,
                    'error': str(e)
                })
                
    def test_player_movement(self):
        """测试玩家移动"""
        player = scene.player
        
        # 测试各个方向移动
        test_positions = [
            (10, 0, 0),
            (-10, 0, 0),
            (0, 0, 10),
            (0, 0, -10),
            (0, 5, 0)  # 跳跃
        ]
        
        for pos in test_positions:
            player.position = (0, 0, 0)
            target_pos = player.position + pos
            
            # 模拟移动
            player.animate_position(target_pos, duration=1)
            
            # 等待动画完成
            time.sleep(1.1)
            
            # 检查位置
            if distance(player.position, target_pos) > 0.1:
                return f"移动测试失败: {pos}"
                
        return "移动测试通过"
        
    def performance_test(self):
        """性能测试"""
        fps_samples = []
        
        for _ in range(100):
            fps = application.fps_counter.get_fps()
            fps_samples.append(fps)
            
        avg_fps = sum(fps_samples) / len(fps_samples)
        min_fps = min(fps_samples)
        
        self.performance_data = {
            'avg_fps': avg_fps,
            'min_fps': min_fps,
            'memory_usage': get_memory_usage()
        }
        
        return f"平均FPS: {avg_fps:.1f}, 最低FPS: {min_fps}"
        
class BuildSystem:
    """打包系统"""
    def __init__(self):
        self.build_targets = ['windows', 'mac', 'linux']
        self.version = '1.0.0'
        
    def build_game(self, target):
        """打包游戏"""
        import subprocess
        import shutil
        
        # 清理旧的构建
        if os.path.exists('build'):
            shutil.rmtree('build')
            
        # 创建构建目录
        os.makedirs('build', exist_ok=True)
        
        # 复制游戏文件
        self.copy_game_files()
        
        # 打包资源
        self.package_assets()
        
        # 创建可执行文件
        if target == 'windows':
            self.build_windows_exe()
        elif target == 'mac':
            self.build_mac_app()
        elif target == 'linux':
            self.build_linux_app()
            
        # 创建安装包
        self.create_installer(target)
        
    def build_windows_exe(self):
        """构建Windows可执行文件"""
        # 使用PyInstaller
        subprocess.run([
            'pyinstaller',
            'main.py',
            '--name', '众生之门',
            '--onefile',
            '--windowed',
            '--icon', 'assets/icon.ico',
            '--add-data', 'assets;assets',
            '--distpath', 'build/windows'
        ])
        
    def create_installer(self, target):
        """创建安装程序"""
        if target == 'windows':
            self.create_nsis_installer()
        elif target == 'mac':
            self.create_dmg_installer()
            
    def create_nsis_installer(self):
        """创建NSIS安装程序"""
        nsis_script = f"""
        !define NAME "众生之门"
        !define VERSION "{self.version}"
        !define PUBLISHER "你的工作室"
        !define WEBSITE "https://yourwebsite.com"
        
        Name "${{NAME}}"
        OutFile "build/众生之门_Setup_v{self.version}.exe"
        InstallDir "$PROGRAMFILES\\${{NAME}}"
        
        Section "游戏文件"
          SetOutPath "$INSTDIR"
          File /r "build/windows/*"
        SectionEnd
        
        Section "开始菜单快捷方式"
          CreateDirectory "$SMPROGRAMS\\${{NAME}}"
          CreateShortCut "$SMPROGRAMS\\${{NAME}}\\${{NAME}}.lnk" "$INSTDIR\\众生之门.exe"
        SectionEnd
        
        Section "桌面快捷方式"
          CreateShortCut "$DESKTOP\\${{NAME}}.lnk" "$INSTDIR\\众生之门.exe"
        SectionEnd
        """
        
        with open('installer.nsi', 'w', encoding='utf-8') as f:
            f.write(nsis_script)
            
        subprocess.run(['makensis', 'installer.nsi'])
```

**发布清单**：
- [ ] 最终测试报告
- [ ] 游戏说明文档
- [ ] 打包配置检查
- [ ] 发布平台账号准备 (Steam、itch.io)
- [ ] 营销材料准备 (截图、预告片)

---

## 三、备用方案

### 1. 引擎备用方案
如果Ursina遇到性能问题：
```python
# 备用方案1: Panda3D
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()
        # Panda3D实现...

# 备用方案2: Pygame + PyOpenGL
import pygame
from OpenGL.GL import *

class PygameGame:
    def __init__(self):
        pygame.init()
        # 手动实现3D渲染...
```

### 2. 性能备用方案
- **简化模型**：如果性能不足，使用更简单的模型
- **2.5D方案**：改为2D精灵+3D背景混合
- **分区加载**：进一步减小同时加载的区域

### 3. 内容备用方案
- **缩短主线**：如果时间不足，简化支线任务
- **减少区域**：合并部分相似区域
- **简化系统**：去掉非核心系统（如天气系统）

## 四、素材详细清单

### 美术资源清单：
1. **角色模型** (FBX格式)：
   - 主角小黑 (含所有动画)
   - 10种NPC (人类、妖精、动物)
   - 8种敌人模型
   - 特殊角色模型

2. **环境模型** (FBX格式)：
   - 20种树木和植物
   - 15种岩石和地形
   - 建筑部件 (门、窗、柱子)
   - 特殊道具模型

3. **纹理贴图** (PNG格式)：
   - 角色贴图 (2048x2048)
   - 环境贴图 (1024x1024)
   - UI贴图 (512x512)
   - 特效贴图 (带透明通道)

4. **音频资源**：
   - 背景音乐 5-8首 (OGG格式)
   - 音效 100+个 (WAV格式)
   - 环境音 10种
   - UI音效 20种

5. **UI素材**：
   - 所有界面设计图
   - 图标集 (64x64, 128x128)
   - 字体文件 (支持中文)
   - 动画特效序列帧

### 技术资源清单：
1. **配置文件**：
   - 游戏平衡数据 (JSON)
   - 对话脚本 (JSON)
   - 任务数据 (JSON)
   - 能力配置 (JSON)

2. **脚本文件**：
   - 剧情脚本 (Markdown)
   - 关卡设计文档
   - AI行为树配置

3. **工具链**：
   - Blender导出脚本
   - 纹理打包工具
   - 音频处理脚本
   - 本地化工具

## 五、风险评估与应对

### 高风险项：
1. **性能问题**
   - 应对：早期性能测试，准备简化版本
   
2. **美术资源不足**
   - 应对：优先使用免费资源，简化艺术风格
   
3. **时间不足**
   - 应对：精简功能，聚焦核心玩法

### 中风险项：
1. **技术难题**
   - 应对：预留调研时间，准备备用方案
   
2. **内容质量**
   - 应对：定期玩家测试，及时调整

### 低风险项：
1. **小功能实现**
   - 应对：预留buffer时间

## 六、成功标准

### 最低可行产品 (MVP)：
- [ ] 可探索的起始区域
- [ ] 基础移动和战斗
- [ ] 3个主要能力
- [ ] 简单主线任务
- [ ] 基础UI

### 完整版本目标：
- [ ] 3个完整区域
- [ ] 10+小时游戏内容
- [ ] 完整的灵质系统
- [ ] 丰富的支线任务
- [ ] 优化的性能表现

### 理想版本：
- [ ] 5个区域以上
- [ ] 多结局系统
- [ ] 在线功能
- [ ] 创意工坊支持

这个详细计划文档涵盖了16周开发的所有方面。建议从第1周开始严格执行，每周结束时评估进度并调整后续计划。开发过程中保持灵活性，优先保证核心玩法的质量。祝你开发顺利！