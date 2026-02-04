import sys
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

TIMEOUT = 10

AUTH_KEYWORDS = [
    "login", "signin", "auth", "session", "token", "password", "account"
]

ROLE_KEYWORDS = [
    "role", "admin", "user", "permission", "access", "privilege"
]


def analyze_auth_surface(url):
    result = {
        "url": url,
        "auth_endpoints_detected": [],
        "cookies_observed": [],
        "auth_headers": [],
        "role_signals": [],
        "risk_signals": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT,
            allow_redirects=True
        )

        # --- Cookies ---
        for cookie in response.cookies:
            result["cookies_observed"].append({
                "name": cookie.name,
                "secure": cookie.secure,
                "httponly": cookie.has_nonstandard_attr("HttpOnly")
            })

            if not cookie.secure:
                result["risk_signals"].append(
                    f"Cookie {cookie.name} missing Secure flag"
                )

        # --- Headers ---
        for header, value in response.headers.items():
            header_l = header.lower()
            value_l = value.lower()

            if any(k in header_l or k in value_l for k in ["auth", "token", "bearer"]):
                result["auth_headers"].append({
                    "header": header,
                    "value_snippet": value[:50]
                })

        # --- HTML Analysis ---
        soup = BeautifulSoup(response.text, "html.parser")

        # Forms
        for form in soup.find_all("form"):
            form_action = (form.get("action") or "").lower()
            form_text = form.get_text().lower()

            if any(k in form_action or k in form_text for k in AUTH_KEYWORDS):
                result["auth_endpoints_detected"].append(
                    form.get("action")
                )

        # Links
        for link in soup.find_all("a", href=True):
            href = link["href"].lower()

            if any(k in href for k in AUTH_KEYWORDS):
                result["auth_endpoints_detected"].append(href)

            if any(k in href for k in ROLE_KEYWORDS):
                result["role_signals"].append(href)

        # Role-related text
        page_text = soup.get_text().lower()
        for k in ROLE_KEYWORDS:
            if k in page_text:
                result["role_signals"].append(
                    f"Keyword detected in content: {k}"
                )

    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(f"Connection issue: {str(e)}")

    # --- Decision Logic ---
    if (
        result["auth_endpoints_detected"]
        or result["role_signals"]
        or result["risk_signals"]
    ):
        result["worth_deeper_testing"] = True

    # Deduplicate
    result["auth_endpoints_detected"] = list(set(result["auth_endpoints_detected"]))
    result["role_signals"] = list(set(result["role_signals"]))

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print({
            "tool": "authentication",
            "status": "error",
            "error": "No target URL provided"
        })
        sys.exit(1)

    target = sys.argv[1].strip()
    data = analyze_auth_surface(target)

    print({
        "tool": "authentication",
        "module": "authentication_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": data
    })
