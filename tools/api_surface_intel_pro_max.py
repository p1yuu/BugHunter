import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

TIMEOUT = 10

API_PATH_KEYWORDS = [
    "/api", "/v1", "/v2", "/v3", "/graphql", "/rest", "/service"
]

OPENAPI_FILES = [
    "/swagger",
    "/swagger-ui",
    "/swagger.json",
    "/openapi.json",
    "/v3/api-docs"
]

ERROR_KEYWORDS = [
    "exception",
    "stack trace",
    "traceback",
    "sql",
    "nullreference",
    "undefined",
    "error:"
]


def analyze_api_surface(url):
    result = {
        "url": url,
        "potential_api_endpoints": [],
        "openapi_signals": [],
        "graphql_signals": [],
        "versioning_detected": [],
        "backend_error_signals": [],
        "technology_clues": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        content = resp.text.lower()
        soup = BeautifulSoup(resp.text, "html.parser")
    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))
        return result

    # --- Script & Link scanning for API paths ---
    elements = soup.find_all(["script", "a", "link"])
    for el in elements:
        text = ""
        if el.name == "script":
            text = (el.string or "").lower()
        elif el.name in ["a", "link"]:
            text = (el.get("href") or "").lower()

        for k in API_PATH_KEYWORDS:
            if k in text:
                full = urljoin(url, text)
                result["potential_api_endpoints"].append(full)

        if "graphql" in text:
            result["graphql_signals"].append("GraphQL usage signal detected")

    # --- OpenAPI / Swagger probing (safe GET only) ---
    for path in OPENAPI_FILES:
        try:
            test_url = urljoin(url, path)
            r = requests.get(test_url, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code == 200 and ("swagger" in r.text.lower() or "openapi" in r.text.lower()):
                result["openapi_signals"].append(test_url)
        except requests.exceptions.RequestException:
            pass

    # --- Versioning detection ---
    for k in API_PATH_KEYWORDS:
        if k in content and k.startswith("/v"):
            result["versioning_detected"].append(k)

    # --- Backend error clues ---
    for ek in ERROR_KEYWORDS:
        if ek in content:
            result["backend_error_signals"].append(
                f"Backend error keyword detected: {ek}"
            )

    # --- Technology clues ---
    if "x-powered-by" in resp.headers:
        result["technology_clues"].append(
            f"X-Powered-By: {resp.headers.get('x-powered-by')}"
        )

    server = resp.headers.get("Server")
    if server:
        result["technology_clues"].append(f"Server header: {server}")

    # Deduplicate
    for k in [
        "potential_api_endpoints",
        "openapi_signals",
        "backend_error_signals",
        "technology_clues",
        "versioning_detected"
    ]:
        result[k] = list(set(result[k]))

    # Decision logic
    if (
        result["potential_api_endpoints"]
        or result["openapi_signals"]
        or result["graphql_signals"]
        or result["backend_error_signals"]
    ):
        result["worth_deeper_testing"] = True

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print({
            "tool": "api_surface",
            "status": "error",
            "error": "No target URL provided"
        })
        sys.exit(1)

    target = sys.argv[1]
    output = analyze_api_surface(target)

    print({
        "tool": "api_surface",
        "module": "api_surface_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": output
    })
