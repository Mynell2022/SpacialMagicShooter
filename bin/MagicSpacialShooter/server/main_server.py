import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) 
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from server.game_loop import GameServer

def main():

    server = GameServer()
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[Main] Interrupción de teclado (Ctrl+C) detectada.")
    except Exception as e:
        print(f"[Main] Error fatal: {e}")
    finally:
        print("[Main] Cerrando servidor...")
        server.stop()
        print("[Main] Servidor cerrado correctamente.")

if __name__ == "__main__":
    main()
