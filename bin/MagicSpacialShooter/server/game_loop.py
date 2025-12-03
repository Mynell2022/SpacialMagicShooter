import time
import math
from server.input_receiver import InputReceiver
from server.broadcaster import StateBroadcaster
from server.player_manager import PlayerManager, update_player_state
from server.bullet_manager import BulletManager

class GameServer:

    def __init__(self):
        self.input_receiver = InputReceiver(port=5555)
        self.broadcaster = StateBroadcaster(port=5556)

        self.player_manager = PlayerManager()
        self.bullet_manager = BulletManager()

        self.target_fps = 60
        self.tick_rate = 1.0 / self.target_fps
        self.running = False
        
        self.last_cleanup_time = time.time()
        self.cleanup_interval = 1.0  

    def start(self):
     
        print("[GameServer] Iniciando servidor...")
        
        self.input_receiver.start()
        self.broadcaster.start()

        self.running = True
        self._main_loop()

    def _main_loop(self):
  
        print(f"[GameServer] Bucle iniciado a {self.target_fps} Hz")
        
        last_time = time.perf_counter()

        while self.running:
            current_time = time.perf_counter()
            delta_time = current_time - last_time
            last_time = current_time

            self._process_inputs(delta_time)

            self.bullet_manager.handle_collisions(self.player_manager)
            self.bullet_manager.update(delta_time)

            self._cleanup_dead_players()

            self._cleanup_disconnected_players()

            self._broadcast_state()

            elapsed = time.perf_counter() - current_time
            sleep_time = self.tick_rate - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def _process_inputs(self, delta_time):

        inputs = self.input_receiver.get_pending_inputs()

        for data in inputs:
            player_id = data.get("player_id")
            input_cmds = data.get("inputs")

            if not player_id or not input_cmds:
                continue

            player = self.player_manager.get_player(player_id)
            if not player:
                print(f"[GameServer] Nuevo jugador detectado: {player_id}")
                player = self.player_manager.create_player(player_id)
                
                if not player:
                    continue  

            self.player_manager.update_player_activity(player_id)

            update_player_state(player, input_cmds, delta_time)

            if input_cmds.get("shoot"):
                now = time.time()
                if now - player.last_shot_time >= 0.5:  
                    player.last_shot_time = now
                    
                    aim_x = input_cmds.get("aim_x", player.x)
                    aim_y = input_cmds.get("aim_y", player.y)
                    
                    dx = aim_x - player.x
                    dy = aim_y - player.y
                    
                    if dx != 0 or dy != 0:
                        angle = math.degrees(math.atan2(dy, dx))
                        self.bullet_manager.create_bullet(
                            player.id, 
                            player.x, 
                            player.y, 
                            angle
                        )

    def _cleanup_dead_players(self):

        dead_players = self.player_manager.remove_dead_players()
        
    def _cleanup_disconnected_players(self):
     
        current_time = time.time()
        
        if current_time - self.last_cleanup_time >= self.cleanup_interval:
            self.last_cleanup_time = current_time
            
            disconnected_players = self.player_manager.remove_disconnected_players()
            
    def _broadcast_state(self):

        players_list = self.player_manager.get_all_players()

        players_dict = {p.id: p.to_dict() for p in players_list}

        state_snapshot = {
            "type": "state",
            "players": players_dict, 
            "bullets": [b.to_dict() for b in self.bullet_manager.get_all_bullets()],
            "powerups": [],         
            "game_time": 0,          
        }

        self.broadcaster.broadcast(state_snapshot)


    def stop(self):
 
        self.running = False
        self.input_receiver.stop()
        self.broadcaster.stop()
        print("[GameServer] Servidor detenido.")