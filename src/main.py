
from my_server.mcp_tools import mcp


def run_mcp():
    print("🚀 Iniciando MCP en http://0.0.0.0:8000")
    mcp.run(transport="sse")
    

if __name__ == "__main__":
    run_mcp()