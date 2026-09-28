import json
from typing import Optional

import pandas as pd

from app.core.config import DATA_DIR

NAMA_BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]

DESKRIPSI_VEGETASI = {
    "Rendah": "yang umumnya mengindikasikan tutupan vegetasi minim, misalnya fase awal tanam atau pascapanen.",
    "Sedang": "yang umumnya mengindikasikan tanaman pada fase pertumbuhan.",
    "Tinggi": "yang umumnya mengindikasikan tutupan vegetasi lebat, sejalan dengan fase pertumbuhan vegetatif yang baik.",
}

_cache = {}


def _load_data() -> dict:
    if not _cache:
        with open(DATA_DIR / "produksi_stats.json") as f:
            _cache["stats"] = json.load(f)
        _cache["riwayat"] = pd.read_csv(DATA_DIR / "produksi_historis.csv")
        with open(DATA_DIR / "model_insight.json") as f:
            _cache["model_insight"] = json.load(f)
    return _cache


def _format_angka(nilai: float, desimal: int = 2) -> str:
    teks = f"{nilai:,.{desimal}f}"
    return teks.replace(",", "X").replace(".", ",").replace("X", ".")


def kabupaten_tersedia(kabupaten: str) -> bool:
    return kabupaten in _load_data()["stats"]


def get_model_insight() -> dict:
    return _load_data()["model_insight"]


def get_riwayat_produksi(kabupaten: str) -> list[dict]:
    df = _load_data()["riwayat"]
    df_kab = df[df["Kabupaten"] == kabupaten].sort_values(["Tahun", "Bulan"])
    return [
        {"tahun": int(r.Tahun), "bulan": int(r.Bulan), "produksi_ton": float(r.Produksi_Ton)}
        for r in df_kab.itertuples()
    ]


def klasifikasi_produksi(kabupaten: str, prediksi: float) -> tuple[str, dict]:
    s = _load_data()["stats"][kabupaten]
    batas = {"q25": s["q25"], "median": s["median"], "q75": s["q75"]}
    if prediksi < s["q25"]:
        kategori = "Rendah"
    elif prediksi > s["q75"]:
        kategori = "Tinggi"
    else:
        kategori = "Sedang"
    return kategori, batas


def klasifikasi_vegetasi(ndvi: float) -> str:
    if ndvi < 0.3:
        return "Rendah"
    if ndvi < 0.6:
        return "Sedang"
    return "Tinggi"


def bandingkan_musiman(kabupaten: str, bulan: int, prediksi: float) -> tuple[Optional[float], Optional[float]]:
    rata = _load_data()["stats"][kabupaten]["rata_rata_per_bulan"].get(str(bulan))
    if not rata:
        return None, None
    selisih = (prediksi - rata) / rata * 100
    return rata, selisih


def susun_narasi(kabupaten, tahun, bulan, prediksi, ndvi, kategori_prod, kategori_veg, rata_bulan, selisih) -> str:
    nama_bulan = NAMA_BULAN[bulan - 1]

    kalimat = [
        f"Produksi padi di {kabupaten} pada {nama_bulan} {tahun} diprediksi sebesar "
        f"{_format_angka(prediksi)} ton, termasuk kategori {kategori_prod.lower()} "
        f"dibandingkan sebaran produksi bulanan historis kabupaten ini."
    ]

    if rata_bulan is not None and selisih is not None:
        arah = "lebih tinggi" if selisih >= 0 else "lebih rendah"
        kalimat.append(
            f"Nilai ini {_format_angka(abs(selisih), 1)}% {arah} dari rata-rata historis bulan "
            f"{nama_bulan} ({_format_angka(rata_bulan)} ton)."
        )

    kalimat.append(
        f"Nilai NDVI pada periode tersebut adalah {ndvi:.4f} (kategori {kategori_veg.lower()}), "
        f"{DESKRIPSI_VEGETASI[kategori_veg]}"
    )
    kalimat.append(
        "Interpretasi ini bersifat indikatif dan didasarkan pada pola data historis, "
        "bukan pengganti data produksi resmi."
    )
    return " ".join(kalimat)