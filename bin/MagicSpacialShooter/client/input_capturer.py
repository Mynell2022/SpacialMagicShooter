# ==========================================
# client/input_capturer.py
# Lo minimo necesario 
# ==========================================

import arcade
import time

class InputCapturer:
    """Placeholder - Le toca a otro compañero"""
    
    def __init__(self, player_id):
        self.player_id = player_id
        self.input_state = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'shoot': False
        }
    
    def on_key_press(self, key, modifiers):
        """TODO: Implementar por otro compañero"""
        pass
    
    def on_key_release(self, key, modifiers):
        """TODO: Implementar por otro compañero"""
        pass
    
    def get_input_message(self):
        """TODO: Implementar por otro compañero"""
        return {
            'player_id': self.player_id,
            'inputs': self.input_state.copy(),
            'timestamp': time.time()
        }