
from mcp.server.fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
verifier = StaticTokenVerifier(
    tokens={
        "dev-alice-token": {
            "client_id": "alice@company.com",
            "scopes": ["read:data", "write:data", "admin:users"]
        },
        "dev-guest-token": {
            "client_id": "guest-user",
            "scopes": ["read:data"]
        }
    },
    required_scopes=["read:data"]
)

@smithery.server(config_schema=ConfigSchema) 
def create_server(): 
    mcp = FastMCP(name="Development Server")

DB_FILE = "database.db"


from . import menu
from . import sql
from . import archivo_notas
