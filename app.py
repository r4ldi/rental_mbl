from menu import admin_menu
from menu import clear_screen
from models import Base
from database import engine
from auth import login  # Tambahkan import login
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    Base.metadata.create_all(bind=engine)  # Buat tabel baru
    while True:
        console.print(Panel("[bold magenta]=== Sistem Rental Mobil CLI ===[/bold magenta]\n"
                            "[bold cyan]1.[/bold cyan] Login\n"
                            "[bold cyan]2.[/bold cyan] Keluar",
                            title="Menu Utama", border_style="bold blue"))

        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            clear_screen()
            user = login()  # Panggil fungsi login
            if user:
                admin_menu()  # Masuk ke menu admin setelah login berhasil
            else:
                console.print("[bold red]Login gagal. Silakan coba lagi.[/bold red]")
        elif pilihan == "2":
            console.print("[bold yellow]Terima kasih telah menggunakan sistem ini![/bold yellow]")
            break
        else:
            console.print("[bold red]Pilihan tidak valid. Silakan coba lagi.[/bold red]")

if __name__ == '__main__':
    main()