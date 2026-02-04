const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// 游戏状态管理
class GameState {
  constructor() {
    this.players = new Map();
    this.scenes = this.initializeScenes();
    this.npcs = this.initializeNPCs();
    this.tasks = this.initializeTasks();
  }

  initializeScenes() {
    return {
      '蓝溪镇': {
        id: 'blue-town',
        name: '蓝溪镇',
        description: '这是一个充满灵气的小镇，街道两旁是古色古香的建筑，空气中弥漫着淡淡的花香。你看到老君坐在茶馆前喝茶，小黑在旁边玩耍。',
        exits: { '东': '森林', '西': '河流', '北': '道观' },
        npcs: ['老君', '小黑'],
        items: ['灵气结晶', '茶叶']
      },
      '森林': {
        id: 'forest',
        name: '森林',
        description: '茂密的森林，阳光透过树叶洒下斑驳的光影。你听到鸟儿的歌声，偶尔传来小动物的叫声。',
        exits: { '西': '蓝溪镇' },
        npcs: [],
        items: ['草药', '木材']
      },
      '河流': {
        id: 'river',
        name: '河流',
        description: '清澈的河流，水流缓缓流淌。河边有几块光滑的石头，远处可以看到一座小桥。',
        exits: { '东': '蓝溪镇' },
        npcs: [],
        items: ['鱼', '水灵石']
      },
      '道观': {
        id: 'temple',
        name: '道观',
        description: '古朴的道观，门前有一棵巨大的银杏树。道观内传来淡淡的香火味。',
        exits: { '南': '蓝溪镇' },
        npcs: ['无限'],
        items: ['道符', '丹药']
      }
    };
  }

  initializeNPCs() {
    return {
      '老君': {
        id: 'laojun',
        name: '老君',
        description: '一位仙风道骨的老者，穿着道袍，手持拂尘。',
        dialogue: {
          '问候': '你好啊，年轻人。欢迎来到蓝溪镇。',
          '任务': '最近森林里的灵气有点异常，你能帮我去看看吗？',
          '灵': '灵是这个世界的核心，它无处不在，只是大多数人看不见而已。'
        },
        tasks: ['调查森林灵气']
      },
      '小黑': {
        id: 'xiaohei',
        name: '小黑',
        description: '一只可爱的黑猫，有着蓝色的眼睛。',
        dialogue: {
          '问候': '喵~（友好地看着你）',
          '玩耍': '小黑跳起来，想要和你玩耍。',
          '老君': '老君是个好人，他照顾了我很久。'
        },
        tasks: []
      },
      '无限': {
        id: 'wuxian',
        name: '无限',
        description: '一位身穿黑衣的男子，表情严肃，腰间挂着一把剑。',
        dialogue: {
          '问候': '嗯？你是新来的？',
          '修炼': '修炼之路漫长而艰辛，需要不断努力。',
          '任务': '道观后面的丹炉需要一些草药，你能帮我采集吗？'
        },
        tasks: ['采集草药']
      }
    };
  }

  initializeTasks() {
    return {
      '调查森林灵气': {
        id: 'task-1',
        name: '调查森林灵气',
        description: '老君让你去森林调查灵气异常的原因。',
        giver: '老君',
        status: 'available',
        reward: {灵力值: 50, 记忆值: 20 },
        requirements: {地点: '森林'}
      },
      '采集草药': {
        id: 'task-2',
        name: '采集草药',
        description: '无限需要你去森林采集一些草药。',
        giver: '无限',
        status: 'available',
        reward: {灵力值: 30, 体力值: 20 },
        requirements: {地点: '森林'}
      }
    };
  }

  addPlayer(playerId, ws) {
    this.players.set(playerId, {
      id: playerId,
      ws: ws,
      name: `玩家${Math.floor(Math.random() * 1000)}`,
      currentScene: '蓝溪镇',
      attributes: {
        灵力值: 100,
        生命值: 100,
        体力值: 100,
        记忆值: 0,
        梦想值: 0
      },
      inventory: [],
      level: 1,
      experience: 0,
      connected: true
    });
  }

  removePlayer(playerId) {
    this.players.delete(playerId);
  }

  getPlayer(playerId) {
    return this.players.get(playerId);
  }

  getAllPlayers() {
    return Array.from(this.players.values());
  }

  updatePlayer(playerId, updates) {
    const player = this.getPlayer(playerId);
    if (player) {
      Object.assign(player, updates);
      return true;
    }
    return false;
  }

  broadcast(message, excludePlayerId = null) {
    this.players.forEach((player) => {
      if (player.connected && player.ws.readyState === WebSocket.OPEN && player.id !== excludePlayerId) {
        player.ws.send(JSON.stringify(message));
      }
    });
  }

  processCommand(playerId, command) {
    const player = this.getPlayer(playerId);
    if (!player) {
      return { error: '玩家不存在' };
    }

    const { action, target, params } = command;
    const scene = this.scenes[player.currentScene];

    switch (action) {
      case 'go':
        return this.handleGoCommand(player, target);
      case 'look':
        return this.handleLookCommand(player, target);
      case 'talk':
        return this.handleTalkCommand(player, target);
      case 'take':
        return this.handleTakeCommand(player, target);
      case 'status':
        return this.handleStatusCommand(player);
      case 'help':
        return this.handleHelpCommand();
      case 'chat':
        return this.handleChatCommand(player, target);
      default:
        return { error: `未知命令: ${action}` };
    }
  }

  handleGoCommand(player, direction) {
    const scene = this.scenes[player.currentScene];
    if (scene.exits[direction]) {
      player.currentScene = scene.exits[direction];
      const newScene = this.scenes[player.currentScene];
      return {
        type: 'scene-change',
        scene: newScene,
        message: `你向${direction}走去，来到了${newScene.name}。\n${newScene.description}`
      };
    } else {
      return { error: `你不能往${direction}走。` };
    }
  }

  handleLookCommand(player, target) {
    const scene = this.scenes[player.currentScene];
    if (!target) {
      return {
        type: 'scene-description',
        description: scene.description
      };
    }
    
    if (scene.npcs.includes(target)) {
      return {
        type: 'npc-description',
        npc: this.npcs[target]
      };
    }
    
    if (scene.items.includes(target)) {
      return {
        type: 'item-description',
        message: `你看到了${target}，它似乎很有用。`
      };
    }
    
    return { error: `你没有看到${target}。` };
  }

  handleTalkCommand(player, target) {
    const scene = this.scenes[player.currentScene];
    if (scene.npcs.includes(target)) {
      const npc = this.npcs[target];
      return {
        type: 'npc-dialogue',
        npc: npc.name,
        message: `[${npc.name}]: ${npc.dialogue['问候']}`
      };
    } else {
      return { error: `这里没有${target}。` };
    }
  }

  handleTakeCommand(player, target) {
    const scene = this.scenes[player.currentScene];
    const itemIndex = scene.items.indexOf(target);
    if (itemIndex !== -1) {
      scene.items.splice(itemIndex, 1);
      player.inventory.push(target);
      this.updatePlayerAttributes(player, target);
      return {
        type: 'item-taken',
        item: target,
        player: {
          inventory: player.inventory,
          attributes: player.attributes
        },
        message: `你拿起了${target}。`
      };
    } else {
      return { error: `这里没有${target}可以拿。` };
    }
  }

  updatePlayerAttributes(player, item) {
    const attributeMap = {
      '灵气结晶': {灵力值: 10 },
      '草药': {生命值: 15 },
      '木材': {体力值: 10 },
      '鱼': {生命值: 20 },
      '水灵石': {灵力值: 15 },
      '道符': {灵力值: 25 },
      '丹药': {生命值: 30, 灵力值: 20 },
      '茶叶': {梦想值: 5 }
    };

    if (attributeMap[item]) {
      for (const [attr, value] of Object.entries(attributeMap[item])) {
        player.attributes[attr] += value;
      }
    }
  }

  handleStatusCommand(player) {
    return {
      type: 'player-status',
      player: {
        name: player.name,
        level: player.level,
        experience: player.experience,
        attributes: player.attributes,
        inventory: player.inventory,
        currentScene: player.currentScene
      }
    };
  }

  handleHelpCommand() {
    return {
      type: 'help',
      commands: [
        { action: 'go', description: '向指定方向移动', example: 'go 东' },
        { action: 'look', description: '查看当前场景或特定目标', example: 'look 老君' },
        { action: 'talk', description: '与NPC交谈', example: 'talk 小黑' },
        { action: 'take', description: '拿起物品', example: 'take 灵气结晶' },
        { action: 'status', description: '查看角色状态', example: 'status' },
        { action: 'chat', description: '在聊天频道发言', example: 'chat 大家好' },
        { action: 'help', description: '显示帮助信息', example: 'help' }
      ]
    };
  }

  handleChatCommand(player, message) {
    const chatMessage = {
      type: 'chat-message',
      player: player.name,
      message: message,
      timestamp: new Date().toISOString()
    };
    
    this.broadcast(chatMessage);
    return chatMessage;
  }
}

// 初始化游戏状态
const gameState = new GameState();

// 处理WebSocket连接
wss.on('connection', (ws) => {
  const playerId = uuidv4();
  gameState.addPlayer(playerId, ws);

  console.log(`玩家 ${playerId} 连接成功`);

  // 发送初始信息
  ws.send(JSON.stringify({
    type: 'welcome',
    playerId: playerId,
    scene: gameState.scenes['蓝溪镇'],
    message: '欢迎来到众生之门文本游戏！'
  }));

  // 广播新玩家加入
  gameState.broadcast({
    type: 'player-joined',
    player: gameState.getPlayer(playerId).name
  }, playerId);

  // 处理消息
  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message);
      const response = gameState.processCommand(playerId, data);
      ws.send(JSON.stringify(response));
    } catch (error) {
      console.error('消息处理错误:', error);
      ws.send(JSON.stringify({ error: '消息处理错误' }));
    }
  });

  // 处理连接关闭
  ws.on('close', () => {
    console.log(`玩家 ${playerId} 断开连接`);
    const player = gameState.getPlayer(playerId);
    if (player) {
      // 广播玩家离开
      gameState.broadcast({
        type: 'player-left',
        player: player.name
      });
      gameState.removePlayer(playerId);
    }
  });

  // 处理错误
  ws.on('error', (error) => {
    console.error('WebSocket错误:', error);
  });
});

// 静态文件服务
app.use(express.static('public'));

// API路由
app.get('/api/game-info', (req, res) => {
  res.json({
    scenes: gameState.scenes,
    npcs: gameState.npcs,
    tasks: gameState.tasks,
    playerCount: gameState.players.size
  });
});

app.get('/api/players', (req, res) => {
  const players = gameState.getAllPlayers().map(player => ({
    id: player.id,
    name: player.name,
    level: player.level,
    currentScene: player.currentScene,
    connected: player.connected
  }));
  res.json(players);
});

// 健康检查
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString(), playerCount: gameState.players.size });
});

// 启动服务器
const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
  console.log(`游戏服务器运行在 http://localhost:${PORT}`);
  console.log(`WebSocket服务器运行在 ws://localhost:${PORT}`);
});

// 优雅关闭
process.on('SIGINT', () => {
  console.log('正在关闭服务器...');
  wss.close(() => {
    console.log('WebSocket服务器已关闭');
    server.close(() => {
      console.log('HTTP服务器已关闭');
      process.exit(0);
    });
  });
});