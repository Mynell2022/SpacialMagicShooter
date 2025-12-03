# client/renderer.py

import os
import arcade
from config import *

class Renderer:
    def __init__(self):
        self.powerup_colors = {
            'speed': arcade.color.YELLOW,
            'health': arcade.color.GREEN,
            'damage': arcade.color.RED,
            'shield': arcade.color.BLUE
        }
        
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

        self.spell = arcade.load_texture(os.path.join(res_path, "spell.png"))
        self.scoreBoard = arcade.load_texture(os.path.join(res_path, "scoreboard.png"))
        self.board = arcade.SpriteList()

        self.screen_texture = arcade.load_texture(os.path.join(res_path, "SpacialMagicScreen.png"))
        self.player_list = arcade.SpriteList()
        self.spells_list = arcade.SpriteList()

        self.statsButton = None
        
    def draw_background(self):
        arcade.set_background_color(BACKGROUND_COLOR)

        sprite = arcade.Sprite()
        sprite.texture = self.screen_texture
        sprite.center_x = 640
        sprite.center_y = 360
        sprite.angle = 0
        sprite.scale = 1

        temp = arcade.SpriteList()
        temp.append(sprite)
        temp.draw()
    
    def draw_map_borders(self):
        arcade.draw_lrbt_rectangle_filled(
            MAP_X_OFFSET - MAP_BORDER_THICKNESS,
            MAP_X_OFFSET,
            MAP_Y_OFFSET,
            MAP_Y_OFFSET + MAP_HEIGHT,
            MAP_BORDER_COLOR
        )
        
        arcade.draw_lrbt_rectangle_filled(
            MAP_X_OFFSET + MAP_WIDTH,
            MAP_X_OFFSET + MAP_WIDTH + MAP_BORDER_THICKNESS,
            MAP_Y_OFFSET,
            MAP_Y_OFFSET + MAP_HEIGHT,
            MAP_BORDER_COLOR
        )
        
        arcade.draw_lrbt_rectangle_filled(
            MAP_X_OFFSET,
            MAP_X_OFFSET + MAP_WIDTH,
            MAP_Y_OFFSET + MAP_HEIGHT,
            MAP_Y_OFFSET + MAP_HEIGHT + MAP_BORDER_THICKNESS,
            MAP_BORDER_COLOR
        )
        
        arcade.draw_lrbt_rectangle_filled(
            MAP_X_OFFSET,
            MAP_X_OFFSET + MAP_WIDTH,
            MAP_Y_OFFSET - MAP_BORDER_THICKNESS,
            MAP_Y_OFFSET,
            MAP_BORDER_COLOR
        )
    
    def draw_powerups(self, powerups):
 
        for powerup in powerups:
            screen_x = MAP_X_OFFSET + powerup['x']
            screen_y = MAP_Y_OFFSET + powerup['y']
            
            color = self.powerup_colors.get(powerup['type'], arcade.color.WHITE)
            
            arcade.draw_polygon_filled([
                (screen_x, screen_y + POWERUP_SIZE),
                (screen_x + POWERUP_SIZE * 0.866, screen_y + POWERUP_SIZE * 0.5),
                (screen_x + POWERUP_SIZE * 0.866, screen_y - POWERUP_SIZE * 0.5),
                (screen_x, screen_y - POWERUP_SIZE),
                (screen_x - POWERUP_SIZE * 0.866, screen_y - POWERUP_SIZE * 0.5),
                (screen_x - POWERUP_SIZE * 0.866, screen_y + POWERUP_SIZE * 0.5),
            ], color)
            
            arcade.draw_polygon_outline([
                (screen_x, screen_y + POWERUP_SIZE),
                (screen_x + POWERUP_SIZE * 0.866, screen_y + POWERUP_SIZE * 0.5),
                (screen_x + POWERUP_SIZE * 0.866, screen_y - POWERUP_SIZE * 0.5),
                (screen_x, screen_y - POWERUP_SIZE),
                (screen_x - POWERUP_SIZE * 0.866, screen_y - POWERUP_SIZE * 0.5),
                (screen_x - POWERUP_SIZE * 0.866, screen_y + POWERUP_SIZE * 0.5),
            ], arcade.color.WHITE, 2)
    

    def draw_players(self, players, local_player_id):

        self.player_list.clear()

        if isinstance(players, dict):
            iterable = players.values()       
        elif isinstance(players, list):
            iterable = players               
        else:
            return 

        for player_data in iterable:
            pid = player_data.get("id", "unknown")
            x = player_data.get("x", 0)
            y = player_data.get("y", 0)
            health = player_data.get("hp", 100)
            max_hp = player_data.get("max_hp", 100)
            direction = player_data.get("position", "stay")

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
                    case _:
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
                    case _:
                        texture = self.enemy_stay

            sprite = arcade.Sprite()
            sprite.texture = texture
            sprite.center_x = x
            sprite.center_y = y
            sprite.angle = 0
            sprite.scale = 1
            self.player_list.append(sprite)

            if max_hp <= 0:
                max_hp = 1
            health = max(0, min(health, max_hp))
            health_pct = health / max_hp

            bar_width = 4
            bar_height = 30
            bar_offset = 40

            left = x - (bar_height / 2)
            right = x + (bar_height / 2)
            bottom = y + bar_offset - (bar_width / 2)
            top = y + bar_offset + (bar_width / 2)

            arcade.draw_lrbt_rectangle_filled(
                left - 2, right + 2,
                bottom - 2, top + 2,
                (41, 20, 68)
            )

            arcade.draw_lrbt_rectangle_filled(
                left, right,
                bottom, top,
                arcade.color.RED
            )

            green_right = left + (right - left) * health_pct
            arcade.draw_lrbt_rectangle_filled(
                left, green_right,
                bottom, top,
                arcade.color.GREEN
            )

        self.player_list.draw()

        self.player_list.clear()

        if isinstance(players, dict):
            iterable = players.values()     
        elif isinstance(players, list):
            iterable = players                
        else:
            return  

        for player_data in iterable:
            pid = player_data.get("id", "unknown")
            x = player_data.get("x", 0)
            y = player_data.get("y", 0)
            health = player_data.get("hp", 100)
            max_hp = player_data.get("max_hp", 100)
            direction = player_data.get("position", "stay")

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
                    case _:
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
                    case _:
                        texture = self.enemy_stay

            sprite = arcade.Sprite()
            sprite.texture = texture
            sprite.center_x = x
            sprite.center_y = y
            sprite.angle = 0
            sprite.scale = 1
            self.player_list.append(sprite)

  
            if max_hp <= 0:
                max_hp = 1
            health = max(0, min(health, max_hp))
            health_pct = health / max_hp

            bar_width = 4
            bar_height = 30
            bar_offset = 40

            left = x - (bar_height / 2)
            right = x + (bar_height / 2)
            bottom = y + bar_offset - (bar_width / 2)
            top = y + bar_offset + (bar_width / 2)

            arcade.draw_lrbt_rectangle_filled(
                left - 2, right + 2,
                bottom - 2, top + 2,
                (41, 20, 68)
            )

            arcade.draw_lrbt_rectangle_filled(
                left, right,
                bottom, top,
                arcade.color.RED
            )
            cx = left + (right - left) * 0.5
            cy = (top + 5 + top + 10) / 2 
            points = [
                [cx, cy + 4],
                [cx + 4, cy],
                [cx, cy - 4],
                [cx - 4, cy],
            ]
            arcade.draw_polygon_filled(points, getattr(arcade.color, player_data.get("color_tag", "CYAN")))

            green_right = left + (right - left) * health_pct
            arcade.draw_lrbt_rectangle_filled(
                left, green_right,
                bottom, top,
                arcade.color.GREEN
            )

        self.player_list.draw()
        self.board.draw()
        if self.board:
            self.printScoreText(iterable, players.get(local_player_id))
    
    def draw_bullets(self, bullets):
  
        self.spells_list.clear()

        for bullet in bullets:
            if isinstance(bullet, dict):
                x = bullet.get('x', 0)
                y = bullet.get('y', 0)
                angle = bullet.get('angle', 0)
            else:  
                x = bullet[0]
                y = bullet[1]
                angle = bullet[2]     
            sprite = arcade.Sprite()
            sprite.texture = self.spell
            sprite.center_x = x
            sprite.center_y = y
            sprite.angle = angle
            sprite.scale = 1
            self.spells_list.append(sprite)
        
        self.spells_list.draw()

    def draw_ui(self, players, local_player_id):
        """
        Dibuja elementos de la UI (stats, timer, etc)
        
        Args:
            players: jugadores
            local_player_id: ID del jugador local
        """
        # Título del juego
        self.stats_title = arcade.Text(
            "YOUR STATS",
            0, 0,   # luego ajustamos la posición al dibujar
            TEXT_COLOR, 16,
            bold=True
        )

    def showScoreboard(self):
        sprite = arcade.Sprite()
        sprite.texture = self.scoreBoard
        sprite.center_x = 640
        sprite.center_y = 360
        sprite.angle = 0
        sprite.scale = 1
        self.board.append(sprite)
        self.board.draw()

    def printScoreText(self, players, nowPlayer):
        sortPlayers = sorted(players, key=lambda p: p["score"], reverse=True)
        x= 470
        y = 580
        for i in range(0,min(len(sortPlayers), 5)):
            arcade.Text(
                f"User: {sortPlayers[i]['id']} | Score: {sortPlayers[i]['score']}",
                x, y,
                (41, 20, 68),
                25,
                bold=True,
                align= "center"
            ).draw()
            y-=50
        arcade.Text(
            f"{nowPlayer['score']}           {nowPlayer['id']}",
            480, 260,
            (41, 20, 68),
            25,
            bold=True,
            align= "left"
        ).draw()

    def closeScoreboard(self):
        self.board.clear()