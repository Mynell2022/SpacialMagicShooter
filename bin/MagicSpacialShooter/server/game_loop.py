import time
import math
from server.input_receiver import InputReceiver
from server.broadcaster import StateBroadcaster
from server.player_manager import PlayerManager, update_player_state
from server.bullet_manager import BulletManager

class GameServer:
    """
    Clase principal que orquesta el bucle del juego en el servidor.
    Coordina:
    - Recepción de inputs (InputReceiver)
    - Lógica de juego y actualización de entidades (PlayerManager)
    - Difusión de estado (StateBroadcaster)
    """

    def __init__(self):
        # Componentes de red
        self.input_receiver = InputReceiver(port=5555)
        self.broadcaster = StateBroadcaster(port=5556)

        # Gestores de lógica de juego
        self.player_manager = PlayerManager()
        self.bullet_manager = BulletManager()

        # Control de tiempo
        self.target_fps = 60
        self.tick_rate = 1.0 / self.target_fps
        self.running = False

    def start(self):
        """
        Inicia los componentes de red y el bucle principal.
        """
        print("[GameServer] Iniciando servidor...")
        
        # Iniciar hilos de red
        self.input_receiver.start()
        self.broadcaster.start()

        self.running = True
        self._main_loop()

    def _main_loop(self):
        """
        Bucle principal del juego (Game Loop).
        Mantiene un ritmo constante de actualizaciones (tick rate).
        """
        print(f"[GameServer] Bucle iniciado a {self.target_fps} Hz")
        
        last_time = time.perf_counter()

        while self.running:
            current_time = time.perf_counter()
            delta_time = current_time - last_time
            last_time = current_time

            # 1. Procesar Inputs
            self._process_inputs(delta_time)

            # 2. Actualizar Mundo (Física, Colisiones, etc.)
            self.bullet_manager.update(delta_time)

            # 3. Difundir Estado
            self._broadcast_state()

            # Control de Frame Rate (Sleep para no quemar CPU)
            elapsed = time.perf_counter() - current_time
            sleep_time = self.tick_rate - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def _process_inputs(self, delta_time):
        """
        Recupera inputs pendientes y actualiza a los jugadores correspondientes.
        """
        inputs = self.input_receiver.get_pending_inputs()

        for data in inputs:
            # Estructura esperada del input: {"player_id": "...", "inputs": {...}}
            player_id = data.get("player_id")
            input_cmds = data.get("inputs")

            if not player_id or not input_cmds:
                continue

            # Obtener o crear jugador (conexión implícita por ahora)
            player = self.player_manager.get_player(player_id)
            if not player:
                print(f"[GameServer] Nuevo jugador detectado: {player_id}")
                player = self.player_manager.create_player(player_id)

            # Actualizar estado del jugador basado en inputs
            update_player_state(player, input_cmds, delta_time)

            # Manejar disparo
            if input_cmds.get("shoot"):
                now = time.time()
                if now - player.last_shot_time >= 0.5:  # 0.5s cooldown
                    player.last_shot_time = now
                    
                    # Calcular ángulo hacia donde apunta el mouse
                    aim_x = input_cmds.get("aim_x", player.x)
                    aim_y = input_cmds.get("aim_y", player.y)
                    
                    dx = aim_x - player.x
                    dy = aim_y - player.y
                    
                    if dx != 0 or dy != 0:
                        angle = math.degrees(math.atan2(dy, dx))
                        # Crear bala en la dirección del mouse
                        self.bullet_manager.create_bullet(
                            player.id, 
                            player.x, 
                            player.y, 
                            angle
                        )

    def _broadcast_state(self):
        """
        Construye el snapshot del mundo y lo envía a todos los clientes.
        """
        players_list = self.player_manager.get_all_players()

        # Dict {id: data} para que el cliente sea feliz
        players_dict = {p.id: p.to_dict() for p in players_list}

        state_snapshot = {
            "type": "state",
            "players": players_dict, 
            "bullets": [b.to_dict() for b in self.bullet_manager.get_all_bullets()],
            "powerups": [],          
            "scores": {},          
            "game_time": 0,          
        }

        self.broadcaster.broadcast(state_snapshot)


    def stop(self):
        """
        Detiene el servidor y sus componentes.
        """
        self.running = False
        self.input_receiver.stop()
        self.broadcaster.stop()
        print("[GameServer] Servidor detenido.")
