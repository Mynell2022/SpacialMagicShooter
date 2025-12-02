import zmq
import threading
import queue
import json

class InputReceiver:
    """
    Módulo encargado de recibir los inputs de los clientes a través de ZeroMQ (PULL).
    Se ejecuta en un hilo separado para no bloquear el Game Loop principal.
    """

    def __init__(self, port=5555):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.running = False
        self.input_queue = queue.Queue()
        self.thread = None

    def start(self):
        """
        Inicia el socket y el hilo de escucha.
        """
        try:
            self.socket.bind(f"tcp://*:{self.port}")
            self.running = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()
            print(f"[InputReceiver] Escuchando inputs en el puerto {self.port}...")
        except Exception as e:
            print(f"[InputReceiver] Error al iniciar: {e}")

    def _listen_loop(self):
        """
        Bucle interno del hilo que espera mensajes y los encola.
        """
        while self.running:
            try:
                # recv_json bloquea hasta que llega un mensaje
                # Esto está bien porque estamos en un hilo dedicado
                message = self.socket.recv_json()
                self.input_queue.put(message)
            except zmq.ZMQError as e:
                if self.running:
                    print(f"[InputReceiver] Error de ZMQ: {e}")
            except Exception as e:
                print(f"[InputReceiver] Error inesperado: {e}")

    def get_pending_inputs(self):
        """
        Devuelve una lista con todos los inputs acumulados desde la última llamada.
        El Game Loop debe llamar a esto al inicio de cada tick.
        """
        inputs = []
        while not self.input_queue.empty():
            try:
                inputs.append(self.input_queue.get_nowait())
            except queue.Empty:
                break
        return inputs

    def stop(self):
        """
        Detiene el hilo y cierra el socket limpiamente.
        """
        self.running = False
        # Para desbloquear el recv(), podríamos enviar un mensaje dummy o cerrar el contexto,
        # pero por simplicidad en prototipo, cerramos el socket.
        try:
            self.socket.close()
            self.context.term()
        except Exception:
            pass
