from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_session
from app.core.config import KABUPATEN_LIST
from app.schemas.predict_schema import PredictRequest, PredictResponse
from app.services.gee_pipeline import extract_monthly_stats_for_kabupaten
from app.services.historis_service import get_last_n_months, insert_new_month
from app.services.feature_engineering import build_feature_row
from app.services.model_service import predict
from app.core.config import FITUR_FINAL

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
def predict_produksi(payload: PredictRequest, db: Session = Depends(get_session)):
    if payload.kabupaten not in KABUPATEN_LIST:
        raise HTTPException(status_code=400, detail=f"Kabupaten '{payload.kabupaten}' tidak dikenali. Pilihan: {KABUPATEN_LIST}")

    historis_df = get_last_n_months(db, payload.kabupaten, payload.tahun, payload.bulan, n=2)
    if len(historis_df) < 2:
        raise HTTPException(
            status_code=422,
            detail="Data historis 2 bulan sebelum periode ini tidak tersedia. Tidak bisa membangun fitur lag/trend."
        )

    stats = extract_monthly_stats_for_kabupaten(payload.kabupaten, payload.tahun, payload.bulan)

    required_keys = ["NDVI_mean", "EVI_mean", "SAVI_mean"]
    missing = [k for k in required_keys if stats.get(k) is None]
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Citra Sentinel-2 tidak cukup jernih/tersedia untuk periode ini. Data hilang: {missing}"
        )

    index_bulan_ini = {k: stats[k] for k in required_keys}

    fitur_row = build_feature_row(
        kabupaten=payload.kabupaten,
        bulan=payload.bulan,
        index_bulan_ini=index_bulan_ini,
        historis_df=historis_df,
    )

    hasil_prediksi = predict(fitur_row)
    fitur_final_digunakan = {k: fitur_row[k] for k in FITUR_FINAL}

    tanggal_bulan_ini = datetime(payload.tahun, payload.bulan, 1)
    insert_new_month(
        db, payload.kabupaten, payload.tahun, payload.bulan, tanggal_bulan_ini,
        ndvi=index_bulan_ini["NDVI_mean"], evi=index_bulan_ini["EVI_mean"], savi=index_bulan_ini["SAVI_mean"],
    )

    return PredictResponse(
        kabupaten=payload.kabupaten,
        tahun=payload.tahun,
        bulan=payload.bulan,
        prediksi_produksi_ton=hasil_prediksi,
        ndvi_mean=index_bulan_ini["NDVI_mean"],
        evi_mean=index_bulan_ini["EVI_mean"],
        savi_mean=index_bulan_ini["SAVI_mean"],
        jumlah_citra=stats.get("n_images", 0),
        fitur_digunakan=fitur_final_digunakan,
    )