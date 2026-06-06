import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function Login() {

  const navigate = useNavigate()

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = async (e) => {

    e.preventDefault()

    try {

      const res = await fetch(
        'http://127.0.0.1:5000/api/login',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            username,
            password
          })
        }
      )

      const data = await res.json()

      if (data.success) {

        localStorage.setItem(
          'user',
          JSON.stringify(data)
        )

        // pindah ke dashboard
        navigate('/dashboard')

      } else {

        alert(data.message)

      }

    } catch (err) {

      console.log(err)
      alert('Gagal terhubung ke server')

    }

  }

  return (
    <div className="login-page">

      <form
        className="login-box"
        onSubmit={handleLogin}
      >

        <h1>🏥 RS SEHAT</h1>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <button type="submit">
          Login
        </button>

      </form>

    </div>
  )
}

export default Login