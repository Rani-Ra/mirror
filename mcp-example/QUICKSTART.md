# 快速开始 - 5分钟体验 MCP

本指南帮助你在 5 分钟内快速体验 MCP 服务器。

## 步骤 1: 安装依赖 (1分钟)

```bash
cd mcp-example
npm install
```

## 步骤 2: 测试服务器 (1分钟)

```bash
npm test
```

你应该看到类似这样的输出：

```
🚀 启动 MCP 服务器测试...
✅ 成功连接到 MCP 服务器

📋 测试 1: 获取可用工具列表
找到 4 个工具:
  - add: 将两个数字相加
  - subtract: 计算两个数字的差
  - multiply: 将两个数字相乘
  - divide: 计算两个数字的商

➕ 测试 2: 加法运算 (15 + 27)
结果: 计算结果: 15 + 27 = 42

✅ 所有测试完成!
```

## 步骤 3: 配置到 Claude Desktop (2分钟)

### 获取项目路径
```bash
pwd
# 输出示例: /Users/yourname/projects/mirror/mcp-example
```

### 编辑 Claude 配置文件

**macOS:**
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```cmd
notepad %APPDATA%\Claude\claude_desktop_config.json
```

### 添加配置

```json
{
  "mcpServers": {
    "simple-calculator": {
      "command": "node",
      "args": [
        "【这里粘贴你的完整路径】/src/index.js"
      ]
    }
  }
}
```

## 步骤 4: 重启并使用 (1分钟)

1. 重启 Claude Desktop
2. 输入: "请帮我计算 15 + 27"
3. Claude 会自动调用你的 MCP 服务器！

## 完整示例对话

```
你: 请帮我计算 15 + 27

Claude: 让我帮你计算...
[使用 simple-calculator 工具]
计算结果: 15 + 27 = 42

答案是 42。
```

## 恭喜！🎉

你已经成功创建并使用了第一个 MCP 服务器！

## 接下来做什么？

### 学习更多
- 阅读 [完整教程](README.md)
- 查看 [架构文档](ARCHITECTURE.md)
- 探索 [详细使用指南](USAGE_GUIDE.md)

### 自定义服务器
尝试添加新的数学运算：

1. 打开 `src/index.js`
2. 在工具列表中添加新工具（如 `power`, `sqrt`）
3. 在调用处理器中实现功能
4. 保存并重启 Claude Desktop
5. 测试新功能！

### 示例：添加平方运算

在 `src/index.js` 的工具列表中添加：

```javascript
{
  name: "square",
  description: "计算数字的平方",
  inputSchema: {
    type: "object",
    properties: {
      x: { type: "number", description: "要平方的数字" }
    },
    required: ["x"]
  }
}
```

在 `CallToolRequestSchema` 处理器的 switch 语句中添加：

```javascript
case "square":
  result = args.x * args.x;
  break;
```

保存后重启 Claude，就可以使用了：

```
你: 请帮我计算 12 的平方
Claude: [使用 square 工具] 12 的平方是 144
```

## 故障排除

### 测试失败？
```bash
# 检查 Node.js 版本 (需要 18+)
node --version

# 重新安装依赖
rm -rf node_modules package-lock.json
npm install
```

### Claude Desktop 看不到服务器？
1. 检查配置文件路径是否正确
2. 确认使用的是**绝对路径**
3. 检查 JSON 格式是否正确（可以用 JSONLint.com 验证）
4. 重启 Claude Desktop

### 路径中有空格？
确保路径被正确引用：
```json
"/Users/my name/projects/mirror/mcp-example/src/index.js"
```

## 需要帮助？

- 查看 [完整使用指南](USAGE_GUIDE.md)
- 阅读 [常见问题解答](README.md#常见问题)
- 提交 Issue 到 GitHub 仓库

---

**享受你的 MCP 学习之旅！** 🚀
