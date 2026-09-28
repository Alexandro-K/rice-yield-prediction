from typing import Optional
from pydantic import BaseModel


class InterpretRequest(BaseModel):
    kabupaten: str
    tahun: int
    bulan: int
    prediksi_produksi_ton: float
    ndvi_mean: float


class TitikRiwayat(BaseModel):
    tahun: int
    bulan: int
    produksi_ton: float


class InterpretResponse(BaseModel):
    kategori_produksi: str
    batas_kuartil: dict[str, float]
    rata_rata_bulan_sama_ton: Optional[float] = None
    selisih_persen_vs_musiman: Optional[float] = None
    kategori_vegetasi: str
    narasi: str
    riwayat_produksi: list[TitikRiwayat]