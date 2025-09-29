
from mcp_tools import create_server


def run_mcp():
    print("🚀 Iniciando MCP en http://0.0.0.0:8000")
    create_server(transport="sse")
    

if __name__ == "__main__":
    run_mcp()