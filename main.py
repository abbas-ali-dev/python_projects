from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Existing endpoints


@app.get("/welcome-message")
async def root():
    return {"message": "Welcome to the FastAPI app"}

# In-memory database for users
users_db = []


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
    # Check if email already exists
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400, detail="Email already registered")

    # Add the user to the database
    users_db.append({"email": user.email, "password": user.password})
    return {"message": "User signed up successfully", "email": user.email}

# Add a new endpoint for user login


@app.post("/login")
async def login(user: LoginRequest):
    # Check if the user exists
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            # Check if the password matches
            if existing_user["password"] == user.password:
                return {"message": "Login successful", "email": user.email}
            else:
                raise HTTPException(
                    status_code=400, detail="Incorrect password")

    raise HTTPException(status_code=400, detail="Email not registered")
