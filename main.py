import sys
import threading
from PySide6.QtWidgets import (
    QApplication
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import uvicorn
from graphics_signals import GraphicsSignals
from whiteboard.whiteboard import WhiteboardWindow
from whiteboard.point import Point
from typing import List

# Socket.IO 配置
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',  # Allow all origins
    transports=['websocket'],  # Use WebSocket transport only
)
app = FastAPI()
# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
socket_app = socketio.ASGIApp(sio, app)
whiteboard = None
# FastAPI路由
@app.get("/history")
async def get_history():
    return whiteboard.history

@app.post("/clear")
async def clear_board():
    whiteboard.scene.clear()
    whiteboard.history.clear()
    await sio.emit('clear')
    return {"status": "cleared"}

@app.post("/draw_line")
async def draw_line(x: float, y: float, width: float, height:float, color: str):
    data = {
        "type": "line",
        "start": (x, y),
        "end": (x + width, y + height),
        "color": color
    }
    signals.add_shape.emit(data)
    return {"status": "line drawn"}

@app.post("/draw_ellipse")
async def draw_ellipse(x: float, y: float, rx: float, ry: float, color: str):
    data = {
        "type": "circle",
        "start": (x, y),
        "end": (x + rx, y + ry),
        "color": color
    }
    signals.add_shape.emit(data)
    return {"status": "ellipse drawn"} 
    
@app.post("/draw_rect")
async def draw_rect(x: float, y: float, width: float, height:float, color: str):
    data = {
        "type": "rect",
        "start": (x, y),
        "end": (x + width, y + height),
        "color": color
    }
    signals.add_shape.emit(data)
    return {"status": "rectangle drawn"}

@app.post("/draw_curve") 
async def draw_curve(points: str, color: str):
    """
    Draw a curve based on at least three points.
    Each point is an instance of the Point struct.
    """
    data = {
        "type": "curve",
        "points": points,
        "color": color
    }
    signals.add_shape.emit(data)
    return {"status": "curve drawn"}

# Socket.IO事件处理
@sio.event
async def connect(sid, environ):
    await sio.emit('init', whiteboard.history)

@sio.event
async def draw_shape(sid, data):
    signals.add_shape.emit(data)

@sio.event
async def clear(sid):
    await clear_board()

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")

def start_server():
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    app_qt = QApplication(sys.argv)
    whiteboard = WhiteboardWindow()
    signals = GraphicsSignals()
    
    # 信号连接
    signals.add_shape.connect(whiteboard.add_remote_shape)
    
    # 启动服务器线程
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    whiteboard.show()
    res = app_qt.exec()
    sys.exit(res)