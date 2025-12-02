# common/constants.py

"""
AQUI CUALQUIER COSA SE PONEN LAS : Constantes globales del proyecto

En este archivo definimos:
- Dimensiones del mapa.
- Atributos base de los robots (jugadores).
"""

# Dimensiones lógicas del mapa (coherentes con la ventana del cliente)
MAP_WIDTH = 800
MAP_HEIGHT = 600

# Tamaño aproximado del sprite del robot (para colisiones / centrado)
PLAYER_WIDTH = 48
PLAYER_HEIGHT = 48
PLAYER_RADIUS = 32

# Límites del área de juego (zona jugable en pantalla)
GAME_AREA_MIN_X = 265.0
GAME_AREA_MAX_X = 1010.0
GAME_AREA_MIN_Y = 95.0
GAME_AREA_MAX_Y = 630.0

# Tipos de power-ups
POWERUP_SPEED = 'speed'
POWERUP_HEALTH = 'health'
POWERUP_DAMAGE = 'damage'
POWERUP_SHIELD = 'shield'

# Estados del juego
GAME_LOBBY = 'lobby'
GAME_PLAYING = 'playing'
GAME_FINISHED = 'finished'

# Física
BULLET_DAMAGE = 10
BULLET_RADIUS = 16
BULLET_SPEED = 400
BULLET_LIFETIME = 3.0
PLAYER_MAX_HEALTH = 100

# Tipos de robots disponibles en el juego.
# Cada tipo define HP, velocidad y un "color" lógico para usar en el cliente.
ROBOT_TYPES = {
    "scout": {
        "max_hp": 80,
        "speed": 220.0,
        "damage": 25,
        "color": "CYAN",      # Cliente puede mapear esto a un color real
    },
    "tank": {
        "max_hp": 140,
        "speed": 160.0,
        "damage": 10,
        "color": "ORANGE",
    },
    "sniper": {
        "max_hp": 60,
        "speed": 260.0,
        "damage": 40,
        "color": "PURPLE",
    },
    "medic": {
        "max_hp": 100,
        "speed": 200.0,
        "damage": 20,
        "color": "GREEN",
    },
}

# Tipo de robot por defecto si algo falla
DEFAULT_ROBOT_TYPE = "scout"
