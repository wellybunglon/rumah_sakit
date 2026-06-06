import { useEffect, useState } from 'react'
import Sidebar from '../components/Sidebar'
import '../App.css'

function Users() {

  const [users, setUsers] = useState([])

  const [editId, setEditId] = useState(null)

  const [form, setForm] = useState({
    nama: '',
    username: '',
    password: '',
    level: ''
  })

  const loadUsers = () => {

    fetch('http://127.0.0.1:5000/api/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data)
      })
  }

  useEffect(() => {
    loadUsers()
  }, [])

  const simpanUser = async () => {

    const url = editId
      ? `http://127.0.0.1:5000/api/users/${editId}`
      : 'http://127.0.0.1:5000/api/users'

    const method = editId ? 'PUT' : 'POST'

    await fetch(url,{
      method,
      headers:{
        'Content-Type':'application/json'
      },
      body:JSON.stringify(form)
    })

    setForm({
      nama:'',
      username:'',
      password:'',
      level:''
    })

    setEditId(null)

    loadUsers()
  }

  const hapusUser = async(id)=>{

    if(!window.confirm('Hapus user?'))
      return

    await fetch(
      `http://127.0.0.1:5000/api/users/${id}`,
      {
        method:'DELETE'
      }
    )

    loadUsers()
  }

  return (

    <div className="container">

      <Sidebar />

      <div className="main">

        <div className="navbar">
          <h1>Data User</h1>
        </div>

        <div className="content-box">

          <div className="form-row">

            <input
              className="form-control"
              placeholder="Nama"
              value={form.nama}
              onChange={(e)=>
                setForm({
                  ...form,
                  nama:e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Username"
              value={form.username}
              onChange={(e)=>
                setForm({
                  ...form,
                  username:e.target.value
                })
              }
            />

            <input
              className="form-control"
              placeholder="Password"
              value={form.password}
              onChange={(e)=>
                setForm({
                  ...form,
                  password:e.target.value
                })
              }
            />

            <select
              className="form-control"
              value={form.level}
              onChange={(e)=>
                setForm({
                  ...form,
                  level:e.target.value
                })
              }
            >
              <option value="">
                Pilih Level
              </option>

              <option value="admin">
                Admin
              </option>

              <option value="dokter">
                Dokter
              </option>

              <option value="perawat">
                Perawat
              </option>

            </select>

            <button
              className="btn-primary"
              onClick={simpanUser}
            >
              {editId ? 'Update' : 'Simpan'}
            </button>

          </div>

          <table className="data-table">

            <thead>

              <tr>
                <th>ID</th>
                <th>Nama</th>
                <th>Username</th>
                <th>Password</th>
                <th>Level</th>
                <th>Aksi</th>
              </tr>

            </thead>

            <tbody>

              {users.map((item)=>(

                <tr key={item.id}>

                  <td>{item.id}</td>
                  <td>{item.nama}</td>
                  <td>{item.username}</td>
                  <td>{item.password}</td>
                  <td>{item.level}</td>

                  <td>

                    <button
                      className="btn-edit"
                      onClick={() => {

                        setEditId(item.id)

                        setForm({
                          nama:item.nama,
                          username:item.username,
                          password:item.password,
                          level:item.level
                        })

                      }}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-danger"
                      onClick={() =>
                        hapusUser(item.id)
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

export default Users