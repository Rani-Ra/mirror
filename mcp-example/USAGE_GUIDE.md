# 使用指南 - 如何在 Claude Desktop 中使用这个 MCP 服务器

## 前提条件

1. 已安装 Node.js (v18 或更高版本)
2. 已安装 Claude Desktop 应用
3. 已完成项目依赖安装 (`npm install`)

## 详细步骤

### 第一步：找到配置文件

根据你的操作系统，找到 Claude Desktop 的配置文件：

#### macOS
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

如果文件不存在，手动创建它：
```bash
mkdir -p ~/Library/Application\ Support/Claude
touch ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### Windows
```
%APPDATA%\Claude\claude_desktop_config.json
```

如果文件不存在，手动创建它：
```cmd
mkdir %APPDATA%\Claude
type nul > %APPDATA%\Claude\claude_desktop_config.json
```

#### Linux
```bash
~/.config/Claude/claude_desktop_config.json
```

如果文件不存在，手动创建它：
```bash
mkdir -p ~/.config/Claude
touch ~/.config/Claude/claude_desktop_config.json
```

### 第二步：获取项目的绝对路径

在项目目录中运行：

```bash
cd /path/to/mirror/mcp-example
pwd
```

这会显示类似这样的路径：
- macOS/Linux: `/Users/username/projects/mirror/mcp-example`
- Windows: `C:\Users\username\projects\mirror\mcp-example`

### 第三步：编辑配置文件

打开 `claude_desktop_config.json` 并添加以下内容：

```json
{
  "mcpServers": {
    "simple-calculator": {
      "command": "node",
      "args": [
        "/Users/username/projects/mirror/mcp-example/src/index.js"
      ]
    }
  }
}
```

**重要提示：**
- 使用你在第二步中获得的**完整绝对路径**
- 路径必须指向 `src/index.js` 文件
- Windows 用户请使用双反斜杠 `\\` 或单斜杠 `/`
- 确保 JSON 格式正确（注意逗号和括号）

### 第四步：重启 Claude Desktop

1. 完全退出 Claude Desktop 应用
2. 重新启动 Claude Desktop

### 第五步：验证配置

在 Claude Desktop 中：

1. 点击设置图标（通常在右上角）
2. 查找 "MCP Servers" 或相关选项
3. 确认 "simple-calculator" 显示为已连接状态

如果显示错误：
- 检查路径是否正确
- 确认 Node.js 已安装且在 PATH 中
- 查看错误日志了解具体问题

### 第六步：开始使用！

现在你可以在 Claude Desktop 中使用计算器功能了：

#### 示例对话

**你**: 请帮我计算 123 + 456

**Claude**: 让我帮你计算...
*[调用 add 工具]*
结果是 579。

**你**: 那 1000 除以 8 是多少？

**Claude**: 让我计算一下...
*[调用 divide 工具]*
1000 除以 8 等于 125。

**你**: 帮我算一下 15 乘以 23

**Claude**: 好的...
*[调用 multiply 工具]*
15 × 23 = 345

## 故障排除

### 问题 1: Claude Desktop 看不到 MCP 服务器

**可能原因：**
- 配置文件路径不正确
- JSON 格式错误
- Node.js 未安装或不在 PATH 中

**解决方法：**
1. 验证配置文件路径
2. 使用 JSON 验证工具检查格式
3. 在终端运行 `node --version` 确认 Node.js 可用

### 问题 2: 服务器显示错误状态

**可能原因：**
- index.js 路径不正确
- 依赖未安装

**解决方法：**
1. 确认路径指向正确的 `src/index.js` 文件
2. 在项目目录运行 `npm install`

### 问题 3: 工具调用失败

**可能原因：**
- 参数类型不正确
- 除以零等数学错误

**解决方法：**
- 服务器会返回友好的错误消息
- 检查错误提示并相应调整

## 配置文件示例

### 单个 MCP 服务器
```json
{
  "mcpServers": {
    "simple-calculator": {
      "command": "node",
      "args": ["/absolute/path/to/mirror/mcp-example/src/index.js"]
    }
  }
}
```

### 多个 MCP 服务器
```json
{
  "mcpServers": {
    "simple-calculator": {
      "command": "node",
      "args": ["/path/to/mirror/mcp-example/src/index.js"]
    },
    "another-server": {
      "command": "python",
      "args": ["/path/to/another/server.py"]
    }
  }
}
```

### 带环境变量的配置
```json
{
  "mcpServers": {
    "simple-calculator": {
      "command": "node",
      "args": ["/path/to/mirror/mcp-example/src/index.js"],
      "env": {
        "DEBUG": "true"
      }
    }
  }
}
```

## 卸载

如果你想移除这个 MCP 服务器：

1. 编辑 `claude_desktop_config.json`
2. 删除 "simple-calculator" 部分
3. 保存文件
4. 重启 Claude Desktop

## 下一步

- 尝试修改代码添加新的数学运算
- 阅读 [MCP 官方文档](https://modelcontextprotocol.io/) 了解更多
- 探索其他 [MCP 服务器示例](https://github.com/modelcontextprotocol/servers)

## 需要帮助？

如果遇到问题：
1. 检查本指南的故障排除部分
2. 查看 Claude Desktop 的日志文件
3. 在项目仓库提交 Issue
