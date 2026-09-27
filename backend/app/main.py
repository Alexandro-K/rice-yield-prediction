from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db
from app.services.gee_pipeline import init_gee
from app.services.model_service import load_model
from app.api.routes_predict import router as predict_router
from app.api.routes_map import router as map_router

app = FastAPI(title="Prediksi Produksi Padi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rice-yield-prediction-psi.vercel.app/", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(predict_router, prefix="/api")
app.include_router(map_router, prefix="/api")

from app.scripts.seed_database import seed

@app.on_event("startup")
def on_startup():
    init_db()
    seed()
    init_gee()
    load_model()
    print("Aplikasi siap: database, GEE, dan model TabPFN sudah diinisialisasi.")

@app.get("/")
def health_check():
    return {"status": "ok"}