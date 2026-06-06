import { Link } from 'react-router-dom'

function Sidebar() {

  const user = JSON.parse(
    localStorage.getItem('user')
  )

  const level = user?.level

  const handleLogout = () => {
    localStorage.removeItem('user')
    window.location.href = '/login'
  }

  return (
    <div className="sidebar">

      <h2>RS SEHAT</h2>

      <Link to="/dashboard">Dashboard</Link>

      {/* DATA MASTER */}
      <div className="menu-title">
        Data Master
      </div>

      <Link to="/pasien">Data Pasien</Link>

      {level === 'admin' && (
        <>
          <Link to="/tenaga-medis">
            Tenaga Medis
          </Link>

          <Link to="/ruangan">
            Ruangan
          </Link>

          <Link to="/poliklinik">
            Poliklinik
          </Link>
        </>
      )}

      {/* TRANSAKSI MEDIS */}
      <div className="menu-title">
        Transaksi Medis
      </div>

      {(level === 'admin' || level === 'perawat') && (
        <Link to="/registrasi">
          Registrasi
        </Link>
      )}

      {(level === 'admin' || level === 'dokter') && (
        <Link to="/rekam-medis">
          Rekam Medis
        </Link>
      )}

      {(level === 'admin' || level === 'perawat') && (
        <Link to="/rawat-inap">
          Rawat Inap
        </Link>
      )}

      {/* ADMINISTRASI */}
      {(level === 'admin') && (
        <>
          <div className="menu-title">
            Administrasi
          </div>

          <Link to="/billing">
            Billing
          </Link>

          <Link to="/jadwal-dokter">
            Jadwal Dokter
          </Link>

          <Link to="/users">
            User
          </Link>

          <Link to="/farmasi">
            Farmasi
          </Link>

          <Link to="/logistik">
            Logistik
          </Link>
        </>
      )}

      <button
        className="logout-btn"
        onClick={handleLogout}
      >
        Logout
      </button>

    </div>
  )
}

export default Sidebar