from flask import Flask, render_template, request, redirect, session
from mysql.connector.errors import OperationalError
from flask import jsonify
from flask_cors import CORS

from dotenv import load_dotenv
import os


# import koneksi database
from database import db, cursor


# membuat object flask
load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
)
# =========================
# FIX SESSION & COOKIE (PENTING UNTUK REACT)
# =========================
app.config['SECRET_KEY'] = 'rs_sehat'
app.config['SESSION_PERMANENT'] = False

app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
)

# ================================
# FIX SESSION + CORS (TAMBAHAN)
# ================================
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

app.secret_key = 'rs_sehat'

# ==================================
# CEK LOGIN
# ==================================
def cek_login():

    if 'login' not in session:
        return False

    return True


# ==================================
# CEK LEVEL AKSES
# ==================================
def cek_level(roles):

    if 'login' not in session:
        return False

    if session['level'] not in roles:
        return False

    return True

# ==================================
# API LOGIN REACT
# ==================================
@app.route('/api/login', methods=['POST'])
def api_login():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    cursor.execute("""
        SELECT * FROM users
        WHERE username=%s
        AND password=%s
    """, (username, password))

    user = cursor.fetchone()

    if user:

        session.clear()

        session['login'] = True
        session['id'] = user[0]
        session['nama'] = user[1]
        session['username'] = user[2]
        session['level'] = user[4]

        return jsonify({
            "success": True,
            "nama": user[1],
            "level": user[4]
        })

    return jsonify({
        "success": False,
        "message": "Username atau Password Salah"
    }), 401

# ==================================
# API CEK USER LOGIN
# ==================================
@app.route('/api/me')
def me():

    if 'login' not in session:
        return jsonify({
            "login": False
        })

    return jsonify({
        "login": True,
        "nama": session['nama'],
        "level": session['level']
    })

# ==================================
# API DASHBOARD UNTUK REACT
# ==================================
@app.route('/api/dashboard')
def api_dashboard():

    try:

        cursor.execute("SELECT COUNT(*) FROM pasien")
        total_pasien = cursor.fetchone()[0]

        print("TOTAL PASIEN =", total_pasien)

        cursor.execute("SELECT COUNT(*) FROM tenaga_medis")
        total_medis = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM ruangan")
        total_ruangan = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM obat")
        total_obat = cursor.fetchone()[0]

        return jsonify({
            "pasien": total_pasien,
            "medis": total_medis,
            "ruangan": total_ruangan,
            "obat": total_obat
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    
# ==================================
# API PASIEN
# ==================================
@app.route('/api/pasien')
def api_pasien():

    cursor.execute("""
        SELECT * FROM pasien
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:
        hasil.append({
            "id": row[0],
            "nama": row[1],
            "umur": row[2],
            "alamat": row[3],
            "penyakit": row[4]
        })

    return jsonify(hasil)

# ============================
# TAMBAH PASIEN
# ============================
@app.route('/api/pasien', methods=['POST'])
def tambah_pasien_api():

    data = request.json

    sql = """
    INSERT INTO pasien
    (
        nama,
        umur,
        alamat,
        penyakit
    )
    VALUES (%s,%s,%s,%s)
    """

    value = (
        data['nama'],
        data['umur'],
        data['alamat'],
        data['penyakit']
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Pasien berhasil ditambah"
    })

# EDIT PASIEN
# ============================
# EDIT PASIEN
# ============================
@app.route('/api/pasien/<int:id>', methods=['PUT'])
def edit_pasien_api(id):

    data = request.json

    sql = """
    UPDATE pasien
    SET
        nama=%s,
        umur=%s,
        alamat=%s,
        penyakit=%s
    WHERE id=%s
    """

    value = (
        data['nama'],
        data['umur'],
        data['alamat'],
        data['penyakit'],
        id
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Pasien berhasil diupdate"
    })


# hapus pasien
@app.route('/api/pasien/<int:id>', methods=['DELETE'])
def hapus_pasien_api(id):

    cursor.execute(
        "DELETE FROM pasien WHERE id=%s",
        (id,)
    )

    db.commit()

    return jsonify({
        "message": "Pasien berhasil dihapus"
    })

# ==================================
# API TENAGA MEDIS
# ==================================
@app.route('/api/tenaga_medis')
def api_tenaga_medis():

    cursor.execute("""
        SELECT * FROM tenaga_medis
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:

        hasil.append({
            "id": row[0],
            "nama": row[1],
            "profesi": row[2],
            "spesialis": row[3],
            "no_hp": row[4]
        })

    return jsonify(hasil)

# TAMBAH TENAGA MEDIS
@app.route(
    '/api/tenaga_medis',
    methods=['POST']
)
def tambah_tenaga_medis_api():

    data = request.json

    sql = """
    INSERT INTO tenaga_medis
    (
        nama,
        profesi,
        spesialis,
        no_hp
    )
    VALUES (%s,%s,%s,%s)
    """

    value = (
        data['nama'],
        data['profesi'],
        data['spesialis'],
        data['no_hp']
    )

    cursor.execute(sql, value)

    db.commit()

    return jsonify({
        "message": "Berhasil"
    })

# EDIT TENAGA MEDIS
@app.route('/api/tenaga_medis/<int:id>', methods=['PUT'])
def edit_tenaga_medis_api(id):

    data = request.json

    sql = """
    UPDATE tenaga_medis
    SET
        nama=%s,
        profesi=%s,
        spesialis=%s,
        no_hp=%s
    WHERE id=%s
    """

    value = (
        data['nama'],
        data['profesi'],
        data['spesialis'],
        data['no_hp'],
        id
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Tenaga Medis berhasil diupdate"
    })


# HAPUS TENAGA MEDIS
@app.route(
    '/api/tenaga_medis/<int:id>',
    methods=['DELETE']
)
def hapus_tenaga_medis_api(id):

    cursor.execute(
        """
        DELETE FROM tenaga_medis
        WHERE id=%s
        """,
        (id,)
    )

    db.commit()

    return jsonify({
        "message": "Berhasil dihapus"
    })
# ==================================
# API RUANGAN
# ==================================
@app.route('/api/ruangan')
def api_ruangan():

    cursor.execute("""
        SELECT * FROM ruangan
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:

        hasil.append({
            "id": row[0],
            "nama_ruangan": row[1],
            "jenis_ruangan": row[2],
            "kapasitas": row[3],
            "status_ruangan": row[4]
        })

    return jsonify(hasil)

# TAMBAH RUANGAN
@app.route(
    '/api/ruangan',
    methods=['POST']
)
def tambah_ruangan_api():

    data = request.json

    sql = """
    INSERT INTO ruangan
    (
        nama_ruangan,
        jenis_ruangan,
        kapasitas,
        status_ruangan
    )
    VALUES (%s,%s,%s,%s)
    """

    value = (
        data['nama_ruangan'],
        data['jenis_ruangan'],
        data['kapasitas'],
        data['status_ruangan']
    )

    cursor.execute(sql, value)

    db.commit()

    return jsonify({
        "message": "Berhasil"
    })

# EDIT RUANGAN
@app.route('/api/ruangan/<int:id>', methods=['PUT'])
def edit_ruangan_api(id):

    data = request.json

    sql = """
    UPDATE ruangan
    SET
        nama_ruangan=%s,
        jenis_ruangan=%s,
        kapasitas=%s,
        status_ruangan=%s
    WHERE id=%s
    """

    value = (
        data['nama_ruangan'],
        data['jenis_ruangan'],
        data['kapasitas'],
        data['status_ruangan'],
        id
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Ruangan berhasil diupdate"
    })



# HAPUS RUANGAN
@app.route(
    '/api/ruangan/<int:id>',
    methods=['DELETE']
)
def hapus_ruangan_api(id):

    cursor.execute(
        """
        DELETE FROM ruangan
        WHERE id=%s
        """,
        (id,)
    )

    db.commit()

    return jsonify({
        "message": "Berhasil dihapus"
    })


# ==================================
# API POLIKLINIK
# ==================================
@app.route('/api/poliklinik')
def api_poliklinik():

    cursor.execute("""
        SELECT * FROM poliklinik
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:

        hasil.append({
            "id": row[0],
            "nama_poli": row[1],
            "dokter_penanggung_jawab": row[2],
            "jadwal_praktek": row[3],
            "lokasi_ruangan": row[4]
        })

    return jsonify(hasil)



# TAMBAH POLIKLINIK
@app.route(
    '/api/poliklinik',
    methods=['POST']
)
def tambah_poliklinik_api():

    data = request.json

    sql = """
    INSERT INTO poliklinik
    (
        nama_poli,
        dokter_penanggung_jawab,
        jadwal_praktek,
        lokasi_ruangan
    )
    VALUES (%s,%s,%s,%s)
    """

    value = (
        data['nama_poli'],
        data['dokter_penanggung_jawab'],
        data['jadwal_praktek'],
        data['lokasi_ruangan']
    )

    cursor.execute(sql, value)

    db.commit()

    return jsonify({
        "message": "Berhasil"
    })

# EDIT POLIKLINIK
@app.route('/api/poliklinik/<int:id>', methods=['PUT'])
def edit_poliklinik_api(id):

    data = request.json

    sql = """
    UPDATE poliklinik
    SET
        nama_poli=%s,
        dokter_penanggung_jawab=%s,
        jadwal_praktek=%s,
        lokasi_ruangan=%s
    WHERE id=%s
    """

    value = (
        data['nama_poli'],
        data['dokter_penanggung_jawab'],
        data['jadwal_praktek'],
        data['lokasi_ruangan'],
        id
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Poliklinik berhasil diupdate"
    })



# HAPUS POLIKLINIK
@app.route(
    '/api/poliklinik/<int:id>',
    methods=['DELETE']
)
def hapus_poliklinik_api(id):

    cursor.execute(
        """
        DELETE FROM poliklinik
        WHERE id=%s
        """,
        (id,)
    )

    db.commit()

    return jsonify({
        "message": "Berhasil dihapus"
    })

# ==================================
# API REGISTRASI
# ==================================
@app.route('/api/registrasi')
def api_registrasi():

    cursor.execute("""
        SELECT * FROM registrasi
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:

        hasil.append({
            "id": row[0],
            "nama_pasien": row[1],
            "poli_tujuan": row[2],
            "tanggal_kunjungan": row[3],
            "keluhan": row[4]
        })

    return jsonify(hasil)



# TAMBAH REGISTRASI
@app.route(
    '/api/registrasi',
    methods=['POST']
)
def tambah_registrasi_api():

    data = request.json

    sql = """
    INSERT INTO registrasi
    (
        nama_pasien,
        poli_tujuan,
        tanggal_kunjungan,
        keluhan
    )
    VALUES (%s,%s,%s,%s)
    """

    value = (
        data['nama_pasien'],
        data['poli_tujuan'],
        data['tanggal_kunjungan'],
        data['keluhan']
    )

    cursor.execute(sql, value)

    db.commit()

    return jsonify({
        "message": "Berhasil"
    })

# EDIT REGISTRASI
@app.route('/api/registrasi/<int:id>', methods=['PUT'])
def edit_registrasi_api(id):

    data = request.json

    sql = """
    UPDATE registrasi
    SET
        nama_pasien=%s,
        poli_tujuan=%s,
        tanggal_kunjungan=%s,
        keluhan=%s
    WHERE id=%s
    """

    value = (
        data['nama_pasien'],
        data['poli_tujuan'],
        data['tanggal_kunjungan'],
        data['keluhan'],
        id
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Registrasi berhasil diupdate"
    })



# HAPUS REGISTRASI
@app.route(
    '/api/registrasi/<int:id>',
    methods=['DELETE']
)
def hapus_registrasi_api(id):

    cursor.execute(
        """
        DELETE FROM registrasi
        WHERE id=%s
        """,
        (id,)
    )

    db.commit()

    return jsonify({
        "message": "Berhasil dihapus"
    })

# ==================================
# API REKAM MEDIS
# ==================================

@app.route('/api/rekam_medis')
def api_rekam_medis():

    cursor.execute("""
        SELECT * FROM rekam_medis
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:

        hasil.append({
            "id": row[0],
            "nama_pasien": row[1],
            "diagnosa": row[2],
            "tindakan": row[3],
            "resep_obat": row[4],
            "tanggal": str(row[5]) if row[5] else ""
        })

    return jsonify(hasil)


# ==================================
# TAMBAH REKAM MEDIS
# ==================================

@app.route(
    '/api/rekam_medis',
    methods=['POST']
)
def tambah_rekam_medis_api():

    try:

        data = request.json

        sql = """
        INSERT INTO rekam_medis
        (
            nama_pasien,
            diagnosa,
            tindakan,
            resep_obat,
            tanggal
        )
        VALUES (%s,%s,%s,%s,%s)
        """

        value = (
            data['nama_pasien'],
            data['diagnosa'],
            data['tindakan'],
            data['resep_obat'],
            data['tanggal']
        )

        cursor.execute(sql, value)
        db.commit()

        return jsonify({
            "success": True,
            "message": "Data berhasil disimpan"
        })

    except Exception as e:

        print("ERROR TAMBAH REKAM MEDIS =", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==================================
# EDIT REKAM MEDIS
# ==================================

@app.route(
    '/api/rekam_medis/<int:id>',
    methods=['PUT']
)
def edit_rekam_medis_api(id):

    try:

        data = request.json

        sql = """
        UPDATE rekam_medis
        SET
            nama_pasien=%s,
            diagnosa=%s,
            tindakan=%s,
            resep_obat=%s,
            tanggal=%s
        WHERE id=%s
        """

        value = (
            data['nama_pasien'],
            data['diagnosa'],
            data['tindakan'],
            data['resep_obat'],
            data['tanggal'],
            id
        )

        cursor.execute(sql, value)
        db.commit()

        return jsonify({
            "success": True,
            "message": "Data berhasil diupdate"
        })

    except Exception as e:

        print("ERROR EDIT REKAM MEDIS =", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==================================
# HAPUS REKAM MEDIS
# ==================================

@app.route(
    '/api/rekam_medis/<int:id>',
    methods=['DELETE']
)
def hapus_rekam_medis_api(id):

    cursor.execute(
        """
        DELETE FROM rekam_medis
        WHERE id=%s
        """,
        (id,)
    )

    db.commit()

    return jsonify({
        "success": True,
        "message": "Data berhasil dihapus"
    })

# ==================================
# API RAWAT INAP
# ==================================
@app.route('/api/rawat_inap')
def api_rawat_inap():

    cursor.execute("""
        SELECT * FROM rawat_inap
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:

        hasil.append({
            "id": row[0],
            "nama_pasien": row[1],
            "nama_ruangan": row[2],
            "tanggal_masuk": str(row[3]) if row[3] else "",
            "tanggal_keluar": str(row[4]) if row[4] else "",
            "status_pasien": row[5]
        })

    return jsonify(hasil)


# ==================================
# TAMBAH RAWAT INAP
# ==================================
@app.route(
    '/api/rawat_inap',
    methods=['POST']
)
def tambah_rawat_inap_api():

    try:

        data = request.json

        sql = """
        INSERT INTO rawat_inap
        (
            nama_pasien,
            nama_ruangan,
            tanggal_masuk,
            tanggal_keluar,
            status_pasien
        )
        VALUES (%s,%s,%s,%s,%s)
        """

        value = (
            data['nama_pasien'],
            data['nama_ruangan'],
            data['tanggal_masuk'],
            data['tanggal_keluar'],
            data['status_pasien']
        )

        cursor.execute(sql, value)
        db.commit()

        return jsonify({
            "success": True,
            "message": "Data berhasil disimpan"
        })

    except Exception as e:

        print("ERROR TAMBAH RAWAT INAP =", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==================================
# EDIT RAWAT INAP
# ==================================
@app.route(
    '/api/rawat_inap/<int:id>',
    methods=['PUT']
)
def edit_rawat_inap_api(id):

    try:

        data = request.json

        sql = """
        UPDATE rawat_inap
        SET
            nama_pasien=%s,
            nama_ruangan=%s,
            tanggal_masuk=%s,
            tanggal_keluar=%s,
            status_pasien=%s
        WHERE id=%s
        """

        value = (
            data['nama_pasien'],
            data['nama_ruangan'],
            data['tanggal_masuk'],
            data['tanggal_keluar'],
            data['status_pasien'],
            id
        )

        cursor.execute(sql, value)
        db.commit()

        return jsonify({
            "success": True,
            "message": "Data berhasil diupdate"
        })

    except Exception as e:

        print("ERROR EDIT RAWAT INAP =", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==================================
# HAPUS RAWAT INAP
# ==================================
@app.route(
    '/api/rawat_inap/<int:id>',
    methods=['DELETE']
)
def hapus_rawat_inap_api(id):

    try:

        cursor.execute(
            """
            DELETE FROM rawat_inap
            WHERE id=%s
            """,
            (id,)
        )

        db.commit()

        return jsonify({
            "success": True,
            "message": "Data berhasil dihapus"
        })

    except Exception as e:

        print("ERROR HAPUS RAWAT INAP =", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==================================
# API BILLING
# ==================================
@app.route('/api/billing')
def api_billing():

    cursor.execute("""
        SELECT * FROM billing
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:

        hasil.append({
            "id": row[0],
            "nama_pasien": row[1],
            "layanan": row[2],
            "total_tagihan": row[3],
            "status_pembayaran": row[4],
            "tanggal": str(row[5]) if row[5] else ""
        })

    return jsonify(hasil)


# ==================================
# TAMBAH BILLING
# ==================================
@app.route('/api/billing', methods=['POST'])
def tambah_billing_api():

    data = request.json

    sql = """
    INSERT INTO billing
    (
        nama_pasien,
        layanan,
        total_tagihan,
        status_pembayaran,
        tanggal
    )
    VALUES (%s,%s,%s,%s,%s)
    """

    value = (
        data['nama_pasien'],
        data['layanan'],
        data['total_tagihan'],
        data['status_pembayaran'],
        data['tanggal']
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Data Billing Berhasil Ditambahkan"
    })


# ==================================
# EDIT BILLING
# ==================================
@app.route('/api/billing/<int:id>', methods=['PUT'])
def edit_billing_api(id):

    data = request.json

    sql = """
    UPDATE billing
    SET
        nama_pasien=%s,
        layanan=%s,
        total_tagihan=%s,
        status_pembayaran=%s,
        tanggal=%s
    WHERE id=%s
    """

    value = (
        data['nama_pasien'],
        data['layanan'],
        data['total_tagihan'],
        data['status_pembayaran'],
        data['tanggal'],
        id
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Data Billing Berhasil Diupdate"
    })


# ==================================
# HAPUS BILLING
# ==================================
@app.route('/api/billing/<int:id>', methods=['DELETE'])
def hapus_billing_api(id):

    cursor.execute(
        """
        DELETE FROM billing
        WHERE id=%s
        """,
        (id,)
    )

    db.commit()

    return jsonify({
        "message": "Data Billing Berhasil Dihapus"
    })


# ==================================
# API JADWAL DOKTER
# ==================================
@app.route('/api/jadwal_dokter')
def api_jadwal_dokter():

    cursor.execute("""
        SELECT * FROM jadwal_dokter
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:

        hasil.append({
            "id": row[0],
            "nama_dokter": row[1],
            "spesialis": row[2],
            "hari": row[3],
            "jam_praktek": row[4],
            "ruangan": row[5]
        })

    return jsonify(hasil)


# ==================================
# TAMBAH JADWAL DOKTER
# ==================================
@app.route(
    '/api/jadwal_dokter',
    methods=['POST']
)
def tambah_jadwal_dokter_api():

    data = request.json

    sql = """
    INSERT INTO jadwal_dokter
    (
        nama_dokter,
        spesialis,
        hari,
        jam_praktek,
        ruangan
    )
    VALUES (%s,%s,%s,%s,%s)
    """

    value = (
        data['nama_dokter'],
        data['spesialis'],
        data['hari'],
        data['jam_praktek'],
        data['ruangan']
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Jadwal dokter berhasil ditambahkan"
    })


# ==================================
# EDIT JADWAL DOKTER
# ==================================
@app.route(
    '/api/jadwal_dokter/<int:id>',
    methods=['PUT']
)
def edit_jadwal_dokter_api(id):

    data = request.json

    sql = """
    UPDATE jadwal_dokter
    SET
        nama_dokter=%s,
        spesialis=%s,
        hari=%s,
        jam_praktek=%s,
        ruangan=%s
    WHERE id=%s
    """

    value = (
        data['nama_dokter'],
        data['spesialis'],
        data['hari'],
        data['jam_praktek'],
        data['ruangan'],
        id
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Jadwal dokter berhasil diupdate"
    })


# ==================================
# HAPUS JADWAL DOKTER
# ==================================
@app.route(
    '/api/jadwal_dokter/<int:id>',
    methods=['DELETE']
)
def hapus_jadwal_dokter_api(id):

    cursor.execute(
        """
        DELETE FROM jadwal_dokter
        WHERE id=%s
        """,
        (id,)
    )

    db.commit()

    return jsonify({
        "message": "Jadwal dokter berhasil dihapus"
    })


# ==================================
# API USERS
# ==================================
@app.route('/api/users')
def api_users():

    cursor.execute("""
        SELECT * FROM users
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:

        hasil.append({
              "id": row[0],
              "nama": row[1],
              "username": row[2],
              "password": "********",
              "level": row[4]
        })

    return jsonify(hasil)

# TAMBAH USERS
@app.route('/api/users', methods=['POST'])
def tambah_users_api():

    data = request.json

    sql = """
    INSERT INTO users
    (
        nama,
        username,
        password,
        level
    )
    VALUES (%s,%s,%s,%s)
    """

    value = (
        data['nama'],
        data['username'],
        data['password'],
        data['level']
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Berhasil"
    })

# EDIT USERS
@app.route('/api/users/<int:id>', methods=['PUT'])
def edit_users_api(id):

    data = request.json


    sql = """
    UPDATE users
    SET
        nama=%s,
        username=%s,
        password=%s,
        level=%s
    WHERE id=%s
    """

    value = (
        data['nama'],
        data['username'],
        data['password'],
        data['level'],
        id
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "User berhasil diupdate"
    })

# HAPUS USERS
@app.route(
    '/api/users/<int:id>',
    methods=['DELETE']
)
def hapus_users_api(id):

    cursor.execute(
        """
        DELETE FROM users
        WHERE id=%s
        """,
        (id,)
    )

    db.commit()

    return jsonify({
        "message": "Berhasil dihapus"
    })

# ==================================
# API OBAT / FARMASI
# ==================================
@app.route('/api/farmasi')
def api_farmasi():

    cursor.execute("""
        SELECT * FROM obat
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:

        hasil.append({
            "id": row[0],
            "nama_obat": row[1],
            "kategori": row[2],
            "stok": row[3],
            "harga": row[4],
            "tanggal_expired": str(row[5]) if row[5] else ""
        })

    return jsonify(hasil)


# ==================================
# TAMBAH OBAT
# ==================================
@app.route('/api/farmasi', methods=['POST'])
def tambah_farmasi_api():

    data = request.json

    sql = """
    INSERT INTO obat
    (
        nama_obat,
        kategori,
        stok,
        harga,
        tanggal_expired
    )
    VALUES (%s,%s,%s,%s,%s)
    """

    value = (
        data['nama_obat'],
        data['kategori'],
        data['stok'],
        data['harga'],
        data['tanggal_expired']
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Data obat berhasil ditambahkan"
    })


# ==================================
# EDIT OBAT
# ==================================
@app.route('/api/farmasi/<int:id>', methods=['PUT'])
def edit_farmasi_api(id):

    data = request.json

    sql = """
    UPDATE obat
    SET
        nama_obat=%s,
        kategori=%s,
        stok=%s,
        harga=%s,
        tanggal_expired=%s
    WHERE id=%s
    """

    value = (
        data['nama_obat'],
        data['kategori'],
        data['stok'],
        data['harga'],
        data['tanggal_expired'],
        id
    )

    cursor.execute(sql, value)
    db.commit()

    return jsonify({
        "message": "Data obat berhasil diupdate"
    })


# ==================================
# HAPUS OBAT
# ==================================
@app.route('/api/farmasi/<int:id>', methods=['DELETE'])
def hapus_farmasi_api(id):

    cursor.execute(
        """
        DELETE FROM obat
        WHERE id=%s
        """,
        (id,)
    )

    db.commit()

    return jsonify({
        "message": "Data obat berhasil dihapus"
    })

# ==================================
# API LOGISTIK
# ==================================
@app.route('/api/logistik')
def api_logistik():

    cursor.execute("""
        SELECT * FROM logistik
    """)

    data = cursor.fetchall()

    hasil = []

    for row in data:

        hasil.append({
            "id": row[0],
            "nama_barang": row[1],
            "kategori": row[2],
            "jumlah": row[3],
            "lokasi_penyimpanan": row[4],
            "kondisi_barang": row[5]
        })

    return jsonify(hasil)


# ==================================
# TAMBAH LOGISTIK
# ==================================
@app.route('/api/logistik', methods=['POST'])
def tambah_logistik_api():

    data = request.json

    sql = """
    INSERT INTO logistik
    (
        nama_barang,
        kategori,
        jumlah,
        lokasi_penyimpana,
        kondisi_barang
    )
    VALUES (%s,%s,%s,%s,%s)
    """

    value = (
        data['nama_barang'],
        data['kategori'],
        data['jumlah'],
        data['lokasi_penyimpanan'],
        data['kondisi_barang']
    )

    cursor.execute(sql, value)

    db.commit()

    return jsonify({
        "message": "Data logistik berhasil ditambahkan"
    })


# ==================================
# EDIT LOGISTIK
# ==================================
@app.route('/api/logistik/<int:id>', methods=['PUT'])
def edit_logistik_api(id):

    data = request.json

    sql = """
    UPDATE logistik
    SET
        nama_barang=%s,
        kategori=%s,
        jumlah=%s,
        lokasi_penyimpana=%s,
        kondisi_barang=%s
    WHERE id=%s
    """

    value = (
        data['nama_barang'],
        data['kategori'],
        data['jumlah'],
        data['lokasi_penyimpanan'],
        data['kondisi_barang'],
        id
    )

    cursor.execute(sql, value)

    db.commit()

    return jsonify({
        "message": "Data logistik berhasil diupdate"
    })


# ==================================
# HAPUS LOGISTIK
# ==================================
@app.route('/api/logistik/<int:id>', methods=['DELETE'])
def hapus_logistik_api(id):

    cursor.execute(
        """
        DELETE FROM logistik
        WHERE id=%s
        """,
        (id,)
    )

    db.commit()

    return jsonify({
        "message": "Data logistik berhasil dihapus"
    })

# ==================================
# DASHBOARD HTML
# ==================================
@app.route('/')
def dashboard():

    if 'login' not in session:
        return redirect('/login')

    return render_template('dashboard.html')

# MENAMPILKAN DATA PASIEN
@app.route('/pasien')
def index():

    if not cek_level(['admin', 'dokter', 'perawat']):
        return 'Akses Ditolak'

    # mengambil semua data dari tabel pasien
    cursor.execute("SELECT * FROM pasien")

    # menyimpan hasil query
    data_pasien = cursor.fetchall()

    # mengirim data ke html
    return render_template(
        'index.html',
        pasien=data_pasien
    )

# =================================
# TAMBAH PASIEN
# =================================
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():

    # jika tombol submit ditekan
    if request.method == 'POST':

        # mengambil data dari form html
        nama = request.form['nama']
        umur = request.form['umur']
        alamat = request.form['alamat']
        penyakit = request.form['penyakit']

        # query insert data   
        sql = """
        INSERT INTO pasien
        (nama, umur, alamat, penyakit)
        VALUES (%s, %s, %s, %s)
        """
        # value yang aman dimasukkan
        value = (nama, umur, alamat, penyakit)

        # menjalankan query
        cursor.execute(sql, value)

        # menyimpan perubahan database
        db.commit()

        # kembali ke halaman utama
        return redirect('/pasien')
    
    # menampilkan halaman tambah pasien
    return render_template('tambah_pasien.html')

# =================================
# EDIT PASIEN
# =================================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    #jika tombol update ditekan
    if request.method == 'POST':

        # mengambil data dari form
        nama = request.form['nama']
        umur = request.form['umur']
        alamat = request.form['alamat']
        penyakit = request.form['penyakit']

        #query update data
        sql = """
        UPDATE pasien
        SET
            nama=%s,
            umur=%s,
            alamat=%s,
            penyakit=%s
        WHERE id=%s
        """

        # value update
        value = (nama, umur, alamat, penyakit, id)

        # menjalankan query
        cursor.execute(sql, value)

        # simpan perubahan
        db.commit()

        # kembali ke halaman utama
        return redirect('/pasien')
    
    # mengambil data berdasarkan id
    cursor.execute("SELECT * FROM pasien WHERE id=%s", (id,))

    # mengambil satu data saja
    pasien = cursor.fetchone()

    # kirim data ke halaman edit
    return render_template(
        'edit_pasien.html',
        pasien=pasien
    )

# ===============================
# HAPUS PASIEN
# ===============================
@app.route('/hapus/<int:id>')
def hapus(id):

    # query hapus data
    cursor.execute(
        "DELETE FROM pasien WHERE id=%s",
        (id,)
    )

    # simpan perubahan
    db.commit()

    # kembali ke halaman utama
    return redirect('/pasien')

# =================================
# HALAMAN TENAGA MEDIS
# =================================
@app.route('/tenaga_medis')
def tenaga_medis():

    # mengambil semua data tenaga medis
    cursor.execute("SELECT * FROM tenaga_medis")

    # menyimpan hasil query
    data_medis = cursor.fetchall()

    # kirim ke html
    return render_template(
        'tenaga_medis.html',
        medis=data_medis
    )

# ================================
# TAMBAH TENAGA MEDIS
# ================================
@app.route('/tambah_medis', methods=['GET', 'POST'])
def tambah_medis():

    # jika form disubmit
    if request.method == 'POST':

        # mengambil data form
        nama = request.form['nama']
        profesi = request.form['profesi']
        spesialis = request.form['spesialis']
        no_hp = request.form['no_hp']

        # query insert
        sql = """
        INSERT INTO tenaga_medis
        (nama, profesi, spesialis, no_hp)
        VALUES (%s, %s, %s, %s)
        """

        value = (nama, profesi, spesialis, no_hp)

        # jalankan query
        cursor.execute(sql, value)

        # simpan perubahan
        db.commit()

        # kembali ke halaman tenaga medis
        return redirect('/tenaga_medis')
    
    return render_template('tambah_medis.html')

# ================================
# EDIT TENAGA MEDIS
# ================================
@app.route('/edit_medis/<int:id>', methods=['GET', 'POST'])
def edit_medis(id):

    # jika tombol update ditekan
    if request.method == 'POST':

        nama = request.form['nama']
        profesi = request.form['profesi']
        spesialis = request.form['spesialis']
        no_hp = request.form['no_hp']

        # query update
        sql = """
        update tenaga_medis
        SET
            nama=%s,
            profesi=%s,
            spesialis=%s,
            no_hp=%s
        WHERE id=%s
        """

        value = (
            nama,
            profesi,
            spesialis,
            no_hp,
            id
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/tenaga_medis')
    
    # mengambil data berdasarkan id
    cursor.execute(
        "SELECT * FROM tenaga_medis WHERE id=%s",
        (id,)
    )

    medis = cursor.fetchone()

    return render_template(
        'edit_medis.html',
        medis=medis
    )

# =================================
# HAPUS TENAGA MEDIS
# =================================
@app.route('/hapus_medis/<int:id>')
def hapus_medis(id):

    #query hapus
    cursor.execute(
        "DELETE FROM tenaga_medis WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect('/tenaga_medis')

# ======================================
# HALAMAN RUANGAN
# ======================================
@app.route('/ruangan')
def ruangan():

    # mengambil semua data ruangan
    cursor.execute("SELECT * FROM ruangan")

    # menyimpan hasil query
    data_ruangan = cursor.fetchall()

    # kirim ke html
    return render_template(
        'ruangan.html',
        ruangan=data_ruangan
    )
# ======================================
# TAMBAH RUANGAN
# ======================================
@app.route('/tambah_ruangan', methods=['GET', 'POST'])
def tambah_ruangan():

    # jika form disubmit
    if request.method == 'POST':

        # mengambil data form
        nama_ruangan = request.form['nama_ruangan']
        jenis_ruangan= request.form['jenis_ruangan']
        kapasitas = request.form['kapasitas']
        status_ruangan = request.form['status_ruangan']

        # query insert
        sql = """
        INSERT INTO ruangan
        (nama_ruangan, jenis_ruangan, kapasitas, status_ruangan)
        VALUES (%s, %s, %s, %s)
        """

        value = (
            nama_ruangan,
            jenis_ruangan,
            kapasitas,
            status_ruangan
        )

        # menjalankan query
        cursor.execute(sql, value)

        # simpan database
        db.commit()

        # kembali ke halaman ruangan
        return redirect('/ruangan')
    
    return render_template('tambah_ruangan.html')

# =====================================
# EDIT RUANGAN
# =====================================
@app.route('/edit_ruangan/<int:id>', methods=['GET', 'POST'])
def edit_ruangan(id):

    # jika tombol update ditekan
    if request.method == 'POST':

        nama_ruangan = request.form['nama_ruangan']
        jenis_ruangan = request.form['jenis_ruangan']
        kapasitas = request.form['kapasitas']
        status_ruangan = request.form['status_ruangan']

        # query update
        sql = """
        UPDATE ruangan
        SET
            nama_ruangan=%s,
            jenis_ruangan=%s,
            kapasitas=%s,
            status_ruangan=%s
        WHERE id=%s
        """

        value = (
            nama_ruangan,
            jenis_ruangan,
            kapasitas,
            status_ruangan,
            id
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/ruangan')
    
    # mengambil data berdasarkan id
    cursor.execute(
        "SELECT * FROM ruangan WHERE id=%s",
        (id,)
    )

    ruang = cursor.fetchone()

    return render_template(
        'edit_ruangan.html',
        ruang=ruang
    )

# ==================================
# HAPUS RUANGAN
# ==================================
@app.route('/hapus_ruangan/<int:id>')
def hapus_ruangan(id):

    # query hapus
    cursor.execute(
        "DELETE FROM ruangan WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect('/ruangan')

# ==================================
# HALAMAN POLIKLINIK
# ==================================
@app.route('/poliklinik')
def poliklinik():

    # mengambil semua data poliklinik
    cursor.execute("SELECT * FROM poliklinik")

    # menyimpan hasil query
    data_poli = cursor.fetchall()

    # kirim ke html
    return render_template(
        'poliklinik.html',
        poli=data_poli
    )

# ==================================
# TAMBAH POLIKLINIK
# ==================================
@app.route('/tambah_poliklinik', methods=['GET', 'POST'])
def tambah_poliklinik():

    # jika form disubmit
    if request.method == 'POST':

        # mengambil data form
        nama_poli = request.form['nama_poli']
        dokter = request.form['dokter']
        jadwal = request.form['jadwal']
        lokasi = request.form['lokasi']

        # query insert
        sql ="""
        INSERT INTO poliklinik
        (nama_poli, dokter_penanggung_jawab,
        jadwal_praktek, lokasi_ruangan)
        VALUES (%s, %s, %s, %s)
        """

        value = (
            nama_poli,
            dokter,
            jadwal,
            lokasi
        )

        # menjalankan query
        cursor.execute(sql, value)

        # simpan database
        db.commit()

        # kembali ke halaman poliklinik
        return redirect('/poliklinik')
    
    return render_template('tambah_poliklinik.html')

# ==================================
# EDIT POLIKLINIK
# ==================================
@app.route('/edit_poliklinik/<int:id>', methods=['GET', 'POST'])
def edit_poliklinik(id):

    # jika tombol update ditekan
    if request.method == 'POST':

        nama_poli = request.form['nama_poli']
        dokter = request.form['dokter']
        jadwal = request.form['jadwal']
        lokasi = request.form['lokasi']

        # query update
        sql = """
        UPDATE poliklinik
        SET
            nama_poli=%s,
            dokter_penanggung_jawab=%s,
            jadwal_praktek=%s,
            lokasi_ruangan=%s
        WHERE id=%s
        """

        value = (
            nama_poli,
            dokter,
            jadwal,
            lokasi,
            id
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/poliklinik')
    
    # mengambil data berdasarkan id
    cursor.execute(
        "SELECT * FROM poliklinik WHERE id=%s",
        (id,)
    )

    poli = cursor.fetchone()

    return render_template(
        'edit_poliklinik.html',
        poli=poli
    )

# ==================================
# HAPUS POLIKLINIK
# ==================================
@app.route('/hapus_poliklinik/<int:id>')
def hapus_poliklinik(id):
    
    # query hapus
    cursor.execute(
        "DELETE FROM poliklinik WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect('/poliklinik')

# ==================================
# HALAMAN REGISTRASI
# ==================================
@app.route('/registrasi')
def registrasi():

    cursor.execute("SELECT * FROM registrasi")

    data = cursor.fetchall()

    return render_template(
        'registrasi.html',
        registrasi=data
    )

# ==================================
# TAMBAH REGISTRASI
# ==================================
@app.route('/tambah_registrasi',
methods=['GET', 'POST'])
def tambah_registrasi():

    if request.method == 'POST':

        nama_pasien = request.form['nama_pasien']
        poli_tujuan = request.form['poli_tujuan']
        tanggal = request.form['tanggal']
        keluhan = request.form['keluhan']

        sql= """
        INSERT INTO registrasi
        (nama_pasien, poli_tujuan, tanggal_kunjungan, keluhan)
        VALUES (%s, %s, %s, %s)
        """

        value = (
            nama_pasien,
            poli_tujuan,
            tanggal,
            keluhan
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/registrasi')
    
    return render_template(
        'tambah_registrasi.html'
    )
# ==================================
# EDIT REGISTRASI
# ==================================
@app.route('/edit_registrasi/<int:id>',
methods=['GET', 'POST'])
def edit_registrasi(id):

    # jika tombol update ditekan
    if request.method == 'POST':

        # mengambil data dari form
        nama_pasien = request.form['nama_pasien']
        poli_tujuan = request.form['poli_tujuan']
        tanggal = request.form['tanggal']
        keluhan = request.form['keluhan']

        # query update
        sql = """
        UPDATE registrasi
        SET
            nama_pasien=%s,
            poli_tujuan=%s,
            tanggal_kunjungan=%s,
            keluhan=%s
        WHERE id=%s
        """

        value =(
            nama_pasien,
            poli_tujuan,
            tanggal,
            keluhan,
            id
        )

        # menjalankan query
        cursor.execute(sql, value)

        # simpan database
        db.commit()

        # kembali ke halaman registrasi
        return redirect('/registrasi')
    
    # mengambil data berdasarkan id
    cursor.execute(
        "SELECT * FROM registrasi WHERE id=%s",
        (id,)
    )

    registrasi = cursor.fetchone()

    return render_template(
        'edit_registrasi.html',
        registrasi=registrasi
    )

# ==================================
# HAPUS REGISTRASI
# ==================================
@app.route('/hapus_registrasi/<int:id>')
def hapus_registrasi(id):

    # query hapus data
    cursor.execute(
        "DELETE FROM registrasi WHERE id=%s",
        (id,)
    )

    # simpan perubahan database
    db.commit()

    # kembali ke halaman registrasi
    return redirect('/registrasi')


# ==================================
# HALAMAN REKAM MEDIS
# ==================================
@app.route('/rekam_medis')
def rekam_medis():

    if not cek_level(['admin', 'dokter']):
        return 'Akses Ditolak'

    cursor.execute(
        "SELECT * FROM rekam_medis"
    )

    data = cursor.fetchall()

    return render_template(
        'rekam_medis.html',
        rekam=data
    )

# ==================================
# TAMBAH REKAM MEDIS
# ==================================
@app.route('/tambah_rekam',
methods=['GET', 'POST'])
def tambah_rekam():

    if request.method == 'POST':

        nama_pasien = request.form['nama_pasien']
        diagnosa = request.form['diagnosa']
        tindakan = request.form['tindakan']
        resep_obat = request.form ['resep_obat']
        tanggal = request.form['tanggal']

        sql = """
        INSERT INTO rekam_medis
        (nama_pasien, diagnosa, tindakan, resep_obat, tanggal)
        VALUES (%s, %s, %s, %s, %s)
        """

        value = (
            nama_pasien,
            diagnosa,
            tindakan,
            resep_obat,
            tanggal
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/rekam_medis')
    
    return render_template(
        'tambah_rekam.html'
    )

# ==================================
# EDIT REKAM MEDIS
# ==================================
@app.route('/edit_rekam/<int:id>',
methods=['GET', 'POST'])
def edit_rekam(id):

    # jika tombol update ditekan
    if request.method == 'POST':

        # mengambil data dari form
        nama_pasien = request.form['nama_pasien']
        diagnosa = request.form['diagnosa']
        tindakan = request.form['tindakan']
        resep = request.form['resep']
        tanggal = request.form['tanggal']

        # query update
        sql = """
        UPDATE rekam_medis
        SET
            nama_pasien=%s,
            diagnosa=%s,
            tindakan=%s,
            resep_obat=%s,
            tanggal=%s
        WHERE id=%s
        """

        value = (
            nama_pasien,
            diagnosa,
            tindakan,
            resep,
            tanggal,
            id
        )

        # menjalankan query
        cursor.execute(sql, value)

        # simpan database
        db.commit()

        # kembali ke halaman rekam medis
        return redirect('/rekam_medis')
    
    # mengambil data berdasarkan id
    cursor.execute(
        "SELECT * FROM rekam_medis WHERE id=%s",
        (id,)
    )
    
    rekam = cursor.fetchone()

    return render_template(
        'edit_rekam.html',
        rekam=rekam
    )

# ==================================
# HAPUS REKAM MEDIS
# ==================================
@app.route('/hapus_rekam/<int:id>')
def hapus_rekam(id):

    # query hapus data
    cursor.execute(
        "DELETE FROM rekam_medis WHERE id=%s",
        (id,)
    )

    # simpan perubahan database
    db.commit()

    # kembali le halaman rekam medis
    return redirect('/rekam_medis')


# ==================================
# HALAMAN PEMERIKSAAN PENUNJANG
# ==================================
@app.route('/penunjang')
def penunjang():

    if not cek_level(['admin', 'dokter', 'perawat']):
        return 'Akses Ditolak'

    cursor.execute(
        "SELECT * FROM pemeriksaan_penunjang"
    )

    data = cursor.fetchall()

    return render_template(
        'penunjang.html',
        penunjang=data
    )

# ==================================
# TAMBAH PEMERIKSAAN
# ==================================
@app.route('/tambah_penunjang',
methods=['GET', 'POST'])
def tambah_penunjang():

    if request.method == 'POST':

        nama_pasien = request.form['nama_pasien']
        jenis = request.form['jenis']
        hasil = request.form['hasil']
        tanggal = request.form['tanggal']

        sql = """
        INSERT INTO pemeriksaan_penunjang
        (nama_pasien,
        jenis_pemeriksaan,
        hasil_pemeriksaan,
        tanggal)
        VALUES (%s, %s, %s, %s)
        """

        value = (
            nama_pasien,
            jenis,
            hasil,
            tanggal
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/penunjang')
    
    return render_template(
        'tambah_penunjang.html'
    )

# ==================================
# EDIT PEMERIKSAAN 
# ==================================
@app.route('/edit_penunjang/<int:id>',
methods=['GET', 'POST'])
def edit_penunjang(id):

    # jika tombol update ditekan
    if request.method == 'POST':

        nama_pasien = request.form['nama_pasien']
        jenis = request.form['jenis']
        hasil = request.form['hasil']
        tanggal = request.form['tanggal']

        # query update
        sql = """
        UPDATE pemeriksaan_penunjang
        SET
            nama_pasien=%s,
            jenis_pemeriksaan=%s,
            hasil_pemeriksaan=%s,
            tanggal=%s
        WHERE id=%s
        """

        value = (
            nama_pasien,
            jenis,
            hasil,
            tanggal,
            id
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/penunjang')
    
    # mengambil data berdasarkan id
    cursor.execute(
        "SELECT * FROM pemeriksaan_penunjang WHERE id=%s",
        (id,)
    )

    data = cursor.fetchone()

    return render_template(
        'edit_penunjang.html',
        penunjang=data
    )

# ==================================
# HAPUS PEMERIKSAAN
# ==================================
@app.route('/hapus_penunjang/<int:id>')
def hapus_penunjang(id):

    # query hapus
    cursor.execute(
        "DELETE FROM pemeriksaan_penunjang WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect('/penunjang')
# ==================================
# HALAMAN RAWAT INAP
# ==================================
@app.route('/rawat_inap')
def rawat_inap():

    if not cek_level(['admin', 'perawat']):
        return 'Akses Ditolak'

    # mengambil data rawat inap
    cursor.execute(
        "SELECT * FROM rawat_inap"
    )

    # mengambil semua data
    data = cursor.fetchall()

    # kirim ke html
    return render_template(
        'rawat_inap.html',
        rawat=data
    )

# ==================================
# TAMBAH RAWAT INAP
# ==================================
@app.route('/tambah_rawat',
methods=['GET', 'POST'])
def tambah_rawat():

    # jika tombol simpan ditekan
    if request.method == 'POST':

        nama_pasien= request.form['nama_pasien']
        ruangan = request.form['ruangan']
        masuk = request.form['masuk']
        keluar = request.form['keluar']
        status = request.form['status']

        # query insert
        sql = """
        INSERT INTO rawat_inap (
        nama_pasien,
        nama_ruangan,
        tanggal_masuk,
        tanggal_keluar,
        status_pasien
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        value = (
            nama_pasien,
            ruangan,
            masuk,
            keluar,
            status
        )

        # menjalankan query
        cursor.execute(sql, value)

        # simpan database
        db.commit()

        # kembali ke halaman rawat inap
        return redirect('/rawat_inap')

    return render_template(
        'tambah_rawat.html'
    )    

# ==================================
# EDIT RAWAT INAP
# ==================================
@app.route('/edit_rawat/<int:id>',
methods=['GET', 'POST'])
def edit_rawat(id):

    # jika update ditekan
    if request.method == 'POST':

        nama_pasien = request.form['nama_pasien']
        ruangan = request.form['ruangan']
        masuk = request.form['masuk']
        keluar = request.form['keluar']
        status = request.form['status']

        # query update
        sql = """
        UPDATE rawat_inap
        SET
            nama_pasien=%s,
            nama_ruangan=%s,
            tanggal_masuk=%s,
            tanggal_keluar=%s,
            status_pasien=%s
        WHERE id=%s
        """

        value = (
            nama_pasien,
            ruangan,
            masuk,
            keluar,
            status,
            id
        )
        
        cursor.execute(sql, value)

        db.commit()

        return redirect('/rawat_inap')
    
    # mengambil data berdasarkan id
    cursor.execute(
        "SELECT * FROM rawat_inap WHERE id=%s",
        (id,)
    )

    rawat = cursor.fetchone()

    return render_template(
        'edit_rawat.html',
        rawat=rawat
    )

# ==================================
# HAPUS RAWAT INAP
# ==================================
@app.route('/hapus_rawat/<int:id>')
def hapus_rawat(id):

    #query hapus
    cursor.execute(
        "DELETE FROM rawat_inap WHERE id=%s",
        (id,)
    )

    # simpan perubahan
    db.commit()

    return redirect('/rawat_inap')

# ==================================
# HALAMAN FARMASI
# ==================================
@app.route('/farmasi')
def formasi():

    if not cek_level(['admin', 'perawat']):
        return 'Akses Ditolak'

    # mengambil data obat
    cursor.execute(
        "SELECT * FROM obat"
    )

    data_obat = cursor.fetchall()

    return render_template(
        'farmasi.html',
        obat=data_obat
    )

# ==================================
# TAMBAH OBAT
# ==================================
@app.route('/tambah_obat',
methods=['GET', 'POST'])
def tambah_obat():

    if request.method == 'POST':

        nama_obat = request.form['nama_obat']
        kategori = request.form['kategori']
        stok = request.form['stok']
        harga = request.form['harga']
        expired = request.form['expired']

        # query insert
        sql = """
        INSERT INTO obat
        (
            nama_obat,
            kategori,
            stok,
            harga,
            tanggal_expired
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        value = (
            nama_obat,
            kategori,
            stok,
            harga,
            expired
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/farmasi')
    
    return render_template(
        'tambah_obat.html'
    )

# ==================================
# EDIT OBAT
# ==================================
@app.route('/edit_obat/<int:id>',
methods=['GET', 'POST'])
def edit_obat(id):

    if request.method == 'POST':

        nama_obat = request.form['nama_obat']
        kategori = request.form['kategori']
        stok = request.form['stok']
        harga = request.form['harga']
        expired = request.form['expired']

        # query update
        sql = """
        UPDATE obat
        SET
            nama_obat=%s,
            kategori=%s,
            stok=%s,
            harga=%s,
            tanggal_expired=%s
        WHERE id=%s
        """

        value = (
            nama_obat,
            kategori,
            stok,
            harga,
            expired,
            id
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/farmasi')
    
    cursor.execute(
        "SELECT * FROM obat WHERE id=%s",
        (id,)
    )

    obat = cursor.fetchone()

    return render_template(
        'edit_obat.html',
        obat=obat
    )

# ==================================
# HAPUS OBAT
# ==================================
@app.route('/hapus_obat/<int:id>')
def hapus_obat(id):

    cursor.execute(
        "DELETE FROM obat WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect('/farmasi')

# ==================================
# HALAMAN LOGISTIK
# ==================================
@app.route('/logistik')
def logistik():

    if not cek_level(['admin']):
        return 'Akses Ditolak'
    
    cursor.execute(
        "SELECT * FROM logistik" 
    )

    data_barang = cursor.fetchall()

    return render_template(
        'logistik.html',
        barang=data_barang
    )

# =================================
# TAMBAH LOGISTIK
# =================================
@app.route('/tambah_logistik',
methods=['GET', 'POST'])
def tambah_logistik():

    # jika form disubmit
    if request.method == 'POST':

        # mengambil data dari form
        nama_barang = request.form['nama_barang']
        kategori = request.form['kategori']
        jumlah = request.form['jumlah']
        lokasi = request.form['lokasi']
        kondisi = request.form['kondisi']

        # query insert
        sql = """
        INSERT INTO logistik
        (
            nama_barang,
            kategori,
            jumlah,
            lokasi_penyimpana,
            kondisi_barang
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        value = (
            nama_barang,
            kategori,
            jumlah,
            lokasi,
            kondisi
        )

        # menjalankan query
        cursor.execute(sql, value)

        # simpan database
        db.commit()

        # kembali ke halaman logistik
        return redirect('/logistik')

    # tampilkan halaman tambah logistik
    return render_template(
        'tambah_logistik.html'
    )

# ==================================
# EDIT LOGISTIK
# ==================================
@app.route('/edit_logistik/<int:id>',
methods=['GET', 'POST'])
def edit_logistik(id):

    # jika tombol update ditekan
    if request.method == 'POST':

        nama_barang = request.form['nama_barang']
        kategori = request.form['kategori']
        jumlah = request.form['jumlah']
        lokasi = request.form['lokasi']
        kondisi = request.form['kondisi']

        # query update
        sql = """
        UPDATE logistik
        SET
            nama_barang=%s,
            kategori=%s,
            jumlah=%s,
            lokasi_penyimpana=%s,
            kondisi_barang=%s
        WHERE id=%s
        """

        value = (
            nama_barang,
            kategori,
            jumlah,
            lokasi,
            kondisi,
            id
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/logistik')
    
    # mengambil data berdasarkan id
    cursor.execute(
        "SELECT * FROM logistik WHERE id=%s",
        (id,)
    )

    barang = cursor.fetchone()

    return render_template(
        'edit_logistik.html',
        barang=barang
    )
# ==================================
# HAPUS LOGISTIK
# ==================================
@app.route('/hapus_logistik/<int:id>')
def hapus_logistik(id):

    cursor.execute(
        "DELETE FROM logistik WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect('/logistik')

# ==================================
# HALAMAN BILLING
# ==================================
@app.route('/billing')
def billing():

    if not cek_level(['admin']):
        return 'Akses Ditolak'
    
    cursor.execute(
        "SELECT * FROM billing"
    )

    data = cursor.fetchall()

    return render_template(
        'billing.html',
        billing=data
    )

# ==================================
# TAMBAH BILLING
# ==================================
@app.route('/tambah_billing',
methods=['GET', 'POST'])
def tambah_billing():

    if request.method == 'POST':

        nama_pasien = request.form['nama_pasien']
        layanan = request.form['layanan']
        total = request.form['total']
        status = request.form['status']
        tanggal = request.form['tanggal']

        sql = """
        INSERT INTO billing
        (
            nama_pasien,
            layanan,
            total_tagihan,
            status_pembayaran,
            tanggal
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        value = (
            nama_pasien,
            layanan,
            total,
            status,
            tanggal
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/billing')

    return render_template(
        'tambah_billing.html'
    )

# ==================================
# EDIT BILLING
# ==================================
@app.route('/edit_billing/<int:id>',
methods=['GET', 'POST'])
def edit_billing(id):

    if request.method == 'POST':

        nama_pasien = request.form['nama_pasien']
        layanan = request.form['layanan']
        total = request.form['total']
        status = request.form['status']
        tanggal = request.form['tanggal']

        sql = """
        UPDATE billing
        SET
            nama_pasien=%s,
            layanan=%s,
            total_tagihan=%s,
            status_pembayaran=%s,
            tanggal=%s
        WHERE id=%s
        """

        value = (
            nama_pasien,
            layanan,
            total,
            status,
            tanggal,
            id
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/billing')

    cursor.execute(
        "SELECT * FROM billing WHERE id=%s",
        (id,)
    )

    bill = cursor.fetchone()

    return render_template(
        'edit_billing.html',
        billing=bill
    )

# ==================================
# HAPUS BILLING
# ==================================
@app.route('/hapus_billing/<int:id>')
def hapus_billing(id):

    cursor.execute(
        "DELETE FROM billing WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect('/billing')

# ==================================
# HALAMAN JADWAL DOKTER
# ==================================
@app.route('/jadwal_dokter')
def jadwal_dokter():

    if not cek_level(['admin', 'dokter']):
        return 'Akses Ditolak'

    cursor.execute(
        "SELECT * FROM jadwal_dokter"
    )

    data = cursor.fetchall()

    return render_template(
        'jadwal_dokter.html',
        jadwal=data
    )

# ==================================
# TAMBAH JADWAL DOKTER
# ==================================
@app.route('/tambah_jadwal',
methods=['GET', 'POST'])
def tambah_jadwal():

    if request.method == 'POST':

        nama_dokter = request.form['nama_dokter']
        spesialis = request.form['spesialis']
        hari = request.form['hari']
        jam = request.form['jam']
        ruangan = request.form['ruangan']

        sql = """
        INSERT INTO jadwal_dokter
        (
            nama_dokter,
            spesialis,
            hari,
            jam_praktek,
            ruangan
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        value = (
            nama_dokter,
            spesialis,
            hari,
            jam,
            ruangan
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/jadwal_dokter')

    return render_template(
        'tambah_jadwal.html'
    )

# ==================================
# EDIT JADWAL DOKTER
# ==================================
@app.route('/edit_jadwal/<int:id>',
methods=['GET', 'POST'])
def edit_jadwal(id):

    if request.method == 'POST':

        nama_dokter = request.form['nama_dokter']
        spesialis = request.form['spesialis']
        hari = request.form['hari']
        jam = request.form['jam']
        ruangan = request.form['ruangan']

        sql = """
        UPDATE jadwal_dokter
        SET
            nama_dokter=%s,
            spesialis=%s,
            hari=%s,
            jam_praktek=%s,
            ruangan=%s
        WHERE id=%s
        """

        value = (
            nama_dokter,
            spesialis,
            hari,
            jam,
            ruangan,
            id
        )

        cursor.execute(sql, value)

        db.commit()

        return redirect('/jadwal_dokter')

    cursor.execute(
        "SELECT * FROM jadwal_dokter WHERE id=%s",
        (id,)
    )

    jadwal = cursor.fetchone()

    return render_template(
        'edit_jadwal.html',
        jadwal=jadwal
    )

# ==================================
# HAPUS JADWAL
# ==================================
@app.route('/hapus_jadwal/<int:id>')
def hapus_jadwal(id):

    cursor.execute(
        "DELETE FROM jadwal_dokter WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect('/jadwal_dokter')

# ==========================
# LOGOUT
# ==========================
@app.route('/api/logout', methods=['POST'])
def api_logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logout berhasil"
    })

# ==================================
# MENJALANKAN FLASK
# ==================================
if __name__ == '__main__':

    app.config['SECRET_KEY'] = 'rs_sehat'
    app.config['SESSION_PERMANENT'] = False

    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000
    )

