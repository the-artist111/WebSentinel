
import requests

def run_scans(inputs):
    findings = []

    for item in inputs:
        findings.extend(scan_sqli(item))
        findings.extend(scan_xss(item))
        findings.extend(scan_csrf(item))

    return findings

# ---------------- SQL Injection ----------------
def scan_sqli(item):
    results = []
    if not item["fields"]:
        return results

    true_payload = "' OR 1=1--"
    false_payload = "' AND 1=2--"

    data_true = {f: true_payload for f in item["fields"]}
    data_false = {f: false_payload for f in item["fields"]}

    try:
        r1 = requests.post(item["url"], data=data_true, timeout=5)
        r2 = requests.post(item["url"], data=data_false, timeout=5)

        if len(r1.text) != len(r2.text):
            results.append({
                "type": "SQL Injection",
                "url": item["url"],
                "severity": "Critical",
                "confidence": "High",
                "evidence": "Different responses for boolean conditions",
                "remediation": "Use parameterized queries and prepared statements"
            })
    except Exception:
        pass

    return results

# ---------------- XSS ----------------
def scan_xss(item):
    results = []
    if not item["fields"]:
        return results

    payload = "<svg/onload=alert(1)>"
    data = {f: payload for f in item["fields"]}

    try:
        r = requests.post(item["url"], data=data, timeout=5)
        if payload in r.text:
            results.append({
                "type": "Cross-Site Scripting (XSS)",
                "url": item["url"],
                "severity": "High",
                "confidence": "Medium",
                "evidence": "Payload reflected without encoding",
                "remediation": "Apply output encoding and Content Security Policy (CSP)"
            })
    except Exception:
        pass

    return results

# ---------------- CSRF ----------------
def scan_csrf(item):
    results = []

    if item["method"] == "post":
        has_token = any("csrf" in f.lower() for f in item["fields"])
        if not has_token:
            results.append({
                "type": "CSRF",
                "url": item["url"],
                "severity": "Medium",
                "confidence": "High",
                "evidence": "POST request without CSRF token",
                "remediation": "Implement CSRF tokens and SameSite cookies"
            })

    return results
