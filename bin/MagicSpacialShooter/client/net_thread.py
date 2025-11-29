
# ==========================================
# client/net_thread.py
# ==========================================
import threading
import time

class NetIOThread(threading.Thread):
    """Placeholder - Le toca a otro compañero"""
    
    def __init__(self, player_id, input_capturer, state_store):
        super().__init__(daemon=True)
        self.player_id = player_id
        self.input_capturer = input_capturer
        self.state_store = state_store
        self.running = False
    
    def run(self):
        """TODO: Implementar por otro compañero"""
        self.running = True
        print("Net thread placeholder (esperando implementación real)")
        
        while self.running:
            time.sleep(0.1)
    
    def stop(self):
        """TODO: Implementar por otro compañero"""
        self.running = False
