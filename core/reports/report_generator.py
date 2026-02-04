import json
import datetime
from pathlib import Path
from html import escape

REPORT_DIR = Path("reports/output")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def generate_json_report(target, results: dict):
    report = {
        "target": target,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "modules": results
    }

    path = REPORT_DIR / "report.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return path


def generate_html_report(target, results: dict):
    sections = []

    for module_name, data in results.items():
        section = f"""
        <section>
            <h2>{escape(module_name)}</h2>
            <pre>{escape(json.dumps(data, indent=2))}</pre>
        </section>
        """
        sections.append(section)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>SecAI Security Intelligence Report</title>
        <style>
            body {{ font-family: Arial; background:#0f172a; color:#e5e7eb; }}
            h1 {{ color:#38bdf8; }}
            h2 {{ color:#22d3ee; border-bottom:1px solid #334155; }}
            pre {{
                background:#020617;
                padding:15px;
                overflow:auto;
                border-radius:8px;
            }}
            section {{ margin-bottom:30px; }}
        </style>
    </head>
    <body>
        <h1>Security Intelligence Report</h1>
        <p><b>Target:</b> {escape(target)}</p>
        <p><b>Generated:</b> {datetime.datetime.utcnow().isoformat()} UTC</p>
        {''.join(sections)}
    </body>
    </html>
    """

    path = REPORT_DIR / "report.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    return path
