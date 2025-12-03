# client/input_capturer.py

import arcade
import time

class InputCapturer:

    
    def __init__(self, player_id):
        self.player_id = player_id
        self.input_state = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'shoot': False
        }
        self.mouse_x = 0
        self.mouse_y = 0
    
    def on_key_press(self, key, modifiers):

        if key == arcade.key.W or key == arcade.key.UP:
            self.input_state['up'] = True
        if key == arcade.key.S or key == arcade.key.DOWN:
            self.input_state['down'] = True
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.input_state['left'] = True
        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.input_state['right'] = True
    
    def on_key_release(self, key, modifiers):
 
        if key == arcade.key.W or key == arcade.key.UP:
            self.input_state['up'] = False
        if key == arcade.key.S or key == arcade.key.DOWN:
            self.input_state['down'] = False
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.input_state['left'] = False
        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.input_state['right'] = False
    
    def on_mouse_motion(self, x, y, dx, dy):
  
        self.mouse_x = x
        self.mouse_y = y
    
    def on_mouse_press(self, x, y, button, modifiers):
  
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.input_state['shoot'] = True
    
    def on_mouse_release(self, x, y, button, modifiers):
 
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.input_state['shoot'] = False
    
    def get_input_message(self):
 
        return {
            'player_id': self.player_id,
            'inputs': {
                **self.input_state,
                'aim_x': self.mouse_x,
                'aim_y': self.mouse_y
            },
            'timestamp': time.time()
        }