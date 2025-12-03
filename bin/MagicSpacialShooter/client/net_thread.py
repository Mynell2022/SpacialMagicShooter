# client/net_thread.py

import threading
import time
import json
import asyncio
import websockets
import config


class NetIOThread(threading.Thread):

    def __init__(self, player_id, input_capturer, state_store):
        super().__init__(daemon=True)
        self.player_id = player_id
        self.input_capturer = input_capturer
        self.state_store = state_store

        self.running = False

        # URLs de los servidores WebSocket
        self.input_url = f"ws://{config.SERVER_IP}:{config.SERVER_INPUT_PORT}"
        self.state_url = f"ws://{config.SERVER_IP}:{config.SERVER_STATE_PORT}"

        self.loop = None

    # =======================================
    #               RUN
    # =======================================
    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.loop.run_until_complete(self.main_loop())

    # =======================================
    #            MAIN ASYNC LOOP
    # =======================================
    async def main_loop(self):

        print(f"[NetIOThread] Conectando a websockets...")

        try:
            async with websockets.connect(self.input_url) as input_ws, \
                       websockets.connect(self.state_url) as state_ws:

                print("[NetIOThread] Conectado a INPUT y STATE websockets")

                self.running = True

                # Lanzar la tarea que escucha estados
                state_task = asyncio.create_task(self.state_receiver(state_ws))

                while self.running:
                    await self.send_input(input_ws)
                    await asyncio.sleep(1/60)

                state_task.cancel()

        except Exception as e:
            print(f"[NetIOThread] ERROR EN CONEXIÓN WEBSOCKET: {e}")

    # =======================================
    #         ENVÍO DE INPUT
    # =======================================
    async def send_input(self, input_ws):
        try:
            message = self.input_capturer.get_input_message()

            # Asegurar que es JSON válido
            await input_ws.send(json.dumps(message))

        except Exception as e:
            print(f"[NetIOThread] Error enviando INPUT → {e}")

    # =======================================
    #       RECEPCIÓN DE ESTADO
    # =======================================
    async def state_receiver(self, state_ws):

        while self.running:
            try:
                raw_msg = await state_ws.recv()
                state_data = json.loads(raw_msg)

                self.state_store.update_state(state_data)

            except websockets.ConnectionClosed as e:
                print(f"[NetIOThread] STATE cerrado: {e.code} {e.reason}")
                break
            except Exception as e:
                print(f"[NetIOThread] Error recibiendo STATE: {e}")

    # =======================================
    #       DETENER HILO
    # =======================================
    def stop(self):
        self.running = False
        print("[NetIOThread] Detenido.")
