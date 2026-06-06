import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function TenagaMedis() {

  const [medis, setMedis] = useState([])

  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama: '',
    profesi: '',
    spesialis: '',
    no_hp: ''
  })

  const loadMedis = () => {

    fetch('http://127.0.0.1:5000/api/tenaga_medis')
      .then(res => res.json())
      .then(data => {
        setMedis(data)
      })
  }

  useEffect(() => {

    const user = JSON.parse(
    localStorage.getItem('user')
  )

  if (user?.level !== 'admin') {

    alert('Akses ditolak')

    window.location.href = '/dashboard'

    return
  }

  loadMedis()

}, [])

  const simpanMedis = async () => {

    if (editId) {

      await fetch(
        `http://127.0.0.1:5000/api/tenaga_medis/${editId}`,
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
        'http://127.0.0.1:5000/api/tenaga_medis',
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
      profesi: '',
      spesialis: '',
      no_hp: ''
    })

    setEditId(null)

    loadMedis()
  }

  const hapusMedis = async (id) => {

    if (!window.confirm('Hapus data tenaga medis?')) {
      return
    }

    await fetch(
      `http://127.0.0.1:5000/api/tenaga_medis/${id}`,
      {
        method: 'DELETE'
      }
    )

    loadMedis()
  }

  return (
    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Data Tenaga Medis</h1>
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
              placeholder="Profesi"
              value={form.profesi}
              onChange={(e) =>
                setForm({
                  ...form,
                  profesi: e.target.value
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
              placeholder="No HP"
              value={form.no_hp}
              onChange={(e) =>
                setForm({
                  ...form,
                  no_hp: e.target.value
                })
              }
            />

            <button
              className="btn-primary"
              onClick={simpanMedis}
            >
              {editId ? 'Update' : 'Simpan'}
            </button>

          </div>

          <table className="data-table">

            <thead>

              <tr>
                <th>ID</th>
                <th>Nama</th>
                <th>Profesi</th>
                <th>Spesialis</th>
                <th>No HP</th>
                <th>Aksi</th>
              </tr>

            </thead>

            <tbody>

              {medis.map((item) => (

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama}</td>
                  <td>{item.profesi}</td>
                  <td>{item.spesialis}</td>
                  <td>{item.no_hp}</td>

                  <td>

                    <button
                      className="btn-edit"
                      onClick={() => {

                        setEditId(item.id)

                        setForm({
                          nama: item.nama,
                          profesi: item.profesi,
                          spesialis: item.spesialis,
                          no_hp: item.no_hp
                        })

                      }}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-danger"
                      onClick={() =>
                        hapusMedis(item.id)
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

export default TenagaMedis