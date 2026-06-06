import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function Registrasi() {

  const [registrasi, setRegistrasi] = useState([])

  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama_pasien: '',
    poli_tujuan: '',
    tanggal_kunjungan: '',
    keluhan: ''
  })

  const loadRegistrasi = () => {

    fetch('http://127.0.0.1:5000/api/registrasi')
      .then(res => res.json())
      .then(data => {
        setRegistrasi(data)
      })
  }

  useEffect(() => {
    loadRegistrasi()
  }, [])

  const simpanRegistrasi = async () => {

    if (editId) {

      await fetch(
        `http://127.0.0.1:5000/api/registrasi/${editId}`,
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
        'http://127.0.0.1:5000/api/registrasi',
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
      nama_pasien: '',
      poli_tujuan: '',
      tanggal_kunjungan: '',
      keluhan: ''
    })

    setEditId(null)

    loadRegistrasi()
  }

  const hapusRegistrasi = async (id) => {

    if (!window.confirm('Hapus data registrasi?')) {
      return
    }

    await fetch(
      `http://127.0.0.1:5000/api/registrasi/${id}`,
      {
        method: 'DELETE'
      }
    )

    loadRegistrasi()
  }

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Registrasi Pasien</h1>
        </div>

        <div className="content-box">

          <div className="form-row">

            <input
              className="form-control"
              placeholder="Nama Pasien"
              value={form.nama_pasien}
              onChange={(e) =>
                setForm({
                  ...form,
                  nama_pasien: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Poli Tujuan"
              value={form.poli_tujuan}
              onChange={(e) =>
                setForm({
                  ...form,
                  poli_tujuan: e.target.value
                })
              }
            />

            <input
              className="form-control"
              type="date"
              value={form.tanggal_kunjungan}
              onChange={(e) =>
                setForm({
                  ...form,
                  tanggal_kunjungan: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Keluhan"
              value={form.keluhan}
              onChange={(e) =>
                setForm({
                  ...form,
                  keluhan: e.target.value
                })
              }
            />

            <button
              className="btn-primary"
              onClick={simpanRegistrasi}
            >
              {editId ? 'Update' : 'Simpan'}
            </button>

          </div>

          <table className="data-table">

            <thead>

              <tr>
                <th>ID</th>
                <th>Nama Pasien</th>
                <th>Poli Tujuan</th>
                <th>Tanggal Kunjungan</th>
                <th>Keluhan</th>
                <th>Aksi</th>
              </tr>

            </thead>

            <tbody>

              {registrasi.map((item) => (

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama_pasien}</td>
                  <td>{item.poli_tujuan}</td>
                  <td>{item.tanggal_kunjungan}</td>
                  <td>{item.keluhan}</td>

                  <td>

                    <button
                      className="btn-edit"
                      onClick={() => {

                        setEditId(item.id)

                        setForm({
                          nama_pasien: item.nama_pasien,
                          poli_tujuan: item.poli_tujuan,
                          tanggal_kunjungan: item.tanggal_kunjungan,
                          keluhan: item.keluhan
                        })

                      }}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-danger"
                      onClick={() =>
                        hapusRegistrasi(item.id)
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

export default Registrasi