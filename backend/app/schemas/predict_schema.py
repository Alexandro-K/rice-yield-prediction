from pydantic import BaseModel
from datetime import datetime


class PredictRequest(BaseModel):
    kabupaten: str
    tahun: int
    bulan: int


class PredictResponse(BaseModel):
    kabupaten: str
    tahun: int
    bulan: int
    prediksi_produksi_ton: float
    ndvi_mean: float
    evi_mean: float
    savi_mean: float
    jumlah_citra: int
    fitur_digunakan: dict