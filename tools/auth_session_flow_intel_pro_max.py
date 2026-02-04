import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

TIMEOUT = 10

LOGIN_KEYWORDS = [
    "login", "sign in", "signin", "auth", "authentication",
    "password", "username", "email", "otp", "2fa", "mfa"
]

TOKEN_HINTS = [
    "authorization",
    "bearer",
    "jwt",
    "token"
]


def analyze_auth_and_session(base_url):
    result = {
        "url": base_url,
        "login_surface_detected": False,
        "login_indicators": [],
        "forms_detected": [],
        "cookies_observed": [],
        "session_security_flags": [],
        "token_indicators": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        response = requests.get(
            base_url,
            headers=HEADERS,
            timeout=TIMEOUT,
            allow_redirects=True
        )

        html = response.text.lower()
        soup = BeautifulSoup(response.text, "html.parser")

        # --- Login keyword scan ---
        for kw in LOGIN_KEYWORDS:
            if kw in html:
                result["login_indicators"].append(kw)

        if result["login_indicators"]:
            result["login_surface_detected"] = True

        # --- Form discovery ---
        for form in soup.find_all("form"):
            action = form.get("action")
            method = form.get("method", "get").lower()
            inputs = [i.get("type", "text") for i in form.find_all("input")]

            result["forms_detected"].append({
                "action": urljoin(base_url, action) if action else base_url,
                "method": method,
                "inputs": list(set(inputs))
            })

        # --- Cookies & session flags ---
        for cookie in response.cookies:
            cookie_info = {
                "name": cookie.name,
                "secure": cookie.secure,
                "httponly": cookie.has_nonstandard_attr("HttpOnly"),
                "path": cookie.path,
                "domain": cookie.domain
            }
            result["cookies_observed"].append(cookie_info)

            if not cookie.secure:
                result["session_security_flags"].append(
                    f"Cookie '{cookie.name}' missing Secure flag"
                )

            if not cookie.has_nonstandard_attr("HttpOnly"):
                result["session_security_flags"].append(
                    f"Cookie '{cookie.name}' missing HttpOnly flag"
                )

        # --- Header-based token hints ---
        for header, value in response.headers.items():
            header_l = header.lower()
            value_l = value.lower()

            for hint in TOKEN_HINTS:
                if hint in header_l or hint in value_l:
                    result["token_indicators"].append(
                        f"{header}: {value}"
                    )

    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))

    # --- Decision Logic ---
    if (
        result["login_surface_detected"]
        or result["cookies_observed"]
        or result["session_security_flags"]
        or result["token_indicators"]
    ):
        result["worth_deeper_testing"] = True

    # Deduplicate
    result["login_indicators"] = list(set(result["login_indicators"]))
    result["session_security_flags"] = list(set(result["session_security_flags"]))
    result["token_indicators"] = list(set(result["token_indicators"]))

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

    output = analyze_auth_and_session(target)

    print({
        "tool": "authentication",
        "module": "authentication_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": output
    })

