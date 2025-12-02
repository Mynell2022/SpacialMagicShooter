# client/client_game_loop.py
"""
Game Loop del cliente - por el momento solo maneja límites del mapa
"""
from config import *

class ClientGameLoop:
    """Maneja verificación de límites del mapa"""
    
    def __init__(self, state_store, player_id):
        """
        Args:
            state_store: Referencia al LocalStateStore
            player_id: ID del jugador local
        """
        self.state_store = state_store
        self.player_id = player_id
    
    def update(self, delta_time):
        """
        Actualización local cada frame
        SOLO verifica límites del mapa
        
        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """
        # Obtener estado actual
        state = self.state_store.get_state()
        
        # Verificar límites del mapa para todos los jugadores
        self._check_map_boundaries(state)
    
    def _check_map_boundaries(self, state):
        """
        Verifica que los jugadores estén dentro de los límites del mapa
        Esta es una verificación local - el servidor tiene la autoridad final
        
        Args:
            state: Estado actual del juego
        """
        players = state.get('players', [])
        
        # Si players viene como lista (formato del servidor)
        if isinstance(players, list):
            for player_data in players:
                # Obtener posición actual
                x = player_data.get('x', 0)
                y = player_data.get('y', 0)
                
                # Límites del mapa (coordenadas relativas al mapa, no a la pantalla)
                min_x = PLAYER_SIZE / 2
                max_x = MAP_WIDTH - PLAYER_SIZE / 2
                min_y = PLAYER_SIZE / 2
                max_y = MAP_HEIGHT - PLAYER_SIZE / 2
                
                # Clamping (ajustar a límites)
                clamped_x = max(min_x, min(x, max_x))
                clamped_y = max(min_y, min(y, max_y))
                
                # Si hubo cambio, actualizar localmente
                # (el servidor enviará la posición correcta después)
                if clamped_x != x or clamped_y != y:
                    player_data['x'] = clamped_x
                    player_data['y'] = clamped_y
    
    def is_position_in_map(self, x, y):
        """
        Verifica si una posición está dentro del mapa
        
        Args:
            x, y: Coordenadas a verificar (relativas al mapa)
        
        Returns:
            True si está dentro, False si no
        """
        return (0 <= x <= MAP_WIDTH and 0 <= y <= MAP_HEIGHT)