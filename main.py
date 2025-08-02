from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
import mysql.connector

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de registro!"}

@app.post("/register")
async def register_user(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Faltan campos"}

    if len(password) < 6:
        return {"message": "La contraseña debe tener más de 6 caracteres"}

    hashed_password = pwd_context.hash(password)

    conn = mysql.connector.connect(user='nicolas_morales', password='1234567890',
                                   host='localhost', database='mybd')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE Email=%s", (email,))
    if cursor.fetchone():
        return {"message": "El usuario ya está registrado"}
    
    cursor.execute("INSERT INTO Users (Email, Password) VALUES (%s, %s)", (email, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Usuario registrado exitosamente"}
