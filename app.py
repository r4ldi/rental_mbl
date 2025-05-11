from menu import admin_menu
from models import Base
from database import engine
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    Base.metadata.create_all(bind=engine)  # Buat tabel baru
    while True:
        console.print(Panel("[bold magenta]=== Sistem Rental Mobil CLI ===[/bold magenta]\n"
                            "[bold cyan]1.[/bold cyan] Masuk ke Menu Admin\n"
                            "[bold cyan]2.[/bold cyan] Keluar",
                            title="Menu Utama", border_style="bold blue"))

        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            admin_menu()
        elif pilihan == "2":
            console.print("[bold yellow]Terima kasih telah menggunakan sistem ini![/bold yellow]")
            break
        else:
            console.print("[bold red]Pilihan tidak valid. Silakan coba lagi.[/bold red]")

if __name__ == '__main__':
    main()