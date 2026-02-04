import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0",
    "Accept": "*/*"
}

TIMEOUT = 10

API_KEYWORDS = [
    "/api", "/v1", "/v2", "/v3",
    "/graphql", "/rest", "/internal",
    "/private", "/admin", "/service"
]

SENSITIVE_RESPONSE_KEYWORDS = [
    "email", "role", "token", "jwt",
    "is_admin", "permissions", "password",
    "user_id", "session", "api_key"
]


def extract_js_files(soup, base_url):
    js_files = []
    for script in soup.find_all("script", src=True):
        js_files.append(urljoin(base_url, script["src"]))
    return list(set(js_files))


def extract_api_candidates(text):
    found = set()
    for kw in API_KEYWORDS:
        if kw in text:
            matches = re.findall(rf"{kw}[a-zA-Z0-9_/\-?=&]*", text)
            for m in matches:
                found.add(m)
    return list(found)


def analyze_api_surface(url):
    result = {
        "url": url,
        "api_endpoints_detected": [],
        "js_files_analyzed": [],
        "unauthenticated_api_signals": [],
        "data_exposure_signals": [],
        "risk_signals": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(response.text, "html.parser")

        # --- HTML API clues ---
        html_api_candidates = extract_api_candidates(response.text)
        for api in html_api_candidates:
            result["api_endpoints_detected"].append(urljoin(url, api))

        # --- JavaScript analysis ---
        js_files = extract_js_files(soup, url)
        for js_url in js_files:
            try:
                js_resp = requests.get(js_url, headers=HEADERS, timeout=TIMEOUT)
                result["js_files_analyzed"].append(js_url)

                js_api_candidates = extract_api_candidates(js_resp.text)
                for api in js_api_candidates:
                    result["api_endpoints_detected"].append(urljoin(url, api))

            except requests.exceptions.RequestException:
                continue

        # --- Passive API response probing (safe) ---
        for api_url in list(set(result["api_endpoints_detected"]))[:10]:
            try:
                api_resp = requests.get(api_url, headers=HEADERS, timeout=TIMEOUT)

                if api_resp.status_code == 200:
                    result["unauthenticated_api_signals"].append(api_url)

                    for key in SENSITIVE_RESPONSE_KEYWORDS:
                        if key in api_resp.text.lower():
                            result["data_exposure_signals"].append(
                                f"{api_url} may expose sensitive field: {key}"
                            )

            except requests.exceptions.RequestException:
                continue

    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))

    # --- Decision Logic ---
    if (
        len(result["api_endpoints_detected"]) > 0
        or len(result["data_exposure_signals"]) > 0
        or len(result["unauthenticated_api_signals"]) > 0
    ):
        result["worth_deeper_testing"] = True

    # Deduplicate
    for k in result:
        if isinstance(result[k], list):
            result[k] = list(set(result[k]))

    return result

if __name__ == "__main__":
    target = input("Target URL (https://example.com): ").strip()
    api_surface_intel_report = analyze_api_surface(target)

    print("\n=== API SURFACE INTELLIGENCE REPORT ===\n")
    for k, v in api_surface_intel_report.items():
        print(f"{k}: {v}")