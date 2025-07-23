import argparse
import os
import sys
import json
import subprocess
from utils.error_handler import log_info, log_warn, log_error
from utils.notify import notify
from rich.prompt import Confirm

RECON_OUTPUT = 'recon/output/'
SCAN_OUTPUT = 'scan/output/'
EXPLOIT_OUTPUT = 'exploit/output/'

os.makedirs(RECON_OUTPUT, exist_ok=True)
os.makedirs(SCAN_OUTPUT, exist_ok=True)
os.makedirs(EXPLOIT_OUTPUT, exist_ok=True)

def run_cmd(cmd, output_file=None):
    log_info(f"در حال اجرای: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            log_error(result.stderr)
        if output_file:
            with open(output_file, 'w') as f:
                f.write(result.stdout)
        return result.stdout
    except Exception as e:
        log_error(str(e))
        return None

def phase1_recon(domain):
    log_info(f"[Recon] شناسایی ساب‌دامین‌ها برای {domain}")
    subfinder_out = f"{RECON_OUTPUT}subfinder_{domain}.txt"
    amass_out = f"{RECON_OUTPUT}amass_{domain}.txt"
    assetfinder_out = f"{RECON_OUTPUT}assetfinder_{domain}.txt"
    run_cmd(f"subfinder -d {domain}", subfinder_out)
    run_cmd(f"amass enum -passive -d {domain}", amass_out)
    run_cmd(f"assetfinder --subs-only {domain}", assetfinder_out)
    # Merge and dedup
    all_subs = set()
    for f in [subfinder_out, amass_out, assetfinder_out]:
        with open(f) as fd:
            all_subs.update([line.strip() for line in fd if line.strip()])
    subs_json = f"{RECON_OUTPUT}subdomains.json"
    with open(subs_json, 'w') as f:
        json.dump(sorted(list(all_subs)), f, indent=2)
    log_info(f"ساب‌دامین‌ها ذخیره شد: {subs_json}")
    # Port scan
    ports_out = f"{RECON_OUTPUT}ports_{domain}.json"
    run_cmd(f"rustscan -a {domain} --ulimit 5000 -- -sS -Pn -n -oJ {ports_out}")
    log_info(f"اسکن پورت ذخیره شد: {ports_out}")
    # Web screenshot
    screenshot_csv = f"{RECON_OUTPUT}screenshots.csv"
    run_cmd(f"gowitness file -f {subs_json} -P recon/web_screenshot/ --csv {screenshot_csv}")
    log_info(f"اسکرین‌شات‌ها ذخیره شد: {screenshot_csv}")
    return subs_json

def phase2_scan(subs_json):
    log_info("[Scan] اجرای nuclei روی دامنه‌ها")
    with open(subs_json) as f:
        subs = json.load(f)
    nuclei_out = f"{SCAN_OUTPUT}nuclei_results.json"
    subs_file = f"{SCAN_OUTPUT}subs.txt"
    with open(subs_file, 'w') as f:
        f.write('\n'.join(subs))
    run_cmd(f"nuclei -l {subs_file} -o {nuclei_out} -json -t config/nuclei-custom.yaml")
    log_info(f"نتایج nuclei ذخیره شد: {nuclei_out}")
    return nuclei_out

def parse_vulns(nuclei_out):
    vulns = []
    with open(nuclei_out) as f:
        for line in f:
            try:
                data = json.loads(line)
                vulns.append(data)
            except Exception:
                continue
    return vulns

def phase3_exploit(vulns):
    log_info("[Exploit] بررسی و اجرای اسکریپت‌های اکسپلویت")
    report = []
    for v in vulns:
        vuln_type = v.get('templateID', '').lower()
        url = v.get('matched-at', '')
        exploit_path = None
        if 'xss' in vuln_type:
            exploit_path = 'exploit/xss/reflected.py'
        elif 'ssrf' in vuln_type:
            exploit_path = 'exploit/ssrf/ssrf.py'
        elif 'rce' in vuln_type:
            exploit_path = 'exploit/rce/rce.py'
        elif 'ssti' in vuln_type:
            exploit_path = 'exploit/ssti/ssti.py'
        if exploit_path and os.path.exists(exploit_path):
            log_info(f"اجرای اکسپلویت: {exploit_path} روی {url}")
            try:
                result = subprocess.run([sys.executable, exploit_path, url], capture_output=True, text=True, timeout=300)
                report.append({'vuln': vuln_type, 'url': url, 'exploit': exploit_path, 'output': result.stdout})
            except Exception as e:
                log_error(str(e))
    report_file = f"{EXPLOIT_OUTPUT}exploits_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    log_info(f"گزارش اکسپلویت ذخیره شد: {report_file}")

def main():
    parser = argparse.ArgumentParser(description='BugBounty Automation')
    parser.add_argument('--target', required=True, help='دامنه هدف')
    args = parser.parse_args()
    notify("شروع فرآیند BugBounty", f"هدف: {args.target}")
    subs_json = phase1_recon(args.target)
    nuclei_out = phase2_scan(subs_json)
    notify("تحلیل دستی", "لطفاً نتایج اسکن را بررسی و تأیید کنید. ادامه؟")
    if not Confirm.ask("آیا ادامه دهیم و بهره‌برداری را آغاز کنیم؟", default=False):
        log_warn("فرآیند متوقف شد.")
        sys.exit(0)
    vulns = parse_vulns(nuclei_out)
    phase3_exploit(vulns)
    notify("پایان فرآیند", "تمام مراحل با موفقیت انجام شد.")

if __name__ == '__main__':
    main()