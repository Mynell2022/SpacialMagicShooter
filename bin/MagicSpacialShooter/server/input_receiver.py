# server/input_receiver.py

import asyncio
import threading
import queue
import websockets
import json


class InputReceiver:

    def __init__(self, port=5555):
        self.port = port
        self.input_queue = queue.Queue()
        self.running = False
        self.thread = None
        self.loop = None

    # ---------------------------------------------
    # Start thread
    # ---------------------------------------------
    def start(self):
        self.thread = threading.Thread(target=self._run_async_loop, daemon=True)
        self.thread.start()

    # ---------------------------------------------
    # Async loop inside thread
    # ---------------------------------------------
    def _run_async_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        async def start():
            print(f"[InputReceiver] WebSocket en puerto {self.port}")
            self.server = await websockets.serve(
                self._ws_handler,
                host="0.0.0.0",
                port=self.port,
                process_request=self._process_request
            )
            self.running = True
            await self.server.wait_closed()
        try:
            self.loop.run_until_complete(start())
        finally:
            self.loop.close()
    
    async def _process_request(self, path, request_headers):
        if "Upgrade" not in request_headers.headers:
            return (
                200,
                [("Content-Type", "text/plain")],
                b"OK"
            )
        return None


    async def _ws_handler(self, websocket):
        print("[InputReceiver] Cliente conectado")

        try:
            async for message in websocket:
                self.handle_message(message)
        except Exception as e:
            print("[InputReceiver] Error en cliente:", e)
        finally:
            print("[InputReceiver] Cliente desconectado")

    def handle_message(self, raw_message):
        try:
            data = json.loads(raw_message)
            self.input_queue.put(data)
        except Exception as e:
            print("[InputReceiver] Error procesando mensaje:", e)

    # ---------------------------------------------
    def get_pending_inputs(self):
        items = []
        while not self.input_queue.empty():
            items.append(self.input_queue.get())
        return items

    # ---------------------------------------------
    def stop(self):
        self.running = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)