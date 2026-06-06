import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function Pasien() {

  const [pasien, setPasien] = useState([])

  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama: '',
    umur: '',
    alamat: '',
    penyakit: ''
  })

  const loadPasien = () => {

    fetch('http://127.0.0.1:5000/api/pasien')
      .then(res => res.json())
      .then(data => {
        setPasien(data)
      })
  }

  useEffect(() => {
    loadPasien()
  }, [])

    const simpanPasien = async () => {

  if (editId) {

    await fetch(
      `http://127.0.0.1:5000/api/pasien/${editId}`,
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
      'http://127.0.0.1:5000/api/pasien',
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
    nama: '',
    umur: '',
    alamat: '',
    penyakit: ''
  })

  setEditId(null)

  loadPasien()
}
  const hapusPasien = async (id) => {

    if (!window.confirm('Hapus data pasien?')) {
      return
    }

    await fetch(
      `http://127.0.0.1:5000/api/pasien/${id}`,
      {
        method: 'DELETE'
      }
    )

    loadPasien()
  }

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Data Pasien</h1>
        </div>

        <div className="content-box">

          <div className="form-row">

            <input
              className="form-control"
              placeholder="Nama"
              value={form.nama}
              onChange={(e) =>
                setForm({
                  ...form,
                  nama: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Umur"
              value={form.umur}
              onChange={(e) =>
                setForm({
                  ...form,
                  umur: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Alamat"
              value={form.alamat}
              onChange={(e) =>
                setForm({
                  ...form,
                  alamat: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Penyakit"
              value={form.penyakit}
              onChange={(e) =>
                setForm({
                  ...form,
                  penyakit: e.target.value
                })
              }
            />

            <button
              className="btn-primary"
              onClick={simpanPasien}
            >
              Simpan
            </button>

          </div>

          <table className="data-table">

            <thead>

              <tr>
                <th>ID</th>
                <th>Nama</th>
                <th>Umur</th>
                <th>Alamat</th>
                <th>Penyakit</th>
                <th>Aksi</th>
              </tr>

            </thead>

            <tbody>

              {pasien.map((item) => (

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama}</td>
                  <td>{item.umur}</td>
                  <td>{item.alamat}</td>
                  <td>{item.penyakit}</td>

                  <td>

                     <button
                     className="btn-edit"
                     onClick={() => {

                    setEditId(item.id)

                    setForm({
                       nama: item.nama,
                       umur: item.umur,
                       alamat: item.alamat,
                       penyakit: item.penyakit
                     })

                   }}
                         >
                           Edit
                        </button>

                      <button
                        className="btn-danger"
                         onClick={() =>
                          hapusPasien(item.id)
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

export default Pasien