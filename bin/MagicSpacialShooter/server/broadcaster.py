import zmq
import json

class StateBroadcaster:
 

    def __init__(self, port=5556):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)

    def start(self):
    
        try:
            self.socket.bind(f"tcp://0.0.0.0:{self.port}")
            print(f"[StateBroadcaster] Publicando estado en el puerto {self.port}...")
        except Exception as e:
            print(f"[StateBroadcaster] Error al iniciar: {e}")

    def broadcast(self, state_dict):
  
        try:
            self.socket.send_json(state_dict)
        except Exception as e:
            print(f"[StateBroadcaster] Error al enviar estado: {e}")

    def stop(self):
 
        try:
            self.socket.close()
            self.context.term()
        except Exception:
            pass
