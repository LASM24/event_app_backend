import uvicorn
from fastapi import FastAPI
from app.routes import router as main_router
from app.database import engine, Base

app = FastAPI()

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Incluir las rutas definidas en routes.py
app.include_router(main_router)

# Ejecutar el servidor de Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
