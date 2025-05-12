from models import User
from database import SessionLocal
from rich.console import Console
from rich.panel import Panel

console = Console()

def login():
    session = SessionLocal()
    console.print(Panel("[bold magenta]=== Login ===[/bold magenta]", border_style="bold blue"))
    try:
        user_id = int(input("Masukkan ID: "))
    except ValueError:
        console.print("[bold red]ID harus berupa angka.[/bold red]")
        session.close()
        return None

    password = input("Masukkan Password: ")

    user = session.query(User).filter_by(id=user_id, password=password).first()
    if user:
        console.print(f"[bold green]Login berhasil! Selamat datang, {user.username}.[/bold green]")
        session.close()
        return user
    else:
        console.print("[bold red]ID atau password salah.[/bold red]")
        session.close()
        return None