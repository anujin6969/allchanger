#!/usr/bin/env python3
import os
import time
import signal
import sys
import requests
from stem import Signal
from stem.control import Controller
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

PROXY = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

def clear():
    os.system("clear")

def banner():
    txt = Text("""
     ___    __    __    ________  _____    _   __________________
    /   |  / /   / /   / ____/ / / /   |  / | / / ____/ ____/ __ \\
   / /| | / /   / /   / /   / /_/ / /| | /  |/ / / __/ __/ / /_/ /
  / ___ |/ /___/ /___/ /___/ __  / ___ |/ /|  / /_/ / /___/ _, _/
 /_/  |_/_____/_____/\____/_/ /_/_/  |_/_/ |_/\____/_____/_/ |_|

""", style="bold red")
    return Panel(txt, border_style="red")

def renew_ip():
    try:
        with Controller.from_port(port=9051) as c:
            c.authenticate()
            c.signal(Signal.NEWNYM)
    except Exception as e:
        console.print(f"[bold red]Tor ControlPort error:[/bold red] {e}")
        time.sleep(5)

def get_ip():
    try:
        r = requests.get("https://api.ipify.org", proxies=PROXY, timeout=15)
        return r.text.strip()
    except:
        return "ERROR"

def ip_changer():
    clear()
    console.print(banner())
    console.print("[bold green]IP rotation active (5 seconds)[/bold green]\n")

    while True:
        renew_ip()
        time.sleep(2)
        ip = get_ip()
        console.print(f"[bold red]NEW IP[/bold red] -> {ip}")
        time.sleep(5)

def creator():
    clear()
    info = Text()
    info.append("Owner: huslen\n", style="bold white")
    info.append("Created by: n0mercy\n", style="bold white")
    info.append("GitHub: anujin6969\n", style="bold white")
    console.print(Panel(info, title="CREATOR", border_style="red"))
    input("\nPress Enter to return...")

def menu():
    while True:
        clear()
        console.print(banner())
        console.print("""
[1] IP Changer
[2] Creator
[0] Exit
""", style="bold white")

        choice = input("Select > ").strip()

        if choice == "1":
            ip_changer()   # menu алга болно
        elif choice == "2":
            creator()
        elif choice == "0":
            clear()
            sys.exit()

if __name__ == "__main__":
    menu()

