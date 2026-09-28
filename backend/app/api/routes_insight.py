from fastapi import APIRouter, HTTPException

from app.schemas.insight_schema import InterpretRequest, InterpretResponse
from app.services import insight_service as svc

router = APIRouter()


@router.post("/interpret", response_model=InterpretResponse)
def interpret_hasil(payload: InterpretRequest):
    if not svc.kabupaten_tersedia(payload.kabupaten):
        raise HTTPException(status_code=400, detail=f"Kabupaten '{payload.kabupaten}' tidak dikenali.")
    if not 1 <= payload.bulan <= 12:
        raise HTTPException(status_code=400, detail="Bulan harus bernilai 1 sampai 12.")

    kategori_prod, batas = svc.klasifikasi_produksi(payload.kabupaten, payload.prediksi_produksi_ton)
    kategori_veg = svc.klasifikasi_vegetasi(payload.ndvi_mean)
    rata_bulan, selisih = svc.bandingkan_musiman(payload.kabupaten, payload.bulan, payload.prediksi_produksi_ton)

    narasi = svc.susun_narasi(
        payload.kabupaten, payload.tahun, payload.bulan,
        payload.prediksi_produksi_ton, payload.ndvi_mean,
        kategori_prod, kategori_veg, rata_bulan, selisih,
    )

    return InterpretResponse(
        kategori_produksi=kategori_prod,
        batas_kuartil=batas,
        rata_rata_bulan_sama_ton=rata_bulan,
        selisih_persen_vs_musiman=selisih,
        kategori_vegetasi=kategori_veg,
        narasi=narasi,
        riwayat_produksi=svc.get_riwayat_produksi(payload.kabupaten),
    )


@router.get("/model-info")
def informasi_model():
    return svc.get_model_insight()