from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from pydantic_settings import BaseSettings
import requests
from typing import Any, Dict, Optional
import os

class Settings(BaseSettings):
    server_url: str = "http://localhost:4000/user_type"

    class Config:
        env_prefix = ""
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

app = FastAPI(title="User creation service", version="1.0.0")

class UserRequest(BaseModel):
    name: str

class APIResponse(BaseModel):
    success: bool
    detail: str
    data: Optional[Dict[str, Any]] = None

def _validate_remote_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Verify that the remote service returned the expected schema."""
    expected_keys = {"name", "code", "state"}
    if not expected_keys.issubset(payload):
        raise ValueError("Respuesta del microservicio con formato inesperado")
    return payload

@app.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=APIResponse)
def create_user(user: UserRequest):
    try:
        response = requests.post(settings.server_url, json={"name": user.name}, timeout=5)
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al comunicarse con la aplicación de tipo de cliente: {exc}"
        ) from exc

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error al comunicarse con la aplicación de tipo de cliente"
        )

    try:
        data = _validate_remote_payload(response.json())
    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Respuesta del microservicio inválida"
        )

    if data.get("state") is True:
        return APIResponse(
            success=True,
            detail="Usuario creado correctamente",
            data=data
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="El usuario está desactivado"
    )
