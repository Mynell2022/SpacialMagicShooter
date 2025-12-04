# client/net_thread.py


import threading
import time
import zmq
import config
import json

class NetIOThread(threading.Thread):
 
    
    def __init__(self, player_id, input_capturer, state_store):
        super().__init__(daemon=True)
        self.player_id = player_id
        self.input_capturer = input_capturer
        self.state_store = state_store
        self.running = False
        
        self.context = zmq.Context()
        
        self.push_socket = self.context.socket(zmq.PUSH)
        
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")  
        
        self.input_send_rate = 1.0 / 60.0  
        self.last_input_send = 0
        
    def run(self):

        try:
            server_address = config.SERVER_IP
            input_port = config.SERVER_INPUT_PORT
            state_port = config.SERVER_STATE_PORT
            
            self.push_socket.connect(f"tcp://{server_address}:{input_port}") 
            self.sub_socket.connect(f"tcp://{server_address}:{state_port}")
            
            print(f"[NetIOThread] Conectado al servidor {server_address}")
            print(f"Enviando inputs a puerto {input_port}")
            print(f"Recibiendo estado desde puerto {state_port}")
            
            self.running = True
            
            poller = zmq.Poller()
            poller.register(self.sub_socket, zmq.POLLIN)
            
            while self.running:
                current_time = time.time()
                if current_time - self.last_input_send >= self.input_send_rate:
                    self._send_input()
                    self.last_input_send = current_time
                
                socks = dict(poller.poll(timeout=10))  
                
                if self.sub_socket in socks and socks[self.sub_socket] == zmq.POLLIN:
                    self._receive_state()
                
                time.sleep(0.001)
                
        except Exception as e:
            print(f"[NetIOThread] Error en bucle de red: {e}")
        finally:
            self._cleanup()
    
    def _send_input(self):

        try:
            input_message = self.input_capturer.get_input_message()
            self.push_socket.send_json(input_message)
        except Exception as e:
            print(f"[NetIOThread] Error enviando input: {e}")
    
    def _receive_state(self):
   
        try:
            raw = self.sub_socket.recv_string(zmq.NOBLOCK)
        except zmq.Again:
            return  # No hay mensaje real

        if not raw or raw.strip() == "":
            print("[NetIOThread] Mensaje vacío recibido")
            return

        try:
            data = json.loads(raw)
            self.state_store.update_state(data)
        except json.JSONDecodeError:
            print("[NetIOThread] JSON inválido:", raw)
            return
    
    def _cleanup(self):
 
        try:
            self.push_socket.close()
            self.sub_socket.close()
            self.context.term()
            print("[NetIOThread] Conexión cerrada limpiamente")
        except Exception as e:
            print(f"[NetIOThread] Error en cleanup: {e}")
    
    def stop(self):
        self.running = False
        print("[NetIOThread] Deteniendo hilo de red...")
