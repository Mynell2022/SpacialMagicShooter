import zmq
import threading
import queue
import json

class InputReceiver:
 

    def __init__(self, port=5555):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.running = False
        self.input_queue = queue.Queue()
        self.thread = None

    def start(self):

        try:
            self.socket.bind(f"tcp://*:{self.port}")
            self.running = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()
            print(f"[InputReceiver] Escuchando inputs en el puerto {self.port}...")
        except Exception as e:
            print(f"[InputReceiver] Error al iniciar: {e}")

    def _listen_loop(self):
     
        while self.running:
            try:
      
                message = self.socket.recv_json()
                self.input_queue.put(message)
            except zmq.ZMQError as e:
                if self.running:
                    print(f"[InputReceiver] Error de ZMQ: {e}")
            except Exception as e:
                print(f"[InputReceiver] Error inesperado: {e}")

    def get_pending_inputs(self):
  
        inputs = []
        while not self.input_queue.empty():
            try:
                inputs.append(self.input_queue.get_nowait())
            except queue.Empty:
                break
        return inputs

    def stop(self):

        self.running = False
 
        try:
            self.socket.close()
            self.context.term()
        except Exception:
            pass
