const readline = require('readline');

// 创建命令行界面
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: '> '
});

// 游戏状态
class GameState {
  constructor() {
    this.player = new Player();
    this.currentScene = '蓝溪镇';
    this.scenes = this.initializeScenes();
    this.npcs = this.initializeNPCs();
    this.tasks = this.initializeTasks();
    this.gameRunning = true;
  }

  initializeScenes() {
    return {
      '蓝溪镇': {
        description: '这是一个充满灵气的小镇，街道两旁是古色古香的建筑，空气中弥漫着淡淡的花香。你看到老君坐在茶馆前喝茶，小黑在旁边玩耍。',
        exits: { '东': '森林', '西': '河流', '北': '道观' },
        npcs: ['老君', '小黑'],
        items: ['灵气结晶', '茶叶']
      },
      '森林': {
        description: '茂密的森林，阳光透过树叶洒下斑驳的光影。你听到鸟儿的歌声，偶尔传来小动物的叫声。',
        exits: { '西': '蓝溪镇' },
        npcs: [],
        items: ['草药', '木材']
      },
      '河流': {
        description: '清澈的河流，水流缓缓流淌。河边有几块光滑的石头，远处可以看到一座小桥。',
        exits: { '东': '蓝溪镇' },
        npcs: [],
        items: ['鱼', '水灵石']
      },
      '道观': {
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
        name: '调查森林灵气',
        description: '老君让你去森林调查灵气异常的原因。',
        giver: '老君',
        status: 'available',
        reward: {灵力值: 50, 记忆值: 20 },
        requirements: {地点: '森林'}
      },
      '采集草药': {
        name: '采集草药',
        description: '无限需要你去森林采集一些草药。',
        giver: '无限',
        status: 'available',
        reward: {灵力值: 30, 体力值: 20 },
        requirements: {地点: '森林'}
      }
    };
  }

  processCommand(command) {
    const parts = command.toLowerCase().split(' ');
    const action = parts[0];
    const target = parts.slice(1).join(' ');

    switch (action) {
      case 'go':
        return this.handleGoCommand(target);
      case 'look':
        return this.handleLookCommand(target);
      case 'talk':
        return this.handleTalkCommand(target);
      case 'take':
        return this.handleTakeCommand(target);
      case 'status':
        return this.player.getStatus();
      case 'help':
        return this.showHelp();
      case 'quit':
        this.gameRunning = false;
        return '游戏结束，再见！';
      default:
        return `未知命令: ${command}。输入 'help' 查看可用命令。`;
    }
  }

  handleGoCommand(direction) {
    const scene = this.scenes[this.currentScene];
    if (scene.exits[direction]) {
      this.currentScene = scene.exits[direction];
      return `你向${direction}走去，来到了${this.currentScene}。\n${this.scenes[this.currentScene].description}`;
    } else {
      return `你不能往${direction}走。`;
    }
  }

  handleLookCommand(target) {
    const scene = this.scenes[this.currentScene];
    if (!target) {
      return scene.description;
    }
    
    if (scene.npcs.includes(target)) {
      return this.npcs[target].description;
    }
    
    if (scene.items.includes(target)) {
      return `你看到了${target}，它似乎很有用。`;
    }
    
    return `你没有看到${target}。`;
  }

  handleTalkCommand(target) {
    const scene = this.scenes[this.currentScene];
    if (scene.npcs.includes(target)) {
      const npc = this.npcs[target];
      return `[${npc.name}]: ${npc.dialogue['问候']}`;
    } else {
      return `这里没有${target}。`;
    }
  }

  handleTakeCommand(target) {
    const scene = this.scenes[this.currentScene];
    const itemIndex = scene.items.indexOf(target);
    if (itemIndex !== -1) {
      scene.items.splice(itemIndex, 1);
      this.player.addItem(target);
      this.player.updateAttributes(target);
      return `你拿起了${target}。`;
    } else {
      return `这里没有${target}可以拿。`;
    }
  }

  showHelp() {
    return `可用命令:\n` +
           `go [方向] - 向指定方向移动\n` +
           `look [目标] - 查看当前场景或特定目标\n` +
           `talk [NPC] - 与NPC交谈\n` +
           `take [物品] - 拿起物品\n` +
           `status - 查看角色状态\n` +
           `help - 显示帮助信息\n` +
           `quit - 退出游戏`;
  }
}

// 玩家类
class Player {
  constructor() {
    this.name = '旅行者';
    this.attributes = {
      灵力值: 100,
      生命值: 100,
      体力值: 100,
      记忆值: 0,
      梦想值: 0
    };
    this.inventory = [];
    this.level = 1;
    this.experience = 0;
  }

  addItem(item) {
    this.inventory.push(item);
  }

  updateAttributes(item) {
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
        this.attributes[attr] += value;
      }
    }
  }

  getStatus() {
    return `=== 角色状态 ===\n` +
           `姓名: ${this.name}\n` +
           `等级: ${this.level}\n` +
           `经验: ${this.experience}\n` +
           `灵力值: ${this.attributes.灵力值}\n` +
           `生命值: ${this.attributes.生命值}\n` +
           `体力值: ${this.attributes.体力值}\n` +
           `记忆值: ${this.attributes.记忆值}\n` +
           `梦想值: ${this.attributes.梦想值}\n` +
           `背包: ${this.inventory.length > 0 ? this.inventory.join(', ') : '空'}\n` +
           `================`;
  }
}

// 游戏初始化
const game = new GameState();

// 游戏开始
console.log('=== 众生之门文本游戏原型 ===');
console.log('欢迎来到蓝溪镇！这是一个充满灵气的世界。');
console.log(game.scenes[game.currentScene].description);
console.log('输入 "help" 查看可用命令。');
console.log('===============================');

rl.prompt();

// 命令处理循环
rl.on('line', (input) => {
  const response = game.processCommand(input.trim());
  console.log('\n' + response);
  
  if (game.gameRunning) {
    rl.prompt();
  } else {
    rl.close();
  }
}).on('close', () => {
  console.log('\n感谢游玩！');
  process.exit(0);
});