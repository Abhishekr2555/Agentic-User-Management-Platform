from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic_ai.exceptions import UnexpectedModelBehavior
from app.agent import weather_agent
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="FastAPI PydanticAI WebSocket Agent")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI PydanticAI Agent WebSocket Server. Go to /static/index.html to chat."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            user_message = await websocket.receive_text()
            
            try:
                result = await weather_agent.run(user_message)
                
                await websocket.send_text(result.output)
                
            except UnexpectedModelBehavior as e:
                await websocket.send_text(f"Error: {str(e)}")
            except Exception as e:
                print(f"Agent Run Error: {e}")
                await websocket.send_text(f"Processing Error: {str(e)}")
                
    except WebSocketDisconnect:
        print("Client disconnected")
