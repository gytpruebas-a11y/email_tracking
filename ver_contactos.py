import sqlite3

conn = sqlite3.connect("app/data/tracking.db")
cursor = conn.cursor()

cursor.execute("SELECT id, nombre, correo, telefono, direccion, rubro FROM contactos")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
