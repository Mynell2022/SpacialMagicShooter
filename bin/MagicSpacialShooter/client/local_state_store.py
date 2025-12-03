# client/local_state_store.py

import threading
import copy
import json
from datetime import datetime

class LocalStateStore:

    
    def __init__(self):
        self.lock = threading.Lock()
        self.current_state = {
            'players': {},
            'bullets': [],
            'powerups': [],
            'scores': {},
            'game_time': 0
        }
        self.state_history = [] 
        self.max_history = 3     
    
    def update_state(self, new_state):

        with self.lock:
            if self.current_state.get('players'):  
                self.state_history.append(copy.deepcopy(self.current_state))
                
                if len(self.state_history) > self.max_history:
                    self.state_history.pop(0)
            
            self.current_state = new_state
    
    def get_state(self):
 
        with self.lock:
            return copy.deepcopy(self.current_state)
    
    def get_state_history(self):
 
        with self.lock:
            return copy.deepcopy(self.state_history)
    
    def save_to_json(self, filename="game_state.json"):

        with self.lock:
            try:
                state_with_metadata = {
                    'timestamp': datetime.now().isoformat(),
                    'state': self.current_state
                }
                with open(filename, 'w') as f:
                    json.dump(state_with_metadata, f, indent=2)
                print(f"Estado guardado en {filename}")
            except Exception as e:
                print(f"Error guardando estado: {e}")
    
    def load_from_json(self, filename="game_state.json"):

        with self.lock:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                    self.current_state = data.get('state', self.current_state)
                print(f"Estado cargado desde {filename}")
            except FileNotFoundError:
                print(f"Archivo {filename} no encontrado")
            except Exception as e:
                print(f"Error cargando estado: {e}")
    
    def clear_state(self):
        with self.lock:
            self.current_state = {
                'players': {},
                'bullets': [],
                'powerups': [],
                'scores': {},
                'game_time': 0
            }
            self.state_history.clear()
            print("Estado limpiado")
