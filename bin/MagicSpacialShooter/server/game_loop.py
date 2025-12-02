import time
from server.input_receiver import InputReceiver
from server.broadcaster import StateBroadcaster
from server.player_manager import PlayerManager, update_player_state

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
            # (Por ahora solo movimiento de jugadores en process_inputs, 
            #  pero aquí irían colisiones de proyectiles, etc.)

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

    def _broadcast_state(self):
        """
        Recopila el estado de todos los jugadores y lo envía a la red.
        """
        players_list = self.player_manager.get_all_players()
        
        # Construir snapshot del mundo
        # Formato: {"players": [ {data_jugador}, ... ], "timestamp": ...}
        state_snapshot = {
            "players": [p.to_dict() for p in players_list],
            "timestamp": time.time()
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
