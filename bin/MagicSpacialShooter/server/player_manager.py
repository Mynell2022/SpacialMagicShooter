

from common import constants
import math
import time
from typing import Dict, List, Optional
import random


class WizardPlayer:

    def __init__(self, player_id: str, robot_type: str, start_x: float, start_y: float):
        self.id = player_id

        self.robot_type = robot_type
        template = constants.ROBOT_TYPES.get(
            robot_type, constants.ROBOT_TYPES[constants.DEFAULT_ROBOT_TYPE]
        )

        self.max_hp: int = template["max_hp"]
        self.hp: int = template["max_hp"]
        self.speed: float = template["speed"]
        self.color_tag: str = template["color"]  
        self.damage: str = template["damage"]
        self.score: int = 0

        self.x: float = start_x
        self.y: float = start_y
        self.rotation: float = 0.0  
        self.position: str = "stay"  
        
        self.last_shot_time: float = 0.0

        self.last_activity: float = time.time()
        self.metadata: dict = {}


    def get_direction(self) -> str:
  
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

    def __init__(self):
        self.players: Dict[str, WizardPlayer] = {}
        self._robot_type_cycle = list(constants.ROBOT_TYPES.keys())
        self._next_type_index = 0

        self.disconnect_timeout = 10.0  
        
        self.respawn_cooldowns: Dict[str, float] = {}  
        self.respawn_delay = constants.RESPAWN_DELAY 

    def _pick_next_robot_type(self) -> str:
        if not self._robot_type_cycle:
            return constants.DEFAULT_ROBOT_TYPE

        robot_type = self._robot_type_cycle[self._next_type_index]
        self._next_type_index = (self._next_type_index + 1) % len(self._robot_type_cycle)
        return robot_type

    def create_player(self, player_id: str) -> WizardPlayer:
   
        if player_id in self.respawn_cooldowns:
            time_since_death = time.time() - self.respawn_cooldowns[player_id]
            
            if time_since_death < self.respawn_delay:
                remaining = self.respawn_delay - time_since_death
                return None
            else:
                del self.respawn_cooldowns[player_id]
                
        start_x = random.randint(265, constants.MAP_WIDTH)
        start_y = random.randint(95, constants.MAP_HEIGHT)
        robot_type = self._pick_next_robot_type()

        player = WizardPlayer(player_id, robot_type, start_x, start_y)
        self.players[player_id] = player
        return player

    def remove_player(self, player_id: str, reason: str = "unknown") -> None:

        if player_id in self.players:
            del self.players[player_id]
            
            if reason == "death":
                self.respawn_cooldowns[player_id] = time.time()
                print(f"[PlayerManager] Jugador eliminado por muerte: {player_id} (cooldown: {self.respawn_delay}s)")
            else:
                print(f"[PlayerManager] Jugador eliminado ({reason}): {player_id}")

    def get_player(self, player_id: str) -> Optional[WizardPlayer]:
        return self.players.get(player_id)

    def get_all_players(self) -> List[WizardPlayer]:
        return list(self.players.values())
    
    def update_player_activity(self, player_id: str) -> None:
 
        player = self.get_player(player_id)
        if player:
            player.last_activity = time.time()

    def remove_dead_players(self) -> List[str]:
    
        dead_players = []
        
        for player_id, player in list(self.players.items()):
            if player.hp <= 0:
                dead_players.append(player_id)
                self.remove_player(player_id, reason="death")  
        
        return dead_players
    
    def remove_disconnected_players(self) -> List[str]:
   
        current_time = time.time()
        disconnected_players = []
        
        for player_id, player in list(self.players.items()):
            time_since_activity = current_time - player.last_activity
            
            if time_since_activity > self.disconnect_timeout:
                disconnected_players.append(player_id)
                self.remove_player(player_id, reason="disconnect")  
                
                if player_id in self.respawn_cooldowns:
                    del self.respawn_cooldowns[player_id]
        
        return disconnected_players



def update_player_movement(player: WizardPlayer, inputs: dict, delta_time: float) -> None:
 
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

    if dx != 0.0 and dy != 0.0:
        factor = 1.0 / math.sqrt(2.0)
        dx *= factor
        dy *= factor

    player.x += dx * player.speed * delta_time
    player.y += dy * player.speed * delta_time

    player.x = max(constants.GAME_AREA_MIN_X, min(player.x, constants.GAME_AREA_MAX_X))
    player.y = max(constants.GAME_AREA_MIN_Y, min(player.y, constants.GAME_AREA_MAX_Y))


def update_player_rotation(player: WizardPlayer, inputs: dict) -> None:

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
    update_player_movement(player, inputs, delta_time)
    update_player_rotation(player, inputs)

