# client/main_client.py

import arcade
import uuid
from config import *
from renderer import Renderer
from local_state_store import LocalStateStore
from input_capturer import InputCapturer
from net_thread import NetIOThread
from client_game_loop import ClientGameLoop
from typing import Literal

class GameWindow(arcade.Window):
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.player_id = str(uuid.uuid4())[:8]
        
        self.renderer = Renderer()
        self.game_loop = ClientGameLoop(None, self.player_id)  
        
        self.state_store = LocalStateStore()
        self.input_capturer = InputCapturer(self.player_id)
        self.net_thread = None
        
        self.game_loop.state_store = self.state_store
        
        print(f"Cliente iniciado - Player ID: {self.player_id}")
    
    def setup(self):
        self.net_thread = NetIOThread(
            self.player_id,
            self.input_capturer,
            self.state_store
        )
        self.net_thread.start()
        
        print("Esperando conexión al servidor...")
        print("Mapa y objetos listos para recibir datos")
    
    def on_draw(self):
        self.clear()
        
        game_state = self.state_store.get_state()
        
        self.renderer.draw_background()
        
        self.renderer.draw_powerups(game_state.get('powerups', []))
        self.renderer.draw_bullets(game_state.get('bullets', []))
        self.renderer.draw_players(game_state.get('players', {}), self.player_id)
        
        self.renderer.draw_ui(game_state, self.player_id)


    
    def on_update(self, delta_time):
  
        self.game_loop.update(delta_time)
    
    def on_key_press(self, key, modifiers):
        self.input_capturer.on_key_press(key, modifiers)
    
    def on_key_release(self, key, modifiers):
        self.input_capturer.on_key_release(key, modifiers)
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.input_capturer.on_mouse_motion(x, y, dx, dy)
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.input_capturer.on_mouse_press(x, y, button, modifiers)
        if x-60 < 140 < x+60 and y-60 <670 < y+60:
            self.renderer.showScoreboard()
        if x-60 < 870 < x+60 and y-60 <130 < y+60:
            self.renderer.closeScoreboard()
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.input_capturer.on_mouse_release(x, y, button, modifiers)
    
    def on_close(self):
        if self.net_thread:
            self.net_thread.stop()
        print("Cliente cerrado")
        self.close()

def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()