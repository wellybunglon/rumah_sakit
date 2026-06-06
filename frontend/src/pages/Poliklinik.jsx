import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function Poliklinik() {

  const [poli, setPoli] = useState([])

  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama_poli: '',
    dokter_penanggung_jawab: '',
    jadwal_praktek: '',
    lokasi_ruangan: ''
  })

  const loadPoli = () => {

    fetch('http://127.0.0.1:5000/api/poliklinik')
      .then(res => res.json())
      .then(data => {
        setPoli(data)
      })
  }

  useEffect(() => {
    loadPoli()
  }, [])

  const simpanPoli = async () => {

    if (editId) {

      await fetch(
        `http://127.0.0.1:5000/api/poliklinik/${editId}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(form)
        }
      )

    } else {

      await fetch(
        'http://127.0.0.1:5000/api/poliklinik',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(form)
        }
      )

    }

    setForm({
      nama_poli: '',
      dokter_penanggung_jawab: '',
      jadwal_praktek: '',
      lokasi_ruangan: ''
    })

    setEditId(null)

    loadPoli()
  }

  const hapusPoli = async (id) => {

    if (!window.confirm('Hapus data poliklinik?')) {
      return
    }

    await fetch(
      `http://127.0.0.1:5000/api/poliklinik/${id}`,
      {
        method: 'DELETE'
      }
    )

    loadPoli()
  }

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Data Poliklinik</h1>
        </div>

        <div className="content-box">

          <div className="form-row">

            <input
              className="form-control"
              placeholder="Nama Poli"
              value={form.nama_poli}
              onChange={(e) =>
                setForm({
                  ...form,
                  nama_poli: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Dokter Penanggung Jawab"
              value={form.dokter_penanggung_jawab}
              onChange={(e) =>
                setForm({
                  ...form,
                  dokter_penanggung_jawab: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Jadwal Praktek"
              value={form.jadwal_praktek}
              onChange={(e) =>
                setForm({
                  ...form,
                  jadwal_praktek: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Lokasi Ruangan"
              value={form.lokasi_ruangan}
              onChange={(e) =>
                setForm({
                  ...form,
                  lokasi_ruangan: e.target.value
                })
              }
            />

            <button
              className="btn-primary"
              onClick={simpanPoli}
            >
              {editId ? 'Update' : 'Simpan'}
            </button>

          </div>

          <table className="data-table">

            <thead>

              <tr>
                <th>ID</th>
                <th>Nama Poli</th>
                <th>Dokter PJ</th>
                <th>Jadwal Praktek</th>
                <th>Lokasi Ruangan</th>
                <th>Aksi</th>
              </tr>

            </thead>

            <tbody>

              {poli.map((item) => (

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama_poli}</td>
                  <td>{item.dokter_penanggung_jawab}</td>
                  <td>{item.jadwal_praktek}</td>
                  <td>{item.lokasi_ruangan}</td>

                  <td>

                    <button
                      className="btn-edit"
                      onClick={() => {

                        setEditId(item.id)

                        setForm({
                          nama_poli: item.nama_poli,
                          dokter_penanggung_jawab: item.dokter_penanggung_jawab,
                          jadwal_praktek: item.jadwal_praktek,
                          lokasi_ruangan: item.lokasi_ruangan
                        })

                      }}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-danger"
                      onClick={() => hapusPoli(item.id)}
                    >
                      Hapus
                    </button>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  )
}

export default Poliklinik