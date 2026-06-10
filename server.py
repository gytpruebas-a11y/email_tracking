from fastapi import FastAPI, Request, Response
import sqlite3
from datetime import datetime

app = FastAPI()

def registrar_apertura(contacto_id, ip):
    with sqlite3.connect("app/data/tracking.db") as conn:
        cursor = conn.cursor()
        fecha = datetime.now().isoformat()
        cursor.execute("INSERT INTO aperturas (contacto_id, fecha, ip) VALUES (?, ?, ?)",
                       (contacto_id, fecha, ip))
        conn.commit()

@app.get("/open/{contacto_id}")
async def open(contacto_id: int, request: Request):
    ip = request.client.host
    registrar_apertura(contacto_id, ip)

    # Pixel transparente GIF 1x1
    pixel = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00' \
            b'\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,' \
            b'\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02' \
            b'D\x01\x00;'

    return Response(content=pixel, media_type="image/gif")
