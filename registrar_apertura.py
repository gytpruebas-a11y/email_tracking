import sqlite3
from datetime import datetime

def registrar_apertura(contacto_id, ip):
    # Conexión a la base
    with sqlite3.connect("app/data/tracking.db") as conn:
        cursor = conn.cursor()

        # Fecha y hora actual en formato ISO
        fecha = datetime.now().isoformat()

        # Insertar la apertura
        cursor.execute("""
        INSERT INTO aperturas (contacto_id, fecha, ip)
        VALUES (?, ?, ?)
        """, (contacto_id, fecha, ip))

        conn.commit()

# Ejemplo de uso manual
if __name__ == "__main__":
    # Simulamos que el contacto con id=1 abrió el correo desde la IP 192.168.0.10
    registrar_apertura(1, "192.168.0.10")
    print("Apertura registrada correctamente.")
