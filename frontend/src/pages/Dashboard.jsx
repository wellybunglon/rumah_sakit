import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'

function Dashboard() {

  const [data, setData] = useState({
    pasien: 0,
    medis: 0,
    ruangan: 0,
    obat: 0
  })

  useEffect(() => {

    // CEK LOGIN
    const user = localStorage.getItem('user')

    if (!user) {
      window.location.href = '/login'
      return
    }

    fetch('http://127.0.0.1:5000/api/dashboard', {
      credentials: 'include'
    })
      .then(res => {
        if (!res.ok) throw new Error("Unauthorized")
        return res.json()
      })
      .then(data => {
        console.log("DATA API:", data)
        setData(data)
      })
      .catch(err => {
        console.log("ERROR:", err)

        // Jika session habis, kembali ke login
        localStorage.removeItem('user')
        window.location.href = '/login'
      })

  }, [])

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Dashboard Rumah Sakit</h1>
        </div>

        <div className="hero">
          <div className="overlay">
            <h2>Selamat Datang</h2>
            <p>Sistem Informasi Rumah Sakit Modern</p>
          </div>
        </div>

        <div className="card-container">

          <div className="card">
            <h3>Total Pasien</h3>
            <p>{data.pasien}</p>
          </div>

          <div className="card">
            <h3>Tenaga Medis</h3>
            <p>{data.medis}</p>
          </div>

          <div className="card">
            <h3>Ruangan</h3>
            <p>{data.ruangan}</p>
          </div>

          <div className="card">
            <h3>Farmasi</h3>
            <p>{data.obat}</p>
          </div>

        </div>

      </div>

    </div>
  )
}

export default Dashboard