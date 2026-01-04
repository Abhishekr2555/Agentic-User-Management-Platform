# Quick Start Guide - Agentic User Management Platform (FastAPI + FastMCP)

## Output

<img width="999" height="832" alt="image" src="https://github.com/user-attachments/assets/e51fa280-220a-4f3c-85e7-53aec7a4ee92" />

### Sample Prompt :
1.  call the create_user tool and create user with name is Charlie Davis and email id is bob@example.com and it's had role Admin and tell me what tool return response.
2.  Call the ping tool and tell me what string it returns. 
3.  List all users and show me their IDs, names, emails, and roles in a table format.

## 🚀 How to Run

### Step 1: Start Both Servers

This will open **two terminal windows**:
- **Terminal 1**: FastMCP Server (Port 8001)
- **Terminal 2**: FastAPI WebSocket Server (Port 8000)

### Step 2: Open the Chat Interface

Open your browser and navigate to:
```
http://localhost:8000/static/index.html
```

### Step 3: Start Chatting!

Try these example commands:

#### Create a User
```
Create a new user named Alice Johnson with email alice@example.com and role admin
```

#### List All Users
```
Show me all users
```

#### Read a Specific User
```
Get details for user <user-id>
```

#### Update a User
```
Update user <user-id> to change their email to newemail@example.com
```

#### Delete a User
```
Delete user <user-id>
```

## Project Structure

```
FASTAPI/
├── fastmcp-user-crud/
│   ├── user_crud_server.py    # FastMCP server with user tools
│   ├── venv/
│   └── .env
├── fastapi-pydanticai-websocket/
│   ├── app/
│   │   ├── main.py            # FastAPI WebSocket server
│   │   ├── agent.py           # PydanticAI agent configuration
│   │   └── static/
│   │       └── index.html     # Chat interface
│   ├── venv/
│   └── .env
├── start_servers.ps1          # Startup script
└── README.md                  # This file
```

## 🔧 Manual Startup (Alternative)

If you prefer to start servers manually:

### Terminal 1 - FastMCP Server
```powershell
cd fastmcp-user-crud
.\venv\Scripts\Activate.ps1
python user_crud_server.py
```

You should see:
```
FastMCP Server running on http://localhost:8001
```

### Terminal 2 - FastAPI Server
```powershell
cd fastapi-pydanticai-websocket
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## ✅ Verify Connection

Run the test script to verify everything is connected:

```powershell
python test_connection.py
```

## 🛠️ Troubleshooting

### "Connection failed" error
- Make sure both servers are running
- Check that no other applications are using ports 8000 or 8001

### "Tool not found" error
- Restart the FastMCP server
- Ensure the agent.py has the correct MCP server URL: `http://localhost:8001/sse`


## 📝 Architecture Summary
```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                        │
│                  http://localhost:8000/static/index.html    │
└────────────────────────┬────────────────────────────────────┘
                         │ WebSocket
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI WebSocket Server (Port 8000)           │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         PydanticAI Agent (Groq LLM)                   │  │
│  │  - Processes user messages                            │  │
│  │  - Calls MCP tools when needed                        │  │
│  └───────────────────┬───────────────────────────────────┘  │
└────────────────────────┼────────────────────────────────────|
                         │ SSE Connection
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            FastMCP Server (Port 8001)                       │
│                                                             │
│  Tools Available:                                           │
│  - create_user(name, email, role)                           │
│  - read_user(user_id)                                       │
│  - list_users()                                             │
│  - update_user(user_id, name, email, role)                  │
│  - delete_user(user_id)                                     │
│  - ping()                                                   │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 What's Happening Behind the Scenes

1. You type a message in the chat
2. Message sent via WebSocket to FastAPI server
3. PydanticAI agent processes your message
4. Agent determines if it needs to call a tool
5. Agent connects to FastMCP server via SSE
6. FastMCP executes the tool (create_user, list_users, etc.)
7. Result sent back to agent
8. Agent formats response and sends back to you

