import sys
import requests
import re
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0",
    "Accept": "*/*"
}

TIMEOUT = 10

AUTH_KEYWORDS = [
    "admin", "user", "account", "profile",
    "dashboard", "settings", "manage",
    "billing", "order", "invoice"
]

ID_PATTERNS = [
    r"/\d+",
    r"id=\d+",
    r"user_id=\d+",
    r"account_id=\d+"
]

SENSITIVE_FIELDS = [
    "email", "role", "is_admin",
    "permissions", "user_id",
    "account_id", "balance"
]


def extract_links(html, base_url):
    links = set()
    for match in re.findall(r'href=["\'](.*?)["\']', html):
        full = urljoin(base_url, match)
        if urlparse(full).netloc == urlparse(base_url).netloc:
            links.add(full)
    return list(links)


def analyze_authorization(url):
    result = {
        "url": url,
        "protected_endpoints_detected": [],
        "idor_suspected_endpoints": [],
        "unauthenticated_accessible_endpoints": [],
        "data_exposure_signals": [],
        "risk_signals": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        base_resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        links = extract_links(base_resp.text, url)

        for link in links:
            link_l = link.lower()

            if any(k in link_l for k in AUTH_KEYWORDS):
                result["protected_endpoints_detected"].append(link)

            if any(re.search(p, link_l) for p in ID_PATTERNS):
                result["idor_suspected_endpoints"].append(link)

        # --- Passive unauthenticated access test ---
        for endpoint in result["protected_endpoints_detected"][:10]:
            try:
                r = requests.get(endpoint, headers=HEADERS, timeout=TIMEOUT)
                if r.status_code == 200:
                    result["unauthenticated_accessible_endpoints"].append(endpoint)

                    body_l = r.text.lower()
                    for field in SENSITIVE_FIELDS:
                        if field in body_l:
                            result["data_exposure_signals"].append(
                                f"{endpoint} exposes sensitive field: {field}"
                            )

            except requests.exceptions.RequestException:
                continue

    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))

    # --- Risk logic ---
    if (
        result["unauthenticated_accessible_endpoints"]
        or result["idor_suspected_endpoints"]
        or result["data_exposure_signals"]
    ):
        result["worth_deeper_testing"] = True
        result["risk_signals"].append(
            "Possible Broken Access Control / IDOR condition"
        )

    # Deduplicate lists
    for k, v in result.items():
        if isinstance(v, list):
            result[k] = list(set(v))

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print({
            "tool": "authorization",
            "status": "error",
            "error": "No target URL provided"
        })
        sys.exit(1)

    target = sys.argv[1].strip()
    data = analyze_authorization(target)

    print({
        "tool": "authorization",
        "module": "authorization_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": data
    })
