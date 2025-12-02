# client/test_wizards_demo.py
"""
Demostración visual del MÓDULO DE ENTIDADES (Joseph)
Mostrando magos BLUE y RED con sprites reales del juego.

- Usa WizardPlayer desde server/player_manager.py
- Dibuja con renderer.py de tus compas
- Control: WASD para mover al mago azul
- Mouse para rotar
"""

import time
import arcade

from server.player_manager import PlayerManager, update_player_state
from common import constants
from client.config import *          # <- así lo dejaste antes, está OK si se ejecuta desde root
from client.renderer import Renderer  # <- CAMBIAR A ESTO

class WizardDemoWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "DEMO ENTIDADES – JOSEPH")

        # Renderer de tus compas
        self.renderer = Renderer()

        # PlayerManager de tus ENTIDADES
        self.pm = PlayerManager()

        # Crear dos magos (blue y red)
        self.blue_id = "blue_mage"
        self.red_id = "red_mage"

        self.blue_player = self.pm.create_player(self.blue_id)
        self.red_player = self.pm.create_player(self.red_id)

        # mover al rojo un toque hacia la izquierda para que no se monten
        self.red_player.x -= 60

        # Estado de inputs del mago azul (controlable)
        self.inputs = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "aim_x": None,
            "aim_y": None,
        }

        # game_state que usa el renderer
        self.game_state = {
            "players": {},
            "scores": {self.blue_id: 0, self.red_id: 0},
            "game_time": 0
        }

        self.last_time = time.perf_counter()
        self.set_mouse_visible(True)

    # -------------------------
    # Controles (solo azul)
    # -------------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.inputs["up"] = True
        if key == arcade.key.S:
            self.inputs["down"] = True
        if key == arcade.key.A:
            self.inputs["left"] = True
        if key == arcade.key.D:
            self.inputs["right"] = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.inputs["up"] = False
        if key == arcade.key.S:
            self.inputs["down"] = False
        if key == arcade.key.A:
            self.inputs["left"] = False
        if key == arcade.key.D:
            self.inputs["right"] = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.inputs["aim_x"] = x - MAP_X_OFFSET
        self.inputs["aim_y"] = y - MAP_Y_OFFSET

    # -------------------------
    # Lógica
    # -------------------------
    def on_update(self, delta_time):
        now = time.perf_counter()
        dt = now - self.last_time
        self.last_time = now

        # Mover/rotar mago azul (el tuyo)
        update_player_state(self.blue_player, self.inputs, dt)

        # El rojo no se mueve (NPC estático solo pa' la foto)

        
        
        def _hp_to_percent(player):
            return min(100, int(player.hp / player.max_hp * 100))

        self.game_state["players"] = {
            self.blue_id: {
                "x": MAP_X_OFFSET + self.blue_player.x,
                "y": MAP_Y_OFFSET + self.blue_player.y,
                "rotation": self.blue_player.rotation,
                "health": _hp_to_percent(self.blue_player),
                "score": 0,
            },
            self.red_id: {
                "x": MAP_X_OFFSET + self.red_player.x,
                "y": MAP_Y_OFFSET + self.red_player.y,
                "rotation": self.red_player.rotation,
                "health": _hp_to_percent(self.red_player),
                "score": 0,
            },
        }


        self.game_state["game_time"] += dt

    # -------------------------
    # Dibujado
    # -------------------------
    def on_draw(self):
        
        # Arcade 3.x → limpiar ventana con clear(), NO start_render()
        self.clear()

        self.renderer.draw_background()
        self.renderer.draw_map_borders()
        self.renderer.draw_players(self.game_state["players"], self.blue_id)
        self.renderer.draw_ui(self.game_state, self.blue_id)


def main():
    window = WizardDemoWindow()
    arcade.run()


if __name__ == "__main__":
    main()
