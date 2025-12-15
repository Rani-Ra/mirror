# MCP 学习教程 - 从零开始

欢迎学习 Model Context Protocol (MCP)！这个仓库提供了一个完整的从零开始的 MCP 学习示例。

## 📚 什么是 MCP？

MCP (Model Context Protocol) 是由 Anthropic 开发的开放协议，用于在大型语言模型应用（如 Claude）和外部数据源/工具之间建立标准化连接。

### 主要优势

- **标准化**: 一次开发，多处使用
- **安全性**: 可控的权限和数据访问
- **可扩展**: 轻松添加新功能和工具
- **跨平台**: 支持多种编程语言和环境

## 🎯 本教程包含什么？

本仓库提供了一个**简单计算器 MCP 服务器**作为学习示例，包括：

- ✅ 完整的 MCP 服务器实现（加减乘除四则运算）
- ✅ 详细的中英文文档
- ✅ 测试脚本
- ✅ Claude Desktop 配置示例
- ✅ 逐步教学指南

## 🚀 快速开始

### 前置要求

- Node.js 18 或更高版本
- npm 或 yarn
- （可选）Claude Desktop 应用

### 安装步骤

```bash
# 1. 进入示例目录
cd mcp-example

# 2. 安装依赖
npm install

# 3. 测试服务器（可选）
npm test

# 4. 启动服务器
npm start
```

## 📖 完整教程

### 快速入门
- **⚡ 5分钟快速开始**: [QUICKSTART.md](./mcp-example/QUICKSTART.md) - 最快速度体验 MCP

### 详细文档
- **📘 中文完整教程**: [mcp-example/README.md](./mcp-example/README.md) - 详细的学习指南
- **📗 English Tutorial**: [mcp-example/README_EN.md](./mcp-example/README_EN.md) - Complete guide in English
- **🏗️ 架构图解**: [mcp-example/ARCHITECTURE.md](./mcp-example/ARCHITECTURE.md) - 深入理解 MCP 架构
- **📖 使用指南**: [mcp-example/USAGE_GUIDE.md](./mcp-example/USAGE_GUIDE.md) - Claude Desktop 配置详解

### 内容包括：
1. MCP 基础概念详解
2. 代码逐行解析
3. 如何配置到 Claude Desktop
4. 如何扩展和自定义
5. 常见问题解答
6. 调试技巧

## 📁 项目结构

```
mirror/
├── mcp-example/                    # MCP 示例项目
│   ├── src/
│   │   ├── index.js               # MCP 服务器主文件
│   │   └── test.js                # 测试脚本
│   ├── package.json               # 项目配置
│   ├── README.md                  # 中文详细教程
│   ├── README_EN.md               # 英文详细教程
│   ├── .gitignore                 # Git 忽略文件
│   └── claude_desktop_config.example.json  # 配置示例
└── README.md                      # 本文件
```

## 🎓 学习路径

### 第一步：理解基础概念
阅读 [mcp-example/README.md](./mcp-example/README.md) 中的"什么是 MCP"部分

### 第二步：运行示例
```bash
cd mcp-example
npm install
npm test
```

### 第三步：研究代码
打开 `mcp-example/src/index.js`，跟随注释理解每一部分的作用

### 第四步：配置到 Claude Desktop
按照教程配置文件，在 Claude Desktop 中实际使用

### 第五步：自定义扩展
尝试添加新的数学运算功能（如平方根、幂运算等）

## 💡 示例功能

这个计算器 MCP 服务器提供以下工具：

| 工具名称 | 描述 | 示例 |
|---------|------|------|
| `add` | 两数相加 | 15 + 27 = 42 |
| `subtract` | 两数相减 | 100 - 45 = 55 |
| `multiply` | 两数相乘 | 8 × 9 = 72 |
| `divide` | 两数相除 | 144 ÷ 12 = 12 |

## 🔧 在 Claude Desktop 中使用

配置完成后，你可以在 Claude Desktop 中这样使用：

```
你: 请帮我计算 1234 + 5678
Claude: [调用 add 工具] 计算结果是 6912

你: 帮我算一下 987 除以 3
Claude: [调用 divide 工具] 987 ÷ 3 = 329
```

## 📚 扩展学习资源

- [MCP 官方网站](https://modelcontextprotocol.io/)
- [MCP 技术规范](https://spec.modelcontextprotocol.io/)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [更多 MCP 服务器示例](https://github.com/modelcontextprotocol/servers)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个教程！

## 📄 许可证

MIT License

## ❓ 常见问题

### Q: 我需要什么编程基础？

A: 基础的 JavaScript/Node.js 知识即可。教程中包含详细注释。

### Q: 除了 Claude Desktop，还能在哪里使用？

A: MCP 服务器可以与任何支持 MCP 协议的客户端配合使用，包括自定义的 AI 应用。

### Q: 可以用 Python 实现吗？

A: 可以！MCP 提供了 Python SDK。本教程使用 JavaScript 是因为它更易于入门。

### Q: 如何调试我的 MCP 服务器？

A: 可以使用 `npx @modelcontextprotocol/inspector` 工具，详见教程中的调试部分。

---

**开始你的 MCP 学习之旅吧！** 🚀

有问题？请查看 [详细教程](./mcp-example/README.md) 或提交 Issue。
