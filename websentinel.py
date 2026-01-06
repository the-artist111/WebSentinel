#!/usr/bin/env python3
import argparse
from crawler import crawl_and_extract_inputs
from scanner import run_scans
from report import generate_html_report, generate_json_report

# ANSI Colors (Kali-style)
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def banner():
    print(f"""{RED}{BOLD}
██╗    ██╗███████╗██████╗ ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗
██║    ██║██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║
██║ █╗ ██║█████╗  ██████╔╝███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║
██║███╗██║██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║
╚███╔███╔╝███████╗██████╔╝███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
 ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
{RESET}{CYAN}
----------------------------------------------------------------------------------------
{BOLD} WebSentinel v2.0{RESET}{CYAN} — Advanced Web Application Vulnerability Scanner
{YELLOW} SQL Injection  |  Cross-Site Scripting (XSS)  |  CSRF
{CYAN}----------------------------------------------------------------------------------------
{RESET}""")

def main():
    banner()

    parser = argparse.ArgumentParser(
        prog="websentinel",
        description="WebSentinel - Advanced Web Vulnerability Scanner"
    )
    parser.add_argument("-u", "--url", required=True, help="Target URL (https://example.com)")
    parser.add_argument("-d", "--depth", type=int, default=2, help="Crawl depth (default: 2)")
    parser.add_argument("-o", "--output", default="report", help="Report output name (without extension)")
    parser.add_argument("--json", action="store_true", help="Generate JSON report")

    args = parser.parse_args()

    print(f"{BLUE}[+] Target:{RESET} {args.url}")
    print(f"{BLUE}[+] Crawl depth:{RESET} {args.depth}\n")

    print(f"{CYAN}[*] Crawling and detecting inputs...{RESET}")
    inputs = crawl_and_extract_inputs(args.url, args.depth)

    print(f"{CYAN}[*] Running vulnerability scans (SQLi, XSS, CSRF)...{RESET}")
    findings = run_scans(inputs)

    print(f"{CYAN}[*] Generating HTML report...{RESET}")
    generate_html_report(args.url, findings, args.output + ".html")

    if args.json:
        print(f"{CYAN}[*] Generating JSON report...{RESET}")
        generate_json_report(args.url, findings, args.output + ".json")

    print(f"\n{GREEN}{BOLD}[✓] Scan completed successfully{RESET}")
    print(f"{GREEN}[✓] Report saved as:{RESET} {args.output}.html")
    if args.json:
        print(f"{GREEN}[✓] JSON report saved as:{RESET} {args.output}.json")

if __name__ == "__main__":
    main()

