# Sistema de Seguridad Inteligente

Este proyecto implementa un sistema de seguridad con reconocimiento facial compuesto por:

- **Backend** FastAPI con almacenamiento en SQLite y modelo de reconocimiento facial entrenable.
- **Frontend** Angular para monitorizar eventos, gestionar usuarios y revisar alertas.
- **Módulos de IA** que generan vectores de características ligeros a partir de las imágenes y calculan coincidencias mediante distancia euclidiana.
- **Firmware IoT** para ESP32-CAM + sensor PIR que captura imágenes y las envía al backend.

## Requisitos

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Entrenamiento del modelo

1. Registra usuarios y sube fotografías desde el frontend o mediante `/faces/enroll`.
2. Ejecuta `python scripts/train_model.py` para generar el modelo.
3. Reinicia el backend (o espera al siguiente arranque) para cargar el modelo entrenado.

### Frontend

```bash
cd frontend/smart-security
npm install
npm start
```

El panel se sirve en `http://localhost:4200` y se comunica con el backend en `http://localhost:8000`.

### IoT

Carga `iot/esp32_cam/main.ino` en tu ESP32-CAM, configurando SSID/Password y la URL del backend.

### Tests

```bash
pytest
```

## Estructura principal

- `app/` código del backend (routers, servicios, IA, WebSocket).
- `frontend/smart-security/` panel Angular.
- `iot/` firmware y documentación de cableado.
- `scripts/` utilidades CLI (seed, entrenamiento).

## Variables de entorno

Crea un archivo `.env` si deseas personalizar:

```
DATABASE_URL=sqlite:///./security.db
SECRET_KEY=tu_clave_super_secreta
FACE_MATCH_THRESHOLD=0.6
```
