# BugBounty Automation

یک پروژه نیمه‌اتوماتیک برای اجرای فرایندهای Bug Bounty در سه فاز: شناسایی، اسکن آسیب‌پذیری و بهره‌برداری.

## ساختار دایرکتوری

```
bugbounty-automation/
├── recon/
│   ├── subdomain_enum/
│   ├── port_scan/
│   ├── web_screenshot/
│   └── output/
├── scan/
│   ├── nuclei/
│   ├── custom_scanners/
│   └── output/
├── exploit/
│   ├── xss/
│   ├── ssrf/
│   ├── rce/
│   ├── ssti/
│   └── output/
├── utils/
│   ├── install.sh
│   ├── error_handler.py
│   └── notify.py
├── config/
│   └── nuclei-custom.yaml
├── run.py
└── README.md
```

## نصب ابزارها

```bash
cd bugbounty-automation
chmod +x utils/install.sh
./utils/install.sh
```

## اجرای پروژه

```bash
python3 run.py --target example.com
```

## نمونه خروجی

- خروجی شناسایی: `recon/output/subdomains.json`
- خروجی اسکن پورت: `recon/output/ports_example.com.json`
- خروجی اسکرین‌شات: `recon/output/screenshots.csv`
- خروجی nuclei: `scan/output/nuclei_results.json`
- خروجی اکسپلویت: `exploit/output/exploits_report.json`

## نکات مهم
- همه مراحل با لاگ رنگی و هندل خطا اجرا می‌شوند.
- خروجی‌ها قابل بایگانی و تحلیل دستی هستند.
- بهره‌برداری فقط پس از تأیید دستی انجام می‌شود.

## توسعه‌دهنده
- [GitHub: bugbounty-automation](https://github.com/nerdznj/Automation-Bug_Bounty)
