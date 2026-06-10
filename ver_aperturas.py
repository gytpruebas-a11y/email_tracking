import sqlite3

conn = sqlite3.connect("tracking.db")
cursor = conn.cursor()

cursor.execute("""
SELECT c.nombre, c.correo, COUNT(a.id) AS total_aperturas
FROM contactos c
LEFT JOIN aperturas a ON c.id = a.contacto_id
GROUP BY c.id, c.nombre, c.correo
ORDER BY total_aperturas DESC
""")

rows = cursor.fetchall()

for row in rows:
    print(f"Nombre: {row[0]} | Correo: {row[1]} | Aperturas: {row[2]}")

conn.close()
