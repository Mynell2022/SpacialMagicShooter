# client/client_game_loop.py



from config import *

class ClientGameLoop:
    
    def __init__(self, state_store, player_id):
     
        self.state_store = state_store
        self.player_id = player_id
    
    def update(self, delta_time):
   
        state = self.state_store.get_state()
        
        self._check_map_boundaries(state)
    
    def _check_map_boundaries(self, state):
  
        players = state.get('players', [])
        
        if isinstance(players, list):
            for player_data in players:
                x = player_data.get('x', 0)
                y = player_data.get('y', 0)
                
                min_x = PLAYER_SIZE / 2
                max_x = MAP_WIDTH - PLAYER_SIZE / 2
                min_y = PLAYER_SIZE / 2
                max_y = MAP_HEIGHT - PLAYER_SIZE / 2
                
                clamped_x = max(min_x, min(x, max_x))
                clamped_y = max(min_y, min(y, max_y))
                

                if clamped_x != x or clamped_y != y:
                    player_data['x'] = clamped_x
                    player_data['y'] = clamped_y
    
    def is_position_in_map(self, x, y):
 
        return (0 <= x <= MAP_WIDTH and 0 <= y <= MAP_HEIGHT)