import math
from common import constants

class Bullet:
    def __init__(self, bullet_id, owner_id, x, y, angle_deg):
        self.id = bullet_id
        self.owner_id = owner_id
        self.x = x
        self.y = y
        self.angle = -angle_deg
        self.lifetime = constants.BULLET_LIFETIME
        
        # Calcular velocidad basada en el ángulo
        angle_rad = math.radians(angle_deg)
        self.vx = math.cos(angle_rad) * constants.BULLET_SPEED
        self.vy = math.sin(angle_rad) * constants.BULLET_SPEED

    def update(self, delta_time):
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        self.lifetime -= delta_time

    def to_dict(self):
        return {
            "id": self.id,
            "owner": self.owner_id,
            "x": self.x,
            "y": self.y,
            "angle": self.angle
        }

class BulletManager:
    def __init__(self):
        self.bullets = []
        self.bullet_counter = 0

    def create_bullet(self, owner_id, x, y, angle):
        self.bullet_counter += 1
        bullet_id = f"{owner_id}_{self.bullet_counter}"
        bullet = Bullet(bullet_id, owner_id, x, y, angle)
        self.bullets.append(bullet)
        return bullet

    def update(self, delta_time):
        # Actualizar posición y vida
        for bullet in self.bullets:
            bullet.update(delta_time)
        
        # Eliminar balas muertas o fuera del área de juego
        self.bullets = [
            b for b in self.bullets 
            if b.lifetime > 0 
            and constants.GAME_AREA_MIN_X <= b.x <= constants.GAME_AREA_MAX_X 
            and constants.GAME_AREA_MIN_Y <= b.y <= constants.GAME_AREA_MAX_Y
        ]

    def get_all_bullets(self):
        return self.bullets
