# mcp
[![smithery badge](https://smithery.ai/badge/@bigboss32/mcp)](https://smithery.ai/server/@bigboss32/mcp)

mcp JSON-RPC server

## Usage
Start mcp server with invoke options:

- in node.js
```js
// intialize model context server
let server = new ModelContextServer()

server.tools.add(myTool) // Use model context server utility to register method

// or define manually method in ModelContext
server.model.context.test.method = ({foo}) => {}
```
---

- via cli
```
$ npx mcp
```
or
```
$ npx mcp -i <initialization.json>

$  mcp -h                                  
Usage: mcp [options]

Model Context Protocol JSON-RPC Server

Options:
  -i, --init_file		Initialisation JSON, sets server capabilities response. --tools and --resources will be appended
  -t, --tools_dir		Tools directory to import in server
  -r, --resources_dir	Resources directory to expose in server

  -h, --help		display help for command
```

## Installing via Smithery

To install mcp automatically via [Smithery](https://smithery.ai/server/@bigboss32/mcp):

```bash
npx -y @smithery/cli install @bigboss32/mcp
```
