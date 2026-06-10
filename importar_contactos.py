import sqlite3
import csv

# Encodings comunes que pueden venir de Excel/Windows
encodings = ["utf-8", "latin-1", "cp1252"]

with sqlite3.connect("app/data/tracking.db") as conn:
    cursor = conn.cursor()

    for enc in encodings:
        try:
            with open("contactos.csv", newline='', encoding=enc) as csvfile:
                reader = csv.DictReader(csvfile)

                inserted = 0
                for row in reader:
                    nombre = row.get("nombre")
                    correo = row.get("correo")
                    telefono = row.get("telefono")
                    direccion = row.get("direccion")
                    rubro = row.get("rubro")

                    # Solo insertamos si hay correo válido
                    if correo and correo.strip():
                        cursor.execute("""
                        INSERT INTO contactos (nombre, correo, telefono, direccion, rubro)
                        VALUES (?, ?, ?, ?, ?)
                        """, (nombre, correo.strip(), telefono, direccion, rubro))
                        inserted += 1

                conn.commit()
                print(f"✅ Archivo leído con encoding {enc}. Registros insertados: {inserted}")
                break  # Si funcionó, salimos del loop
        except Exception as e:
            print(f"❌ Error con encoding {enc}: {e}")

