import sys
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

TIMEOUT = 10

ERROR_KEYWORDS = [
    "exception",
    "stack trace",
    "traceback",
    "fatal error",
    "warning:",
    "notice:",
    "undefined",
    "nullreference",
    "syntax error",
    "internal server error",
    "application error"
]

TECH_KEYWORDS = {
    "php": ["php", "laravel", "symfony"],
    "java": ["exception", "spring", "tomcat"],
    "dotnet": ["asp.net", "viewstate", "iis"],
    "python": ["traceback", "django", "flask"],
    "node": ["node.js", "express", "npm"],
}


def analyze_errors(url):
    result = {
        "url": url,
        "http_status": None,
        "error_indicators": [],
        "technology_clues": [],
        "debug_signals": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        result["http_status"] = response.status_code
        content = response.text.lower()

        for keyword in ERROR_KEYWORDS:
            if keyword in content:
                result["error_indicators"].append(keyword)

        for tech, keywords in TECH_KEYWORDS.items():
            for kw in keywords:
                if kw in content:
                    result["technology_clues"].append(tech)
                    break

        soup = BeautifulSoup(response.text, "html.parser")
        if soup.find("pre"):
            result["debug_signals"].append(
                "Preformatted blocks detected (possible stack trace formatting)"
            )

        if "x-powered-by" in response.headers:
            result["technology_clues"].append(
                f"X-Powered-By: {response.headers.get('x-powered-by')}"
            )

        if "server" in response.headers:
            result["technology_clues"].append(
                f"Server: {response.headers.get('server')}"
            )

    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))

    if (
        result["error_indicators"]
        or result["debug_signals"]
        or (result["http_status"] and result["http_status"] >= 500)
    ):
        result["worth_deeper_testing"] = True

    result["error_indicators"] = list(set(result["error_indicators"]))
    result["technology_clues"] = list(set(result["technology_clues"]))
    result["debug_signals"] = list(set(result["debug_signals"]))

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print({
            "tool": "error_intel",
            "status": "error",
            "error": "No target URL provided"
        })
        sys.exit(1)

    target = sys.argv[1].strip()
    data = analyze_errors(target)

    print({
        "tool": "error_intel",
        "module": "error_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": data
    })
