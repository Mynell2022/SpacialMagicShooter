"""
ENTIDADES - Magos (Joseph)

- Define la entidad de jugador (mago) en el servidor.
- Administra la lista de magos conectados.
- Aplica movimiento y rotación según inputs.
"""

from common import constants
import math
from typing import Dict, List, Optional


class WizardPlayer:
    """Estado autoritativo de un mago en el servidor."""

    def __init__(self, player_id: str, robot_type: str, start_x: float, start_y: float):
        self.id = player_id

        # Usamos ROBOT_TYPES como plantillas de "clase de mago"
        self.robot_type = robot_type
        template = constants.ROBOT_TYPES.get(
            robot_type, constants.ROBOT_TYPES[constants.DEFAULT_ROBOT_TYPE]
        )

        self.max_hp: int = template["max_hp"]
        self.hp: int = template["max_hp"]
        self.speed: float = template["speed"]
        self.color_tag: str = template["color"]  # etiqueta para el cliente si quiere usarla

        # Posición y orientación
        self.x: float = start_x
        self.y: float = start_y
        self.rotation: float = 0.0  # grados, 0 = derecha
        self.position: str = "stay"  # dirección lógica para el renderer
        
        # Cooldown de disparo
        self.last_shot_time: float = 0.0


        # Campo libre para el resto del equipo
        self.metadata: dict = {}

    # ---- helpers visuales para el cliente ----

    def get_direction(self) -> str:
        """
        Dirección lógica según la rotación.
        (Opcional, por si luego quieren usar rotación para sprites).
        """
        a = self.rotation % 360.0

        if 45 <= a < 135:
            return "up"
        elif 135 <= a < 225:
            return "left"
        elif 225 <= a < 315:
            return "down"
        else:
            return "right"

    def to_dict(self) -> dict:
        """
        Snapshot ligero para mandar al cliente.
        """
        return {
            "id": self.id,
            "robot_type": self.robot_type,
            "x": self.x,
            "y": self.y,
            "rotation": self.rotation,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "color_tag": self.color_tag,
            "position": self.position,  # usado por renderer
        }

    def __repr__(self) -> str:
        return (
            f"<WizardPlayer id={self.id} type={self.robot_type} "
            f"x={self.x:.1f} y={self.y:.1f} rot={self.rotation:.1f}° "
            f"hp={self.hp}/{self.max_hp} color={self.color_tag}>"
        )


class PlayerManager:
    """Administra los magos activos."""

    def __init__(self):
        self.players: Dict[str, WizardPlayer] = {}
        self._robot_type_cycle = list(constants.ROBOT_TYPES.keys())
        self._next_type_index = 0

    def _pick_next_robot_type(self) -> str:
        """Rota entre plantillas de mago para variar."""
        if not self._robot_type_cycle:
            return constants.DEFAULT_ROBOT_TYPE

        robot_type = self._robot_type_cycle[self._next_type_index]
        self._next_type_index = (self._next_type_index + 1) % len(self._robot_type_cycle)
        return robot_type

    def create_player(self, player_id: str) -> WizardPlayer:
        """
        Crea un nuevo mago en el centro del mapa.
        """
        start_x = constants.MAP_WIDTH / 2
        start_y = constants.MAP_HEIGHT / 2
        robot_type = self._pick_next_robot_type()

        player = WizardPlayer(player_id, robot_type, start_x, start_y)
        self.players[player_id] = player
        return player

    def remove_player(self, player_id: str) -> None:
        """Eliminar mago (desconexión)."""
        if player_id in self.players:
            del self.players[player_id]

    def get_player(self, player_id: str) -> Optional[WizardPlayer]:
        return self.players.get(player_id)

    def get_all_players(self) -> List[WizardPlayer]:
        return list(self.players.values())


# ---- Movimiento y rotación ----

def update_player_movement(player: WizardPlayer, inputs: dict, delta_time: float) -> None:
    """
    Aplica movimiento base según WASD y actualiza la 'position' lógica.
    """
    dx = 0.0
    dy = 0.0

    if inputs.get("up"):
        player.position = "up"
        dy += 1.0
    elif inputs.get("down"):
        player.position = "down"
        dy -= 1.0
    elif inputs.get("left"):
        player.position = "left"
        dx -= 1.0
    elif inputs.get("right"):
        player.position = "right"
        dx += 1.0
    else:
        player.position = "stay"

    # Normalizar diagonal
    if dx != 0.0 and dy != 0.0:
        factor = 1.0 / math.sqrt(2.0)
        dx *= factor
        dy *= factor

    # Movimiento
    player.x += dx * player.speed * delta_time
    player.y += dy * player.speed * delta_time

    # Limites de mapa lógicos
    player.x = max(constants.GAME_AREA_MIN_X, min(player.x, constants.GAME_AREA_MAX_X))
    player.y = max(constants.GAME_AREA_MIN_Y, min(player.y, constants.GAME_AREA_MAX_Y))


def update_player_rotation(player: WizardPlayer, inputs: dict) -> None:
    """
    Gira el mago hacia la mira (mouse).
    """
    if "aim_x" not in inputs or "aim_y" not in inputs:
        return

    ax = float(inputs["aim_x"]) - player.x
    ay = float(inputs["aim_y"]) - player.y

    if ax == 0.0 and ay == 0.0:
        return

    angle_rad = math.atan2(ay, ax)
    angle_deg = math.degrees(angle_rad)
    player.rotation = angle_deg % 360.0


def update_player_state(player: WizardPlayer, inputs: dict, delta_time: float) -> None:
    """Punto de entrada para el GameLoop del servidor."""
    update_player_movement(player, inputs, delta_time)
    update_player_rotation(player, inputs)
