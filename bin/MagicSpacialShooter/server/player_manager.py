"""
ENTIDADES - Magos (Joseph)

- Define la entidad de jugador (mago) en el servidor.
- Administra la lista de magos conectados.
- Aplica movimiento y rotación según inputs.
"""

from common import constants
import math
import time
from typing import Dict, List, Optional
import random


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
        self.damage: str = template["damage"]
        self.score: int = 0

        # Posición y orientación
        self.x: float = start_x
        self.y: float = start_y
        self.rotation: float = 0.0  # grados, 0 = derecha
        self.position: str = "stay"  # dirección lógica para el renderer
        
        # Cooldown de disparo
        self.last_shot_time: float = 0.0

        # Timestamp de última actividad (para detectar desconexión)
        self.last_activity: float = time.time()
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
            "damage": self.damage,
            "score": self.score,
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

        # Configuración de timeout
        self.disconnect_timeout = 10.0  # segundos sin actividad = desconectado
        
        # Sistema de respawn
        self.respawn_cooldowns: Dict[str, float] = {}  # {player_id: timestamp_muerte}
        self.respawn_delay = 10.0  # segundos antes de poder reaparecer

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
        Verifica que no esté en cooldown de respawn.
        """
        # Verificar si está en cooldown de respawn
        if player_id in self.respawn_cooldowns:
            time_since_death = time.time() - self.respawn_cooldowns[player_id]
            
            if time_since_death < self.respawn_delay:
                # Todavía en cooldown
                remaining = self.respawn_delay - time_since_death
                return None
            else:
                # Cooldown terminado, puede reaparecer
                del self.respawn_cooldowns[player_id]
                
        start_x = random.randint(265, constants.MAP_WIDTH)
        start_y = random.randint(95, constants.MAP_HEIGHT)
        robot_type = self._pick_next_robot_type()

        player = WizardPlayer(player_id, robot_type, start_x, start_y)
        self.players[player_id] = player
        return player

    def remove_player(self, player_id: str, reason: str = "unknown") -> None:
        """
        Eliminar mago (desconexión o muerte).
        
        Args:
            player_id: ID del jugador a eliminar
            reason: 'death' para muerte por combate, 'disconnect' para desconexión
        """
        if player_id in self.players:
            del self.players[player_id]
            
            # Solo agregar cooldown si murió en combate (no en desconexión)
            if reason == "death":
                self.respawn_cooldowns[player_id] = time.time()
                print(f"[PlayerManager] Jugador eliminado por muerte: {player_id} (cooldown: {self.respawn_delay}s)")
            else:
                print(f"[PlayerManager] Jugador eliminado ({reason}): {player_id}")

    def get_player(self, player_id: str) -> Optional[WizardPlayer]:
        return self.players.get(player_id)

    def get_all_players(self) -> List[WizardPlayer]:
        return list(self.players.values())
    
    # Actualizar actividad del jugador
    def update_player_activity(self, player_id: str) -> None:
        """
        Actualiza el timestamp de última actividad del jugador.
        Debe llamarse cada vez que se recibe un input.
        """
        player = self.get_player(player_id)
        if player:
            player.last_activity = time.time()

    # Eliminar jugadores sin vida
    def remove_dead_players(self) -> List[str]:
        """
        Elimina jugadores con hp <= 0.
        Retorna lista de IDs eliminados.
        """
        dead_players = []
        
        for player_id, player in list(self.players.items()):
            if player.hp <= 0:
                dead_players.append(player_id)
                self.remove_player(player_id, reason="death")  # Especificar razón
        
        return dead_players
    
    def remove_disconnected_players(self) -> List[str]:
        """
        Elimina jugadores que no han enviado input en más de X segundos.
        Retorna lista de IDs eliminados.
        """
        current_time = time.time()
        disconnected_players = []
        
        for player_id, player in list(self.players.items()):
            time_since_activity = current_time - player.last_activity
            
            if time_since_activity > self.disconnect_timeout:
                disconnected_players.append(player_id)
                self.remove_player(player_id, reason="disconnect")  # ✅ Especificar razón
                
                # Limpiar cooldown si existía (desconexión = puede volver cuando quiera)
                if player_id in self.respawn_cooldowns:
                    del self.respawn_cooldowns[player_id]
        
        return disconnected_players


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
    if inputs.get("down"):
        player.position = "down"
        dy -= 1.0
    if inputs.get("left"):
        player.position = "left"
        dx -= 1.0
    if inputs.get("right"):
        player.position = "right"
        dx += 1.0
    if not (inputs.get("up") or inputs.get("down") or inputs.get("left") or inputs.get("right")):
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

