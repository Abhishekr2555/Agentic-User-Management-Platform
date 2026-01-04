from fastmcp import FastMCP
import uuid
from typing import Optional, List, Dict

mcp = FastMCP(name="User CRUD Server")

users_db: Dict[str, dict] = {}

@mcp.tool()
def create_user(name: str, email: str, role: str = "user") -> dict:
    """Create a new user."""
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "name": name,
        "email": email,
        "role": role
    }
    users_db[user_id] = user
    return user

@mcp.tool()
def ping() -> str:
    """Check if the server is running."""
    return "bhai bhai"

@mcp.tool()
def read_user(user_id: str) -> dict:
    """Get details of a user by their ID."""
    user = users_db.get(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found")
    return user

@mcp.tool()
def list_users() -> List[dict]:
    """
    List all users in the database.
    
    This function takes no parameters and returns a list of all user dictionaries.
    Each user dict contains: id, name, email, and role.
    
    Returns:
        List[dict]: A list of all users with their complete information.
    """
    return list(users_db.values())

@mcp.resource("users://list")
def list_users_resource() -> str:
    """Get a list of all users as a JSON string."""
    import json
    return json.dumps(list(users_db.values()), indent=2)

@mcp.tool()
def update_user(user_id: str, name: Optional[str] = None, email: Optional[str] = None, role: Optional[str] = None) -> dict:
    """Update a user's details."""
    user = users_db.get(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found")
    
    if name is not None:
        user["name"] = name
    if email is not None:
        user["email"] = email
    if role is not None:
        user["role"] = role
        
    users_db[user_id] = user
    return user

@mcp.tool()
def delete_user(user_id: str) -> str:
    """Delete a user."""
    if user_id not in users_db:
        raise ValueError(f"User with ID {user_id} not found")
    
    del users_db[user_id]
    return f"User {user_id} deleted successfully"

@mcp.prompt()
def onboard_user(name: str) -> str:
    """
    Create a prompt to onboard a new user.
    
    This is an MCP prompt template that generates a welcoming message for new users.
    
    Args:
        name (str): The name of the user to onboard
        
    Returns:
        str: A formatted welcome message
        
    Example:
        >>> onboard_user("Alice")
        "Welcome Alice! We're excited to have you on board. Please provide your email and role so we can set up your account."
    """
    return f"Welcome {name}! We're excited to have you on board. Please provide your email and role so we can set up your account."

if __name__ == "__main__":
    mcp.run(transport='sse', port=8001)