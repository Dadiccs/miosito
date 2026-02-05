import psutil
import json
import time
import os
import platform
import socket

def get_system_data():
    battery = psutil.sensors_battery()
    
    # Controllo Wi-Fi (Nome della rete)
    wifi_name = "DISCONNECTED"
    try:
        # Metodo rapido per vedere se c'è connessione internet
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        wifi_name = "CONNECTED" # In Python standard è difficile leggere il nome SSID esatto senza permessi admin
    except:
        pass

    # Spazio Disco
    disk = psutil.disk_usage('/')
    
    data = {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "batt": battery.percent if battery else 100,
        "plugged": battery.power_plugged if battery else True,
        "ram_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "uptime": round(time.time() - psutil.boot_time()),
        "disk_free": round(disk.free / (1024**3), 1),
        "wifi": wifi_name,
        "os_version": platform.release(),
        "proc_count": len(psutil.pids())
    }
    return data

try:
    while True:
        stats = get_system_data()
        with open('dati_sistema.json', 'w') as f:
            json.dump(stats, f)
        time.sleep(1) 
except KeyboardInterrupt:
    print("\nMonitoraggio terminato.")