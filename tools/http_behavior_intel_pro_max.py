import sys
import requests
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

TIMEOUT = 10


def analyze_http_behavior(url):
    result = {
        "url": url,
        "reachable": False,
        "status_code": None,
        "redirect_chain": [],
        "headers": {},
        "risk_signals": [],
        "behavior_notes": [],
        "worth_deeper_testing": False
    }

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT,
            allow_redirects=True
        )

        result["reachable"] = True
        result["status_code"] = response.status_code

        # Redirect chain
        for r in response.history:
            result["redirect_chain"].append({
                "from": r.url,
                "status": r.status_code,
                "to": r.headers.get("Location")
            })

        result["headers"] = dict(response.headers)

        # --- Behavior heuristics ---
        if response.status_code == 500:
            result["risk_signals"].append("Server error on basic GET")
            result["behavior_notes"].append(
                "500 on simple request often indicates weak input handling"
            )

        if response.status_code == 403:
            result["behavior_notes"].append(
                "403 detected — access control present but may be bypassable via logic"
            )

        if response.status_code == 401:
            result["risk_signals"].append("Authentication surface detected")
            result["behavior_notes"].append(
                "401 suggests auth-protected area"
            )

        if "X-Powered-By" in response.headers:
            result["risk_signals"].append(
                f"Technology disclosure: {response.headers.get('X-Powered-By')}"
            )

        if "Server" in response.headers:
            result["risk_signals"].append(
                f"Server header exposed: {response.headers.get('Server')}"
            )

        lower_text = response.text.lower()
        if "exception" in lower_text or "stack trace" in lower_text:
            result["risk_signals"].append("Verbose error content")
            result["behavior_notes"].append(
                "Error response leaks internal exception wording"
            )

        # Decision logic
        if (
            response.status_code in [500, 401]
            or len(result["risk_signals"]) >= 2
        ):
            result["worth_deeper_testing"] = True

    except requests.exceptions.RequestException as e:
        result["behavior_notes"].append(f"Connection issue: {str(e)}")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print({
            "tool": "http_behavior_intel",
            "module": "http_behavior_intel_pro_max",
            "status": "error",
            "error": "No target URL provided"
        })
        sys.exit(1)

    target = sys.argv[1].strip()
    data = analyze_http_behavior(target)

    print({
        "tool": "http_behavior_intel",
        "module": "http_behavior_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": data
    })
