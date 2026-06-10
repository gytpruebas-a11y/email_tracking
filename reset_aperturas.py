import sqlite3

conn = sqlite3.connect("tracking.db")
cursor = conn.cursor()

# Borrar todas las aperturas
cursor.execute("DELETE FROM aperturas")

# Reiniciar el contador de IDs
cursor.execute("DELETE FROM sqlite_sequence WHERE name='aperturas'")

conn.commit()
conn.close()

print("✅ Aperturas reiniciadas correctamente")
