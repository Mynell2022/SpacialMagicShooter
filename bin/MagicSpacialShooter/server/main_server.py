import sys
import os

# Ajustar el path para permitir imports desde 'common' y otros módulos hermanos
# Se asume que este script está en bin/MagicSpacialShooter/server/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) # bin/MagicSpacialShooter
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from server.game_loop import GameServer

def main():
    """
    Punto de entrada para ejecutar el Servidor Central.
    """
    server = GameServer()
    
    try:
        # start() bloquea el hilo principal con el bucle del juego
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
