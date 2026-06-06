import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function Billing() {

  const [billing, setBilling] = useState([])
  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama_pasien: '',
    layanan: '',
    total_tagihan: '',
    status_pembayaran: '',
    tanggal: ''
  })

  const loadBilling = () => {

    fetch('http://127.0.0.1:5000/api/billing')
      .then(res => res.json())
      .then(data => {
        setBilling(data)
      })

  }

  useEffect(() => {
    loadBilling()
  }, [])

  const simpanBilling = async () => {

    if (editId) {

      await fetch(
        `http://127.0.0.1:5000/api/billing/${editId}`,
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
        'http://127.0.0.1:5000/api/billing',
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
      layanan: '',
      total_tagihan: '',
      status_pembayaran: '',
      tanggal: ''
    })

    setEditId(null)

    loadBilling()
  }

  const hapusBilling = async (id) => {

    if (!window.confirm('Hapus data billing?')) {
      return
    }

    await fetch(
      `http://127.0.0.1:5000/api/billing/${id}`,
      {
        method: 'DELETE'
      }
    )

    loadBilling()
  }

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Data Billing</h1>
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
              placeholder="Layanan"
              value={form.layanan}
              onChange={(e) =>
                setForm({
                  ...form,
                  layanan: e.target.value
                })
              }
            />

            <input
              type="number"
              className="form-control"
              placeholder="Total Tagihan"
              value={form.total_tagihan}
              onChange={(e) =>
                setForm({
                  ...form,
                  total_tagihan: e.target.value
                })
              }
            />

            <select
              className="form-control"
              value={form.status_pembayaran}
              onChange={(e) =>
                setForm({
                  ...form,
                  status_pembayaran: e.target.value
                })
              }
            >
              <option value="">Pilih Status</option>
              <option value="Belum Lunas">Belum Lunas</option>
              <option value="Lunas">Lunas</option>
            </select>

            <input
              type="date"
              className="form-control"
              value={form.tanggal}
              onChange={(e) =>
                setForm({
                  ...form,
                  tanggal: e.target.value
                })
              }
            />

            <button
              className="btn-primary"
              onClick={simpanBilling}
            >
              {editId ? 'Update' : 'Simpan'}
            </button>

          </div>

          <table className="data-table">

            <thead>
              <tr>
                <th>ID</th>
                <th>Nama Pasien</th>
                <th>Layanan</th>
                <th>Total Tagihan</th>
                <th>Status Pembayaran</th>
                <th>Tanggal</th>
                <th>Aksi</th>
              </tr>
            </thead>

            <tbody>

              {billing.map((item) => (

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama_pasien}</td>
                  <td>{item.layanan}</td>

                  <td>
                    Rp {Number(item.total_tagihan).toLocaleString('id-ID')}
                  </td>

                  <td>{item.status_pembayaran}</td>
                  <td>{item.tanggal}</td>

                  <td>

                    <button
                      className="btn-edit"
                      onClick={() => {

                        setEditId(item.id)

                        setForm({
                          nama_pasien: item.nama_pasien,
                          layanan: item.layanan,
                          total_tagihan: item.total_tagihan,
                          status_pembayaran: item.status_pembayaran,
                          tanggal: item.tanggal
                        })

                      }}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-danger"
                      onClick={() => hapusBilling(item.id)}
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

export default Billing