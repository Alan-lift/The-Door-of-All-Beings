# 《众生之门》3D游戏开发详细计划文档

## 一、项目总览
**项目名称**：众生之门（仿《罗小黑战记》风格）  
**项目周期**：16周（4个月）  
**目标平台**：Windows/Mac/Linux  
**技术栈**：Python + Ursina Engine + Blender

## 二、详细时间轴

### 第1-2周：项目基础与原型
**目标**：建立开发环境，创建可运行的最小原型

**详细任务：**
- **第1周**：
  - [ ] 环境搭建（Python 3.9+, Ursina安装）
  - [ ] 项目结构设计
  - [ ] 基础窗口与摄像机系统
  - [ ] 角色移动原型（WASD控制）
  
- **第2周**：
  - [ ] 简单地形生成系统
  - [ ] 基础UI：生命值/灵力值显示
  - [ ] 基础交互系统（拾取物品）
  - [ ] 第一版原型演示

### 第3-6周：核心系统开发
**目标**：实现游戏核心机制

**详细任务：**
- **第3周**：角色系统
  - [ ] 角色属性系统（生命、灵力、敏捷等）
  - [ ] 基础动画系统（走、跑、跳）
  - [ ] 摄像机跟随系统

- **第4周**：灵质能力系统
  - [ ] 木系能力：藤蔓生长、植物控制
  - [ ] 金系能力：金属操控、防御护盾
  - [ ] 空间系：瞬移、空间存储

- **第5周**：世界交互
  - [ ] 物理交互系统（推、拉、举起）
  - [ ] 环境互动系统（开关门、采集）
  - [ ] 天气系统基础

- **第6周**：AI系统
  - [ ] NPC基础AI（巡逻、对话）
  - [ ] 敌人AI（追击、攻击）
  - [ ] 对话系统框架

### 第7-10周：游戏内容开发
**目标**：填充游戏世界内容

**详细任务：**
- **第7-8周**：游戏区域1 - 新手森林
  - [ ] 地形设计与制作（1平方公里）
  - [ ] 场景布置：树木、岩石、建筑
  - [ ] NPC放置：5个主要NPC
  - [ ] 任务线设计：3个引导任务

- **第9-10周**：游戏区域2 - 灵质遗迹
  - [ ] 遗迹建筑群设计
  - [ ] 谜题系统：机关、符文解密
  - [ ] 敌人类型：2种遗迹守卫
  - [ ] 隐藏区域设计

### 第11-14周：系统完善与优化
**目标**：完善游戏体验

**详细任务：**
- **第11周**：任务与叙事系统
  - [ ] 任务追踪系统
  - [ ] 对话树系统
  - [ ] 剧情推进机制
  - [ ] 分支选择系统

- **第12周**：UI/UX全面优化
  - [ ] 主菜单/暂停菜单
  - [ ] 背包/技能界面
  - [ ] 地图系统（小地图+世界地图）
  - [ ] 提示与教程系统

- **第13周**：音效与视觉效果
  - [ ] 环境音效系统
  - [ ] 技能特效优化
  - [ ] 光影系统完善
  - [ ] 粒子系统增强

- **第14周**：性能优化与测试
  - [ ] 内存优化（区块加载）
  - [ ] 渲染优化（LOD系统）
  - [ ] 碰撞检测优化
  - [ ] Beta测试与bug修复

### 第15-16周：发布准备
**目标**：打包与发布

**详细任务：**
- **第15周**：
  - [ ] 游戏平衡调整
  - [ ] 最终内容审核
  - [ ] 打包脚本制作（PyInstaller）
  - [ ] 兼容性测试

- **第16周**：
  - [ ] 游戏文档编写
  - [ ] 宣传材料准备
  - [ ] 发布到Itch.io等平台
  - [ ] 收集玩家反馈

## 三、详细素材需求清单

### 1. 3D模型资源
```
角色模型（需要制作）：
- 主角小黑（低多边形，三角形耳朵，大尾巴）：约2000面
- 人类角色模型（3种体型）：各1500面
- 妖精NPC（5种不同种类）：各1200-1800面
- 敌人模型（遗迹守卫、森林精怪）：各1000-1500面

环境模型：
- 树木（4种风格）：各800面
- 岩石（5种形状）：各500面
- 建筑元素（门、窗、柱子）：各200-500面
- 特殊植物（发光的灵质植物）：3种，各300面

道具模型：
- 灵质结晶（5种颜色）
- 任务物品（10种）
- 交互道具（开关、按钮等）
```

### 2. 纹理材质
```
角色材质：
- 小黑毛皮质感（2K贴图）
- 服装纹理（人类角色用）
- 特殊材质（发光、半透明效果）

环境材质：
- 地形纹理（草地、泥土、岩石）：各2K
- 建筑纹理（木材、石材）：各2K
- 特效纹理（法线贴图、高光贴图）

UI纹理：
- 图标集合（技能、状态、物品）
- 界面背景（木质、布纹质感）
- 按钮状态（正常、悬停、按下）
```

### 3. 动画资源
```
角色动画（需要制作）：
- 基础移动：走、跑、跳、蹲
- 战斗动画：轻攻击、重攻击、防御
- 技能动画：各能力施放动作
- 互动动画：拾取、推拉、对话

特效动画：
- 技能特效：藤蔓生长、金属变形、空间扭曲
- 环境特效：树叶飘落、水面波纹、光线变化
- UI动画：按钮反馈、提示弹出
```

### 4. 音频资源
```
环境音效：
- 森林环境音（风声、鸟鸣）
- 遗迹环境音（回声、机械声）
- 天气音效（雨声、雷声）

角色音效：
- 脚步声（草地、石地、木地板）
- 攻击音效（物理、能力攻击）
- 互动音效（拾取、开门）

UI音效：
- 按钮点击
- 菜单切换
- 提示音

背景音乐：
- 主菜单音乐（1-2分钟）
- 探索音乐（森林、遗迹各1首）
- 战斗音乐（1首）
- 剧情音乐（3首不同情绪）
```

### 5. 字体与界面
```
中文字体：
- 标题字体（1种，有中国风特色）
- 正文字体（1-2种，清晰易读）

界面元素：
- 血条/灵力条设计
- 技能图标（20-30个）
- 物品图标（50-80个）
```

## 四、详细实现逻辑架构

### 1. 核心游戏循环
```python
class GameLoop:
    def __init__(self):
        self.running = True
        self.clock = Clock()
        
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # 60 FPS
            
            # 处理输入
            self.process_input()
            
            # 更新逻辑
            self.update(dt)
            
            # 渲染
            self.render()
            
            # 检查游戏状态
            self.check_game_state()
```

### 2. 灵质能力系统详细设计
```python
class SpiritAbilitySystem:
    def __init__(self):
        self.abilities = {
            'wood': {
                'vine_growth': VineGrowthAbility(),
                'plant_control': PlantControlAbility(),
                'healing': HealingAbility()
            },
            'metal': {
                'shield': MetalShieldAbility(),
                'blade': MetalBladeAbility(),
                'construct': ConstructAbility()
            },
            'spatial': {
                'blink': BlinkAbility(),
                'pocket_space': PocketSpaceAbility(),
                'portal': PortalAbility()
            }
        }
        
    def activate_ability(self, element, ability_name, caster):
        """激活能力"""
        ability = self.abilities[element][ability_name]
        
        # 检查灵力
        if caster.spirit_energy < ability.cost:
            return False
            
        # 执行能力效果
        result = ability.execute(caster)
        
        # 消耗灵力
        if result:
            caster.spirit_energy -= ability.cost
            caster.trigger_cooldown(ability)
            
        return result
```

### 3. 任务系统详细设计
```python
class QuestSystem:
    def __init__(self):
        self.active_quests = []
        self.quest_log = []
        
    def add_quest(self, quest_data):
        quest = Quest(
            id=quest_data['id'],
            title=quest_data['title'],
            description=quest_data['description'],
            objectives=[
                QuestObjective(type, target, count)
                for type, target, count in quest_data['objectives']
            ],
            rewards=quest_data['rewards'],
            prerequisites=quest_data.get('prerequisites', [])
        )
        self.active_quests.append(quest)
        
    def update_quest_progress(self, event_type, target, amount=1):
        """更新任务进度"""
        for quest in self.active_quests:
            if not quest.completed:
                quest.update_progress(event_type, target, amount)
                
                if quest.is_completed():
                    self.complete_quest(quest)
                    
    def complete_quest(self, quest):
        """完成任务"""
        quest.completed = True
        self.active_quests.remove(quest)
        self.quest_log.append(quest)
        
        # 发放奖励
        self.grant_rewards(quest.rewards)
        
        # 触发后续任务
        self.check_chain_quests(quest.id)
```

### 4. 世界生成算法
```python
class WorldGenerator:
    def __init__(self, seed=12345):
        self.seed = seed
        random.seed(seed)
        self.noise_generator = PerlinNoise()
        self.chunks = {}  # (x,z) -> Chunk
        self.active_chunks = set()
        
    def generate_chunk(self, chunk_x, chunk_z):
        """生成地形区块（32x32单位）"""
        chunk_key = (chunk_x, chunk_z)
        
        if chunk_key in self.chunks:
            return self.chunks[chunk_key]
            
        chunk = Chunk(chunk_x, chunk_z)
        
        # 使用柏林噪声生成高度图
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                world_x = chunk_x * CHUNK_SIZE + x
                world_z = chunk_z * CHUNK_SIZE + z
                
                # 基础地形高度
                height = self.noise_generator.fractal(
                    world_x * 0.01, 
                    world_z * 0.01, 
                    octaves=4
                )
                
                # 添加细节噪声
                detail = self.noise_generator.noise(
                    world_x * 0.05,
                    world_z * 0.05
                )
                
                final_height = height * 20 + detail * 5
                
                # 确定地形类型
                terrain_type = self.get_terrain_type(height, detail)
                
                # 生成方块
                chunk.set_block(x, final_height, z, terrain_type)
                
                # 在地表生成植被
                if terrain_type == 'grass':
                    self.generate_vegetation(chunk, x, final_height, z)
                    
        self.chunks[chunk_key] = chunk
        return chunk
```

### 5. NPC AI状态机
```python
class NPCStateMachine:
    def __init__(self, npc):
        self.npc = npc
        self.current_state = 'idle'
        self.states = {
            'idle': IdleState(),
            'patrol': PatrolState(),
            'chase': ChaseState(),
            'combat': CombatState(),
            'flee': FleeState(),
            'conversation': ConversationState()
        }
        
    def update(self, dt, player_position):
        state_obj = self.states[self.current_state]
        
        # 检查状态转移条件
        new_state = state_obj.check_transition(self.npc, player_position)
        
        if new_state and new_state != self.current_state:
            # 退出当前状态
            state_obj.exit(self.npc)
            
            # 进入新状态
            self.current_state = new_state
            self.states[new_state].enter(self.npc)
            
        # 执行当前状态行为
        self.states[self.current_state].execute(self.npc, dt, player_position)
```

## 五、备用方案与风险应对

### 技术风险应对：
1. **性能不足问题**：
   - 主要方案：Ursina引擎优化
   - 备用方案1：切换到Panda3D（更专业但更复杂）
   - 备用方案2：使用Godot引擎（GDScript类似Python）

2. **3D模型制作困难**：
   - 主要方案：Blender制作低多边形模型
   - 备用方案1：使用MagicaVoxel制作体素风格
   - 备用方案2：使用免费资源修改适应风格
   - 备用方案3：程序化生成简单模型

3. **Python打包问题**：
   - 主要方案：PyInstaller打包
   - 备用方案1：使用Nuitka编译
   - 备用方案2：制作绿色免安装版

### 内容风险应对：
1. **美术资源不足**：
   - 主要方案：按计划制作
   - 备用方案：简化美术风格（增加程序化生成）
   - 最低方案：使用纯色几何体+简单贴图

2. **开发时间不足**：
   - 核心功能优先：确保基础玩法完整
   - 内容删减预案：
     - 将3个区域缩减为2个
     - 减少NPC种类和任务数量
     - 简化技能系统

3. **技术实现困难**：
   - 复杂功能简化：如将实时天气改为静态天空盒
   - 寻求社区帮助：Ursina Discord/中文论坛
   - 使用现成插件：如对话系统插件

### 开发流程保障：
1. **版本控制**：
   - 主分支：稳定版本
   - 开发分支：功能开发
   - 每周提交：确保进度可追溯

2. **测试计划**：
   - 每周末：内部测试最新功能
   - 第8周：Alpha测试（核心玩家测试）
   - 第14周：Beta测试（公开测试）

3. **进度监控**：
   - 每日：简短进度汇报（个人开发日志）
   - 每周：功能演示与调整
   - 每月：里程碑评估与计划调整

## 六、开发资源与工具

### 必需工具：
1. **编程工具**：
   - VS Code + Python扩展
   - Git + GitHub/Gitee
   
2. **美术工具**：
   - Blender 3.0+（3D建模）
   - GIMP/Krita（2D贴图）
   - MagicaVoxel（体素备用）

3. **音频工具**：
   - Audacity（音效处理）
   - Bosca Ceoil（免费音乐制作）

4. **项目管理**：
   - Trello/Notion（任务跟踪）
   - Miro（系统设计图）

### 学习资源：
1. Ursina官方示例与文档
2. Blender Guru教程（Donut系列）
3. 《游戏编程模式》电子书
4. 《罗小黑战记》分镜与设定分析

## 七、成功标准与交付物

### 最低可行产品（MVP）：
- [ ] 可控制角色在1个区域移动
- [ ] 实现3种基础灵质能力
- [ ] 完成1条主线任务
- [ ] 5个可交互NPC
- [ ] 基础UI和音效

### 完整版本目标：
- [ ] 2-3个风格各异的游戏区域
- [ ] 完整的灵质能力树（9种能力）
- [ ] 3-5小时游戏内容
- [ ] 丰富的NPC和支线任务
- [ ] 优化的视觉效果和音效
- [ ] 稳定的60FPS性能

### 最终交付物：
1. 可执行游戏文件（.exe/.app）
2. 游戏文档（操作指南、世界观介绍）
3. 源代码（可选开源）
4. 开发日志与设计文档
5. 宣传素材（截图、视频）

---

这个计划文档提供了从零开始开发《众生之门》的完整路线图。建议从小型原型开始，逐步迭代，每周评估进度并适当调整计划。最重要的是保持动力和创意，享受创造游戏世界的过程！