# 🚀 Long-Running Tools in MCP with PydanticAI

> **Complete guide and examples for creating long-running tools in FastMCP that work seamlessly with PydanticAI agents**

## ⚡ Quick Answer

**Question:** How do I create long-running tools in MCP that a PydanticAI agent can invoke and wait for?

**Answer:** Just create an async tool and return the result. **The agent automatically waits!** ✅

```python
@mcp.tool()
async def my_long_running_tool(data: str) -> dict:
    await asyncio.sleep(10)  # Do your work (10 seconds)
    return {"result": data}

# When the agent calls this tool, it automatically waits
# for the 10 seconds and gets the result. No special code needed!
```

## 📚 Documentation

Start with **[INDEX.md](./INDEX.md)** for a complete guide to all resources.

### Quick Links

- **[SUMMARY.md](./SUMMARY.md)** - 5-minute overview (START HERE ⭐)
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - Code snippets cheat sheet
- **[LONG_RUNNING_TOOLS_GUIDE.md](./LONG_RUNNING_TOOLS_GUIDE.md)** - Complete detailed guide
- **[FLOW_DIAGRAM.md](./FLOW_DIAGRAM.md)** - Visual diagrams
- **[INDEX.md](./INDEX.md)** - Navigation hub for all resources

## 🎯 The 4 Patterns

### Pattern 1: Synchronous (Simple)
```python
@mcp.tool()
def process_sync(data: str) -> dict:
    time.sleep(5)
    return {"result": data}
```
**Use when:** Quick CPU tasks (< 5 seconds)

### Pattern 2: Async (RECOMMENDED ⭐)
```python
@mcp.tool()
async def process_async(data: str) -> dict:
    await asyncio.sleep(5)
    return {"result": data}
```
**Use when:** API calls, DB queries, file I/O (90% of use cases)

### Pattern 3: Background Task
```python
@mcp.tool()
async def start_task(data: str) -> dict:
    task_id = str(uuid.uuid4())
    asyncio.create_task(process_in_background(task_id, data))
    return {"task_id": task_id}
```
**Use when:** Very long operations (minutes/hours)

### Pattern 4: Progressive
```python
@mcp.tool()
async def process_with_steps(data: str) -> dict:
    checkpoints = []
    for step in range(5):
        await asyncio.sleep(1)
        checkpoints.append({"step": step})
    return {"checkpoints": checkpoints}
```
**Use when:** Multi-step processes with intermediate results

## 🚀 Quick Start

### 1. Start the Example Server
```bash
python long_running_tool_example.py
# Server runs on http://localhost:8002/sse
```

### 2. Test It
```bash
python test_long_running_tools.py
# Should see: ✅ ALL TESTS PASSED!
```

### 3. Try the Agent Examples
```bash
cd ../fastapi-pydanticai-websocket
python app/long_running_agent_example.py
```

### 4. Use Your Updated Server
```bash
python user_crud_server.py
# Now includes batch_create_users_async() tool!
```

## 📁 Files Included

### Documentation
- `INDEX.md` - Navigation hub
- `SUMMARY.md` - Complete overview
- `QUICK_REFERENCE.md` - Code snippets
- `LONG_RUNNING_TOOLS_GUIDE.md` - Detailed guide
- `FLOW_DIAGRAM.md` - Visual diagrams
- `README.md` - This file

### Code
- `long_running_tool_example.py` - Example MCP server with all 4 patterns
- `test_long_running_tools.py` - Test suite
- `user_crud_server.py` - Your server (updated with batch tool)
- `../fastapi-pydanticai-websocket/app/long_running_agent_example.py` - Agent examples

## 💡 Key Insights

### 1. Agent Waits Automatically ✅
```python
# You write this:
@mcp.tool()
async def my_tool(data: str) -> dict:
    await asyncio.sleep(10)
    return {"result": data}

# Agent does this automatically:
result = await agent.run("Use my_tool with 'test data'")
# ⏳ Waits 10 seconds
print(result.data)  # Gets result after 10 seconds
```

### 2. Use Async for I/O Operations
```python
# ✅ GOOD - Async for I/O
@mcp.tool()
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# ❌ BAD - Sync blocks the thread
@mcp.tool()
def fetch_data(url: str) -> dict:
    response = requests.get(url)  # Blocks!
    return response.json()
```

### 3. Return Structured Results
```python
@mcp.tool()
async def my_tool(data: str) -> dict:
    return {
        "status": "completed",
        "result": processed_data,
        "duration_seconds": 5.2,
        "timestamp": datetime.now().isoformat()
    }
```

## 🎓 Learning Path

### Beginner (15 minutes)
1. Read [SUMMARY.md](./SUMMARY.md) (5 min)
2. Look at [FLOW_DIAGRAM.md](./FLOW_DIAGRAM.md) (5 min)
3. Run `test_long_running_tools.py` (5 min)

### Intermediate (30 minutes)
1. Read [LONG_RUNNING_TOOLS_GUIDE.md](./LONG_RUNNING_TOOLS_GUIDE.md) (15 min)
2. Study `long_running_tool_example.py` (10 min)
3. Run `long_running_agent_example.py` (5 min)

### Advanced (1 hour)
1. Add custom tools to `user_crud_server.py`
2. Implement background tasks with status tracking
3. Add retry logic and error handling

## 🔧 Real-World Example

Your `user_crud_server.py` now includes a real long-running tool:

```python
@mcp.tool()
async def batch_create_users_async(
    users_data: List[Dict[str, str]], 
    delay_between_users: float = 0.5
) -> dict:
    """Create multiple users with rate limiting."""
    created_users = []
    
    for i, user_data in enumerate(users_data):
        if i > 0:
            await asyncio.sleep(delay_between_users)  # Rate limiting
        
        user = create_user(user_data)
        created_users.append(user)
    
    return {
        "successful": len(created_users),
        "created_users": created_users,
        "duration_seconds": total_time
    }
```

### How the Agent Uses It:

```python
result = await agent.run(
    "Create 5 users: Alice, Bob, Charlie, Diana, and Eve "
    "using batch_create_users_async with 1 second delay"
)

# Agent automatically:
# 1. Calls batch_create_users_async()
# 2. Waits ~5 seconds for completion
# 3. Gets the results
# 4. Responds to user
```

## 🎯 Decision Guide

**Need a long-running tool?**

1. **Takes < 5 seconds?** → Use Pattern 1 (Sync) or Pattern 2 (Async)
2. **I/O operation (API, DB, file)?** → Use Pattern 2 (Async) ⭐
3. **Takes minutes/hours?** → Use Pattern 3 (Background Task)
4. **Need intermediate results?** → Use Pattern 4 (Progressive)

**90% of the time, use Pattern 2 (Async)!**

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port is in use
netstat -ano | findstr :8002

# Kill process if needed
taskkill /PID <PID> /F
```

### Tests fail
Make sure the server is running:
```bash
python long_running_tool_example.py
```

### Agent doesn't wait
- Make sure tool returns a value
- Use `async def` for async tools
- Check for exceptions in tool code

See [LONG_RUNNING_TOOLS_GUIDE.md](./LONG_RUNNING_TOOLS_GUIDE.md) → "Troubleshooting" for more help.

## 📖 Resources

- **PydanticAI Documentation:** https://ai.pydantic.dev
- **FastMCP Documentation:** https://github.com/jlowin/fastmcp
- **MCP Protocol:** https://modelcontextprotocol.io

## ✅ Checklist

- [ ] Read [SUMMARY.md](./SUMMARY.md)
- [ ] Run `python long_running_tool_example.py`
- [ ] Run `python test_long_running_tools.py`
- [ ] All tests pass ✅
- [ ] Understand the 4 patterns
- [ ] Try `long_running_agent_example.py`
- [ ] Add tools to your own server

## 🎉 Summary

**You asked:** "How to create long-running tools in MCP that a PydanticAI agent can invoke and wait for?"

**Answer:** 
1. Create an async tool with `@mcp.tool()` and `async def`
2. Do your work (with `await` for I/O operations)
3. Return the result
4. **The agent automatically waits!** ✅

**That's it!** No special configuration needed. The agent handles everything.

---

**Start here:** [INDEX.md](./INDEX.md) → [SUMMARY.md](./SUMMARY.md)

**Happy coding! 🚀**
