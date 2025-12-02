# client/main_client.py
"""
Cliente principal - por el momento solo setup del mapa y renderizado
"""
import arcade
import uuid
from config import *
from renderer import Renderer
from local_state_store import LocalStateStore
from input_capturer import InputCapturer
from net_thread import NetIOThread
from client_game_loop import ClientGameLoop

class GameWindow(arcade.Window):
    """Ventana principal del juego"""
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # ID del jugador
        self.player_id = str(uuid.uuid4())[:8]
        
        # === Renderer y Game Loop ===
        self.renderer = Renderer()
        self.game_loop = ClientGameLoop(None, self.player_id)  # state_store se pasa después
        
        # === placeholder mínimo ===
        self.state_store = LocalStateStore()
        self.input_capturer = InputCapturer(self.player_id)
        self.net_thread = None
        
        # Actualizar referencia en game_loop
        self.game_loop.state_store = self.state_store
        
        print(f"Cliente iniciado - Player ID: {self.player_id}")
    
    def setup(self):
        """Configuración inicial del juego"""
        # Thread de red (parte de otros, pero necesario para no romper)
        self.net_thread = NetIOThread(
            self.player_id,
            self.input_capturer,
            self.state_store
        )
        self.net_thread.start()
        
        print("Esperando conexión al servidor...")
        print("Mapa y objetos listos para recibir datos")
    
    def on_draw(self):
        """
        Dibuja el mapa y objetos (power-ups) ===
        """
        self.clear()
        
        # Obtener estado actual del juego
        game_state = self.state_store.get_state()
        
        # === RENDERIZADO DEL MAPA Y OBJETOS ===
        self.renderer.draw_background()
        #self.renderer.draw_map_borders()
        
        # === Power-ups ===
        self.renderer.draw_powerups(game_state.get('powerups', []))
        
        self.renderer.draw_bullets(game_state.get('bullets', []))
        self.renderer.draw_players(game_state.get('players', {}), self.player_id)
        
        # UI
        self.renderer.draw_ui(game_state, self.player_id)
        """
        players = [
            {"id": "ab12cd34", "x": 265, "y": 95, "hp": 70, "position": "stay"},
            {"id": "fe56ab78", "x": 1010, "y": 620, "hp": 100, "position": "right"},
            {"id": "p1aa22", "x": 50, "y": 50, "hp": 90, "position": "left"},
            {"id": "p2bb33", "x": 1050, "y": 40, "hp": 85, "position": "stay"},
            {"id": "p3cc44", "x": 40, "y": 650, "hp": 60, "position": "right"},
            {"id": "p4dd55", "x": 1080, "y": 680, "hp": 75, "position": "up"},
            {"id": "p5ee66", "x": 550, "y": 350, "hp": 100, "position": "down"},
            {"id": "p6ff77", "x": 600, "y": 150, "hp": 95, "position": "stay"},
            {"id": "p7gg88", "x": 500, "y": 580, "hp": 40, "position": "left"},
            {"id": "p8hh99", "x": 300, "y": 400, "hp": 90, "position": "up"},
            {"id": "p9ii00", "x": 850, "y": 250, "hp": 55, "position": "right"},
            {"id": "p10jj11", "x": 750, "y": 500, "hp": 30, "position": "stay"}
        ]
        self.renderer.draw_players(players, "ab12cd34")
        spells = [
            [150, 120, 20],
            [450, 100, 350],
            [800, 80, 10],
            [250, 300, 90],
            [350, 350, 270],
            [600, 350, 180],
            [700, 400, 45],
            [1000, 320, 200],
            [1150, 280, 300],
            [300, 600, 60],
            [700, 650, 120],
            [900, 580, 250],
        ]
        self.renderer.draw_bullets(spells)"""
    
    def on_update(self, delta_time):
        """
        === Verificación de límites del mapa ===
        """
        self.game_loop.update(delta_time)
    
    def on_key_press(self, key, modifiers):
        """Input (parte de otros)"""
        self.input_capturer.on_key_press(key, modifiers)
    
    def on_key_release(self, key, modifiers):
        """Input (parte de otros)"""
        self.input_capturer.on_key_release(key, modifiers)
    
    def on_mouse_motion(self, x, y, dx, dy):
        """Captura movimiento del mouse para apuntar"""
        self.input_capturer.on_mouse_motion(x, y, dx, dy)
    
    def on_close(self):
        """Limpieza al cerrar"""
        if self.net_thread:
            self.net_thread.stop()
            self.net_thread.join()
        print("Cliente cerrado")
        self.close()

def main():
    """Punto de entrada del cliente"""
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()