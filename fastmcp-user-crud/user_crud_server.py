from fastmcp import FastMCP
import uuid
import asyncio
import httpx
from typing import Optional, List, Dict
import json
from datetime import datetime

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

async def wait_for_bot_completion(execution_id: str, token: str, max_retries: int = 60, poll_interval: int = 5):
    """
    Poll for bot execution completion.
    
    Returns:
        dict: Complete execution data with all node results
    """

    status_url = f"https://api-test.autobot.live/bot_executions/{execution_id}"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        for attempt in range(max_retries):
            try:
                resp = await client.get(status_url, headers=headers)
                resp.raise_for_status()

                data = resp.json()
                state = data.get("state") or data.get("status")
                
                print(f"[Poll {attempt + 1}/{max_retries}] State: {state}")

                if state in ["SUCCEEDED", "COMPLETED"]:
                    print("✓ Bot execution completed successfully")
                    return data
                
                elif state == "FAILED":
                    errors = data.get('errors') or 'Unknown error'
                    raise RuntimeError(f"Bot execution failed: {errors}")
                
                elif state in ["RUNNING", "PENDING", "QUEUED"]:
                    await asyncio.sleep(poll_interval)
                
                else:
                    print(f"Warning: Unexpected state '{state}'")
                    await asyncio.sleep(poll_interval)
            except httpx.HTTPError as e:
                print(f"✗ Network error during polling: {e}")
                await asyncio.sleep(poll_interval)

        raise TimeoutError(
            f"Bot execution did not complete after {max_retries * poll_interval} seconds"
        )

async def get_node_results(execution_id: str, token: str, node_names: list[str]) -> dict:

    headers = {"Authorization": f"Bearer {token}"}
    node_results = {}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for node_name in node_names:
            try:
                url = f"https://api-test.autobot.live/bot_executions/{execution_id}/{node_name}/results"
                resp = await client.get(url, headers=headers)
                resp.raise_for_status()
                
                node_results[node_name] = resp.json()
                print(f"✓ Fetched results for node: {node_name}")
                
            except httpx.HTTPError as e:
                node_results[node_name] = {"error": str(e)}
    
    return node_results

def filter_intermediate_nodes(results: dict) -> list[str]:
   
    if not results:
        return []
    
    return [
        node_name for node_name in results.keys()
        if node_name not in ["start", "end"]
    ]

@mcp.tool()
async def run_bot(url: str, payload: Optional[dict] = None) -> str:
    payload = {
        "bot_id": "695b46b802274a22219c4609",
        "test_events": {
            "start": []
        }
    }
    url = 'https://api-test.autobot.live/bot_executions'
    token = 'eyJraWQiOiJuaFU2eWlkdGpleSthUjd3SURWRXcyeDNrclNibTYxUEV3K1RrZ056UkNZPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI5ZmYxNmM2Yi1lMDBiLTRiMmItODQ4My1hN2QxYmFkNGYxMmQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoLTEuYW1hem9uYXdzLmNvbVwvYXAtc291dGgtMV90SFRSTlpjZ3YiLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiOmZhbHNlLCJjb2duaXRvOnVzZXJuYW1lIjoiYW1pdEBzaHVueWVrYS5jb20iLCJhdWQiOiI3bmJmZG9vbTFzcnJkbW1ybnU0ZTdobnI3aiIsImV2ZW50X2lkIjoiZmMxNjI2N2MtYjNjMy00YzYyLWIyNmItMzZmZDZhMGI1YTVmIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3Njc1ODk1MjYsIm5hbWUiOiJBbWl0IENob3RhbGl5YSIsInBob25lX251bWJlciI6Iis5MTgwODgyNjMwMTAiLCJleHAiOjE3Njc2MTE2NTEsImlhdCI6MTc2NzYwODA1MSwiZW1haWwiOiJhbWl0QHNodW55ZWthLmNvbSJ9.WF4tf_1jsCqUvktg5NbSpvfURybpItXzfmLNBpNu-wp9DcUN_Y23_W3zpVWCJk5riWTxJdB68aZwOlev-H0Q5utElc31ad-Q4aX-KkIRn5BSPcM9h3DtejfoGjJM8OX5H3Dc_2bAepfOGNKDbHPIWoT14Bs9CoTc9Oa0a_f3m931bxEbbEpeo4SuQqkBCaxqBhQ45NJG7svGpda7NBVZPbfS86BB-QHgwZa75CttGHB7BoCJ7qKqaGqJcKFA8dQXMaGgWgD-px7aSuEQ_hos3vkIsNT5A30V8ZWiWqOosFCZqmPCorlPn-c5ClgPk8H1A8iYM9IlpzCmBTB_o0ZMVw'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    async with httpx.AsyncClient() as client:
        try:
            # api_id = "M-0MzaXoZkZ5gQyRyBkr0Q"
            # api_key = "ca24147a809ba4d95ac6500b812dc882"
            # headers = {
            #     "X-API-ID": api_id,
            #     "X-API-KEY": api_key,
            #     "Content-Type": "application/json"
            # }
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print('RESPONSE STATUS: ', response.status_code)

            execution = response.json()
            print('EXECUTION: ', execution)
            execution_id = execution["_id"]
            print('EXECUTION ID: ', execution_id)

            # 2️⃣ Wait for completion
            final_result = await wait_for_bot_completion(
                execution_id=execution_id,
                token=token
            )
            state = final_result.get("state")

            all_results = final_result.get("results", {})

            intermediate_nodes = filter_intermediate_nodes(all_results)

            node_results = await get_node_results(
                execution_id=execution_id,
                token=token,
                node_names=intermediate_nodes
            )

            if state == "COMPLETED" or state == "SUCCEEDED":
                return json.dumps({
                    "success": True,
                    "execution_id": execution_id,
                    "state": state,
                    "bot_name": final_result.get("bot_name"),
                    "total_intermediate_nodes": len(intermediate_nodes),
                    "node_results": node_results,
                    "full_execution_data": final_result
                }, indent=2)

        except Exception as e:
            return f"Error triggering bot: {str(e)}"



if __name__ == "__main__":
    mcp.run(transport='sse', port=8001)


# introduce 2 features in autobotai :
# 1. Add optinal input json scheema and validation for listener 
# 2. End Node should allow output selection



# M-0MzaXoZkZ5gQyRyBkr0Q api key-id
# ca24147a809ba4d95ac6500b812dc882 api key-secret


# Lister secret: ba8a8dd1b2c04aa7a26b552cacbe44b5
# https://api-test.autobot.live/integrations/generic/webhook/695bacacf573e080d8319bdf