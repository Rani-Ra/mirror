#!/usr/bin/env node

/**
 * 简单计算器 MCP 服务器
 * 这是一个最基础的 MCP 服务器实现示例
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// 创建 MCP 服务器实例
const server = new Server(
  {
    name: "simple-calculator",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {}, // 声明服务器支持工具调用
    },
  }
);

/**
 * 处理工具列表请求
 * 客户端会调用这个方法来获取服务器支持的所有工具
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "add",
        description: "将两个数字相加",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "number",
              description: "第一个数字",
            },
            b: {
              type: "number",
              description: "第二个数字",
            },
          },
          required: ["a", "b"],
        },
      },
      {
        name: "subtract",
        description: "计算两个数字的差",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "number",
              description: "被减数",
            },
            b: {
              type: "number",
              description: "减数",
            },
          },
          required: ["a", "b"],
        },
      },
      {
        name: "multiply",
        description: "将两个数字相乘",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "number",
              description: "第一个数字",
            },
            b: {
              type: "number",
              description: "第二个数字",
            },
          },
          required: ["a", "b"],
        },
      },
      {
        name: "divide",
        description: "计算两个数字的商",
        inputSchema: {
          type: "object",
          properties: {
            a: {
              type: "number",
              description: "被除数",
            },
            b: {
              type: "number",
              description: "除数（不能为0）",
            },
          },
          required: ["a", "b"],
        },
      },
    ],
  };
});

/**
 * 处理工具调用请求
 * 当客户端调用某个工具时，这个方法会被触发
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    // 验证参数
    if (!args || typeof args.a !== "number" || typeof args.b !== "number") {
      throw new Error("参数必须是数字");
    }

    const { a, b } = args;
    let result;

    // 根据工具名称执行相应的操作
    switch (name) {
      case "add":
        result = a + b;
        break;
      case "subtract":
        result = a - b;
        break;
      case "multiply":
        result = a * b;
        break;
      case "divide":
        if (b === 0) {
          throw new Error("除数不能为0");
        }
        result = a / b;
        break;
      default:
        throw new Error(`未知的工具: ${name}`);
    }

    return {
      content: [
        {
          type: "text",
          text: `计算结果: ${a} ${getOperatorSymbol(name)} ${b} = ${result}`,
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `错误: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

/**
 * 辅助函数：获取操作符符号
 */
function getOperatorSymbol(toolName) {
  const operators = {
    add: "+",
    subtract: "-",
    multiply: "×",
    divide: "÷",
  };
  return operators[toolName] || "?";
}

/**
 * 启动服务器
 */
async function main() {
  // 使用标准输入/输出作为传输层
  const transport = new StdioServerTransport();
  
  // 连接服务器和传输层
  await server.connect(transport);
  
  // 服务器现在正在运行，等待客户端连接
  console.error("简单计算器 MCP 服务器已启动");
}

// 运行主函数
main().catch((error) => {
  console.error("服务器错误:", error);
  process.exit(1);
});
