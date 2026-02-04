### 众生之门：罗小黑战记开源AI文本游戏（Portal of All Beings）

[![GitHub stars](https://img.shields.io/github/stars/ewanqian/portal-of-all-beings.svg?style=social)](https://github.com/ewanqian/portal-of-all-beings/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ewanqian/portal-of-all-beings.svg?style=social)](https://github.com/ewanqian/portal-of-all-beings/network/members)
[![GitHub issues](https://img.shields.io/github/issues/ewanqian/portal-of-all-beings.svg)](https://github.com/ewanqian/portal-of-all-beings/issues)
[![GitHub license](https://img.shields.io/github/license/ewanqian/portal-of-all-beings.svg)](https://github.com/ewanqian/portal-of-all-beings/blob/main/LICENSE)

### 项目介绍

**众生之门AI文本游戏**是一个基于《罗小黑战记》动画中"众生之门"设定开发的开源AI文本游戏项目。我们致力于使用人工智能技术和多人在线文本游戏系统，构建一个模拟众生之门世界观的智能游戏体验。

### 核心功能

#### 🎮 沉浸式文本游戏体验
- 基于罗小黑战记众生之门设定的丰富游戏世界
- 真实还原原作的灵力体系和世界观
- 动态生成的游戏场景和剧情

#### 🤖 AI驱动的NPC系统
- 智能NPC，能够与玩家进行自然交互
- 核心角色（罗小黑、无限、老君等）具有个性化的AI行为模式
- 角色具备情感记忆和行为模仿能力

#### 🌐 多人在线交互
- 支持实时多人聊天、组队和协作
- 阵营博弈系统，三大阵营（老君派、风息派、中立派）的动态平衡
- 玩家之间可以进行PVP战斗和PVE挑战

#### 📊 动态游戏世界
- 根据玩家行为动态变化的游戏环境
- 玩家的选择会影响世界的发展和剧情走向
- 场景细节会随玩家互动而变化

#### 🎯 多样化的成长系统
- 六大系灵力体系（御灵系、锁御系、造物系、生灵系、心灵系、空间系）
- 基于行为的能力进化机制，玩家行为直接影响角色成长
- 无固定职业，玩家可自由组合灵力模块创造新技能

#### 🏆 竞技与挑战
- PVP、PVE挑战和Boss战
- 基于种族特性的团队挑战
- 解谜系统，分为"法则层"和"现象层"双重解谜

#### 🏙️ 完整的社交系统
- 好友、公会、交易等社交功能
- 基于好感度的动态对话系统
- 玩家行为影响阵营声望和世界反馈

### 游戏玩法

本游戏支持两种主要玩法模式，玩家可以根据自己的喜好自由选择：

#### 🎭 角色扮演模式
- **基于动画剧情**：根据TV动画的众生之门篇进行游戏
- **扮演动画角色**：玩家可以选择扮演山新、阿根、小白、小黑、老君、无限等动画角色
- **剧情体验**：体验动画中角色的视角和经历，与其他角色互动
- **线性体验**：按照动画剧情的发展进行游戏，增强代入感

#### 🌍 开放世界模式
- **自由创建角色**：玩家可以创建自己的角色，选择种族、灵力倾向等
- **自由探索**：在开放的游戏世界中自由探索，完成任务，提升能力
- **沙盒玩法**：没有固定的剧情路线，玩家可以按照自己的意愿发展
- **模拟经营**：玩家可以建立自己的势力，影响游戏世界

#### 🎨 玩法兼容
- 两种玩法模式完全兼容，玩家可以随时切换
- 下版本更新将进一步增强两种玩法的融合
- 支持跨玩法的玩家互动

### 下版本更新计划

我们正在积极开发下一版本"灵质空间1.0"，主要更新内容包括：
- 实现角色扮演模式，支持玩家扮演动画角色
- 增强开放世界模式的内容和玩法
- 完善AI驱动的角色创建系统
- 优化核心角色AI交互
- 实现动态叙事与剧情系统
- 改进战斗与解谜系统
- 完善内容合规与风险控制

详细的更新计划请查看[NEXT_VERSION_PLAN.md](NEXT_VERSION_PLAN.md)

### 技术栈

本项目正在探索多种技术方案，目前主要考虑以下技术栈：

#### 前端
- **框架**：现代前端框架（React / Vue / Svelte）+ TypeScript
- **构建工具**：现代化构建工具（Vite / Webpack 5）
- **3D渲染**：Three.js 或其他WebGL库
- **状态管理**：轻量级状态管理方案（Zustand / Jotai / Pinia）
- **UI组件库**：主流UI组件库（Ant Design / Arco Design / Element Plus）
- **样式**：CSS预处理器或CSS-in-JS方案（Tailwind CSS / Styled Components / CSS Modules）

#### 后端
- **运行时**：Node.js 18+ 或其他JavaScript运行时
- **框架**：Express / Koa / NestJS 或其他Node.js框架
- **实时通信**：WebSocket (ws库 / Socket.io)
- **数据库**：MongoDB / PostgreSQL / Redis 或其他数据库
- **AI服务**：大语言模型API / 自定义AI模型 / 本地AI模型

#### AI技术
- 自然语言处理
- 对话生成
- 动态内容生成
- 智能决策系统
- 角色行为模拟

### 快速开始

#### 环境要求
- Node.js 18+
- npm 9+ 或 yarn 3+
- MongoDB 6+
- Redis 7+

#### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/ewanqian/portal-of-all-beings.git
cd portal-of-all-beings
```

2. **安装依赖**
```bash
# 安装根依赖
npm install

# 安装前端依赖
cd client
npm install

# 安装后端依赖
cd ../server
npm install
```

3. **配置环境变量**
```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑.env文件，配置数据库连接、API密钥等
```

4. **启动开发服务器**
```bash
# 启动后端开发服务器
cd server
npm run dev

# 启动前端开发服务器（新开一个终端）
cd ../client
npm run dev
```

5. **访问游戏**
打开浏览器访问 `http://localhost:5173`

### 项目结构

```
portal-of-all-beings/
├── .github/                    # GitHub配置文件
├── docs/                       # 项目文档
├── client/                     # 前端代码
├── server/                     # 后端代码
├── shared/                     # 共享代码
├── tests/                      # 测试代码
├── .editorconfig               # 编辑器配置
├── .env.example                # 环境变量示例
├── .gitignore                  # Git忽略文件
├── LICENSE                     # 许可证
├── package.json                # 根依赖配置
└── README.md                   # 项目说明文档
```

### 贡献指南

我们欢迎社区贡献！请查看[贡献指南](docs/guides/贡献指南.md)了解如何参与项目开发。

### 编码规范

请遵循我们的[编码规范](docs/guides/编码规范.md)以保持代码质量和一致性。

### 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

### 联系方式

- **GitHub Issues**：[提交问题或建议](https://github.com/ewanqian/portal-of-all-beings/issues)
- **Email**：project@example.com

### 特别感谢

- **寒木春华动画团队**：感谢《罗小黑战记》动画团队为我们提供了精彩的世界观和设定，这是本项目创作的灵感源泉
- 所有为项目做出贡献的开发者和社区成员

### 版权声明

1. 本项目是基于《罗小黑战记》及其衍生作品《众生之门》设定的**非盈利、粉丝爱好向开源项目**
2. 项目仅供学习、研究和交流使用，不用于任何商业目的
3. 所有与《罗小黑战记》相关的版权、商标、角色、设定等知识产权均归**寒木春华动画团队**所有
4. 本项目尊重原作知识产权，所有内容均以原作设定为准，寒木春华动画团队保留最终解释权
5. 本项目的原创代码和设计采用 MIT 许可证开源

### 项目愿景

我们致力于打造一个：
- 开放、包容的开源游戏项目
- 结合人工智能和游戏设计的创新体验
- 能够让玩家自由探索和创造的虚拟世界
- 促进社区协作和创新的平台
- 尊重原作知识产权的粉丝作品典范

---

**众生之门（Portal of All Beings）** - 探索灵的世界，连接现实与虚拟

*"空间不是冷漠的容器，而是充满了记忆和梦想。" - Gaston Bachelard*
