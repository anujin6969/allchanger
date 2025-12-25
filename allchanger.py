#!/usr/bin/env python3
import os
import time
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

IP_INTERVAL = 5


def clear():
    os.system("clear")


def banner():
    txt = Text("""
     ___    __    __    ________  _____    _   __________________
    /   |  / /   / /   / ____/ / / /   |  / | / / ____/ ____/ __ \\
   / /| | / /   / /   / /   / /_/ / /| | /  |/ / / __/ __/ / /_/ /
  / ___ |/ /___/ /___/ /___/ __  / ___ |/ /|  / /_/ / /___/ _, _/
 /_/  |_/_____/_____\\____/_/ /_/_/  |_/_/ |_|\\____/_____/_/ |_|


""", style="bold red")
    return Panel(txt, border_style="red")


def footer():
    console.print("\n[bold yellow][CTRL+C][/bold yellow] Back to menu\n")


def tor_status():
    """Check if Tor is running and port 9050 is accessible"""
    try:
        r = requests.get("https://api.ipify.org", proxies=PROXY, timeout=10)
        return True
    except:
        return False


def renew_ip():
    try:
        with Controller.from_port(port=9051) as c:
            c.authenticate()
            c.signal(Signal.NEWNYM)
    except Exception as e:
        console.print(f"[bold red]Tor ControlPort error:[/bold red] {e}")
        time.sleep(5)


def get_ip_info():
    """Return IP, country and ISP"""
    try:
        r = requests.get("https://ipwho.is/", proxies=PROXY, timeout=10)
        data = r.json()
        ip = data.get("ip", "ERROR")
        country = data.get("country", "Unknown")
        isp = data.get("isp", "Unknown")
        return ip, country, isp
    except:
        return "ERROR", "Unknown", "Unknown"


def ip_changer():
    clear()
    console.print(banner())
    status = tor_status()
    if not status:
        console.print("[bold red]Tor not detected or not running![/bold red]")
        input("Press Enter to return to menu...")
        return

    console.print(f"[bold green]IP rotation active ({IP_INTERVAL} seconds)[/bold green]")
    footer()

    try:
        while True:
            renew_ip()
            time.sleep(2)
            ip, country, isp = get_ip_info()
            console.print(f"[bold red]NEW IP[/bold red] -> {ip} | Country: {country} | ISP: {isp}")
            time.sleep(IP_INTERVAL)

    except KeyboardInterrupt:
        console.print("\n[bold yellow][!] IP rotation stopped[/bold yellow]")
        time.sleep(1)
        return


def set_interval():
    global IP_INTERVAL
    clear()
    console.print(banner())
    try:
        value = int(input("Enter IP change interval (seconds): ").strip())
        if value < 3:
            console.print("[red]Interval too low! Minimum is 3 seconds[/red]")
            time.sleep(2)
        else:
            IP_INTERVAL = value
            console.print(f"[green]Interval set to {IP_INTERVAL} seconds[/green]")
            time.sleep(2)
    except ValueError:
        console.print("[red]Invalid number[/red]")
        time.sleep(2)


def creator():
    clear()
    info = Text()
    info.append("Owner: huslen\n", style="bold white")
    info.append("Created by: n0mercy\n", style="bold white")
    info.append("GitHub: anujin6969\n", style="bold white")
    console.print(Panel(info, title="CREATOR", border_style="red"))
    input("\nPress Enter to return...")


def exit_confirm():
    choice = input("Are you sure you want to exit? (y/n): ").lower().strip()
    if choice == "y":
        clear()
        sys.exit()


def menu():
    while True:
        clear()
        console.print(banner())
        console.print(f"""
[1] IP Changer
[2] Set Interval (current: {IP_INTERVAL}s)
[3] Creator
[0] Exit
""", style="bold white")

        choice = input("Select > ").strip()

        if choice == "1":
            ip_changer()
        elif choice == "2":
            set_interval()
        elif choice == "3":
            creator()
        elif choice == "0":
            exit_confirm()


if __name__ == "__main__":
    menu()

