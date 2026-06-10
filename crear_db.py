import sqlite3

conn = sqlite3.connect("tracking.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contactos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    correo TEXT,
    telefono TEXT,
    direccion TEXT,
    rubro TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS aperturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contacto_id INTEGER,
    fecha TEXT,
    ip TEXT,
    FOREIGN KEY(contacto_id) REFERENCES contactos(id)
)
""")

conn.commit()
conn.close()

