import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("tracking.db")
cursor = conn.cursor()

# Borrar todos los registros de la tabla contactos
cursor.execute("DELETE FROM contactos")

# Reiniciar el contador de IDs (autoincremento)
cursor.execute("DELETE FROM sqlite_sequence WHERE name='contactos'")

conn.commit()
conn.close()

print("✅ Todos los contactos fueron eliminados correctamente.")
