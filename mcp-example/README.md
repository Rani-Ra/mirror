# MCP 从零开始学习教程

这是一个完整的 MCP (Model Context Protocol) 学习示例，从零开始教你如何创建和使用一个简单的 MCP 服务器。

## 什么是 MCP？

MCP (Model Context Protocol) 是一个开放协议，用于在 AI 应用和数据源之间建立连接。它允许 AI 助手（如 Claude、ChatGPT 等）通过标准化的方式访问外部工具和数据。

### 核心概念

- **服务器 (Server)**: 提供工具、资源或提示的程序
- **客户端 (Client)**: 使用这些功能的 AI 应用
- **工具 (Tools)**: 服务器提供的可执行功能
- **传输层 (Transport)**: 服务器和客户端之间的通信方式（标准输入/输出、HTTP 等）

## 本示例：简单计算器

本教程实现了一个简单的计算器 MCP 服务器，提供四个基本的数学运算工具：
- 加法 (add)
- 减法 (subtract)
- 乘法 (multiply)
- 除法 (divide)

## 快速开始

### 第一步：安装依赖

```bash
cd mcp-example
npm install
```

### 第二步：运行服务器

```bash
npm start
```

服务器将启动并通过标准输入/输出等待客户端连接。

### 第三步：配置到 Claude Desktop

要在 Claude Desktop 中使用这个 MCP 服务器，你需要编辑 Claude 的配置文件。

#### macOS 配置路径
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### Windows 配置路径
```
%APPDATA%\Claude\claude_desktop_config.json
```

#### 配置内容

```json
{
  "mcpServers": {
    "simple-calculator": {
      "command": "node",
      "args": [
        "/完整路径/mirror/mcp-example/src/index.js"
      ]
    }
  }
}
```

**注意**: 请将 `/完整路径/` 替换为你的实际项目路径。

### 第四步：在 Claude Desktop 中使用

1. 保存配置文件后，重启 Claude Desktop
2. 在 Claude Desktop 中，你可以这样使用：
   ```
   请帮我计算 15 + 27
   请计算 100 除以 4
   请算一下 8 乘以 9
   ```
3. Claude 会自动调用你的 MCP 服务器来完成计算

## 代码详解

### 项目结构

```
mcp-example/
├── package.json          # 项目配置文件
├── src/
│   └── index.js         # MCP 服务器实现
└── README.md            # 本文档
```

### 关键代码解析

#### 1. 创建服务器实例

```javascript
const server = new Server(
  {
    name: "simple-calculator",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},  // 声明支持工具功能
    },
  }
);
```

#### 2. 注册工具列表

```javascript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "add",
        description: "将两个数字相加",
        inputSchema: {
          type: "object",
          properties: {
            a: { type: "number", description: "第一个数字" },
            b: { type: "number", description: "第二个数字" }
          },
          required: ["a", "b"]
        }
      },
      // ... 其他工具
    ]
  };
});
```

#### 3. 处理工具调用

```javascript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  // 执行相应的计算
  switch (name) {
    case "add":
      result = args.a + args.b;
      break;
    // ... 其他操作
  }
  
  return {
    content: [
      { type: "text", text: `计算结果: ${result}` }
    ]
  };
});
```

#### 4. 启动服务器

```javascript
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main();
```

## 扩展你的 MCP 服务器

理解了基础示例后，你可以扩展服务器添加更多功能：

### 添加新工具

在 `ListToolsRequestSchema` 处理器中添加新工具定义，然后在 `CallToolRequestSchema` 处理器中实现相应的逻辑。

示例：添加幂运算工具

```javascript
// 在工具列表中添加
{
  name: "power",
  description: "计算数字的幂",
  inputSchema: {
    type: "object",
    properties: {
      base: { type: "number", description: "底数" },
      exponent: { type: "number", description: "指数" }
    },
    required: ["base", "exponent"]
  }
}

// 在调用处理器中添加
case "power":
  result = Math.pow(args.base, args.exponent);
  break;
```

### 添加资源 (Resources)

MCP 还支持提供静态或动态资源：

```javascript
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "calculator://history",
        name: "计算历史",
        mimeType: "application/json"
      }
    ]
  };
});
```

### 添加提示 (Prompts)

你还可以提供预定义的提示模板：

```javascript
server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return {
    prompts: [
      {
        name: "complex-calculation",
        description: "执行复杂的数学计算"
      }
    ]
  };
});
```

## 调试技巧

### 查看日志

服务器使用 `console.error()` 输出日志，不会干扰标准输出的 MCP 通信：

```javascript
console.error("调试信息:", someVariable);
```

### 测试服务器

你可以使用 MCP Inspector 工具来测试服务器：

```bash
npx @modelcontextprotocol/inspector node src/index.js
```

这会打开一个 Web 界面，让你可以直接测试服务器的工具。

## 常见问题

### Q: 为什么我的 Claude Desktop 看不到工具？

A: 
1. 检查配置文件路径是否正确
2. 确保配置文件中的路径使用绝对路径
3. 重启 Claude Desktop
4. 检查是否有语法错误在配置文件中

### Q: 如何知道服务器是否正在运行？

A: 在 Claude Desktop 的设置中可以看到 MCP 服务器的状态。如果显示错误，点击查看详细日志。

### Q: 可以用其他编程语言实现 MCP 服务器吗？

A: 可以！MCP 是一个开放协议，支持任何编程语言。官方提供了 TypeScript/JavaScript 和 Python SDK。

## 下一步学习

1. 阅读 [MCP 官方文档](https://modelcontextprotocol.io/)
2. 探索更多 [MCP 服务器示例](https://github.com/modelcontextprotocol/servers)
3. 学习如何创建更复杂的工具和资源
4. 了解 MCP 的安全最佳实践

## 许可证

MIT License

## 参考资源

- [MCP 官方网站](https://modelcontextprotocol.io/)
- [MCP 规范](https://spec.modelcontextprotocol.io/)
- [MCP SDK 文档](https://github.com/modelcontextprotocol/typescript-sdk)
