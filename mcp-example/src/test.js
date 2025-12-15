/**
 * MCP 服务器测试脚本
 * 这个脚本模拟客户端请求来测试 MCP 服务器的功能
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { spawn } from "child_process";

async function testMCPServer() {
  console.log("🚀 启动 MCP 服务器测试...\n");

  try {
    // 启动服务器进程
    const serverProcess = spawn("node", ["src/index.js"], {
      stdio: ["pipe", "pipe", "pipe"],
    });

    // 创建客户端和传输层
    const transport = new StdioClientTransport({
      command: "node",
      args: ["src/index.js"],
    });

    const client = new Client(
      {
        name: "test-client",
        version: "1.0.0",
      },
      {
        capabilities: {},
      }
    );

    // 连接到服务器
    await client.connect(transport);
    console.log("✅ 成功连接到 MCP 服务器\n");

    // 测试 1: 获取工具列表
    console.log("📋 测试 1: 获取可用工具列表");
    const toolsResponse = await client.listTools();
    console.log(`找到 ${toolsResponse.tools.length} 个工具:`);
    toolsResponse.tools.forEach((tool) => {
      console.log(`  - ${tool.name}: ${tool.description}`);
    });
    console.log();

    // 测试 2: 加法
    console.log("➕ 测试 2: 加法运算 (15 + 27)");
    const addResult = await client.callTool({
      name: "add",
      arguments: { a: 15, b: 27 },
    });
    console.log(`结果: ${addResult.content[0].text}`);
    console.log();

    // 测试 3: 减法
    console.log("➖ 测试 3: 减法运算 (100 - 45)");
    const subtractResult = await client.callTool({
      name: "subtract",
      arguments: { a: 100, b: 45 },
    });
    console.log(`结果: ${subtractResult.content[0].text}`);
    console.log();

    // 测试 4: 乘法
    console.log("✖️  测试 4: 乘法运算 (8 × 9)");
    const multiplyResult = await client.callTool({
      name: "multiply",
      arguments: { a: 8, b: 9 },
    });
    console.log(`结果: ${multiplyResult.content[0].text}`);
    console.log();

    // 测试 5: 除法
    console.log("➗ 测试 5: 除法运算 (144 ÷ 12)");
    const divideResult = await client.callTool({
      name: "divide",
      arguments: { a: 144, b: 12 },
    });
    console.log(`结果: ${divideResult.content[0].text}`);
    console.log();

    // 测试 6: 错误处理 - 除以零
    console.log("⚠️  测试 6: 错误处理 (除以零)");
    try {
      const errorResult = await client.callTool({
        name: "divide",
        arguments: { a: 10, b: 0 },
      });
      console.log(`结果: ${errorResult.content[0].text}`);
    } catch (error) {
      console.log(`捕获到错误: ${error.message}`);
    }
    console.log();

    // 关闭连接
    await client.close();
    serverProcess.kill();
    
    console.log("✅ 所有测试完成!");
    console.log("\n💡 提示: 现在你可以将这个 MCP 服务器配置到 Claude Desktop 中使用了！");
    
  } catch (error) {
    console.error("❌ 测试失败:", error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// 运行测试
testMCPServer();
