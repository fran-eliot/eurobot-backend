# app/core/websockets/manager.py

# 📋 Gestor de conexiones WebSocket: clase que maneja las conexiones WebSocket
# activas, permitiendo enviar mensajes a todos los clientes conectados. Este gestor se
# utiliza para enviar notificaciones en tiempo real a los usuarios cuando ocurren
# eventos importantes, como la creación o actualización de tareas, sin necesidad de
# que los usuarios tengan que refrescar la página.

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.rooms = {}
        self.users = {}
        self.dashboard_connections = []
        self.user_connections = {}

    async def connect(self, websocket: WebSocket, project_id: int, user):
        await websocket.accept()

        if project_id not in self.rooms:
            self.rooms[project_id] = []
            self.users[project_id] = {}

        self.rooms[project_id].append(websocket)

        self.users[project_id][user.id_usuario] = {
            "id": user.id_usuario,
            "name": user.nombre,
        }

        await self.broadcast_users(project_id)

    def disconnect(self, websocket: WebSocket, project_id: int, user):
        if project_id in self.rooms and websocket in self.rooms[project_id]:
            self.rooms[project_id].remove(websocket)

        if project_id in self.users:
            self.users[project_id].pop(user.id_usuario, None)

        if project_id in self.rooms and not self.rooms[project_id]:
            del self.rooms[project_id]
            del self.users[project_id]
            return

    async def broadcast_to_project(self, project_id: int, message: dict):
        connections = self.rooms.get(project_id, [])

        disconnected = []

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception:
                disconnected.append(websocket)

        for websocket in disconnected:
            if websocket in self.rooms.get(project_id, []):
                self.rooms[project_id].remove(websocket)

    async def broadcast_users(self, project_id: int):
        users = list(self.users.get(project_id, {}).values())

        await self.broadcast_to_project(
            project_id,
            {
                "type": "users_online",
                "users": users,
            },
        )

    async def connect_dashboard(self, websocket):
        await websocket.accept()
        self.dashboard_connections.append(websocket)

    def disconnect_dashboard(self, websocket):
        if websocket in self.dashboard_connections:
            self.dashboard_connections.remove(websocket)

    async def broadcast_dashboard(self, message: dict):
        disconnected = []

        for websocket in self.dashboard_connections:
            try:
                await websocket.send_json(message)
            except Exception:
                disconnected.append(websocket)

        for websocket in disconnected:
            self.disconnect_dashboard(websocket)

    async def connect_user(self, websocket, user):
        await websocket.accept()

        user_id = user.id_usuario

        if user_id not in self.user_connections:
            self.user_connections[user_id] = []

        self.user_connections[user_id].append(websocket)

    def disconnect_user(self, websocket, user):
        user_id = user.id_usuario

        if user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)

            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

    async def broadcast_to_user(self, user_id: int, message: dict):
        connections = self.user_connections.get(user_id, [])

        disconnected = []

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception:
                disconnected.append(websocket)

        for websocket in disconnected:
            if websocket in self.user_connections.get(user_id, []):
                self.user_connections[user_id].remove(websocket)


manager = ConnectionManager()
