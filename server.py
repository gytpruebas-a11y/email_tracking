from fastapi import FastAPI, Request, Response, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3
import csv
import io
import os
from datetime import datetime

IMPORT_TOKEN = os.getenv("IMPORT_TOKEN", "test123")

DB_PATH = "app/data/tracking.db"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
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


init_db()



@app.get("/open/{email:path}")
async def open(email: str, request: Request):
    ip = request.headers.get("X-Forwarded-For", request.client.host)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM contactos WHERE correo = ?", (email.strip(),))
        row = cursor.fetchone()
        if row:
            contacto_id = row[0]
            fecha = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO aperturas (contacto_id, fecha, ip) VALUES (?, ?, ?)",
                (contacto_id, fecha, ip)
            )
            conn.commit()

    pixel = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00' \
            b'\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,' \
            b'\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02' \
            b'D\x01\x00;'

    return Response(content=pixel, media_type="image/gif")


@app.post("/api/importar")
async def importar_contactos(token: str, file: UploadFile = File(...)):
    if token != IMPORT_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")

    content = await file.read()
    text = None
    for enc in ["utf-8", "latin-1", "cp1252"]:
        try:
            text = content.decode(enc)
            break
        except Exception:
            continue

    if text is None:
        raise HTTPException(status_code=400, detail="No se pudo decodificar el archivo")

    lines = text.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1].replace('""', '"')
        cleaned.append(line)
    reader = csv.DictReader(io.StringIO('\n'.join(cleaned)))
    insertados = 0
    omitidos = 0

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for row in reader:
            correo = (row.get("correo") or "").strip()
            if not correo:
                omitidos += 1
                continue
            cursor.execute("SELECT id FROM contactos WHERE correo = ?", (correo,))
            if cursor.fetchone():
                omitidos += 1
                continue
            cursor.execute(
                "INSERT INTO contactos (nombre, correo, telefono, direccion, rubro) VALUES (?, ?, ?, ?, ?)",
                (row.get("nombre"), correo, row.get("telefono"), row.get("direccion"), row.get("rubro"))
            )
            insertados += 1
        conn.commit()

    return {"insertados": insertados, "omitidos": omitidos}


@app.get("/api/aperturas")
async def get_aperturas():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nombre, c.correo, COUNT(a.id) AS total_aperturas
            FROM contactos c
            LEFT JOIN aperturas a ON c.id = a.contacto_id
            GROUP BY c.id, c.nombre, c.correo
            ORDER BY total_aperturas DESC
        """)
        rows = cursor.fetchall()
        return [{"nombre": row[0], "correo": row[1], "total_aperturas": row[2]} for row in rows]


if os.path.isdir("frontend/build"):
    app.mount("/", StaticFiles(directory="frontend/build", html=True), name="frontend")
