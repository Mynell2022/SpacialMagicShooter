"""
ENTIDADES – MAGOS (Joseph)

Responsabilidades:
- Definir la entidad WizardPlayer y sus atributos.
- Administrar la colección de jugadores/magos en el servidor.
- Proveer funciones de movimiento y rotación.
"""

from common import constants
import math
from typing import Dict, List, Optional


# -----------------------------------------
# Entidad: WizardPlayer
# -----------------------------------------

class WizardPlayer:
    """
    Representa a un mago dentro del servidor.
    Mantiene su posición, vida, tipo y orientación.
    """

    def __init__(self, player_id: str, wizard_type: str, start_x: float, start_y: float):
        self.id = player_id
        self.wizard_type = wizard_type

        template = constants.WIZARD_TYPES.get(
            wizard_type, constants.WIZARD_TYPES[constants.DEFAULT_WIZARD_TYPE]
        )

        self.max_hp: int = template["max_hp"]
        self.hp: int = template["max_hp"]
        self.speed: float = template["speed"]
        self.color_tag: str = template["color"]

        # posición y orientación
        self.x = start_x
        self.y = start_y
        self.rotation = 0.0

        # por si más adelante necesitan estado extra
        self.metadata = {}

    def to_dict(self) -> dict:
        """
        Estructura que el cliente necesita para dibujar al mago.
        """
        return {
            "id": self.id,
            "wizard_type": self.wizard_type,
            "x": self.x,
            "y": self.y,
            "rotation": self.rotation,
            "hp": self.hp,
            "health": self.hp,  # compatibilidad con renderer
            "max_hp": self.max_hp,
            "color_tag": self.color_tag,
        }

    def __repr__(self):
        return (
            f"<WizardPlayer {self.id} type={self.wizard_type} "
            f"x={self.x:.1f} y={self.y:.1f} rot={self.rotation:.1f}° "
            f"hp={self.hp}/{self.max_hp} color={self.color_tag}>"
        )


# -----------------------------------------
# Manager
# -----------------------------------------

class PlayerManager:
    """
    Administra todos los magos conectados al servidor.
    """

    def __init__(self):
        self.players: Dict[str, WizardPlayer] = {}

        # si quieren auto-asignar color/tipo alternado
        self._cycle = list(constants.WIZARD_TYPES.keys())
        self._index = 0

    def _pick_type(self) -> str:
        if not self._cycle:
            return constants.DEFAULT_WIZARD_TYPE

        t = self._cycle[self._index]
        self._index = (self._index + 1) % len(self._cycle)
        return t

    def create_player(self, player_id: str) -> WizardPlayer:
        start_x = constants.MAP_WIDTH / 2
        start_y = constants.MAP_HEIGHT / 2
        wizard_type = self._pick_type()

        player = WizardPlayer(player_id, wizard_type, start_x, start_y)
        self.players[player_id] = player
        return player

    def remove_player(self, player_id: str):
        if player_id in self.players:
            del self.players[player_id]

    def get_player(self, player_id: str) -> Optional[WizardPlayer]:
        return self.players.get(player_id)

    def get_all_players(self) -> List[WizardPlayer]:
        return list(self.players.values())


# -----------------------------------------
# Movimiento y rotación
# -----------------------------------------

def update_player_movement(player: WizardPlayer, inputs: dict, dt: float):
    dx = 0.0
    dy = 0.0

    if inputs.get("up"):
        dy += 1
    if inputs.get("down"):
        dy -= 1
    if inputs.get("left"):
        dx -= 1
    if inputs.get("right"):
        dx += 1

    # diagonal
    if dx != 0 and dy != 0:
        scale = 1 / math.sqrt(2)
        dx *= scale
        dy *= scale

    player.x += dx * player.speed * dt
    player.y += dy * player.speed * dt

    # límites
    player.x = max(0, min(player.x, constants.MAP_WIDTH))
    player.y = max(0, min(player.y, constants.MAP_HEIGHT))


def update_player_rotation(player, inputs: dict):
    """
    Actualiza la rotación del mago según un punto de mira opcional.

    Si todavía no hay aim_x/aim_y (ej: antes de mover el mouse),
    simplemente no modifica la rotación.
    """
    ax_raw = inputs.get("aim_x")
    ay_raw = inputs.get("aim_y")

    # Si no se ha movido el mouse, no hay nada que hacer
    if ax_raw is None or ay_raw is None:
        return

    ax = float(ax_raw) - player.x
    ay = float(ay_raw) - player.y

    if ax == 0 and ay == 0:
        return

    angle = math.degrees(math.atan2(ay, ax))
    player.rotation = angle % 360



def update_player_state(player: WizardPlayer, inputs: dict, dt: float):
    update_player_movement(player, inputs, dt)
    update_player_rotation(player, inputs)
