from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

        # notify others that user came online
        await self.broadcast({
            "type": "online_status",
            "data": {
                "user_id": user_id,
                "online": True
            }
        }, exclude_user_id=user_id)

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def send_to_user(self, user_id: int, message: dict):
        websocket = self.active_connections.get(user_id)

        if websocket:
            await websocket.send_json(message)

    async def broadcast(self, message: dict, exclude_user_id: int = None):
        for user_id, websocket in self.active_connections.items():
            if user_id != exclude_user_id:
                await websocket.send_json(message)

    def is_online(self, user_id: int) -> bool:
        online = user_id in self.active_connections

        return online


manager = ConnectionManager()
