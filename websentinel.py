#!/usr/bin/env python3
import argparse
import json
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
{BOLD} WebSentinel v2.x{RESET}{CYAN} — Web + API Vulnerability Scanner (Batch Ready)
{YELLOW} SQLi | XSS | CSRF | Auth Intelligence | API (IDOR/BFLA) | Smuggling Playbook
{CYAN}----------------------------------------------------------------------------------------
{RESET}""")

def parse_cookie(cookie_str: str) -> dict:
    jar = {}
    if not cookie_str:
        return jar
    for pair in cookie_str.split(";"):
        pair = pair.strip()
        if "=" in pair:
            k, v = pair.split("=", 1)
            jar[k.strip()] = v.strip()
    return jar

def load_targets(url_arg, list_file):
    if list_file:
        targets = []
        with open(list_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                t = line.strip()
                if not t or t.startswith("#"):
                    continue
                targets.append(t)
        return targets
    return [url_arg]

def main():
    banner()

    parser = argparse.ArgumentParser(
        prog="websentinel",
        description="WebSentinel v2.x - Advanced Web+API Vulnerability Scanner (Batch Mode)"
    )

    # Single target OR batch list
    parser.add_argument("-u", "--url", help="Target URL (https://example.com)")
    parser.add_argument("-l", "--list", help="File with target URLs (one per line), e.g., url.txt")

    # Crawl/report
    parser.add_argument("-d", "--depth", type=int, default=2, help="Crawl depth (default: 2)")
    parser.add_argument("-o", "--output", default="report", help="Output prefix (default: report)")
    parser.add_argument("--json", action="store_true", help="Generate JSON report (single target)")
    parser.add_argument("--profile", choices=["web", "api", "both"], default="both", help="Scan profile (default: both)")
    parser.add_argument("--graph", action="store_true", help="Generate API graph JSON (batch or single)")

    # Single-session auth (for authenticated crawling/scanning)
    parser.add_argument("--cookie", help="Session cookie for authenticated scan (single session)")
    parser.add_argument("--auth-header", help="Authorization header value (e.g. 'Bearer <token>')")

    # Auth intelligence check path
    parser.add_argument("--auth-check-path", default="/", help="Path used to verify auth state (default: /)")

    # Multi-role auth (for IDOR/BFLA)
    parser.add_argument("--user-cookie", help="Low-privilege user session cookie")
    parser.add_argument("--admin-cookie", help="High-privilege admin session cookie")

    # Smuggling playbook tuning (safe)
    parser.add_argument("--smuggle-repeats", type=int, default=3, help="Smuggling playbook repeats (default: 3)")
    parser.add_argument("--timeout", type=float, default=8.0, help="HTTP timeout seconds (default: 8)")

    args = parser.parse_args()

    if not args.url and not args.list:
        print(f"{RED}[!] Error:{RESET} Provide either -u/--url or -l/--list")
        return

    # Build headers/cookies
    headers = {}
    cookies = {}

    if args.auth_header:
        headers["Authorization"] = args.auth_header

    if args.cookie:
        cookies = parse_cookie(args.cookie)

    # Role sessions
    role_sessions = {}
    if args.user_cookie:
        role_sessions["user"] = parse_cookie(args.user_cookie)
    if args.admin_cookie:
        role_sessions["admin"] = parse_cookie(args.admin_cookie)

    targets = load_targets(args.url, args.list)

    print(f"{BLUE}[+] Targets:{RESET} {len(targets)}")
    print(f"{BLUE}[+] Profile:{RESET} {args.profile}")
    print(f"{BLUE}[+] Depth:{RESET} {args.depth}")
    print(f"{BLUE}[+] Auth (single-session):{RESET} {'ON' if (cookies or headers) else 'OFF'}")
    print(f"{BLUE}[+] Roles (user/admin):{RESET} {'ON' if ('user' in role_sessions and 'admin' in role_sessions) else 'OFF'}")
    print()

    all_findings = []
    graphs = {}

    # Shared module plan: one command = all safe modules
    modules = {
        "sqli_boolean": True,
        "sqli_time": True,
        "xss": True,
        "csrf": True,
        "api_intel": True,
        "idor": True,   # will auto-skip if roles not provided
        "bfla": True,   # will auto-skip if roles not provided
        "smuggle_playbook": True
    }

    for i, target in enumerate(targets, 1):
        print(f"{CYAN}[*] ({i}/{len(targets)}) Crawling:{RESET} {target}")

        inputs = crawl_and_extract_inputs(
            target,
            depth=args.depth,
            headers=headers if headers else None,
            cookies=cookies if cookies else None,
            profile=args.profile,
            timeout=args.timeout
        )

        config = {
            "base_url": target,
            "profile": args.profile,
            "headers": headers,
            "cookies": cookies,
            "auth_check_path": args.auth_check_path,
            "role_sessions": role_sessions,
            "modules": modules,
            "timeout": args.timeout,
            "smuggle_repeats": max(1, args.smuggle_repeats),
        }

        print(f"{CYAN}[*] ({i}/{len(targets)}) Scanning:{RESET} {target}")
        findings, graph = run_scans(inputs, config, return_graph=args.graph)

        all_findings.extend(findings)
        if args.graph and graph:
            graphs[target] = graph

    # Output behavior:
    # - If batch (-l), write JSONL and (optional) graph json, plus one HTML report for all findings.
    # - If single (-u), also allow --json output file.
    if args.list:
        jsonl_path = args.output + ".jsonl"
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for item in all_findings:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        html_path = args.output + ".html"
        generate_html_report(f"BATCH ({len(targets)} targets)", all_findings, html_path)

        if args.graph:
            graph_path = args.output + "_graph.json"
            with open(graph_path, "w", encoding="utf-8") as f:
                json.dump(graphs, f, indent=2, ensure_ascii=False)

        print(f"\n{GREEN}{BOLD}[✓] Batch completed{RESET}")
        print(f"{GREEN}[✓] JSONL:{RESET} {jsonl_path}")
        print(f"{GREEN}[✓] HTML:{RESET}  {html_path}")
        if args.graph:
            print(f"{GREEN}[✓] Graph:{RESET} {graph_path}")
        return

    # Single target output (legacy)
    html_path = args.output + ".html"
    generate_html_report(args.url, all_findings, html_path)
    print(f"\n{GREEN}{BOLD}[✓] Scan completed{RESET}")
    print(f"{GREEN}[✓] HTML:{RESET} {html_path}")

    if args.json:
        json_path = args.output + ".json"
        generate_json_report(args.url, all_findings, json_path)
        print(f"{GREEN}[✓] JSON:{RESET} {json_path}")

if __name__ == "__main__":
    main()


