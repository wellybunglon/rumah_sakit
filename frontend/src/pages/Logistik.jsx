import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function Logistik() {

  const [barang, setBarang] = useState([])

  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama_barang: '',
    kategori: '',
    jumlah: '',
    lokasi_penyimpanan: '',
    kondisi_barang: ''
  })

  const loadBarang = () => {

    fetch('http://127.0.0.1:5000/api/logistik')
      .then(res => res.json())
      .then(data => {
        setBarang(data)
      })

  }

  useEffect(() => {
    loadBarang()
  }, [])

  const simpanBarang = async () => {

    if (editId) {

      await fetch(
        `http://127.0.0.1:5000/api/logistik/${editId}`,
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
        'http://127.0.0.1:5000/api/logistik',
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
      nama_barang: '',
      kategori: '',
      jumlah: '',
      lokasi_penyimpanan: '',
      kondisi_barang: ''
    })

    setEditId(null)

    loadBarang()
  }

  const hapusBarang = async (id) => {

    if (!window.confirm('Hapus data logistik?')) {
      return
    }

    await fetch(
      `http://127.0.0.1:5000/api/logistik/${id}`,
      {
        method: 'DELETE'
      }
    )

    loadBarang()
  }

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Data Logistik</h1>
        </div>

        <div className="content-box">

          <div className="form-row">

            <input
              className="form-control"
              placeholder="Nama Barang"
              value={form.nama_barang}
              onChange={(e) =>
                setForm({
                  ...form,
                  nama_barang: e.target.value
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
              placeholder="Jumlah"
              value={form.jumlah}
              onChange={(e) =>
                setForm({
                  ...form,
                  jumlah: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Lokasi Penyimpanan"
              value={form.lokasi_penyimpanan}
              onChange={(e) =>
                setForm({
                  ...form,
                  lokasi_penyimpanan: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Kondisi Barang"
              value={form.kondisi_barang}
              onChange={(e) =>
                setForm({
                  ...form,
                  kondisi_barang: e.target.value
                })
              }
            />

            <button
              className="btn-primary"
              onClick={simpanBarang}
            >
              {editId ? 'Update' : 'Simpan'}
            </button>

          </div>

          <table className="data-table">

            <thead>
              <tr>
                <th>ID</th>
                <th>Nama Barang</th>
                <th>Kategori</th>
                <th>Jumlah</th>
                <th>Lokasi Penyimpanan</th>
                <th>Kondisi Barang</th>
                <th>Aksi</th>
              </tr>
            </thead>

            <tbody>

              {barang.map((item) => (

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama_barang}</td>
                  <td>{item.kategori}</td>
                  <td>{item.jumlah}</td>
                  <td>{item.lokasi_penyimpanan}</td>
                  <td>{item.kondisi_barang}</td>

                  <td>

                    <button
                      className="btn-edit"
                      onClick={() => {

                        setEditId(item.id)

                        setForm({
                          nama_barang: item.nama_barang,
                          kategori: item.kategori,
                          jumlah: item.jumlah,
                          lokasi_penyimpanan: item.lokasi_penyimpanan,
                          kondisi_barang: item.kondisi_barang
                        })

                      }}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-danger"
                      onClick={() => hapusBarang(item.id)}
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

export default Logistik