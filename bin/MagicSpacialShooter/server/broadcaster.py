import asyncio
import websockets
import json

class StateBroadcaster:

    def __init__(self, port=5556):
        self.port = port
        self.clients = set()
        self.server = None
        self.loop = None
        self.running = False

    async def _ws_handler(self, websocket):
        print("[StateBroadcaster] Cliente conectado")
        self.clients.add(websocket)

        try:
            async for _ in websocket:
                pass
        except Exception as e:
            print("[StateBroadcaster] Error conexión:", e)
        finally:
            self.clients.discard(websocket)
            print("[StateBroadcaster] Cliente desconectado")


    async def _broadcast_loop(self):
        while self.running:
            await asyncio.sleep(0.0005)

    def _run_async_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        async def run_ws():
            print(f"[Broadcaster] WebSocket escuchando en {self.port}")

            self.server = await websockets.serve(
                self._ws_handler,
                host="0.0.0.0",
                port=self.port
            )

            self.running = True
            await self.server.wait_closed()

        try:
            self.loop.run_until_complete(run_ws())
        finally:
            self.loop.close()

    async def broadcast_async(self, state_dict):
        msg = json.dumps(state_dict)

        dead = []
        for ws in list(self.clients):
            try:
                await ws.send(msg)
            except:
                dead.append(ws)

        for ws in dead:
            self.clients.discard(ws)

    def broadcast(self, state_dict):
        if not self.running:
            return
        asyncio.run_coroutine_threadsafe(
            self.broadcast_async(state_dict),
            self.loop
        )

    def start(self):
        import threading
        t = threading.Thread(target=self._run_async_loop, daemon=True)
        t.start()

    def stop(self):
        self.running = False
        if self.server:
            self.server.close()
