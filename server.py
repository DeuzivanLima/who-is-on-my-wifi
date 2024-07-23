from fastapi import FastAPI
import sqlite3, datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
sqlite_conn = sqlite3.connect("devices.db")
cursor = sqlite_conn.cursor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    devices = cursor.execute("SELECT * FROM device").fetchall()
    return devices
