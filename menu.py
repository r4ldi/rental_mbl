import os
import platform
from sqlalchemy.sql import text
from models import Mobil, Penyewa, Transaksi
from database import SessionLocal
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def clear_screen():
    """
    Membersihkan layar terminal agar lebih rapi.
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def admin_menu():
    session = SessionLocal()
    clear_screen()
    while True:
        console.print(Panel("[bold magenta]=== Menu Admin ===[/bold magenta]\n"
                            "[bold cyan]1.[/bold cyan] Kelola Mobil\n"
                            "[bold cyan]2.[/bold cyan] Input Data Penyewaan\n"
                            "[bold cyan]3.[/bold cyan] Lihat Laporan\n"
                            "[bold cyan]4.[/bold cyan] Selesaikan Penyewaan\n"
                            "[bold cyan]5.[/bold cyan] Lihat Data Penyewa\n"
                            "[bold cyan]6.[/bold cyan] Reset Data (Hapus Semua)\n"
                            "[bold cyan]7.[/bold cyan] Keluar",
                            title="Sistem Rental Mobil CLI", border_style="bold cyan"))

        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            clear_screen()
            kelola_mobil(session)
        elif pilihan == "2":
            input_data_penyewaan(session)
            clear_screen()
        elif pilihan == "3":
            lihat_laporan(session)
            clear_screen()
        elif pilihan == "4":
            selesaikan_penyewaan(session)
            clear_screen()
        elif pilihan == "5":
            lihat_data_penyewa(session)
            clear_screen()
        elif pilihan == "6":
            konfirmasi = input("Apakah Anda yakin ingin menghapus semua data? (y/n): ").strip().lower()
            if konfirmasi == "y":
                reset_data(session)
            else:
                console.print("[bold yellow]Reset data dibatalkan.[/bold yellow]")
        elif pilihan == "7":
            clear_screen()
            break
        else:
            console.print("[bold red]Pilihan tidak valid.[/bold red]")
    session.close()

def kelola_mobil(session):
    while True:
        console.print(Panel("[bold magenta]=== Kelola Mobil ===[/bold magenta]\n"
                            "[bold cyan]1.[/bold cyan] Tambah Mobil\n"
                            "[bold cyan]2.[/bold cyan] Hapus Mobil\n"
                            "[bold cyan]3.[/bold cyan] Edit Mobil\n"
                            "[bold cyan]4.[/bold cyan] Lihat Semua Mobil\n"
                            "[bold cyan]5.[/bold cyan] Cari Mobil\n"
                            "[bold cyan]6.[/bold cyan] Kembali",
                            title="Menu Kelola Mobil", border_style="bold blue"))

        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            clear_screen()
            console.print(Panel("[bold magenta]=== Tambah Mobil ===[/bold magenta]", border_style="bold blue"))
            merk = input("Merk Mobil: ")
            nama = input("Nama Mobil: ")

            # Validasi input tahun
            while True:
                try:
                    tahun = int(input("Tahun Pembuatan: "))
                    break
                except ValueError:
                    console.print("[bold red]Tahun Pembuatan harus berupa angka. Silakan coba lagi.[/bold red]")

            # Validasi input kapasitas
            while True:
                try:
                    kapasitas = int(input("Kapasitas Penumpang: "))
                    break
                except ValueError:
                    console.print("[bold red]Kapasitas Penumpang harus berupa angka. Silakan coba lagi.[/bold red]")

            # Validasi input tipe transmisi
            while True:
                tipe_transmisi = input("Tipe Transmisi (Manual/Otomatis): ").strip().capitalize()
                if tipe_transmisi in ["Manual", "Otomatis"]:
                    break
                else:
                    console.print("[bold red]Tipe Transmisi harus 'Manual' atau 'Otomatis'. Silakan coba lagi.[/bold red]")

            # Validasi input harga
            while True:
                try:
                    harga = int(input("Harga Sewa per Hari: "))
                    break
                except ValueError:
                    console.print("[bold red]Harga Sewa per Hari harus berupa angka. Silakan coba lagi.[/bold red]")

            mobil = Mobil(
                merk=merk,
                nama=nama,
                tahun=tahun,
                kapasitas=kapasitas,
                tipe_transmisi=tipe_transmisi,
                harga=harga,
                status="Tersedia"
            )
            session.add(mobil)
            session.commit()
            console.print("[bold blue]Mobil berhasil ditambahkan![/bold blue]")

        elif pilihan == "2":
            clear_screen()
            console.print(Panel("[bold magenta]=== Hapus Mobil ===[/bold magenta]", border_style="bold red"))
            lihat_semua_mobil(session, pause=False)  # Tampilkan daftar mobil
            try:
                id_mobil = int(input("\nMasukkan ID Mobil yang akan dihapus: "))
                mobil = session.query(Mobil).get(id_mobil)

                if not mobil:
                    console.print("[bold red]Mobil tidak ditemukan.[/bold red]")
                else:
                    # Cek apakah mobil sedang disewa
                    if mobil.status == "Disewa":
                        console.print("[bold yellow]Mobil sedang disewa dan tidak dapat dihapus.[/bold yellow]")
                    else:
                        session.delete(mobil)
                        session.commit()
                        # Reset AUTO_INCREMENT menggunakan text()
                        session.execute(text("ALTER TABLE mobil AUTO_INCREMENT = 1"))
                        session.commit()
                        console.print("[bold blue]Mobil berhasil dihapus.[/bold blue]")
            except ValueError:
                console.print("[bold red]ID Mobil harus berupa angka. Silakan coba lagi.[/bold red]")

        elif pilihan == "3":
            clear_screen()
            console.print(Panel("[bold magenta]=== Edit Mobil ===[/bold magenta]", border_style="bold cyan"))
            edit_mobil(session)

        elif pilihan == "4":
            clear_screen()
            console.print(Panel("[bold magenta]=== Lihat Semua Mobil ===[/bold magenta]", border_style="bold blue"))
            lihat_semua_mobil(session)

        elif pilihan == "5":
            clear_screen()
            console.print(Panel("[bold magenta]=== Cari Mobil ===[/bold magenta]", border_style="bold blue"))
            cari_mobil(session)

        elif pilihan == "6":
            clear_screen()
            break

        else:
            console.print("[bold red]Pilihan tidak valid. Silakan coba lagi.[/bold red]")

            print("Pilihan tidak valid.")

def input_data_penyewaan(session):
    clear_screen()
    console.print(Panel("[bold magenta]=== Input Data Penyewaan ===[/bold magenta]", border_style="bold blue"))

    # Tanya pekerjaan penyewa
    while True:
        status_pekerjaan = input("Apakah penyewa sudah bekerja atau pelajar/mahasiswa? (bekerja/pelajar): ").strip().lower()
        if status_pekerjaan in ["bekerja", "pelajar"]:
            break
        else:
            console.print("[bold red]Input tidak valid. Masukkan 'bekerja' atau 'pelajar'.[/bold red]")

    # Data umum penyewa
    while True:
        nik = input("Masukkan NIK (16 digit): ")
        if nik.isdigit() and len(nik) == 16:
            break
        else:
            console.print("[bold red]NIK harus berupa 16 digit angka.[/bold red]")

    nama = input("Masukkan Nama Penyewa: ")

    while True:
        tempat_tanggal_lahir = input("Masukkan Tempat dan Tanggal Lahir (contoh: BANDUNG, 26-11-2007): ")
        try:
            tempat, tanggal_lahir = tempat_tanggal_lahir.split(", ")
            datetime.strptime(tanggal_lahir, "%d-%m-%Y")  # Validasi format tanggal
            break
        except ValueError:
            console.print("[bold red]Format tempat dan tanggal lahir tidak valid. Contoh: BANDUNG, 26-11-2007.[/bold red]")

    while True:
        jenis_kelamin = input("Masukkan Jenis Kelamin (Laki-laki/Perempuan): ").strip().lower()
        if jenis_kelamin in ["laki-laki", "perempuan"]:
            break
        else:
            console.print("[bold red]Jenis kelamin harus 'Laki-laki' atau 'Perempuan'.[/bold red]")

    alamat = input("Masukkan Alamat: ")

    while True:
        rt_rw = input("Masukkan RT/RW (contoh: 01/02): ")
        if "/" in rt_rw and all(part.isdigit() for part in rt_rw.split("/")):
            break
        else:
            console.print("[bold red]RT/RW harus dalam format angka, contoh: 01/02.[/bold red]")

    kel_desa = input("Masukkan Kelurahan/Desa: ")
    kecamatan = input("Masukkan Kecamatan: ")

    while True:
        kontak = input("Masukkan Kontak Penyewa (contoh: 081234567890): ")
        if kontak.isdigit() and len(kontak) >= 10:
            break
        else:
            console.print("[bold red]Kontak harus berupa angka minimal 10 digit.[/bold red]")

    # Data pekerjaan
    if status_pekerjaan == "bekerja":
        pekerjaan = input("Masukkan Pekerjaan: ")
        while True:
            no_identitas = input("Masukkan Nomor NPWP (15 digit): ")
            if no_identitas.isdigit() and len(no_identitas) == 15:
                break
            else:
                console.print("[bold red]Nomor NPWP harus berupa 15 digit angka.[/bold red]")
    else:
        pekerjaan = "Pelajar/Mahasiswa"
        while True:
            no_identitas = input("Masukkan Nomor Kartu Pelajar (minimal 5 karakter): ")
            if len(no_identitas) >= 5:
                break
            else:
                console.print("[bold red]Nomor Kartu Pelajar harus minimal 5 karakter.[/bold red]")

    # Tampilkan daftar mobil
    console.print(Panel("[bold magenta]=== Daftar Mobil ===[/bold magenta]", border_style="bold blue"))
    lihat_semua_mobil(session, pause=False)
    while True:
        try:
            id_mobil = int(input("Pilih ID Mobil yang ingin disewa: "))
            mobil = session.query(Mobil).get(id_mobil)
            if mobil and mobil.status == "Tersedia":
                break
            else:
                console.print("[bold red]Mobil tidak tersedia atau ID tidak valid.[/bold red]")
        except ValueError:
            console.print("[bold red]ID Mobil harus berupa angka.[/bold red]")

    # Input lama sewa dan jarak tempuh
    while True:
        try:
            durasi = int(input("Durasi sewa (hari): "))
            break
        except ValueError:
            console.print("[bold red]Durasi harus berupa angka.[/bold red]")

    while True:
        try:
            jarak_tempuh = float(input("Jarak tempuh (km): "))
            break
        except ValueError:
            console.print("[bold red]Jarak tempuh harus berupa angka.[/bold red]")

    # Kalkulasi estimasi harga, waktu tempuh, dan total bensin
    total_sewa = durasi * mobil.harga
    rata_rata_bbm = 12  # Asumsi rata-rata konsumsi BBM mobil (km/liter)
    harga_bbm = 10000  # Harga BBM per liter (contoh)
    total_bensin = jarak_tempuh / rata_rata_bbm
    biaya_bahan_bakar = total_bensin * harga_bbm
    total_pembayaran = total_sewa + biaya_bahan_bakar

    console.print(Panel("[bold magenta]=== Estimasi Biaya ===[/bold magenta]", border_style="bold blue"))
    console.print(f"[bold cyan]Durasi Sewa:[/bold cyan] {durasi} hari")
    console.print(f"[bold cyan]Jarak Tempuh:[/bold cyan] {jarak_tempuh} km")
    console.print(f"[bold cyan]Total Harga Sewa:[/bold cyan] Rp{total_sewa:,}")
    console.print(f"[bold cyan]Total Bensin yang Dibutuhkan:[/bold cyan] {total_bensin:.2f} liter")
    console.print(f"[bold cyan]Biaya Bahan Bakar:[/bold cyan] Rp{biaya_bahan_bakar:,}")
    console.print(f"[bold cyan]Total Pembayaran:[/bold cyan] Rp{total_pembayaran:,}")

    konfirmasi = input("Lanjutkan (y/n)? ")
    if konfirmasi.lower() == 'y':
        penyewa = Penyewa(
            nik=nik,
            nama=nama,
            tempat_tanggal_lahir=f"{tempat}, {tanggal_lahir}",
            jenis_kelamin=jenis_kelamin,
            alamat=alamat,
            rt_rw=rt_rw,
            kel_desa=kel_desa,
            kecamatan=kecamatan,
            pekerjaan=pekerjaan,
            no_identitas=no_identitas,
            kontak=kontak
        )
        session.add(penyewa)
        session.commit()

        transaksi = Transaksi(
            penyewa_id=penyewa.id,
            mobil_id=mobil.id,
            durasi=durasi,
            total_bayar=total_pembayaran,
            tanggal_sewa=datetime.now()
        )
        mobil.status = "Disewa"
        session.add(transaksi)
        session.commit()
        console.print("[bold blue]Data penyewaan berhasil disimpan![/bold blue]")
    else:
        console.print("[bold yellow]Transaksi dibatalkan.[/bold yellow]")
def lihat_laporan(session):
    transaksi_list = session.query(Transaksi).all()
    if not transaksi_list:
        console.print("[bold red]Tidak ada transaksi yang tersedia.[/bold red]")
        input("Tekan Enter untuk kembali...")
        return

    table = Table(title="Laporan Transaksi", show_header=True, header_style="bold magenta")
    table.add_column("ID Transaksi", style="dim", width=12)
    table.add_column("Penyewa", style="bold cyan")
    table.add_column("Mobil")
    table.add_column("Durasi (hari)", justify="center")
    table.add_column("Total Bayar", justify="right")

    total_pendapatan = 0
    for t in transaksi_list:
        penyewa = t.penyewa
        mobil = t.mobil
        table.add_row(
            str(t.id),
            penyewa.nama if penyewa else "N/A",
            mobil.nama if mobil else "N/A",
            str(t.durasi),
            f"Rp{t.total_bayar:,}"
        )
        total_pendapatan += t.total_bayar

    console.print(table)
    console.print(f"[bold blue]Total Pendapatan: Rp{total_pendapatan:,}[/bold blue]")
    input("Tekan Enter untuk kembali...")

def lihat_semua_mobil(session, pause=True):
    """
    Menampilkan semua mobil yang ada di database, diurutkan berdasarkan nama secara abjad.
    Parameter:
        - pause (bool): Jika True, tampilkan prompt "Tekan Enter untuk kembali".
    """
    mobil_list = session.query(Mobil).order_by(Mobil.nama).all()
    if not mobil_list:
        console.print("[bold red]Tidak ada mobil yang tersedia.[/bold red]")
        return

    table = Table(title="Daftar Mobil", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Merk", style="bold cyan")
    table.add_column("Nama")
    table.add_column("Tahun", justify="center")
    table.add_column("Kapasitas", justify="center")
    table.add_column("Transmisi", justify="center")
    table.add_column("Harga", justify="right")
    table.add_column("Status", justify="center")

    for mobil in mobil_list:
        table.add_row(
            str(mobil.id),
            mobil.merk,
            mobil.nama,
            str(mobil.tahun),
            str(mobil.kapasitas),
            mobil.tipe_transmisi,
            f"Rp{mobil.harga:,}",
            mobil.status,
        )

    console.print(table)

    if pause:
        input("Tekan Enter untuk kembali...")

def selesaikan_penyewaan(session):
    clear_screen()
    console.print(Panel("[bold magenta]=== Selesaikan Penyewaan ===[/bold magenta]", border_style="bold blue"))
    transaksi_list = session.query(Transaksi).all()

    if not transaksi_list:
        console.print("[bold red]Tidak ada transaksi yang sedang berlangsung.[/bold red]")
        input("Tekan Enter untuk kembali...")
        return

    # Tampilkan daftar transaksi dalam bentuk tabel
    table = Table(title="Daftar Transaksi", show_header=True, header_style="bold magenta")
    table.add_column("ID Transaksi", style="dim", width=12)
    table.add_column("Penyewa", style="bold cyan")
    table.add_column("Mobil")
    table.add_column("Status", justify="center")

    for t in transaksi_list:
        mobil = t.mobil
        penyewa = t.penyewa
        status = "Selesai" if mobil.status == "Tersedia" else "Sedang Disewa"
        table.add_row(
            str(t.id),
            penyewa.nama if penyewa else "N/A",
            mobil.nama if mobil else "N/A",
            status
        )

    console.print(table)

    while True:
        id_transaksi = input("\nMasukkan ID Transaksi yang ingin diselesaikan: ").strip()
        if not id_transaksi.isdigit():
            console.print("[bold red]ID Transaksi harus berupa angka. Silakan coba lagi.[/bold red]")
            continue

        id_transaksi = int(id_transaksi)
        transaksi = session.query(Transaksi).get(id_transaksi)

        if not transaksi:
            console.print("[bold red]Transaksi tidak ditemukan. Silakan masukkan ID yang valid.[/bold red]")
        elif transaksi.mobil.status == "Tersedia":
            console.print("[bold yellow]Transaksi ini sudah selesai.[/bold yellow]")
        else:
            transaksi.mobil.status = "Tersedia"
            session.commit()
            console.print("[bold blue]Transaksi berhasil diselesaikan. Mobil sekarang tersedia.[/bold blue]")
            break

    input("Tekan Enter untuk kembali...")

def lihat_data_penyewa(session):
    clear_screen()
    console.print(Panel("[bold magenta]=== Lihat Data Penyewa ===[/bold magenta]", border_style="bold blue"))
    penyewa_list = session.query(Penyewa).all()

    if not penyewa_list:
        console.print("[bold red]Tidak ada data penyewa.[/bold red]")
        input("Tekan Enter untuk kembali...")
        return

    # Tampilkan daftar penyewa dalam bentuk tabel
    table = Table(title="Daftar Penyewa", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Nama", style="bold cyan")
    table.add_column("Kontak", justify="center")

    for penyewa in penyewa_list:
        table.add_row(
            str(penyewa.id),
            penyewa.nama,
            penyewa.kontak
        )

    console.print(table)

    try:
        id_penyewa = int(input("\nMasukkan ID Penyewa yang ingin dilihat: "))
        penyewa = session.query(Penyewa).get(id_penyewa)

        if not penyewa:
            console.print("[bold red]Penyewa tidak ditemukan.[/bold red]")
        else:
            # Tampilkan detail penyewa dalam bentuk panel
            detail_panel = Panel(
                f"[bold cyan]ID:[/bold cyan] {penyewa.id}\n"
                f"[bold cyan]NIK:[/bold cyan] {penyewa.nik}\n"
                f"[bold cyan]Nama:[/bold cyan] {penyewa.nama}\n"
                f"[bold cyan]Tempat/Tanggal Lahir:[/bold cyan] {penyewa.tempat_tanggal_lahir}\n"
                f"[bold cyan]Jenis Kelamin:[/bold cyan] {penyewa.jenis_kelamin}\n"
                f"[bold cyan]Alamat:[/bold cyan] {penyewa.alamat}\n"
                f"[bold cyan]RT/RW:[/bold cyan] {penyewa.rt_rw}\n"
                f"[bold cyan]Kelurahan/Desa:[/bold cyan] {penyewa.kel_desa}\n"
                f"[bold cyan]Kecamatan:[/bold cyan] {penyewa.kecamatan}\n"
                f"[bold cyan]Pekerjaan:[/bold cyan] {penyewa.pekerjaan}\n"
                f"[bold cyan]No Identitas:[/bold cyan] {penyewa.no_identitas}\n"
                f"[bold cyan]Kontak:[/bold cyan] {penyewa.kontak}",
                title="Detail Data Penyewa",
                border_style="bold blue"
            )
            console.print(detail_panel)

            # Tambahkan opsi untuk edit atau hapus data penyewa
            console.print(Panel("[bold magenta]Pilih Opsi:[/bold magenta]\n"
                                "[bold cyan]1.[/bold cyan] Edit Data Penyewa\n"
                                "[bold cyan]2.[/bold cyan] Hapus Data Penyewa\n"
                                "[bold cyan]3.[/bold cyan] Kembali",
                                border_style="bold blue"))

            pilihan = input("Pilih opsi: ")

            if pilihan == "1":
                edit_data_penyewa(session, penyewa)
            elif pilihan == "2":
                hapus_data_penyewa(session, penyewa)
            elif pilihan == "3":
                return
            else:
                console.print("[bold red]Pilihan tidak valid.[/bold red]")
    except ValueError:
        console.print("[bold red]Input tidak valid. Harap masukkan ID yang benar.[/bold red]")

    input("\nTekan Enter untuk kembali...")

def edit_data_penyewa(session, penyewa):
    clear_screen()
    console.print(Panel("[bold magenta]=== Edit Data Penyewa ===[/bold magenta]\nTekan Enter jika tidak ingin mengubah data.", border_style="bold blue"))

    # Tampilkan data penyewa sebelum diedit
    detail_panel = Panel(
        f"[bold cyan]ID:[/bold cyan] {penyewa.id}\n"
        f"[bold cyan]NIK:[/bold cyan] {penyewa.nik}\n"
        f"[bold cyan]Nama:[/bold cyan] {penyewa.nama}\n"
        f"[bold cyan]Tempat/Tanggal Lahir:[/bold cyan] {penyewa.tempat_tanggal_lahir}\n"
        f"[bold cyan]Jenis Kelamin:[/bold cyan] {penyewa.jenis_kelamin}\n"
        f"[bold cyan]Alamat:[/bold cyan] {penyewa.alamat}\n"
        f"[bold cyan]RT/RW:[/bold cyan] {penyewa.rt_rw}\n"
        f"[bold cyan]Kelurahan/Desa:[/bold cyan] {penyewa.kel_desa}\n"
        f"[bold cyan]Kecamatan:[/bold cyan] {penyewa.kecamatan}\n"
        f"[bold cyan]Pekerjaan:[/bold cyan] {penyewa.pekerjaan}\n"
        f"[bold cyan]No Identitas:[/bold cyan] {penyewa.no_identitas}\n"
        f"[bold cyan]Kontak:[/bold cyan] {penyewa.kontak}",
        title="Data Penyewa Saat Ini",
        border_style="bold blue"
    )
    console.print(detail_panel)

    # Input data baru
    penyewa.nik = input(f"NIK ({penyewa.nik}): ") or penyewa.nik
    penyewa.nama = input(f"Nama ({penyewa.nama}): ") or penyewa.nama
    penyewa.tempat_tanggal_lahir = input(f"Tempat/Tanggal Lahir ({penyewa.tempat_tanggal_lahir}): ") or penyewa.tempat_tanggal_lahir
    penyewa.jenis_kelamin = input(f"Jenis Kelamin ({penyewa.jenis_kelamin}): ") or penyewa.jenis_kelamin
    penyewa.alamat = input(f"Alamat ({penyewa.alamat}): ") or penyewa.alamat
    penyewa.rt_rw = input(f"RT/RW ({penyewa.rt_rw}): ") or penyewa.rt_rw
    penyewa.kel_desa = input(f"Kelurahan/Desa ({penyewa.kel_desa}): ") or penyewa.kel_desa
    penyewa.kecamatan = input(f"Kecamatan ({penyewa.kecamatan}): ") or penyewa.kecamatan
    penyewa.pekerjaan = input(f"Pekerjaan ({penyewa.pekerjaan}): ") or penyewa.pekerjaan
    penyewa.no_identitas = input(f"No Identitas ({penyewa.no_identitas}): ") or penyewa.no_identitas
    penyewa.kontak = input(f"Kontak ({penyewa.kontak}): ") or penyewa.kontak

    # Simpan perubahan
    session.commit()
    console.print(Panel("[bold blue]Data penyewa berhasil diperbarui![/bold blue]", border_style="bold blue"))

def hapus_data_penyewa(session, penyewa):
    clear_screen()
    konfirmasi = input(f"Apakah Anda yakin ingin menghapus penyewa '{penyewa.nama}'? (y/n): ").strip().lower()
    if konfirmasi == "y":
        session.delete(penyewa)
        session.commit()
        print("\nData penyewa berhasil dihapus.")
    else:
        print("\nPenghapusan data penyewa dibatalkan.")

def reset_data(session):
    """
    Menghapus semua data dari tabel mobil, transaksi, dan penyewa, lalu mereset ID.
    """
    clear_screen()
    try:
        # Hapus semua data dari tabel transaksi, mobil, dan penyewa
        session.query(Transaksi).delete()
        session.query(Mobil).delete()
        session.query(Penyewa).delete()
        session.commit()

        # Reset AUTO_INCREMENT untuk tabel transaksi, mobil, dan penyewa
        session.execute(text("ALTER TABLE transaksi AUTO_INCREMENT = 1"))
        session.execute(text("ALTER TABLE mobil AUTO_INCREMENT = 1"))
        session.execute(text("ALTER TABLE penyewa AUTO_INCREMENT = 1"))
        session.commit()

        print("Semua data berhasil dihapus dan ID telah direset.")
    except Exception as e:
        session.rollback()
        print(f"Terjadi kesalahan: {e}")

def edit_mobil(session):
    clear_screen()
    print("\n--- Edit Mobil ---")
    
    # Tampilkan daftar mobil sebelum meminta ID
    lihat_semua_mobil(session, pause=False)  # Menampilkan semua mobil tanpa jeda
    
    id_mobil = input("\nMasukkan ID Mobil yang ingin diedit: ")

    try:
        id_mobil = int(id_mobil)
        mobil = session.query(Mobil).get(id_mobil)

        if not mobil:
            print("Mobil tidak ditemukan.")
            return

        print(f"\nData Mobil Saat Ini:")
        print(f"ID: {mobil.id}")
        print(f"Merk: {mobil.merk}")
        print(f"Nama: {mobil.nama}")
        print(f"Tahun: {mobil.tahun}")
        print(f"Kapasitas: {mobil.kapasitas}")
        print(f"Tipe Transmisi: {mobil.tipe_transmisi}")
        print(f"Harga: {mobil.harga:,}")
        print(f"Status: {mobil.status}")

        print("\nMasukkan data baru (tekan Enter untuk tidak mengubah):")
        merk_baru = input(f"Merk Mobil ({mobil.merk}): ") or mobil.merk
        nama_baru = input(f"Nama Mobil ({mobil.nama}): ") or mobil.nama
        tahun_baru = input(f"Tahun Pembuatan ({mobil.tahun}): ") or mobil.tahun
        kapasitas_baru = input(f"Kapasitas Penumpang ({mobil.kapasitas}): ") or mobil.kapasitas
        tipe_transmisi_baru = input(f"Tipe Transmisi ({mobil.tipe_transmisi}): ") or mobil.tipe_transmisi
        harga_baru = input(f"Harga Sewa per Hari ({mobil.harga}): ") or mobil.harga

        # Validasi tahun, kapasitas, dan harga baru
        try:
            tahun_baru = int(tahun_baru)
            kapasitas_baru = int(kapasitas_baru)
            harga_baru = int(harga_baru)
        except ValueError:
            print("Tahun, kapasitas, dan harga harus berupa angka. Perubahan dibatalkan.")
            return

        # Update data mobil
        mobil.merk = merk_baru
        mobil.nama = nama_baru
        mobil.tahun = tahun_baru
        mobil.kapasitas = kapasitas_baru
        mobil.tipe_transmisi = tipe_transmisi_baru
        mobil.harga = harga_baru
        session.commit()
        print("Data mobil berhasil diperbarui.")
    except ValueError:
        print("ID Mobil harus berupa angka.")

def cari_mobil(session):
    clear_screen()
    console.print("[bold magenta]--- Cari Mobil ---[/bold magenta]")
    merk = input("Merk Mobil: ").strip()
    try:
        harga_max = int(input("Harga Maksimal (Rp): ") or 0)
    except ValueError:
        console.print("[bold red]Harga Maksimal harus berupa angka. Mengabaikan kriteria ini.[/bold red]")
        harga_max = 0
    try:
        kapasitas_min = int(input("Kapasitas Minimal: ") or 0)
    except ValueError:
        console.print("[bold red]Kapasitas Minimal harus berupa angka. Mengabaikan kriteria ini.[/bold red]")
        kapasitas_min = 0
    tipe_transmisi = input("Tipe Transmisi (Manual/Otomatis): ").strip().capitalize()

    query = session.query(Mobil)
    if merk:
        query = query.filter(Mobil.merk.ilike(f"%{merk}%"))
    if harga_max > 0:
        query = query.filter(Mobil.harga <= harga_max)
    if kapasitas_min > 0:
        query = query.filter(Mobil.kapasitas >= kapasitas_min)
    if tipe_transmisi in ["Manual", "Otomatis"]:
        query = query.filter(Mobil.tipe_transmisi == tipe_transmisi)

    hasil = query.all()

    if hasil:
        table = Table(title="Hasil Pencarian Mobil", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Merk", style="bold cyan")
        table.add_column("Nama")
        table.add_column("Tahun", justify="center")
        table.add_column("Kapasitas", justify="center")
        table.add_column("Transmisi", justify="center")
        table.add_column("Harga", justify="right")
        table.add_column("Status", justify="center")

        for mobil in hasil:
            table.add_row(
                str(mobil.id),
                mobil.merk,
                mobil.nama,
                str(mobil.tahun),
                str(mobil.kapasitas),
                mobil.tipe_transmisi,
                f"Rp{mobil.harga:,}",
                mobil.status,
            )

        console.print(table)
    else:
        console.print("[bold red]Tidak ada mobil yang sesuai dengan kriteria pencarian.[/bold red]")

    input("Tekan Enter untuk kembali...")