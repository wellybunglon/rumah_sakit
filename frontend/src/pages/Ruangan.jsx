import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function Ruangan() {

  const [ruangan, setRuangan] = useState([])

  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama_ruangan: '',
    jenis_ruangan: '',
    kapasitas: '',
    status_ruangan: ''
  })

  const loadRuangan = () => {

    fetch('http://127.0.0.1:5000/api/ruangan')
      .then(res => res.json())
      .then(data => {
        setRuangan(data)
      })

  }

  useEffect(() => {
    loadRuangan()
  }, [])

  const simpanRuangan = async () => {

    if (editId) {

      await fetch(
        `http://127.0.0.1:5000/api/ruangan/${editId}`,
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
        'http://127.0.0.1:5000/api/ruangan',
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
      nama_ruangan: '',
      jenis_ruangan: '',
      kapasitas: '',
      status_ruangan: ''
    })

    setEditId(null)

    loadRuangan()
  }

  const hapusRuangan = async (id) => {

    if (!window.confirm('Hapus data ruangan?'))
      return

    await fetch(
      `http://127.0.0.1:5000/api/ruangan/${id}`,
      {
        method: 'DELETE'
      }
    )

    loadRuangan()
  }

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Data Ruangan</h1>
        </div>

        <div className="content-box">

          <div className="form-row">

            <input
              className="form-control"
              placeholder="Nama Ruangan"
              value={form.nama_ruangan}
              onChange={(e) =>
                setForm({
                  ...form,
                  nama_ruangan: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Jenis Ruangan"
              value={form.jenis_ruangan}
              onChange={(e) =>
                setForm({
                  ...form,
                  jenis_ruangan: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Kapasitas"
              value={form.kapasitas}
              onChange={(e) =>
                setForm({
                  ...form,
                  kapasitas: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Status Ruangan"
              value={form.status_ruangan}
              onChange={(e) =>
                setForm({
                  ...form,
                  status_ruangan: e.target.value
                })
              }
            />

            <button
              className="btn-primary"
              onClick={simpanRuangan}
            >
              {editId ? 'Update' : 'Simpan'}
            </button>

          </div>

          <table className="data-table">

            <thead>

              <tr>
                <th>ID</th>
                <th>Nama Ruangan</th>
                <th>Jenis Ruangan</th>
                <th>Kapasitas</th>
                <th>Status</th>
                <th>Aksi</th>
              </tr>

            </thead>

            <tbody>

              {ruangan.map((item) => (

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama_ruangan}</td>
                  <td>{item.jenis_ruangan}</td>
                  <td>{item.kapasitas}</td>
                  <td>{item.status_ruangan}</td>

                  <td>

                    <button
                      className="btn-edit"
                      onClick={() => {

                        setEditId(item.id)

                        setForm({
                          nama_ruangan: item.nama_ruangan,
                          jenis_ruangan: item.jenis_ruangan,
                          kapasitas: item.kapasitas,
                          status_ruangan: item.status_ruangan
                        })

                      }}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-danger"
                      onClick={() =>
                        hapusRuangan(item.id)
                      }
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

export default Ruangan