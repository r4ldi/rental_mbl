from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

class Mobil(Base):
    __tablename__ = 'mobil'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100), nullable=False)
    merk = Column(String(100), nullable=False)
    tahun = Column(Integer, nullable=False)
    kapasitas = Column(Integer, nullable=False)
    tipe_transmisi = Column(String(50), nullable=False)
    harga = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default='Tersedia')
    jumlah = Column(Integer, nullable=False, default=1)  # Tambahkan atribut jumlah

    # Relasi ke tabel transaksi
    transaksi = relationship('Transaksi', back_populates='mobil')

class Penyewa(Base):
    __tablename__ = 'penyewa'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nik = Column(String(16), nullable=False)  # NIK
    nama = Column(String(100), nullable=False)
    tempat_tanggal_lahir = Column(String(100), nullable=False)  # Tempat dan tanggal lahir
    jenis_kelamin = Column(String(10), nullable=False)  # Laki-laki/Perempuan
    alamat = Column(String(255), nullable=False)
    rt_rw = Column(String(20), nullable=False)
    kel_desa = Column(String(100), nullable=False)
    kecamatan = Column(String(100), nullable=False)
    pekerjaan = Column(String(100), nullable=False)
    no_identitas = Column(String(50), nullable=False)  # Kartu pelajar atau NPWP
    kontak = Column(String(15), nullable=False)  # Kontak penyewa (baru)

    # Relasi ke tabel transaksi
    transaksi = relationship('Transaksi', back_populates='penyewa')

class Transaksi(Base):
    __tablename__ = 'transaksi'
    id = Column(Integer, primary_key=True, autoincrement=True)
    penyewa_id = Column(Integer, ForeignKey('penyewa.id'))
    mobil_id = Column(Integer, ForeignKey('mobil.id'))
    tanggal_sewa = Column(DateTime, default=datetime.utcnow)
    durasi = Column(Integer, nullable=False)
    jarak_tempuh = Column(Integer, nullable=False)  # Tambahkan kolom jarak tempuh
    total_bayar = Column(Integer, nullable=False)

    # Relasi ke tabel penyewa dan mobil
    penyewa = relationship('Penyewa', back_populates='transaksi')
    mobil = relationship('Mobil', back_populates='transaksi')