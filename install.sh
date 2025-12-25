#!/bin/bash

echo "[*] Installing ALLCHANGER..."

# Update and upgrade system
sudo apt update -y
sudo apt upgrade -y

# Install Python3, pip and Tor
sudo apt install -y tor python3-pip

# Install Python dependencies
pip3 install --upgrade pip
pip3 install stem requests pysocks rich

# Configure Tor ControlPort if not exists
if ! grep -q "ControlPort 9051" /etc/tor/torrc; then
    echo "[*] Configuring Tor ControlPort..."
    echo "ControlPort 9051" | sudo tee -a /etc/tor/torrc
    echo "CookieAuthentication 1" | sudo tee -a /etc/tor/torrc
fi

# Restart Tor service
echo "[*] Restarting Tor..."
sudo systemctl restart tor || sudo systemctl restart tor@default

echo "[+] Installation complete!"
echo "[+] Run the tool with: python3 allchanger.py"

