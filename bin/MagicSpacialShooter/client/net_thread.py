# ==========================================
# client/net_thread.py
# ==========================================
"""
Módulo de red del cliente - Comunicación bidireccional con el servidor
- Envía inputs del jugador (PUSH)
- Recibe estado del juego (SUB)
"""

import threading
import time
import zmq
import config

class NetIOThread(threading.Thread):
    """
    Hilo dedicado a la comunicación de red.
    Separa la lógica de red del renderizado para evitar bloqueos.
    """
    
    def __init__(self, player_id, input_capturer, state_store):
        super().__init__(daemon=True)
        self.player_id = player_id
        self.input_capturer = input_capturer
        self.state_store = state_store
        self.running = False
        
        # Contexto ZeroMQ
        self.context = zmq.Context()
        
        # Socket PUSH para enviar inputs al servidor
        self.push_socket = self.context.socket(zmq.PUSH)
        
        # Socket SUB para recibir estado del servidor
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Suscribirse a todos los mensajes
        
        # Control de tiempo para envío de inputs
        self.input_send_rate = 1.0 / 60.0  # 60 updates por segundo
        self.last_input_send = 0
        
    def run(self):
        """
        Bucle principal del hilo de red.
        1. Conecta a los sockets del servidor
        2. Envía inputs periódicamente
        3. Escucha estado del servidor constantemente
        """
        try:
            # Conectar al servidor
            server_address = config.SERVER_IP
            input_port = config.SERVER_INPUT_PORT
            state_port = config.SERVER_STATE_PORT
            
            self.push_socket.connect(f"tcp://{server_address}:{input_port}")
            self.sub_socket.connect(f"tcp://{server_address}:{state_port}")
            
            print(f"[NetIOThread] Conectado al servidor {server_address}")
            print(f"  📤 Enviando inputs a puerto {input_port}")
            print(f"  📥 Recibiendo estado desde puerto {state_port}")
            
            self.running = True
            
            # Configurar poller para recibir mensajes sin bloquear
            poller = zmq.Poller()
            poller.register(self.sub_socket, zmq.POLLIN)
            
            while self.running:
                # 1. Enviar inputs al servidor (throttled)
                current_time = time.time()
                if current_time - self.last_input_send >= self.input_send_rate:
                    self._send_input()
                    self.last_input_send = current_time
                
                # 2. Recibir estado del servidor (non-blocking)
                socks = dict(poller.poll(timeout=10))  # Esperar hasta 10ms
                
                if self.sub_socket in socks and socks[self.sub_socket] == zmq.POLLIN:
                    self._receive_state()
                
                # Pequeño sleep para no quemar CPU
                time.sleep(0.001)
                
        except Exception as e:
            print(f"[NetIOThread] Error en bucle de red: {e}")
        finally:
            self._cleanup()
    
    def _send_input(self):
        """
        Envía el estado actual de los inputs al servidor.
        """
        try:
            input_message = self.input_capturer.get_input_message()
            self.push_socket.send_json(input_message)
        except Exception as e:
            print(f"[NetIOThread] Error enviando input: {e}")
    
    def _receive_state(self):
        """
        Recibe y procesa el estado del juego desde el servidor.
        """
        try:
            state_data = self.sub_socket.recv_json(flags=zmq.NOBLOCK)
            
            # Actualizar el state store thread-safe
            self.state_store.update_state(state_data)
            
        except zmq.Again:
            # No hay datos disponibles (normal con NOBLOCK)
            pass
        except Exception as e:
            print(f"[NetIOThread] Error recibiendo estado: {e}")
    
    def _cleanup(self):
        """
        Limpia recursos de red al detener el hilo.
        """
        try:
            self.push_socket.close()
            self.sub_socket.close()
            self.context.term()
            print("[NetIOThread] Conexión cerrada limpiamente")
        except Exception as e:
            print(f"[NetIOThread] Error en cleanup: {e}")
    
    def stop(self):
        """
        Detiene el hilo de red de forma segura.
        """
        self.running = False
        print("[NetIOThread] Deteniendo hilo de red...")
