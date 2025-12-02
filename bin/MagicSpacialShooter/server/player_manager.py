# server/player_manager.py
"""
ENTIDADES - Robots (Joseph)

Responsabilidades:
- Definir la entidad RobotPlayer y sus atributos base.
- Administrar la colección de jugadores/robots en el servidor.
- Proveer funciones de movimiento y rotación (sin tocar red ni render).
"""

from common import constants
import math
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Entidad: RobotPlayer
# ---------------------------------------------------------------------------

class RobotPlayer:
    """
    Representa a un jugador como robot dentro del servidor
    El servidor mantiene este estado como autoritativo
    """

    def __init__(self, player_id: str, robot_type: str, start_x: float, start_y: float):
        self.id = player_id
        self.robot_type = robot_type

        # Aplicar plantilla del tipo de robot
        template = constants.ROBOT_TYPES.get(robot_type, constants.ROBOT_TYPES[constants.DEFAULT_ROBOT_TYPE])

        self.max_hp: int = template["max_hp"]
        self.hp: int = template["max_hp"]
        self.speed: float = template["speed"]
        self.color_tag: str = template["color"]
        self.position: str = "stay"
        # Posición y orientación
        self.x: float = start_x
        self.y: float = start_y
        self.rotation: float = 0.0  # grados (0 = hacia la derecha)
        
        # Campo extra para que el resto del equipo pueda guardar cosas específicas
        self.metadata: dict = {}

    def to_dict(self) -> dict:
        
        
        """
        Estructura ligera para snapshots hacia los clientes.
        El cliente puede usar robot_type y color_tag para decidir sprite/color.
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
            "position": self.position,
        }

    def __repr__(self) -> str:
        return (
            f"<RobotPlayer id={self.id} type={self.robot_type} "
            f"x={self.x:.1f} y={self.y:.1f} rot={self.rotation:.1f}° "
            f"hp={self.hp}/{self.max_hp} color={self.color_tag}>"
        )


# ---------------------------------------------------------------------------
# Manager de jugadores/robots
# ---------------------------------------------------------------------------

class PlayerManager:
    
    
    """
    Administra la lista de jugadores/robots activos en el servidor.
    Uso esperado:
    - Kevin crea/borra jugadores cuando se conectan/desconectan.
    - GameLoop consulta y actualiza posiciones.
    """

    def __init__(self):
        self.players: Dict[str, RobotPlayer] = {}
        self._robot_type_cycle = list(constants.ROBOT_TYPES.keys())
        self._next_type_index = 0

    def _pick_next_robot_type(self) -> str:
        
        """
        Rota entre los tipos de robots para que cada jugador tenga algo distinto.
        """
        if not self._robot_type_cycle:
            return constants.DEFAULT_ROBOT_TYPE

        robot_type = self._robot_type_cycle[self._next_type_index]
        self._next_type_index = (self._next_type_index + 1) % len(self._robot_type_cycle)
        return robot_type

    def create_player(self, player_id: str) -> RobotPlayer:
        
        """
        Crea un nuevo robot para un jugador.
        - Posición inicial: centro del mapa.
        - Tipo de robot: se rota entre los disponibles para variar.
        """
        start_x = constants.MAP_WIDTH / 2
        start_y = constants.MAP_HEIGHT / 2
        robot_type = self._pick_next_robot_type()

        player = RobotPlayer(player_id, robot_type, start_x, start_y)
        self.players[player_id] = player
        return player

    def remove_player(self, player_id: str) -> None:
        
        """
        Eliminar jugador del registro (desconexiones)"""
        if player_id in self.players:
            del self.players[player_id]

    def get_player(self, player_id: str) -> Optional[RobotPlayer]:
        return self.players.get(player_id)

    def get_all_players(self) -> List[RobotPlayer]:
        return list(self.players.values())


# ---------------------------------------------------------------------------
# Movimiento y orientación
# ---------------------------------------------------------------------------

def update_player_movement(player: RobotPlayer, inputs: dict, delta_time: float) -> None:
    
    
    """
    Actualiza la posición del robot según los inputs de movimiento.

    Inputs esperados:
        "up", "down", "left", "right" : bool

    Esta función no sabe nada de red ni de interfaz, solo aplica física básica.
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

    # Normalización en diagonal
    if dx != 0.0 and dy != 0.0:
        factor = 1.0 / math.sqrt(2.0)
        dx *= factor
        dy *= factor

    # Aplicar desplazamiento con delta_time
    player.x += dx * player.speed * delta_time
    player.y += dy * player.speed * delta_time

    # Restringir al área del mapa
    player.x = max(265.0, min(player.x, 1010))
    player.y = max(95.0, min(player.y, 620))


def update_player_rotation(player: RobotPlayer, inputs: dict) -> None:
    """
    Actualiza la rotación del robot según un punto de mira opcional.

    Inputs opcionales:
        "aim_x", "aim_y": coordenadas en el mapa hacia donde apunta el jugador.

    Esto permite que el cliente dispare en cualquier dirección.
    """
    if "aim_x" not in inputs or "aim_y" not in inputs:
        return

    ax = float(inputs["aim_x"]) - player.x
    ay = float(inputs["aim_y"]) - player.y

    # Evitar división por cero si coincide exactamente
    if ax == 0.0 and ay == 0.0:
        return

    angle_rad = math.atan2(ay, ax)
    angle_deg = math.degrees(angle_rad)

    player.rotation = angle_deg % 360.0


def update_player_state(player: RobotPlayer, inputs: dict, delta_time: float) -> None:
    """
    Punto de entrada para el GameLoop:
    - Aplica movimiento.
    - Actualiza orientación (si hay datos de mira).
    """
    update_player_movement(player, inputs, delta_time)
    update_player_rotation(player, inputs)


# ---------------------------------------------------------------------------
# Test local (se puede usar para probar ENTIDADES sin depender del resto)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Prueba rápida de ENTIDADES (robots) sin red ni cliente.

    Ejecutar desde la raíz del proyecto:
        python -m server.player_manager
    """

    import time

    pm = PlayerManager()

    # Creamos varios robots para ver la rotación de tipos
    p1 = pm.create_player("kev")
    p2 = pm.create_player("bay")
    p3 = pm.create_player("dey")
    p4 = pm.create_player("my")
    print("Robots creados:")
    print(" ", p1)
    print(" ", p2)
    print(" ", p3)
    print(" ", p4)

    # Probamos movimiento y rotación en uno de ellos
    player = p1
    print("\nSimulando movimiento del robot:", player.id, "-", player.robot_type)

    # Secuencia de inputs: (inputs, duración_en_segundos)
    sequence = [
        ({"up": True}, 0.5),
        ({"right": True}, 0.5),
        ({"down": True, "right": True}, 0.5),
        ({"left": True}, 0.5),
        ({"aim_x": 0, "aim_y": constants.MAP_HEIGHT}, 0.5),
    ]

    for inp, duration in sequence:
        start = time.perf_counter()
        elapsed = 0.0

        while elapsed < duration:
            now = time.perf_counter()
            dt = now - start
            start = now
            elapsed += dt

            update_player_state(player, inp, dt)
            print(player)
            time.sleep(0.04)

    print("\nFin de prueba de ENTIDADES (robots).")
