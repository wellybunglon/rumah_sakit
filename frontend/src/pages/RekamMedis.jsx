import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function RekamMedis() {

  const [rekamMedis, setRekamMedis] = useState([])

  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama_pasien: '',
    diagnosa: '',
    tindakan: '',
    resep_obat: '',
    tanggal: ''
  })

  const loadRekamMedis = () => {

    fetch('http://127.0.0.1:5000/api/rekam_medis')
      .then(res => res.json())
      .then(data => {
        setRekamMedis(data)
      })

  }

  useEffect(() => {
    loadRekamMedis()
  }, [])

  const simpanRekamMedis = async () => {

    try {

      if (editId) {

        await fetch(
          `http://127.0.0.1:5000/api/rekam_medis/${editId}`,
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
          'http://127.0.0.1:5000/api/rekam_medis',
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
        diagnosa: '',
        tindakan: '',
        resep_obat: '',
        tanggal: ''
      })

      setEditId(null)

      loadRekamMedis()

    } catch (err) {

      console.log(err)
      alert('Gagal menyimpan data')

    }

  }

  const hapusRekamMedis = async (id) => {

    if (!window.confirm('Hapus data rekam medis?')) {
      return
    }

    await fetch(
      `http://127.0.0.1:5000/api/rekam_medis/${id}`,
      {
        method: 'DELETE'
      }
    )

    loadRekamMedis()

  }

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Data Rekam Medis</h1>
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
              placeholder="Diagnosa"
              value={form.diagnosa}
              onChange={(e) =>
                setForm({
                  ...form,
                  diagnosa: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Tindakan"
              value={form.tindakan}
              onChange={(e) =>
                setForm({
                  ...form,
                  tindakan: e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Resep Obat"
              value={form.resep_obat}
              onChange={(e) =>
                setForm({
                  ...form,
                  resep_obat: e.target.value
                })
              }
            />

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
              onClick={simpanRekamMedis}
            >
              {editId ? 'Update' : 'Simpan'}
            </button>

          </div>

          <table className="data-table">

            <thead>
              <tr>
                <th>ID</th>
                <th>Nama Pasien</th>
                <th>Diagnosa</th>
                <th>Tindakan</th>
                <th>Resep Obat</th>
                <th>Tanggal</th>
                <th>Aksi</th>
              </tr>
            </thead>

            <tbody>

              {rekamMedis.map((item) => (

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama_pasien}</td>
                  <td>{item.diagnosa}</td>
                  <td>{item.tindakan}</td>
                  <td>{item.resep_obat}</td>
                  <td>{item.tanggal}</td>

                  <td>

                    <button
                      className="btn-edit"
                      onClick={() => {

                        setEditId(item.id)

                        setForm({
                          nama_pasien: item.nama_pasien,
                          diagnosa: item.diagnosa,
                          tindakan: item.tindakan,
                          resep_obat: item.resep_obat,
                          tanggal: item.tanggal
                        })

                      }}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-danger"
                      onClick={() =>
                        hapusRekamMedis(item.id)
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

export default RekamMedis