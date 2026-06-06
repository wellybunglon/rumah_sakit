import './App.css'

import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from 'react-router-dom'

import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import Pasien from './pages/Pasien'
import TenagaMedis from './pages/TenagaMedis'
import Ruangan from './pages/Ruangan'
import Poliklinik from './pages/Poliklinik'
import Registrasi from './pages/Registrasi'
import RekamMedis from './pages/RekamMedis'
import RawatInap from './pages/RawatInap'
import Billing from './pages/Billing'
import JadwalDokter from './pages/JadwalDokter'
import Users from './pages/Users'
import Farmasi from './pages/Farmasi'
import Logistik from './pages/Logistik'

function App() {

  return (
    <BrowserRouter>

      <Routes>

        {/* Halaman awal diarahkan ke login */}
        <Route
          path="/"
          element={<Navigate to="/login" />}
        />

        {/* Login */}
        <Route
          path="/login"
          element={<Login />}
        />

        {/* Dashboard */}
        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        {/* Data Pasien */}
        <Route
          path="/pasien"
          element={<Pasien />}
        />

        {/* Tenaga Medis */}
        <Route
          path="/tenaga-medis"
          element={<TenagaMedis />}
        />

        {/* Ruangan */}
        <Route
          path="/ruangan"
          element={<Ruangan />}
        />
       
        {/* Poliklinik */}
        <Route
          path="/poliklinik"
          element={<Poliklinik />}
        />
       
        {/* Registrasi */}
        <Route
          path="/registrasi"
          element={<Registrasi />}
        />
        
        {/* RekamMedis */}
        <Route
          path="/rekam-medis"
          element={<RekamMedis />}
        />
       
        {/* RawatInap */}
        <Route
          path="/rawat-inap"
          element={<RawatInap />}
        />
        
        {/* Billing */}
        <Route
          path="/billing"
          element={<Billing />}
        />
        
        {/* JadwalDokter */}
        <Route
          path="/jadwal-dokter"
          element={<JadwalDokter />}
        />
       
        {/* Users */}
        <Route
          path="/users"
          element={<Users />}
        />
        
        {/* Farmasi */}
        <Route
          path="/farmasi"
          element={<Farmasi />}
        />
        
        {/* Logistik */}
        <Route
          path="/logistik"
          element={<Logistik />}
        />

      </Routes>

    </BrowserRouter>
  )
}

export default App