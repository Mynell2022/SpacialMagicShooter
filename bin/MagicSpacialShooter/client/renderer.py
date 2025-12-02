# client/renderer.py
"""
Módulo de renderizado - Dibuja el mapa, objetos y jugadores
"""
import os
import arcade
from config import *

class Renderer:
    def __init__(self):
        """Inicializa el renderer con sus estructuras visuales"""
        # Sprites para diferentes tipos de power-ups
        self.powerup_colors = {
            'speed': arcade.color.YELLOW,
            'health': arcade.color.GREEN,
            'damage': arcade.color.RED,
            'shield': arcade.color.BLUE
        }
        
        # Resolve path to resources relative to this script
        base_path = os.path.dirname(os.path.abspath(__file__))
        res_path = os.path.join(base_path, "resources")

        self.enemy_stay = arcade.load_texture(os.path.join(res_path, "enemy_stay.png"))
        self.player_stay = arcade.load_texture(os.path.join(res_path, "player_stay.png"))

        self.enemy_right = arcade.load_texture(os.path.join(res_path, "enemy_right.png"))
        self.player_right = arcade.load_texture(os.path.join(res_path, "player_right.png"))
        self.enemy_left = arcade.load_texture(os.path.join(res_path, "enemy_left.png"))
        self.player_left = arcade.load_texture(os.path.join(res_path, "player_left.png"))

        self.enemy_up = arcade.load_texture(os.path.join(res_path, "enemy_up.png"))
        self.player_up = arcade.load_texture(os.path.join(res_path, "player_up.png"))
        self.enemy_down = arcade.load_texture(os.path.join(res_path, "enemy_down.png"))
        self.player_down = arcade.load_texture(os.path.join(res_path, "player_down.png"))

        self.screen_texture = arcade.load_texture(os.path.join(res_path, "SpacialMagicScreen.png"))
        self.player_list = arcade.SpriteList()
        
    def draw_background(self):
        """Dibuja el fondo del juego (espacio)"""
        arcade.set_background_color(BACKGROUND_COLOR)

        sprite = arcade.Sprite()
        sprite.texture = self.screen_texture
        sprite.center_x = 640
        sprite.center_y = 360
        sprite.angle = 0
        sprite.scale = 1

        # Agregar a la lista
        temp = arcade.SpriteList()
        temp.append(sprite)
        temp.draw()
        """
        # Dibujar áreas de UI (opciones y stats)
        # Área izquierda (opciones)
        arcade.draw_lrbt_rectangle_filled(
            0, MAP_X_OFFSET, 0, SCREEN_HEIGHT,
            UI_BACKGROUND_COLOR
        )
        
        # Área derecha (stats)
        arcade.draw_lrbt_rectangle_filled(
            MAP_X_OFFSET + MAP_WIDTH, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            UI_BACKGROUND_COLOR
        )
        
        # Área superior e inferior
        arcade.draw_lrbt_rectangle_filled(
            MAP_X_OFFSET, MAP_X_OFFSET + MAP_WIDTH, 0, MAP_Y_OFFSET,
            UI_BACKGROUND_COLOR
        )]

        arcade.draw_lrbt_rectangle_filled(
            MAP_X_OFFSET, MAP_X_OFFSET + MAP_WIDTH, 
            MAP_Y_OFFSET + MAP_HEIGHT, SCREEN_HEIGHT,
            UI_BACKGROUND_COLOR
        )
        
        # Dibujar estrellas de fondo en el área del mapa
        import random
        random.seed(42)  # Seed fijo para que las estrellas siempre estén en el mismo lugar
        for _ in range(100):
            x = MAP_X_OFFSET + random.randint(0, MAP_WIDTH)
            y = MAP_Y_OFFSET + random.randint(0, MAP_HEIGHT)
            size = random.randint(1, 2)
            brightness = random.randint(150, 255)
            arcade.draw_circle_filled(x, y, size, (brightness, brightness, brightness))"""
    
    def draw_map_borders(self):
        """Dibuja los bordes del mapa"""
        # Borde izquierdo
        arcade.draw_lrbt_rectangle_filled(
            MAP_X_OFFSET - MAP_BORDER_THICKNESS,
            MAP_X_OFFSET,
            MAP_Y_OFFSET,
            MAP_Y_OFFSET + MAP_HEIGHT,
            MAP_BORDER_COLOR
        )
        
        # Borde derecho
        arcade.draw_lrbt_rectangle_filled(
            MAP_X_OFFSET + MAP_WIDTH,
            MAP_X_OFFSET + MAP_WIDTH + MAP_BORDER_THICKNESS,
            MAP_Y_OFFSET,
            MAP_Y_OFFSET + MAP_HEIGHT,
            MAP_BORDER_COLOR
        )
        
        # Borde superior
        arcade.draw_lrbt_rectangle_filled(
            MAP_X_OFFSET,
            MAP_X_OFFSET + MAP_WIDTH,
            MAP_Y_OFFSET + MAP_HEIGHT,
            MAP_Y_OFFSET + MAP_HEIGHT + MAP_BORDER_THICKNESS,
            MAP_BORDER_COLOR
        )
        
        # Borde inferior
        arcade.draw_lrbt_rectangle_filled(
            MAP_X_OFFSET,
            MAP_X_OFFSET + MAP_WIDTH,
            MAP_Y_OFFSET - MAP_BORDER_THICKNESS,
            MAP_Y_OFFSET,
            MAP_BORDER_COLOR
        )
    
    def draw_powerups(self, powerups):
        """
        Dibuja los power-ups en el mapa
        
        Args:
            powerups: Lista de diccionarios con estructura:
                     {'id': str, 'type': str, 'x': float, 'y': float}
        """
        for powerup in powerups:
            # Obtener posición absoluta en pantalla
            screen_x = MAP_X_OFFSET + powerup['x']
            screen_y = MAP_Y_OFFSET + powerup['y']
            
            # Color según tipo
            color = self.powerup_colors.get(powerup['type'], arcade.color.WHITE)
            
            # Dibujar el power-up como un hexágono
            arcade.draw_polygon_filled([
                (screen_x, screen_y + POWERUP_SIZE),
                (screen_x + POWERUP_SIZE * 0.866, screen_y + POWERUP_SIZE * 0.5),
                (screen_x + POWERUP_SIZE * 0.866, screen_y - POWERUP_SIZE * 0.5),
                (screen_x, screen_y - POWERUP_SIZE),
                (screen_x - POWERUP_SIZE * 0.866, screen_y - POWERUP_SIZE * 0.5),
                (screen_x - POWERUP_SIZE * 0.866, screen_y + POWERUP_SIZE * 0.5),
            ], color)
            
            # Borde del power-up
            arcade.draw_polygon_outline([
                (screen_x, screen_y + POWERUP_SIZE),
                (screen_x + POWERUP_SIZE * 0.866, screen_y + POWERUP_SIZE * 0.5),
                (screen_x + POWERUP_SIZE * 0.866, screen_y - POWERUP_SIZE * 0.5),
                (screen_x, screen_y - POWERUP_SIZE),
                (screen_x - POWERUP_SIZE * 0.866, screen_y - POWERUP_SIZE * 0.5),
                (screen_x - POWERUP_SIZE * 0.866, screen_y + POWERUP_SIZE * 0.5),
            ], arcade.color.WHITE, 2)
    
    def draw_players(self, players, local_player_id):
        """Dibuja los jugadores en el mapa"""

        # Limpia la lista para este frame
        self.player_list.clear()

        # Convertir lista a dict si es necesario (para compatibilidad)
        if isinstance(players, list):
            for player_data in players:
                pid = player_data.get("id", "unknown")
                x = player_data.get("x", 0)
                y = player_data.get("y", 0)
                health = player_data.get("hp", 100)
                direction = player_data.get("position", "stay")

                # Seleccionar textura
                texture = self.player_stay
                if pid == local_player_id:
                    match direction:
                        case "up":
                            texture = self.player_up
                        case "down":
                            texture = self.player_down
                        case "right":
                            texture = self.player_right
                        case "left":
                            texture = self.player_left
                        case "stay":
                            texture = self.player_stay
                else:
                    match direction:
                        case "up":
                            texture = self.enemy_up
                        case "down":
                            texture = self.enemy_down
                        case "right":
                            texture = self.enemy_right
                        case "left":
                            texture = self.enemy_left
                        case "stay":
                            texture = self.enemy_stay
                # Crear sprite del jugador
                sprite = arcade.Sprite()
                sprite.texture = texture
                sprite.center_x = x
                sprite.center_y = y
                sprite.angle = 0
                sprite.scale = 1

                # Agregar a la lista
                self.player_list.append(sprite)

            # === BARRA DE VIDA ===
            bar_width = 4
            bar_height = 30
            bar_offset = 40

            left = x - (bar_height / 2)
            right = x + (bar_height / 2)

            # Extremos verticales → altura pequeña
            bottom = y + bar_offset - (bar_width / 2)
            top = y + bar_offset + (bar_width / 2)


            arcade.draw_lrbt_rectangle_filled(
                left-2,
                right+2,
                bottom-2,
                top+2,
                (41,20,68)
            )
            arcade.draw_lrbt_rectangle_filled(
                left,
                right,
                bottom,
                top,
                arcade.color.GREEN
            )
            arcade.draw_lrbt_rectangle_filled(
                left,
                right-(right-left)*(health/100),
                bottom,
                top,
                arcade.color.RED
            )

        # Finalmente dibujar todos los sprites DE UNA VEZ
        self.player_list.draw()
    
    def draw_bullets(self, bullets):
        """
        Dibuja los proyectiles en el mapa
        
        Args:
            bullets: Lista de diccionarios con {x, y, player_id}
        """
        pass

    def draw_ui(self, game_state, local_player_id):
        """
        Dibuja elementos de la UI (stats, timer, etc)
        
        Args:
            game_state: Estado completo del juego
            local_player_id: ID del jugador local
        """
        # Título del juego
        self.title_text = arcade.Text(
            "MAGIC SPATIAL SHOOTER",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30,
            TEXT_COLOR, 20,
            anchor_x="center",
            bold=True
        )
        
        # Información del jugador local (área derecha)
        if local_player_id in game_state.get('players', {}):
            player = game_state['players'][local_player_id]
            
            stats_x = MAP_X_OFFSET + MAP_WIDTH + 20
            stats_y = SCREEN_HEIGHT - 100
            
            self.stats_title = arcade.Text(
                "YOUR STATS",
                0, 0,   # luego ajustamos la posición al dibujar
                TEXT_COLOR, 16,
                bold=True
            )
            
            self.health_text = arcade.Text(
                f"Health: {player.get('health', 100)}",
                stats_x, stats_y - 30,
                TEXT_COLOR, 12
            )
            
            self.score_text = arcade.Text(
                f"Score: {player.get('score', 0)}",
                stats_x, stats_y - 50,
                TEXT_COLOR, 12
            )
        
        # Puntuaciones (área izquierda)
        scores = game_state.get('scores', {})
        score_y = SCREEN_HEIGHT - 100
        
        self.leaderboard_title = arcade.Text(
            "LEADERBOARD",
            20, SCREEN_HEIGHT - 100,
            TEXT_COLOR, 16,
            bold=True
        )
        
        self.leaderboard_entries = []
        scores = game_state.get('scores', {})
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        score_y = SCREEN_HEIGHT - 100

        for i, (player_id, score) in enumerate(sorted_scores[:5]):
            marker = "►" if player_id == local_player_id else " "
            entry_text = arcade.Text(
                f"{marker} {player_id[:8]}: {score}",
                20, score_y - 30 - (i * 20),
                TEXT_COLOR, 10
            )
            self.leaderboard_entries.append(entry_text)
        
        # Timer
        game_time = game_state.get('game_time', 0)
        self.timer_text = arcade.Text(
            "Time: 0s",
            SCREEN_WIDTH / 2, 20,
            TEXT_COLOR, 14,
            anchor_x="center"
        )