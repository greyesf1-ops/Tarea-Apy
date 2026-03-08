# Text  API

Este proyecto implementa un microservicio con FastAPI que analiza texto y devuelve
información estructurada en formato JSON.

## Tecnologías

- Python
- FastAPI
- Pydantic

## Ejecutar el proyecto

1. Crear entorno virtual

python -m venv .venv

2. Activar entorno

Windows:
.venv\Scripts\activate

3. Instalar dependencias

pip install -r requirements.txt

4. Ejecutar la API

uvicorn main:app --reload

La API estará disponible en:

http://127.0.0.1:8000

Documentación interactiva:

http://127.0.0.1:8000/docs

## Endpoint

POST /extract

Body:

{
"text": "texto a analizar",
"domain": "universidad"
}
