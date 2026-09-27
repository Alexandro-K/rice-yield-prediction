import { useState } from 'react'
import { predictProduksi, getMapLayer } from './api/client'
import PetaSawah from './components/PetaSawah'

const KABUPATEN_LIST = ['Bojonegoro', 'Jember', 'Ngawi', 'Tuban', 'Lamongan']
const BULAN_LIST = [
  'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
  'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
]


function App() {
  const [kabupaten, setKabupaten] = useState('Ngawi')
  const [tahun, setTahun] = useState(2024)
  const [bulan, setBulan] = useState(6)
  const [hasil, setHasil] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [mapData, setMapData] = useState(null)

  const handlePrediksi = async () => {
  setLoading(true)
  setError(null)
  setHasil(null)
  setMapData(null)
  try {
    const [dataPrediksi, dataMap] = await Promise.all([
      predictProduksi(kabupaten, tahun, bulan),
      getMapLayer(kabupaten, tahun, bulan, 'NDVI'),
    ])
    setHasil(dataPrediksi)
    setMapData(dataMap)
  } catch (err) {
    setError(err.response?.data?.detail || 'Terjadi kesalahan saat memproses prediksi.')
  } finally {
    setLoading(false)
  }
}

  return (
    <div className="app-container">
      <h1>Prediksi Produksi Padi</h1>

      <div className="form-panel">
        <label>
          Kabupaten
          <select value={kabupaten} onChange={(e) => setKabupaten(e.target.value)}>
            {KABUPATEN_LIST.map((kab) => (
              <option key={kab} value={kab}>{kab}</option>
            ))}
          </select>
        </label>

        <label>
          Tahun
          <input
            type="number"
            value={tahun}
            min={2019}
            max={2026}
            onChange={(e) => setTahun(Number(e.target.value))}
          />
        </label>

        <label>
          Bulan
          <select value={bulan} onChange={(e) => setBulan(Number(e.target.value))}>
            {BULAN_LIST.map((nama, idx) => (
              <option key={nama} value={idx + 1}>{nama}</option>
            ))}
          </select>
        </label>

        <button onClick={handlePrediksi} disabled={loading}>
          {loading ? 'Memproses (bisa memakan waktu ~1 menit)...' : 'Prediksi'}
        </button>
      </div>

      {error && <div className="error-panel">{error}</div>}

      {hasil && (
        <div className="result-panel">
          <h2>Hasil Prediksi — {hasil.kabupaten}, {BULAN_LIST[hasil.bulan - 1]} {hasil.tahun}</h2>
          <p className="prediksi-utama">
            {hasil.prediksi_produksi_ton.toLocaleString('id-ID', { maximumFractionDigits: 2 })} Ton
          </p>
          <div className="index-grid">
            <div><span>NDVI</span>{hasil.ndvi_mean.toFixed(4)}</div>
            <div><span>EVI</span>{hasil.evi_mean.toFixed(4)}</div>
            <div><span>SAVI</span>{hasil.savi_mean.toFixed(4)}</div>
            <div><span>Jumlah Citra Terpakai</span>{hasil.jumlah_citra}</div>
          </div>
        </div>
      )}
      <div className="map-panel">
        <PetaSawah mapData={mapData} />
      </div>
    </div>
    
  )
}

export default App