from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
import sqlite3
from contextlib import contextmanager

# Initialize FastAPI app
app = FastAPI()

# Setup SQLite database
def init_db():
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (email TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    conn = sqlite3.connect('data/users.db')
    try:
        yield conn
    finally:
        conn.close()
# Initialize database on startup
init_db()

# Existing endpoints


@app.get("/welcome-message")
async def root():
    return {"message": "Welcome to the FastAPI app"}


# Define a Pydantic model for signup
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str

# Define a Pydantic model for login


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Add a new endpoint for user signup


@app.post("/signup")
async def sign_up(user: SignUpRequest):
    with get_db() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
                     (user.email, user.password))
            conn.commit()
            return {"message": "User signed up successfully", "email": user.email}
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Email already registered")

# Add a new endpoint for user login


@app.post("/login")
async def login(user: LoginRequest):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (user.email,))
        result = c.fetchone()
        if result:
            if result[1] == user.password:
                return {"message": "Login successful", "email": user.email}
            raise HTTPException(status_code=400, detail="Incorrect password")
        raise HTTPException(status_code=400, detail="Email not registered")

@app.get("/getAllUsers")
async def get_all_users():
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT email FROM users")                                
        users = c.fetchall()
        return [{"email": user[0]} for user in users]