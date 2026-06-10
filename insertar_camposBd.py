import sqlite3

with sqlite3.connect("app/data/tracking.db") as conn:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contactos (nombre, correo, telefono, direccion, rubro)
        VALUES (?, ?, ?, ?, ?)
    """, ("lester", "lesterpinedaperez@gmail.com", "98174977", "Casa", "si"))
    conn.commit()
    print("Campos insertados")
