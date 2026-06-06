import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function Farmasi() {

  const [obat, setObat] = useState([])

  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama_obat: '',
    kategori: '',
    stok: '',
    harga: '',
    tanggal_expired: ''
  })

  const loadObat = () => {

    fetch('http://127.0.0.1:5000/api/farmasi')
      .then(res => res.json())
      .then(data => {
        setObat(data)
      })

  }

  useEffect(() => {
    loadObat()
  }, [])

  const simpanObat = async () => {

    if (editId) {

      await fetch(
        `http://127.0.0.1:5000/api/farmasi/${editId}`,
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
        'http://127.0.0.1:5000/api/farmasi',
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
      nama_obat: '',
      kategori: '',
      stok: '',
      harga: '',
      tanggal_expired: ''
    })

    setEditId(null)

    loadObat()
  }

  const hapusObat = async (id) => {

    if (!window.confirm('Hapus data obat?')) {
      return
    }

    await fetch(
      `http://127.0.0.1:5000/api/farmasi/${id}`,
      {
        method: 'DELETE'
      }
    )

    loadObat()
  }

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Data Farmasi</h1>
        </div>

        <div className="content-box">

          <div className="form-row">

            <input
              className="form-control"
              placeholder="Nama Obat"
              value={form.nama_obat}
              onChange={(e) =>
                setForm({
                  ...form,
                  nama_obat: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Kategori"
              value={form.kategori}
              onChange={(e) =>
                setForm({
                  ...form,
                  kategori: e.target.value
                })
              }
            />

            <input
              type="number"
              className="form-control"
              placeholder="Stok"
              value={form.stok}
              onChange={(e) =>
                setForm({
                  ...form,
                  stok: e.target.value
                })
              }
            />

            <input
              type="number"
              className="form-control"
              placeholder="Harga"
              value={form.harga}
              onChange={(e) =>
                setForm({
                  ...form,
                  harga: e.target.value
                })
              }
            />

            <input
              type="date"
              className="form-control"
              value={form.tanggal_expired}
              onChange={(e) =>
                setForm({
                  ...form,
                  tanggal_expired: e.target.value
                })
              }
            />

            <button
              className="btn-primary"
              onClick={simpanObat}
            >
              {editId ? 'Update' : 'Simpan'}
            </button>

          </div>

          <table className="data-table">

            <thead>
              <tr>
                <th>ID</th>
                <th>Nama Obat</th>
                <th>Kategori</th>
                <th>Stok</th>
                <th>Harga</th>
                <th>Tanggal Expired</th>
                <th>Aksi</th>
              </tr>
            </thead>

            <tbody>

              {obat.map((item) => (

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama_obat}</td>
                  <td>{item.kategori}</td>
                  <td>{item.stok}</td>

                  <td>
                    Rp {Number(item.harga).toLocaleString('id-ID')}
                  </td>

                  <td>{item.tanggal_expired}</td>

                  <td>

                    <button
                      className="btn-edit"
                      onClick={() => {

                        setEditId(item.id)

                        setForm({
                          nama_obat: item.nama_obat,
                          kategori: item.kategori,
                          stok: item.stok,
                          harga: item.harga,
                          tanggal_expired: item.tanggal_expired
                        })

                      }}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-danger"
                      onClick={() => hapusObat(item.id)}
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

export default Farmasi