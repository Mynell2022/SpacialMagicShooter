# ==========================================
# client/local_state_store.py
# ==========================================
import threading
import copy
import json
from datetime import datetime

class LocalStateStore:
    """
    Almacena el estado del juego de forma thread-safe
    """
    
    def __init__(self):
        self.lock = threading.Lock()
        self.current_state = {
            'players': {},
            'bullets': [],
            'powerups': [],
            'scores': {},
            'game_time': 0
        }
        self.state_history = []  # Historial de estados recientes
        self.max_history = 3     # Guardar últimos 3 estados
    
    def update_state(self, new_state):
        """
        Actualiza el estado completo del juego
        Thread-safe para que el Net I/O Thread pueda escribir
        mientras el Renderer lee
        
        Args:
            new_state: Nuevo estado del juego
        """
        with self.lock:
            # Guardar estado anterior en historial
            if self.current_state.get('players'):  # Solo si hay datos válidos
                self.state_history.append(copy.deepcopy(self.current_state))
                
                # Mantener solo los últimos N estados
                if len(self.state_history) > self.max_history:
                    self.state_history.pop(0)
            
            # Actualizar al nuevo estado
            self.current_state = new_state
    
    def get_state(self):
        """
        Obtiene una copia del estado actual
        Thread-safe para que el Renderer pueda leer sin problemas
        
        Returns:
            Copia profunda del estado actual
        """
        with self.lock:
            return copy.deepcopy(self.current_state)
    
    def get_state_history(self):
        """
        Obtiene el historial de estados (útil para interpolación)
        
        Returns:
            Lista de estados anteriores
        """
        with self.lock:
            return copy.deepcopy(self.state_history)
    
    def save_to_json(self, filename="game_state.json"):
        """
        Guarda el estado actual a un archivo JSON
        Útil para debugging o persistencia
        
        Args:
            filename: Nombre del archivo donde guardar
        """
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
        """
        Carga el estado desde un archivo JSON
        
        Args:
            filename: Nombre del archivo a cargar
        """
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
        """Limpia el estado actual (útil para reset)"""
        with self.lock:
            self.current_state = {
                'players': {},
                'bullets': [],
                'powerups': [],
                'scores': {},
                'game_time': 0
            }
            self.state_history.clear()
            print("🗑️  Estado limpiado")
