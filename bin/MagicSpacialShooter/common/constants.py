


MAP_WIDTH = 1010
MAP_HEIGHT = 620

PLAYER_WIDTH = 48
PLAYER_HEIGHT = 48
PLAYER_RADIUS = 32
RESPAWN_DELAY = 2.0

GAME_AREA_MIN_X = 265.0
GAME_AREA_MAX_X = 1010.0
GAME_AREA_MIN_Y = 95.0
GAME_AREA_MAX_Y = 630.0

POWERUP_SPEED = 'speed'
POWERUP_HEALTH = 'health'
POWERUP_DAMAGE = 'damage'
POWERUP_SHIELD = 'shield'

GAME_LOBBY = 'lobby'
GAME_PLAYING = 'playing'
GAME_FINISHED = 'finished'

BULLET_DAMAGE = 10
BULLET_RADIUS = 16
BULLET_SPEED = 400
AIM_SPEED = 0.1
BULLET_LIFETIME = 3.0
PLAYER_MAX_HEALTH = 100


ROBOT_TYPES = {
    "scout": {
        "max_hp": 80,
        "speed": 320.0,
        "damage": 25,
        "color": "CYAN",      
    },
    "tank": {
        "max_hp": 140,
        "speed": 260.0,
        "damage": 10,
        "color": "ORANGE",
    },
    "sniper": {
        "max_hp": 60,
        "speed": 360.0,
        "damage": 40,
        "color": "PURPLE",
    },
    "medic": {
        "max_hp": 100,
        "speed": 300.0,
        "damage": 20,
        "color": "GREEN",
    },
}

DEFAULT_ROBOT_TYPE = "scout"
