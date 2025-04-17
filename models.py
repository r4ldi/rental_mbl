from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(10), nullable=False)  # admin / penyewa

class Mobil(Base):
    __tablename__ = 'mobil'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100), nullable=False)
    harga = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default='Tersedia')

class Penyewa(Base):
    __tablename__ = 'penyewa'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100), nullable=False)
    kontak = Column(String(100), nullable=False)

class Transaksi(Base):
    __tablename__ = 'transaksi'
    id = Column(Integer, primary_key=True, autoincrement=True)
    penyewa_id = Column(Integer, ForeignKey('penyewa.id'))
    mobil_id = Column(Integer, ForeignKey('mobil.id'))
    tanggal_sewa = Column(DateTime, default=datetime.utcnow)
    durasi = Column(Integer, nullable=False)
    total_bayar = Column(Integer, nullable=False)

    penyewa = relationship('Penyewa', backref='transaksi')
    mobil = relationship('Mobil', backref='transaksi')
