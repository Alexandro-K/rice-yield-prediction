import { formatAngka, formatPersenBertanda } from '../utils/format'

const KELAS_KATEGORI = {
  Rendah: 'badge-rendah',
  Sedang: 'badge-sedang',
  Tinggi: 'badge-tinggi',
}

function PanelPenjelasan({ insight, loading, error }) {
  if (loading) {
    return <div className="insight-panel insight-info">Menyusun penjelasan hasil...</div>
  }

  if (error) {
    return (
      <div className="insight-panel insight-info">
        Penjelasan hasil tidak dapat dimuat. Angka prediksi di atas tetap valid.
      </div>
    )
  }

  if (!insight) return null

  const { batas_kuartil: batas } = insight

  return (
    <div className="insight-panel">
      <h2>Penjelasan Hasil</h2>

      <div className="insight-grid">
        <div className="insight-card">
          <span className="insight-label">Kategori produksi</span>
          <span className={`badge ${KELAS_KATEGORI[insight.kategori_produksi]}`}>
            {insight.kategori_produksi}
          </span>
          <small>Dibandingkan sebaran produksi historis kabupaten</small>
        </div>

        <div className="insight-card">
          <span className="insight-label">Dibanding rata-rata bulan yang sama</span>
          <span className="insight-nilai">
            {insight.selisih_persen_vs_musiman !== null
              ? formatPersenBertanda(insight.selisih_persen_vs_musiman)
              : '-'}
          </span>
          <small>
            {insight.rata_rata_bulan_sama_ton !== null
              ? `Rata-rata historis: ${formatAngka(insight.rata_rata_bulan_sama_ton)} Ton`
              : 'Data pembanding tidak tersedia'}
          </small>
        </div>

        <div className="insight-card">
          <span className="insight-label">Kondisi vegetasi (NDVI)</span>
          <span className={`badge ${KELAS_KATEGORI[insight.kategori_vegetasi]}`}>
            {insight.kategori_vegetasi}
          </span>
          <small>Rendah di bawah 0,3; sedang 0,3 sampai 0,6; tinggi di atas 0,6</small>
        </div>
      </div>

      <p className="insight-narasi">{insight.narasi}</p>

      <table className="insight-tabel">
        <thead>
          <tr>
            <th>Kategori produksi</th>
            <th>Rentang (Ton per bulan)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Rendah</td>
            <td>Kurang dari {formatAngka(batas.q25, 0)}</td>
          </tr>
          <tr>
            <td>Sedang</td>
            <td>{formatAngka(batas.q25, 0)} sampai {formatAngka(batas.q75, 0)}</td>
          </tr>
          <tr>
            <td>Tinggi</td>
            <td>Lebih dari {formatAngka(batas.q75, 0)}</td>
          </tr>
        </tbody>
      </table>
      <small className="insight-catatan">
        Batas kategori ditentukan dari kuartil pertama dan ketiga produksi historis tiap kabupaten.
      </small>
    </div>
  )
}

export default PanelPenjelasan