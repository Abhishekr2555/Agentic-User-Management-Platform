# Long-Running Tools Quick Reference

## 🚀 Quick Start

### 1. Start the MCP Server
```bash
cd c:\Users\Admin\.vscode\FASTAPI\fastmcp-user-crud
python long_running_tool_example.py
```

### 2. Test the Tools
```bash
# In another terminal
python test_long_running_tools.py
```

### 3. Run the Agent Examples
```bash
cd c:\Users\Admin\.vscode\FASTAPI\fastapi-pydanticai-websocket
python app/long_running_agent_example.py
```

## 📋 The 4 Patterns

### Pattern 1: Synchronous (Simple)
```python
@mcp.tool()
def my_tool(data: str) -> dict:
    time.sleep(5)  # Do work
    return {"result": data}
```
**Use when:** Quick CPU tasks (< 5 seconds)

### Pattern 2: Async (RECOMMENDED ⭐)
```python
@mcp.tool()
async def my_tool(data: str) -> dict:
    await asyncio.sleep(5)  # Do async work
    return {"result": data}
```
**Use when:** API calls, DB queries, file I/O

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
    while task_store[task_id]["status"] != "completed":
        await asyncio.sleep(0.5)
    return task_store[task_id]
```
**Use when:** Very long operations (minutes/hours)

### Pattern 4: Progressive
```python
@mcp.tool()
async def my_tool(data: str) -> dict:
    checkpoints = []
    for step in range(5):
        await asyncio.sleep(1)
        checkpoints.append({"step": step, "data": f"Step {step}"})
    return {"checkpoints": checkpoints}
```
**Use when:** Multi-step processes with intermediate results

## 🎯 How the Agent Uses Tools

The PydanticAI agent **automatically waits** for tools to complete:

```python
# Agent code
result = await agent.run("Process data for 10 seconds")
# ⏳ Agent waits here until tool completes
print(result.data)  # Gets result after 10 seconds
```

## 💡 Key Insights

1. **Agent waits automatically** - No special code needed
2. **Use async for I/O** - API calls, DB, files
3. **Return meaningful results** - Include status, timestamps, errors
4. **Add timeouts** - Prevent infinite waits
5. **Handle errors gracefully** - Return error info in dict

## 🔧 Common Code Snippets

### Add Timeout
```python
@mcp.tool()
async def my_tool(data: str) -> dict:
    try:
        result = await asyncio.wait_for(
            long_operation(data),
            timeout=30.0
        )
        return {"status": "success", "result": result}
    except asyncio.TimeoutError:
        return {"status": "timeout"}
```

### Retry Logic
```python
@mcp.tool()
async def my_tool(data: str, max_retries: int = 3) -> dict:
    for attempt in range(max_retries):
        try:
            result = await risky_operation(data)
            return {"status": "success", "result": result}
        except Exception as e:
            if attempt == max_retries - 1:
                return {"status": "error", "error": str(e)}
            await asyncio.sleep(2 ** attempt)
```

### Progress Tracking
```python
task_store = {}

@mcp.tool()
async def start_task(data: str) -> dict:
    task_id = str(uuid.uuid4())
    task_store[task_id] = {"status": "pending", "progress": 0}
    asyncio.create_task(process(task_id, data))
    return {"task_id": task_id}

@mcp.tool()
def get_progress(task_id: str) -> dict:
    return task_store[task_id]
```

## 📁 Files Created

| File | Purpose |
|------|---------|
| `long_running_tool_example.py` | MCP server with all 4 patterns |
| `long_running_agent_example.py` | PydanticAI agent usage examples |
| `test_long_running_tools.py` | Test suite |
| `LONG_RUNNING_TOOLS_GUIDE.md` | Complete documentation |
| `QUICK_REFERENCE.md` | This file |

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8002 is in use
netstat -ano | findstr :8002

# Kill the process if needed
taskkill /PID <PID> /F
```

### Agent doesn't wait
- Make sure tool returns a value
- Use `async def` for async tools
- Check for exceptions in tool code

### Tool times out
- Increase timeout in `wait_for_task_completion`
- Use background tasks for very long operations
- Add progress tracking

## 📚 Learn More

- Full guide: `LONG_RUNNING_TOOLS_GUIDE.md`
- Example code: `long_running_tool_example.py`
- Agent examples: `long_running_agent_example.py`
- PydanticAI docs: https://ai.pydantic.dev
- FastMCP docs: https://github.com/jlowin/fastmcp

## ✅ Checklist

- [ ] MCP server running on port 8002
- [ ] Test script passes all tests
- [ ] Agent can invoke tools successfully
- [ ] Tools return proper results
- [ ] Error handling works
- [ ] Timeouts configured appropriately

## 🎓 Best Practices

1. ✅ Use `async def` for I/O operations
2. ✅ Return structured dicts with status
3. ✅ Add timeouts to prevent hangs
4. ✅ Include timestamps in results
5. ✅ Handle errors gracefully
6. ✅ Provide clear tool descriptions
7. ✅ Use type hints
8. ✅ Test with realistic data

## 🚦 Decision Tree

```
Need a long-running tool?
│
├─ Takes < 5 seconds?
│  └─ Use Pattern 1 (Sync) or Pattern 2 (Async)
│
├─ I/O operation (API, DB, file)?
│  └─ Use Pattern 2 (Async) ⭐
│
├─ Takes minutes/hours?
│  └─ Use Pattern 3 (Background Task)
│
└─ Need intermediate results?
   └─ Use Pattern 4 (Progressive)
```

---

**Remember:** The agent automatically waits for tools to complete. Just make your tool do its work and return the result! 🎉
