# 🎮 Guía de Configuración Multijugador - SpacialMagicShooter

Esta guía explica cómo configurar el juego para probarlo en múltiples computadoras.

---

## 📋 Requisitos Previos

### En TODAS las PCs (Servidor y Clientes):

1. **Python 3.10 o superior** instalado
2. **Git** (para clonar el repositorio)
3. Las siguientes librerías (se instalan automáticamente con requirements.txt):
   - `pyzmq` (comunicación de red)
   - `arcade` (motor gráfico)



## 🌍 Prueba a través de Internet

Si quieren jugar desde diferentes ubicaciones (casas diferentes), necesitan configuración adicional:

### 🖥️ EN LA PC DEL SERVIDOR:

#### Paso 1: Configurar Port Forwarding en el Router

**Para router:**

1. Abrir navegador y entrar a: `http://192.168.31.1`
2. Iniciar sesión con tu contraseña del router
3. Ir a **Configuración Avanzada (Advanced)**
4. Buscar **Reenvío de puertos / Port Forwarding**
5. Crear DOS reglas:

**Regla 1 - Input Port:**
- Nombre: `SpacialMagic_Input`
- Protocolo: `TCP`
- Puerto externo: `5555`
- IP interna: `TU_IP_LOCAL` (ej: 192.168.31.100)
- Puerto interno: `5555`

**Regla 2 - State Port:**
- Nombre: `SpacialMagic_State`
- Protocolo: `TCP`
- Puerto externo: `5556`
- IP interna: `TU_IP_LOCAL` (misma que antes)
- Puerto interno: `5556`

6. **Guardar** y **reiniciar router** (si es necesario)

#### Paso 2: Obtener tu IP pública
```powershell
# Visitar cualquiera de estos sitios desde tu navegador:
# https://www.whatismyip.com/
# https://ipinfo.io/ip

# O ejecutar en PowerShell:
(Invoke-WebRequest -uri "http://ifconfig.me/ip").Content
```

**Anota esta IP pública**, tus compañeros la necesitarán.

#### Paso 3: Iniciar el servidor
```powershell
python server\main_server.py
```

---

### 💻 EN LAS PCs DE LOS CLIENTES (Internet):

#### Configurar la IP pública del servidor

Editar `bin\MagicSpacialShooter\client\config.py`:

```python
# Cambiar a la IP PÚBLICA del servidor:
SERVER_IP = "190.113.110.212"  # ⬅️ Reemplaza con la IP pública real
```

Luego ejecutar:
```powershell
python client\main_client.py
```

---

## 🎮 Controles del Juego

Una vez conectados, los controles son:

- **WASD** o **Flechas**: Movimiento
- **Mouse**: Apuntar
- **Espacio**: Disparar (cuando esté implementado)

---

## 🔧 Solución de Problemas Comunes

### ❌ "ModuleNotFoundError: No module named 'arcade'"
**Solución:** Asegúrate de activar el entorno virtual primero:
```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### ❌ Cliente dice "Error conectando" o no se conecta
**Posibles causas:**

1. **IP incorrecta en config.py**
   - Verificar que `SERVER_IP` sea correcta
   - En Internet debe ser IP pública

2. **Firewall bloqueando**
   - Revisar que Windows Firewall permita los puertos 5555-5556
   - En router, verificar que Port Forwarding esté activo

3. **Servidor no está corriendo**
   - Asegurarse que el servidor esté ejecutándose primero

### ❌ "zmq.error.ZMQError: Address already in use"
**Solución:** Los puertos ya están siendo usados. Cerrar cualquier instancia anterior del servidor:
```powershell
# Ver procesos de Python
Get-Process python

# Matar todos los procesos de Python (cuidado si tienes otros scripts corriendo)
Stop-Process -Name python
```

### ❌ No veo a los otros jugadores moverse
**Posible causa:** 
- El renderizado de jugadores aún está en desarrollo
- Verifica en la consola del servidor que dice "Nuevo jugador detectado"

---

## 📊 Verificación de Conexión

### En el Servidor:
Deberías ver en la consola:
```
[GameServer] Nuevo jugador detectado: abc12345
[GameServer] Nuevo jugador detectado: def67890
```

### En el Cliente:
Deberías ver en la consola:
```
[NetIOThread] Conectado al servidor X.X.X.X
📤 Enviando inputs a puerto 5555
📥 Recibiendo estado desde puerto 5556
```

---

## 📝 Checklist Rápido

### Para el que hospeda (Servidor):
- [ ] Entorno virtual activado
- [ ] IP pública (Internet)
- [ ] Firewall configurado (puertos 5555-5556)
- [ ] Router configurado (solo para Internet)
- [ ] Servidor corriendo: `python server\main_server.py`

### Para los que se conectan (Clientes):
- [ ] Proyecto clonado
- [ ] Dependencias instaladas
- [ ] `SERVER_IP` configurado en `client\config.py`
- [ ] Cliente ejecutado: `python client\main_client.py`

---

## 🆘 ¿Problemas?

Si siguen teniendo problemas:

1. **Verificar conectividad básica:**
   ```powershell
   # Desde PC del cliente, hacer ping a la IP del servidor:
   ping 190.113.110.212
   ```

2. **Revisar que los puertos estén abiertos:**
   - Usar herramientas online como: https://www.yougetsignal.com/tools/open-ports/
   - Probar puertos 5555 y 5556

3. **Logs del servidor:**
   - Revisar lo que imprime el servidor en consola
   - Buscar mensajes de error