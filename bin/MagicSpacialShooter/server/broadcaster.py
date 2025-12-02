import zmq
import json

class StateBroadcaster:
    """
    Módulo encargado de difundir (PUB) el estado del juego a todos los clientes conectados.
    Utiliza ZeroMQ PUB socket.
    """

    def __init__(self, port=5556):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)

    def start(self):
        """
        Enlaza el socket al puerto especificado.
        """
        try:
            self.socket.bind(f"tcp://*:{self.port}")
            print(f"[StateBroadcaster] Publicando estado en el puerto {self.port}...")
        except Exception as e:
            print(f"[StateBroadcaster] Error al iniciar: {e}")

    def broadcast(self, state_dict):
        """
        Envía el diccionario de estado serializado como JSON a todos los suscriptores.
        """
        try:
            # send_json serializa y envía
            self.socket.send_json(state_dict)
        except Exception as e:
            print(f"[StateBroadcaster] Error al enviar estado: {e}")

    def stop(self):
        """
        Cierra los recursos de ZeroMQ.
        """
        try:
            self.socket.close()
            self.context.term()
        except Exception:
            pass
