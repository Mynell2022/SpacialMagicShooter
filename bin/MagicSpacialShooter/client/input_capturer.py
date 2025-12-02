# ==========================================
# client/input_capturer.py
# Captura y gestiona los inputs del jugador
# ==========================================

import arcade
import time

class InputCapturer:
    """
    Captura los inputs del teclado y mouse del jugador.
    Se integra con Arcade para responder a eventos.
    """
    
    def __init__(self, player_id):
        self.player_id = player_id
        self.input_state = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'shoot': False
        }
        # Guardar posición del mouse para aim
        self.mouse_x = 0
        self.mouse_y = 0
    
    def on_key_press(self, key, modifiers):
        """
        Maneja eventos de teclas presionadas.
        WASD para movimiento, Espacio para disparar.
        """
        if key == arcade.key.W or key == arcade.key.UP:
            self.input_state['up'] = True
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.input_state['down'] = True
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.input_state['left'] = True
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.input_state['right'] = True
        elif key == arcade.key.SPACE:
            self.input_state['shoot'] = True
    
    def on_key_release(self, key, modifiers):
        """
        Maneja eventos de teclas soltadas.
        """
        if key == arcade.key.W or key == arcade.key.UP:
            self.input_state['up'] = False
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.input_state['down'] = False
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.input_state['left'] = False
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.input_state['right'] = False
        elif key == arcade.key.SPACE:
            self.input_state['shoot'] = False
    
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Captura la posición del mouse para apuntar.
        """
        self.mouse_x = x
        self.mouse_y = y
    
    def get_input_message(self):
        """
        Construye el mensaje de input para enviar al servidor.
        Incluye el estado de las teclas y la posición del mouse.
        """
        return {
            'player_id': self.player_id,
            'inputs': {
                **self.input_state,
                'aim_x': self.mouse_x,
                'aim_y': self.mouse_y
            },
            'timestamp': time.time()
        }