import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function RawatInap() {

  const [rawatInap, setRawatInap] = useState([])

  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama_pasien: '',
    nama_ruangan: '',
    tanggal_masuk: '',
    tanggal_keluar: '',
    status_pasien: ''
  })

  const loadRawatInap = () => {

    fetch('http://127.0.0.1:5000/api/rawat_inap')
      .then(res => res.json())
      .then(data => {
        setRawatInap(data)
      })

  }

  useEffect(() => {
    loadRawatInap()
  }, [])

  const simpanRawatInap = async () => {

    if (editId) {

      await fetch(
        `http://127.0.0.1:5000/api/rawat_inap/${editId}`,
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
        'http://127.0.0.1:5000/api/rawat_inap',
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
      nama_ruangan: '',
      tanggal_masuk: '',
      tanggal_keluar: '',
      status_pasien: ''
    })

    setEditId(null)

    loadRawatInap()
  }

  const hapusRawatInap = async (id) => {

    if (!window.confirm('Hapus data rawat inap?')) {
      return
    }

    await fetch(
      `http://127.0.0.1:5000/api/rawat_inap/${id}`,
      {
        method: 'DELETE'
      }
    )

    loadRawatInap()
  }

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Data Rawat Inap</h1>
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
              type="date"
              className="form-control"
              value={form.tanggal_masuk}
              onChange={(e) =>
                setForm({
                  ...form,
                  tanggal_masuk: e.target.value
                })
              }
            />

            <input
              type="date"
              className="form-control"
              value={form.tanggal_keluar}
              onChange={(e) =>
                setForm({
                  ...form,
                  tanggal_keluar: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Status Pasien"
              value={form.status_pasien}
              onChange={(e) =>
                setForm({
                  ...form,
                  status_pasien: e.target.value
                })
              }
            />

            <button
              className="btn-primary"
              onClick={simpanRawatInap}
            >
              {editId ? 'Update' : 'Simpan'}
            </button>

          </div>

          <table className="data-table">

            <thead>

              <tr>
                <th>ID</th>
                <th>Nama Pasien</th>
                <th>Nama Ruangan</th>
                <th>Tanggal Masuk</th>
                <th>Tanggal Keluar</th>
                <th>Status Pasien</th>
                <th>Aksi</th>
              </tr>

            </thead>

            <tbody>

              {rawatInap.map((item) => (

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama_pasien}</td>
                  <td>{item.nama_ruangan}</td>
                  <td>{item.tanggal_masuk}</td>
                  <td>{item.tanggal_keluar}</td>
                  <td>{item.status_pasien}</td>

                  <td>

                    <button
                      className="btn-edit"
                      onClick={() => {

                        setEditId(item.id)

                        setForm({
                          nama_pasien: item.nama_pasien,
                          nama_ruangan: item.nama_ruangan,
                          tanggal_masuk: item.tanggal_masuk,
                          tanggal_keluar: item.tanggal_keluar,
                          status_pasien: item.status_pasien
                        })

                      }}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-danger"
                      onClick={() =>
                        hapusRawatInap(item.id)
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

export default RawatInap