from auth import login, register
from models import Mobil, Penyewa, Transaksi, User
from database import SessionLocal
from datetime import datetime

def admin_menu():
    session = SessionLocal()
    while True:
        print("\n=== Menu Admin ===")
        print("1. Kelola Mobil")
        print("2. Kelola Penyewa")
        print("3. Lihat Laporan")
        print("4. Logout")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            kelola_mobil(session)
        elif pilihan == "2":
            kelola_penyewa(session)
        elif pilihan == "3":
            lihat_laporan(session)
        elif pilihan == "4":
            break
        else:
            print("Pilihan tidak valid.")
    session.close()

def penyewa_menu(penyewa):
    session = SessionLocal()
    while True:
        print(f"\n=== Menu Penyewa ({penyewa.nama}) ===")
        print("1. Cari Mobil")
        print("2. Sewa Mobil")
        print("3. Lihat Riwayat")
        print("4. Logout")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            cari_mobil(session)
        elif pilihan == "2":
            sewa_mobil(session, penyewa)
        elif pilihan == "3":
            lihat_riwayat(session, penyewa)
        elif pilihan == "4":
            break
        else:
            print("Pilihan tidak valid.")
    session.close()

def kelola_mobil(session):
    while True:
        print("\n--- Kelola Mobil ---")
        print("1. Tambah Mobil")
        print("2. Hapus Mobil")
        print("3. Lihat Semua Mobil")
        print("4. Kembali")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            nama = input("Nama Mobil: ")
            harga = int(input("Harga Sewa per Hari: "))
            mobil = Mobil(nama=nama, harga=harga, status="Tersedia")
            session.add(mobil)
            session.commit()
            print("Mobil berhasil ditambahkan.")
        elif pilihan == "2":
            id_mobil = int(input("ID Mobil yang akan dihapus: "))
            mobil = session.query(Mobil).get(id_mobil)
            if mobil:
                session.delete(mobil)
                session.commit()
                session.execute("ALTER TABLE mobil AUTO_INCREMENT = 1")  # Reset ID
                session.commit()
                print("Mobil berhasil dihapus.")
            else:
                print("Mobil tidak ditemukan.")
        elif pilihan == "3":
            mobil_list = session.query(Mobil).all()
            for m in mobil_list:
                print(f"{m.id}. {m.nama} - {m.harga} - {m.status}")
        elif pilihan == "4":
            break

def kelola_penyewa(session):
    penyewa_list = session.query(Penyewa).all()
    print("\n--- Daftar Penyewa ---")
    for p in penyewa_list:
        print(f"{p.id}. {p.nama} - {p.kontak}")

def lihat_laporan(session):
    transaksi_list = session.query(Transaksi).all()
    total = 0
    print("\n--- Laporan Transaksi ---")
    for t in transaksi_list:
        print(f"ID: {t.id}, Penyewa: {t.penyewa.nama}, Mobil: {t.mobil.nama}, Total: {t.total_bayar}")
        total += t.total_bayar
    print(f"Total Pendapatan: {total}")

def cari_mobil(session):
    keyword = input("Masukkan kata kunci: ")
    mobil_list = session.query(Mobil).filter(Mobil.nama.like(f"%{keyword}%")).all()
    print("\n--- Hasil Pencarian ---")
    for m in mobil_list:
        print(f"{m.id}. {m.nama} - {m.harga} - {m.status}")

def sewa_mobil(session, penyewa):
    cari_mobil(session)
    id_mobil = int(input("Pilih ID Mobil yang ingin disewa: "))
    mobil = session.query(Mobil).get(id_mobil)
    if mobil and mobil.status == "Tersedia":
        durasi = int(input("Durasi sewa (hari): "))
        total = durasi * mobil.harga
        print(f"Total bayar: {total}")
        konfirmasi = input("Lanjutkan (y/n)? ")
        if konfirmasi.lower() == 'y':
            transaksi = Transaksi(
                penyewa_id=penyewa.id,
                mobil_id=mobil.id,
                durasi=durasi,
                total_bayar=total,
                tanggal_sewa=datetime.now()
            )
            mobil.status = "Disewa"
            session.add(transaksi)
            session.commit()
            print("Sewa berhasil.")
    else:
        print("Mobil tidak tersedia.")

def lihat_riwayat(session, penyewa):
    transaksi_list = session.query(Transaksi).filter_by(penyewa_id=penyewa.id).all()
    print("\n--- Riwayat Sewa ---")
    for t in transaksi_list:
        print(f"Mobil: {t.mobil.nama}, Tanggal: {t.tanggal_sewa}, Durasi: {t.durasi}, Total: {t.total_bayar}")
