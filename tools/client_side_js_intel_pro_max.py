import sys
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

TIMEOUT = 10

# High-level indicators only (NO exploitation)
DANGEROUS_SINKS = [
    "innerHTML",
    "outerHTML",
    "document.write",
    "document.writeln",
    "eval(",
    "setTimeout(",
    "setInterval(",
    "Function("
]

SUSPICIOUS_SOURCES = [
    "location",
    "document.cookie",
    "document.referrer",
    "window.name",
    "localStorage",
    "sessionStorage"
]

SECRET_PATTERNS = [
    r"api[_-]?key",
    r"secret",
    r"token",
    r"auth",
    r"bearer",
    r"password"
]


def analyze_client_side_js(url):
    result = {
        "url": url,
        "inline_scripts_count": 0,
        "external_scripts": [],
        "dangerous_sinks_detected": [],
        "untrusted_sources_detected": [],
        "potential_secrets": [],
        "client_side_logic_risks": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(resp.text, "html.parser")
    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))
        return result

    scripts = soup.find_all("script")

    for script in scripts:
        # --- External JS ---
        if script.get("src"):
            src = urljoin(url, script["src"])
            result["external_scripts"].append(src)
            continue

        # --- Inline JS ---
        code = script.string or ""
        if not code.strip():
            continue

        result["inline_scripts_count"] += 1
        lowered = code.lower()

        for sink in DANGEROUS_SINKS:
            if sink.lower() in lowered:
                result["dangerous_sinks_detected"].append(sink)

        for source in SUSPICIOUS_SOURCES:
            if source.lower() in lowered:
                result["untrusted_sources_detected"].append(source)

        for pattern in SECRET_PATTERNS:
            if re.search(pattern, lowered):
                result["potential_secrets"].append(
                    f"Keyword match: {pattern}"
                )

        if any(k in lowered for k in ["isadmin", "role", "permission"]):
            result["client_side_logic_risks"].append(
                "Client-side authorization / role logic detected"
            )

    # Deduplicate
    for k, v in result.items():
        if isinstance(v, list):
            result[k] = list(set(v))

    # Decision logic
    if (
        result["dangerous_sinks_detected"]
        or result["untrusted_sources_detected"]
        or result["potential_secrets"]
        or result["client_side_logic_risks"]
    ):
        result["worth_deeper_testing"] = True

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print({
            "tool": "client_js",
            "status": "error",
            "error": "No target URL provided"
        })
        sys.exit(1)

    target = sys.argv[1].strip()
    data = analyze_client_side_js(target)

    print({
        "tool": "client_js",
        "module": "client_js_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": data
    })
