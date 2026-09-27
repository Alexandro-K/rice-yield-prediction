import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // GEE bisa butuh waktu lama, beri ruang hingga 2 menit
})

export async function predictProduksi(kabupaten, tahun, bulan) {
  const response = await apiClient.post('/predict', { kabupaten, tahun, bulan })
  return response.data
}

export async function getMapLayer(kabupaten, tahun, bulan, layer = 'NDVI') {
  const response = await apiClient.post('/map-layer', { kabupaten, tahun, bulan, layer })
  return response.data
}