from fastapi import FastAPI
<<<<<<< HEAD
from fastapi import WebSocket, WebSocketDisconnect

from app.api.routes.player import router as player_router
from app.api.routes.room import router as room_router
from app.state.store import store
from app.websockets.connection_manager import manager

app = FastAPI()

app.include_router(room_router)
app.include_router(player_router)
=======
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
>>>>>>> 66e998475943534f2682a617914678f20cdcc2f2

@app.get("/")
def read_root():
    return {"message": "LuckyBingo backend is running"}


@app.websocket("/ws/{room_code}")
async def room_websocket(websocket: WebSocket, room_code: str) -> None:
    normalized_room = room_code.upper()
    await manager.connect(normalized_room, websocket)

    try:
        snapshot = await store.get_room_snapshot(normalized_room)
        await websocket.send_json({"type": "room_snapshot", "room": snapshot})

        while True:
            # Keep the websocket open for server push updates.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(normalized_room, websocket)