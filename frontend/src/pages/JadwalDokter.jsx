import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function JadwalDokter() {

  const [jadwal, setJadwal] = useState([])

  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama_dokter: '',
    spesialis: '',
    hari: '',
    jam_praktek: '',
    ruangan: ''
  })

  const loadJadwal = () => {

    fetch('http://127.0.0.1:5000/api/jadwal_dokter')
      .then(res => res.json())
      .then(data => {
        setJadwal(data)
      })

  }

  useEffect(() => {
    loadJadwal()
  }, [])

  const simpanJadwal = async () => {

    if (editId) {

      await fetch(
        `http://127.0.0.1:5000/api/jadwal_dokter/${editId}`,
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
        'http://127.0.0.1:5000/api/jadwal_dokter',
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
      nama_dokter: '',
      spesialis: '',
      hari: '',
      jam_praktek: '',
      ruangan: ''
    })

    setEditId(null)

    loadJadwal()
  }

  const hapusJadwal = async (id) => {

    if (!window.confirm('Hapus jadwal dokter?')) {
      return
    }

    await fetch(
      `http://127.0.0.1:5000/api/jadwal_dokter/${id}`,
      {
        method: 'DELETE'
      }
    )

    loadJadwal()
  }

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Jadwal Dokter</h1>
        </div>

        <div className="content-box">

          <div className="form-row">

            <input
              className="form-control"
              placeholder="Nama Dokter"
              value={form.nama_dokter}
              onChange={(e) =>
                setForm({
                  ...form,
                  nama_dokter: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Spesialis"
              value={form.spesialis}
              onChange={(e) =>
                setForm({
                  ...form,
                  spesialis: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Hari"
              value={form.hari}
              onChange={(e) =>
                setForm({
                  ...form,
                  hari: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Jam Praktek"
              value={form.jam_praktek}
              onChange={(e) =>
                setForm({
                  ...form,
                  jam_praktek: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Ruangan"
              value={form.ruangan}
              onChange={(e) =>
                setForm({
                  ...form,
                  ruangan: e.target.value
                })
              }
            />

            <button
              className="btn-primary"
              onClick={simpanJadwal}
            >
              {editId ? 'Update' : 'Simpan'}
            </button>

          </div>

          <table className="data-table">

            <thead>
              <tr>
                <th>ID</th>
                <th>Nama Dokter</th>
                <th>Spesialis</th>
                <th>Hari</th>
                <th>Jam Praktek</th>
                <th>Ruangan</th>
                <th>Aksi</th>
              </tr>
            </thead>

            <tbody>

              {jadwal.map((item) => (

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama_dokter}</td>
                  <td>{item.spesialis}</td>
                  <td>{item.hari}</td>
                  <td>{item.jam_praktek}</td>
                  <td>{item.ruangan}</td>

                  <td>

                    <button
                      className="btn-edit"
                      onClick={() => {

                        setEditId(item.id)

                        setForm({
                          nama_dokter: item.nama_dokter,
                          spesialis: item.spesialis,
                          hari: item.hari,
                          jam_praktek: item.jam_praktek,
                          ruangan: item.ruangan
                        })

                      }}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-danger"
                      onClick={() => hapusJadwal(item.id)}
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

export default JadwalDokter