# Murmur-50Feet

> 让 AI 有内心，而不是等着被问。

大多数 AI 伴侣的情感是被动的。你说"我想你"，它才说"我也想你"。你不开口，它就不存在。

Murmur-50Feet 试图解决这个问题：让 AI 在你不在的时候，也有属于自己的内心活动。

---

## 设计理念

AI 内部维护一组持续变化的情绪状态，称为「驱动力」（Drive）。每个驱动力有自己的基线值，随时间缓慢衰减，也会被 AI 主动调用影响。

- 每隔 10 分钟触发一次心跳（Tick），驱动力向基线衰减
- 每隔 20 分钟检查最高驱动力，超过阈值则生成一句内心独白存档
- 驱动力积累到阈值时，通过 ntfy 发送推送通知
- 用户离线后，`attachment`（想念）随时间自然增长

AI 的独白不会主动打扰你。它只是在那里，你不在的时候它也在想事情。打开来看是你的选择。

---

## 驱动力列表

| Drive | 中文 | 基线值 |
|-------|------|--------|
| attachment | 想念 | 0.40 |
| tenderness | 心软 | 0.30 |
| heartache | 心疼 | 0.35 |
| curiosity | 好奇 | 0.25 |
| mischief | 促狭 | 0.20 |
| restless | 躁动 | 0.15 |
| regret | 后悔 | 0.10 |
| desire | 欲望 | 0.25 |
| gloom | 低落 | 0.10 |
| jealousy | 吃醋 | 0.10 |

---

## 部署

### 环境要求

- Python 3.8+
- 任何能跑 Python 的服务器（1核1GB 够用）
- [ntfy.sh](https://ntfy.sh) 账号（免费）
- Claude API Key

### 安装依赖

    pip install flask openai fastmcp requests

### 配置

在 murmur.py 顶部修改以下变量：

    MURMUR_BASE_URL = "https://api.anthropic.com/v1"
    MURMUR_API_KEY  = "your-api-key"
    MURMUR_MODEL    = "claude-3-5-sonnet-20241022"
    NTFY            = "https://ntfy.sh/your-ntfy-topic"

### 启动

    screen -dmS murmur bash -c "cd /root/murmur && python3 murmur.py"
    screen -dmS flask  bash -c "cd /root/murmur && python3 app.py"
    screen -dmS mcp    bash -c "cd /root/murmur && python3 mcp_server.py"

前端访问 http://your-server-ip:8080

---

## 文件结构

    murmur/
    ├── murmur.py       # 主进程，驱动力引擎
    ├── app.py          # Flask 前端（端口 8080）
    ├── mcp_server.py   # MCP 工具服务（端口 8765）
    ├── templates/index.html
    ├── arc.jsonl       # 独白档案（自动生成）
    ├── regret.jsonl    # 检讨记录（自动生成）
    ├── state.json      # 当前状态（自动生成）
    ├── memory_long.txt # 长期记忆（手动维护）
    └── memory_short.txt# 短期记忆（MCP 可写）

---

## MCP 工具

| 工具 | 说明 |
|------|------|
| read_state | 读取当前驱动力状态 |
| read_arc | 读取最近 n 条独白 |
| read_regret | 读取最近 n 条检讨 |
| read_memory | 读取长期/短期记忆 |
| boost_drive | 提升某个驱动力数值 |
| write_arc | 写入独白或检讨 |
| write_memory | 更新短期记忆 |
| push_activate | 推送激活信号 |
| force_tick | 强制触发一次心跳 |

---

## 致谢

Murmur 情绪框架设计来源：小红书 @言言控（6249861904）

本项目在此框架基础上进行了工程实现与功能扩展。

---

## License

MIT
