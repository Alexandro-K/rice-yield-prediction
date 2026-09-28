const TAB = [
  { id: 'prediksi', label: 'Prediksi' },
  { id: 'performa', label: 'Performa Model' },
  { id: 'tentang', label: 'Tentang Proyek' },
]

function NavTabs({ aktif, onGanti }) {
  return (
    <div className="nav-tabs" role="tablist">
      {TAB.map((t) => (
        <button
          key={t.id}
          role="tab"
          aria-selected={aktif === t.id}
          className={`nav-tab ${aktif === t.id ? 'aktif' : ''}`}
          onClick={() => onGanti(t.id)}
        >
          {t.label}
        </button>
      ))}
    </div>
  )
}

export default NavTabs