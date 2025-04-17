from models import User, Penyewa
from database import SessionLocal

def register():
    session = SessionLocal()
    print("\n=== Registrasi ===")
    username = input("Username: ")
    password = input("Password: ")

    # Validasi input role
    while True:
        role = input("Role (admin/penyewa): ").strip().lower()
        if role in ['admin', 'penyewa']:
            break
        else:
            print("Role tidak valid. Hanya boleh 'admin' atau 'penyewa'.")

    if session.query(User).filter_by(username=username).first():
        print("Username sudah terdaftar.")
        session.close()
        return None

    user = User(username=username, password=password, role=role)
    session.add(user)
    session.commit()

    if role == "penyewa":
        nama = input("Nama lengkap: ")
        kontak = input("Kontak: ")
        penyewa = Penyewa(nama=nama, kontak=kontak)
        session.add(penyewa)
        session.commit()
        print("Penyewa terdaftar.")
        session.close()
        return penyewa
    elif role == "admin":
        print("Admin terdaftar.")
        session.close()
        return user


def login():
    session = SessionLocal()
    print("\n=== Login ===")
    username = input("Username: ")
    password = input("Password: ")

    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        print(f"Login berhasil sebagai {user.role}")
        if user.role == "admin":
            session.close()
            return user
        else:
            penyewa = session.query(Penyewa).filter_by(id=user.id).first()
            session.close()
            return penyewa
    else:
        print("Username atau password salah.")
        session.close()
        return None
