#!/bin/bash
set -e

# رنگ‌ها
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[+] $1${NC}"; }
warn() { echo -e "${YELLOW}[!] $1${NC}"; }
err() { echo -e "${RED}[-] $1${NC}"; }

log "به‌روزرسانی سیستم..."
sudo apt update && sudo apt upgrade -y

log "نصب ابزارهای پایه..."
sudo apt install -y git curl wget python3 python3-pip jq unzip chromium-browser

log "نصب subfinder..."
if ! command -v subfinder &>/dev/null; then
  curl -s https://api.github.com/repos/projectdiscovery/subfinder/releases/latest | \
    grep browser_download_url | grep linux_amd64 | cut -d '"' -f 4 | wget -i - -O subfinder.tar.gz
  tar -xzf subfinder.tar.gz subfinder
  sudo mv subfinder /usr/local/bin/
  rm subfinder.tar.gz
else
  warn "subfinder قبلاً نصب شده است."
fi

log "نصب amass..."
if ! command -v amass &>/dev/null; then
  wget https://github.com/owasp-amass/amass/releases/latest/download/amass_linux_amd64.zip
  unzip amass_linux_amd64.zip
  sudo mv amass_linux_amd64/amass /usr/local/bin/
  rm -rf amass_linux_amd64*
else
  warn "amass قبلاً نصب شده است."
fi

log "نصب assetfinder..."
if ! command -v assetfinder &>/dev/null; then
  wget https://github.com/tomnomnom/assetfinder/releases/latest/download/assetfinder-linux-amd64-0.1.1.tgz
  tar -xzf assetfinder-linux-amd64-0.1.1.tgz
  sudo mv assetfinder /usr/local/bin/
  rm assetfinder-linux-amd64-0.1.1.tgz
else
  warn "assetfinder قبلاً نصب شده است."
fi

log "نصب rustscan..."
if ! command -v rustscan &>/dev/null; then
  wget https://github.com/RustScan/RustScan/releases/latest/download/rustscan_amd64.deb
  sudo dpkg -i rustscan_amd64.deb || sudo apt-get install -f -y
  rm rustscan_amd64.deb
else
  warn "rustscan قبلاً نصب شده است."
fi

log "نصب nmap..."
sudo apt install -y nmap

log "نصب gowitness..."
if ! command -v gowitness &>/dev/null; then
  wget https://github.com/sensepost/gowitness/releases/latest/download/gowitness-2.5.0-linux-amd64
  chmod +x gowitness-2.5.0-linux-amd64
  sudo mv gowitness-2.5.0-linux-amd64 /usr/local/bin/gowitness
else
  warn "gowitness قبلاً نصب شده است."
fi

log "نصب aquatone..."
if ! command -v aquatone &>/dev/null; then
  wget https://github.com/michenriksen/aquatone/releases/latest/download/aquatone_linux_amd64_1.7.0.zip
  unzip aquatone_linux_amd64_1.7.0.zip
  sudo mv aquatone /usr/local/bin/
  rm aquatone_linux_amd64_1.7.0.zip
else
  warn "aquatone قبلاً نصب شده است."
fi

log "نصب nuclei..."
if ! command -v nuclei &>/dev/null; then
  curl -s https://api.github.com/repos/projectdiscovery/nuclei/releases/latest | \
    grep browser_download_url | grep linux_amd64 | cut -d '"' -f 4 | wget -i - -O nuclei.tar.gz
  tar -xzf nuclei.tar.gz nuclei
  sudo mv nuclei /usr/local/bin/
  rm nuclei.tar.gz
else
  warn "nuclei قبلاً نصب شده است."
fi

log "نصب کتابخانه‌های پایتون..."
pip3 install -r requirements.txt || pip install -r requirements.txt

log "نصب کامل شد!"