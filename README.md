# WebSentinel

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Security](https://img.shields.io/badge/Category-Web%20Security-red)
![Status](https://img.shields.io/badge/Status-Active-success)

**WebSentinel** is an advanced web application vulnerability scanner designed to identify common security flaws such as **SQL Injection**, **Cross-Site Scripting (XSS)**, and **Cross-Site Request Forgery (CSRF)**.

It performs intelligent crawling, input analysis, vulnerability testing, and generates **severity-based security reports with remediation guidance**, making it suitable for **security analysts, penetration testers, and blue/purple team learning**.

---

## Features

- Intelligent crawling within target scope
- Automatic discovery of forms and input parameters
- Boolean-based SQL Injection detection
- Reflected Cross-Site Scripting (XSS) detection
- CSRF misconfiguration detection
- Severity and confidence classification
- Professional HTML and JSON reports
- Clean CLI interface (Kali-style output)

---

## Supported Vulnerabilities

| Vulnerability | Detection Type | Severity |
|--------------|---------------|----------|
| SQL Injection | Boolean-based | Critical |
| XSS (Reflected) | Payload reflection | High |
| CSRF | Token absence analysis | Medium |

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/the-artist111/WebSentinel.git
cd WebSentinel
pip install -r requirements.txt
```




Install the tool locally as a CLI command:

```pip install .```

## Usage

Basic scan:

```websentinel -u https://example.com```


Scan with JSON report output:

```websentinel -u https://example.com --json```


Specify crawl depth and output name:

```websentinel -u https://example.com -d 3 -o scan_report --json```

## Output

WebSentinel generates the following files:

report.html — Human-readable security report

report.json — Machine-readable report for automation

## Each finding includes:

Vulnerability type

Affected URL

Severity level

Confidence level

Evidence

Remediation recommendation

## Severity Levels

Critical – Easily exploitable issues with high impact (e.g., SQL Injection)

High – Serious vulnerabilities affecting users (e.g., XSS)

Medium – Security weaknesses requiring user interaction (e.g., CSRF)

Low – Informational or minor issues

## Ethical Use Disclaimer

This tool is intended for educational purposes and authorized security testing only.
You must have explicit permission before scanning any web application you do not own.

The author is not responsible for misuse or illegal activity involving this tool.

## License

This project is licensed under the MIT License.
You are free to use, modify, and distribute it with proper attribution.

## Author

Developed as a security research and portfolio project.

Future Improvements

Time-based SQL Injection detection

Stored XSS detection

Authentication-aware scanning

CVSS scoring

OWASP Top 10 mapping

Rate-limit and WAF evasion techniques

