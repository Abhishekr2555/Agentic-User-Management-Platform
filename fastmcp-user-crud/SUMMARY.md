# 🎯 Long-Running Tools in MCP - Complete Solution

## What You Asked For

You wanted to know how to create long-running tools in MCP that:
1. Can be invoked by a PydanticAI agent
2. The agent waits for the tool to complete
3. Works like an agent or bot

## The Answer

**The PydanticAI agent AUTOMATICALLY waits for MCP tools to complete!** 

You don't need to do anything special. Just:
1. Create your tool (sync or async)
2. Do the work
3. Return the result
4. The agent waits automatically ✅

## Files Created

### 📚 Documentation

1. **`LONG_RUNNING_TOOLS_GUIDE.md`** - Complete guide with all 4 patterns
2. **`QUICK_REFERENCE.md`** - Quick reference card with code snippets
3. **`THIS_FILE.md`** - Summary of everything created

### 💻 Code Examples

4. **`long_running_tool_example.py`** - MCP server with 4 different patterns:
   - Pattern 1: Synchronous blocking
   - Pattern 2: Async (RECOMMENDED ⭐)
   - Pattern 3: Background tasks with status tracking
   - Pattern 4: Progressive/streaming results

5. **`long_running_agent_example.py`** - PydanticAI agent examples showing:
   - How to connect to MCP server
   - How to invoke long-running tools
   - Multiple usage examples
   - Interactive mode

6. **`test_long_running_tools.py`** - Test suite to verify everything works

7. **`user_crud_server.py`** (UPDATED) - Your existing server now includes:
   - `batch_create_users_async()` - Real-world long-running tool example

## The 4 Patterns Explained

### Pattern 1: Synchronous (Simple)
```python
@mcp.tool()
def my_tool(data: str) -> dict:
    time.sleep(5)  # Do work
    return {"result": data}
```
✅ Use for: Quick CPU tasks (< 5 seconds)

### Pattern 2: Async (RECOMMENDED ⭐)
```python
@mcp.tool()
async def my_tool(data: str) -> dict:
    await asyncio.sleep(5)  # Do async work
    return {"result": data}
```
✅ Use for: API calls, DB queries, file I/O (MOST COMMON)

### Pattern 3: Background Task
```python
@mcp.tool()
async def start_task(data: str) -> dict:
    task_id = str(uuid.uuid4())
    asyncio.create_task(process_in_background(task_id, data))
    return {"task_id": task_id}

@mcp.tool()
async def wait_for_task(task_id: str) -> dict:
    # Poll until complete
    ...
```
✅ Use for: Very long operations (minutes/hours)

### Pattern 4: Progressive
```python
@mcp.tool()
async def my_tool(data: str) -> dict:
    checkpoints = []
    for step in range(5):
        await asyncio.sleep(1)
        checkpoints.append({"step": step})
    return {"checkpoints": checkpoints}
```
✅ Use for: Multi-step processes with intermediate results

## How to Use

### Step 1: Start the Example MCP Server
```bash
cd c:\Users\Admin\.vscode\FASTAPI\fastmcp-user-crud
python long_running_tool_example.py
```
Server runs on: `http://localhost:8002/sse`

### Step 2: Test It
```bash
python test_long_running_tools.py
```

### Step 3: Try the Agent Examples
```bash
cd c:\Users\Admin\.vscode\FASTAPI\fastapi-pydanticai-websocket
python app/long_running_agent_example.py
```

### Step 4: Use Your Updated User CRUD Server
```bash
cd c:\Users\Admin\.vscode\FASTAPI\fastmcp-user-crud
python user_crud_server.py
```
Server runs on: `http://localhost:8001/sse`

Now your agent can use `batch_create_users_async()` tool!

## Real-World Example: Batch User Creation

Your `user_crud_server.py` now has a real long-running tool:

```python
@mcp.tool()
async def batch_create_users_async(
    users_data: List[Dict[str, str]], 
    delay_between_users: float = 0.5
) -> dict:
    """Create multiple users with rate limiting."""
    # ... implementation ...
```

### How the Agent Uses It:

```python
# In your PydanticAI agent
result = await agent.run(
    "Create 5 users: Alice, Bob, Charlie, Diana, and Eve. "
    "Use batch_create_users_async with 1 second delay between each."
)

# The agent will:
# 1. Call batch_create_users_async()
# 2. Wait for it to complete (takes ~5 seconds)
# 3. Return the results
```

## Key Insights

### 1. Agent Waits Automatically ✅
```python
# You don't need to do anything special!
result = await agent.run("Process data for 10 seconds")
# ⏳ Agent automatically waits here
print(result.data)  # Gets result after 10 seconds
```

### 2. Use Async for I/O ⭐
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
        "timestamp": datetime.now().isoformat(),
        "message": "Processing completed successfully"
    }
```

### 4. Handle Errors Gracefully
```python
@mcp.tool()
async def my_tool(data: str) -> dict:
    try:
        result = await risky_operation(data)
        return {"status": "success", "result": result}
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }
```

## Quick Decision Guide

**Need a long-running tool?**

1. **Takes < 5 seconds?** → Use Pattern 1 (Sync) or Pattern 2 (Async)
2. **I/O operation (API, DB, file)?** → Use Pattern 2 (Async) ⭐
3. **Takes minutes/hours?** → Use Pattern 3 (Background Task)
4. **Need intermediate results?** → Use Pattern 4 (Progressive)

**90% of the time, use Pattern 2 (Async)!**

## Integration with Your Existing Code

### Option 1: Add to Existing Server
You already did this! `user_crud_server.py` now has `batch_create_users_async()`

### Option 2: Create Separate Server
Run multiple MCP servers and connect them all to your agent:

```python
# In app/agent.py
user_crud_mcp = MCPServerSSE(url="http://localhost:8001/sse")
long_running_mcp = MCPServerSSE(url="http://localhost:8002/sse")

agent = Agent(
    model=groq_model,
    toolsets=[user_crud_mcp, long_running_mcp],  # Multiple servers!
)
```

## Testing Checklist

- [ ] Start MCP server (`python long_running_tool_example.py`)
- [ ] Run tests (`python test_long_running_tools.py`)
- [ ] All tests pass ✅
- [ ] Try agent examples (`python app/long_running_agent_example.py`)
- [ ] Agent successfully invokes tools ✅
- [ ] Agent waits for completion ✅
- [ ] Results are returned correctly ✅

## Common Questions

### Q: Does the agent really wait automatically?
**A:** YES! You don't need to do anything special. Just return the result.

### Q: What if my operation takes hours?
**A:** Use Pattern 3 (Background Tasks) with status tracking.

### Q: Can I show progress to the user?
**A:** Yes! Use Pattern 4 (Progressive) or Pattern 3 with status checks.

### Q: Should I use sync or async?
**A:** Use async for I/O operations (API, DB, files). Use sync only for quick CPU tasks.

### Q: Can the agent call multiple tools in parallel?
**A:** Yes! The agent can orchestrate multiple tool calls as needed.

## Next Steps

1. ✅ Read `LONG_RUNNING_TOOLS_GUIDE.md` for complete documentation
2. ✅ Check `QUICK_REFERENCE.md` for code snippets
3. ✅ Run the examples to see it in action
4. ✅ Add long-running tools to your own MCP server
5. ✅ Test with your PydanticAI agent

## Resources

- **Full Guide:** `LONG_RUNNING_TOOLS_GUIDE.md`
- **Quick Reference:** `QUICK_REFERENCE.md`
- **Example Server:** `long_running_tool_example.py`
- **Agent Examples:** `long_running_agent_example.py`
- **Test Suite:** `test_long_running_tools.py`
- **Your Updated Server:** `user_crud_server.py`

## Summary

You asked: "How to create long-running tools in MCP that a PydanticAI agent can invoke and wait for?"

**Answer:** 
1. Create an async tool with `@mcp.tool()` and `async def`
2. Do your work (with `await` for I/O operations)
3. Return the result
4. **The agent automatically waits!** ✅

**That's it!** No special configuration needed. The agent handles everything.

---

**Remember:** 90% of the time, just use Pattern 2 (Async). It's simple, efficient, and perfect for most use cases! 🎉
