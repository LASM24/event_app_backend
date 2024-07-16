import uvicorn
from fastapi import FastAPI
from app.routes import router as main_router
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://web-fron-end-my-event-management-platform.vercel.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],  
    allow_headers=["*"],  
)

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Incluir las rutas definidas en routes.py
app.include_router(main_router)

# Ejecutar el servidor de Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
