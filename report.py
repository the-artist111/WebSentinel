import json
from datetime import datetime

def generate_html_report(target, findings, output_file):
    with open(output_file, "w") as f:
        f.write("<html><head><title>WebSentinel Report</title></head><body>")
        f.write(f"<h1>WebSentinel Scan Report</h1>")
        f.write(f"<p><b>Target:</b> {target}</p>")
        f.write(f"<p><b>Scan Time:</b> {datetime.now()}</p><hr>")

        if not findings:
            f.write("<p>No vulnerabilities detected.</p>")
        else:
            for v in findings:
                f.write("<div style='border:1px solid #333;padding:10px;margin:10px'>")
                f.write(f"<h3>{v['type']} ({v['severity']})</h3>")
                f.write(f"<p><b>Confidence:</b> {v['confidence']}</p>")
                f.write(f"<p><b>URL:</b> {v['url']}</p>")
                f.write(f"<p><b>Evidence:</b> {v['evidence']}</p>")
                f.write(f"<p><b>Remediation:</b> {v['remediation']}</p>")
                f.write("</div>")

        f.write("</body></html>")

def generate_json_report(target, findings, output_file):
    report = {
        "tool": "WebSentinel",
        "target": target,
        "scan_time": str(datetime.now()),
        "findings": findings
    }

    with open(output_file, "w") as f:
        json.dump(report, f, indent=4)
