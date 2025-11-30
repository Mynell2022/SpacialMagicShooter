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
BULLET_SPEED = 400
BULLET_LIFETIME = 3.0
PLAYER_MAX_HEALTH = 100

# Tipos de robots disponibles en el juego.
# Cada tipo define HP, velocidad y un "color" lógico para usar en el cliente.
ROBOT_TYPES = {
    "scout": {
        "max_hp": 80,
        "speed": 260.0,
        "color": "CYAN",      # Cliente puede mapear esto a un color real
    },
    "tank": {
        "max_hp": 150,
        "speed": 160.0,
        "color": "ORANGE",
    },
    "sniper": {
        "max_hp": 90,
        "speed": 220.0,
        "color": "PURPLE",
    },
    "medic": {
        "max_hp": 100,
        "speed": 200.0,
        "color": "GREEN",
    },
}

# Tipo de robot por defecto si algo falla
DEFAULT_ROBOT_TYPE = "scout"
