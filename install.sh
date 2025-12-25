#!/bin/bash

echo "[*] Installing ALLCHANGER..."

apt update
apt install -y tor python3-pip

pip3 install stem requests pysocks rich

if ! grep -q "ControlPort 9051" /etc/tor/torrc; then
    echo "ControlPort 9051" >> /etc/tor/torrc
    echo "CookieAuthentication 1" >> /etc/tor/torrc
fi

systemctl restart tor@default || systemctl restart tor

echo "[+] Done"
echo "[+] Run: python3 allchanger.py"
