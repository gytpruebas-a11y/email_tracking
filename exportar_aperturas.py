import sqlite3
import csv

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

with open("aperturas_resumen.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Nombre", "Correo", "Total Aperturas"])
    writer.writerows(rows)

conn.close()

print("✅ Archivo 'aperturas_resumen.csv' generado correctamente.")
