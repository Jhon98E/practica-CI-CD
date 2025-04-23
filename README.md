# Clase 9 – FastAPI + Mockoon demo

Este proyecto muestra un endpoint `POST /create_user` que delega la lógica de negocio a un microservicio de tipos de usuario expuesto en Mockoon.

## Requisitos

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Levantar servicios

1. **Mockoon**  
   - Importa el archivo `mockoon.json` en la aplicación de escritorio o ejecuta:

     ```bash
     docker run -d -p 4000:4000 -v $PWD/mockoon.json:/data/mockoon.json mockoon/cli -d /data/mockoon.json
     ```

2. **API FastAPI**

   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## Pruebas

```bash
pytest -q
```

## Variables de entorno

| Variable       | Descripción                                   | Por defecto                         |
|----------------|-----------------------------------------------|-------------------------------------|
| `SERVER_URL`   | URL del microservicio `user_type`             | `http://localhost:4000/user_type`   |

## Docker Compose

Para levantar todo junto:

```bash
docker compose up --build
```
