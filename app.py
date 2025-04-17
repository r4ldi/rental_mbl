from auth import login, register
from menu import admin_menu, penyewa_menu
from models import Base
from database import engine

def main():
    # Buat semua tabel jika belum ada
    Base.metadata.create_all(bind=engine)

    while True:
        print("\n=== Sistem Rental Mobil CLI ===")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            user = login()
            if user:
                if hasattr(user, 'role') and user.role == "admin":
                    admin_menu()
                else:
                    penyewa_menu(user)
        elif pilihan == "2":
            register()
        elif pilihan == "3":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == '__main__':
    main()
