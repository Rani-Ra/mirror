# MCP Tutorial: From Zero to Running

This is a complete MCP (Model Context Protocol) learning example that teaches you how to create and use a simple MCP server from scratch.

## What is MCP?

MCP (Model Context Protocol) is an open protocol for connecting AI applications with data sources. It allows AI assistants (like Claude, ChatGPT, etc.) to access external tools and data in a standardized way.

### Core Concepts

- **Server**: A program that provides tools, resources, or prompts
- **Client**: An AI application that uses these capabilities
- **Tools**: Executable functions provided by the server
- **Transport**: Communication method between server and client (stdio, HTTP, etc.)

## This Example: Simple Calculator

This tutorial implements a simple calculator MCP server with four basic mathematical operation tools:
- Addition (add)
- Subtraction (subtract)
- Multiplication (multiply)
- Division (divide)

## Quick Start

### Step 1: Install Dependencies

```bash
cd mcp-example
npm install
```

### Step 2: Run the Server

```bash
npm start
```

The server will start and wait for client connections via standard input/output.

### Step 3: Configure with Claude Desktop

To use this MCP server in Claude Desktop, you need to edit Claude's configuration file.

#### macOS Configuration Path
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### Windows Configuration Path
```
%APPDATA%\Claude\claude_desktop_config.json
```

#### Configuration Content

```json
{
  "mcpServers": {
    "simple-calculator": {
      "command": "node",
      "args": [
        "/full/path/to/mirror/mcp-example/src/index.js"
      ]
    }
  }
}
```

**Note**: Replace `/full/path/to/` with your actual project path.

### Step 4: Use in Claude Desktop

1. After saving the configuration file, restart Claude Desktop
2. In Claude Desktop, you can use it like this:
   ```
   Please calculate 15 + 27
   Calculate 100 divided by 4
   What's 8 times 9?
   ```
3. Claude will automatically call your MCP server to perform calculations

## Code Explanation

### Project Structure

```
mcp-example/
├── package.json          # Project configuration
├── src/
│   └── index.js         # MCP server implementation
└── README.md            # This document
```

### Key Code Analysis

#### 1. Create Server Instance

```javascript
const server = new Server(
  {
    name: "simple-calculator",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},  // Declare tool support
    },
  }
);
```

#### 2. Register Tool List

```javascript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "add",
        description: "Add two numbers",
        inputSchema: {
          type: "object",
          properties: {
            a: { type: "number", description: "First number" },
            b: { type: "number", description: "Second number" }
          },
          required: ["a", "b"]
        }
      },
      // ... other tools
    ]
  };
});
```

#### 3. Handle Tool Calls

```javascript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  // Perform calculation
  switch (name) {
    case "add":
      result = args.a + args.b;
      break;
    // ... other operations
  }
  
  return {
    content: [
      { type: "text", text: `Result: ${result}` }
    ]
  };
});
```

#### 4. Start Server

```javascript
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main();
```

## Extending Your MCP Server

After understanding the basics, you can extend the server with more features:

### Adding New Tools

Add new tool definitions in the `ListToolsRequestSchema` handler, then implement the logic in the `CallToolRequestSchema` handler.

Example: Adding a power operation tool

```javascript
// Add to tool list
{
  name: "power",
  description: "Calculate power of a number",
  inputSchema: {
    type: "object",
    properties: {
      base: { type: "number", description: "Base number" },
      exponent: { type: "number", description: "Exponent" }
    },
    required: ["base", "exponent"]
  }
}

// Add to call handler
case "power":
  result = Math.pow(args.base, args.exponent);
  break;
```

### Adding Resources

MCP also supports providing static or dynamic resources:

```javascript
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "calculator://history",
        name: "Calculation History",
        mimeType: "application/json"
      }
    ]
  };
});
```

### Adding Prompts

You can also provide predefined prompt templates:

```javascript
server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return {
    prompts: [
      {
        name: "complex-calculation",
        description: "Perform complex mathematical calculations"
      }
    ]
  };
});
```

## Debugging Tips

### View Logs

The server uses `console.error()` for logging, which won't interfere with MCP communication on stdout:

```javascript
console.error("Debug info:", someVariable);
```

### Testing the Server

You can use the MCP Inspector tool to test the server:

```bash
npx @modelcontextprotocol/inspector node src/index.js
```

This opens a web interface for directly testing server tools.

## Common Issues

### Q: Why can't I see the tools in Claude Desktop?

A: 
1. Check if the configuration file path is correct
2. Ensure the path in the configuration uses absolute paths
3. Restart Claude Desktop
4. Check for syntax errors in the configuration file

### Q: How do I know if the server is running?

A: In Claude Desktop settings, you can see the MCP server status. If there's an error, click to view detailed logs.

### Q: Can I implement MCP servers in other programming languages?

A: Yes! MCP is an open protocol supporting any programming language. Official SDKs are provided for TypeScript/JavaScript and Python.

## Next Steps

1. Read the [Official MCP Documentation](https://modelcontextprotocol.io/)
2. Explore more [MCP Server Examples](https://github.com/modelcontextprotocol/servers)
3. Learn how to create more complex tools and resources
4. Understand MCP security best practices

## License

MIT License

## References

- [MCP Official Website](https://modelcontextprotocol.io/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/typescript-sdk)
