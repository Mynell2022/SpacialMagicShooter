# client/config.py
"""
Configuración del cliente - Parámetros visuales y de red
"""

# === VENTANA Y PANTALLA ===
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Magic Spatial Shooter"

# === ÁREA DEL MAPA ===
MAP_WIDTH = 800  # 4:3 ratio
MAP_HEIGHT = 600
MAP_X_OFFSET = 240  # Centra el mapa (deja 240px a la izq para opciones, 240px a la der para stats)
MAP_Y_OFFSET = 60   # Centra verticalmente

# === LÍMITES DEL MAPA ===
MAP_BORDER_THICKNESS = 5
MAP_BORDER_COLOR = (100, 100, 255)

# === JUGADORES ===
PLAYER_SIZE = 32
PLAYER_SPEED = 200  # pixels por segundo

# === POWER-UPS / OBJETOS ===
POWERUP_SIZE = 24
POWERUP_SPAWN_COUNT = 5  # Cantidad inicial de power-ups en el mapa

SERVER_IP = "localhost"
SERVER_INPUT_PORT = 5555
SERVER_STATE_PORT = 5556


# === FÍSICA ===
FPS = 60
TICK_RATE = 1/60

# === COLORES ===
BACKGROUND_COLOR = (15, 15, 30)
UI_BACKGROUND_COLOR = (25, 25, 45)
TEXT_COLOR = (255, 255, 255)