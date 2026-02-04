import requests
from urllib.parse import urlparse
import re
import time

TIMEOUT = 10
HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

def analyze_target(url: str):
    result = {
        "target": url,
        "reachable": False,
        "protocol": None,
        "redirect_chain": [],
        "final_url": None,

        "tech_stack": [],
        "uses_cdn": False,

        "security_headers": {},
        "cookie_signals": {},
        "cors_policy": None,

        "input_surfaces": {},
        "client_side_signals": [],

        "api_surface_signals": [],
        "bot_protection_signals": [],

        "risk_signals": [],
        "risk_score_hint": {},
        "what_is_worth_testing": [],
        "what_is_not_worth_testing": [],
        "confidence_notes": []
    }

    try:
        session = requests.Session()
        response = session.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT,
            allow_redirects=True
        )

        result["reachable"] = True
        result["final_url"] = response.url
        result["redirect_chain"] = [r.url for r in response.history]

        parsed = urlparse(response.url)
        result["protocol"] = parsed.scheme

        headers = response.headers
        body = response.text.lower()

        # -------------------------
        # Security Headers
        # -------------------------
        result["security_headers"] = {
            "csp": headers.get("content-security-policy"),
            "hsts": headers.get("strict-transport-security"),
            "x_frame_options": headers.get("x-frame-options"),
            "x_content_type": headers.get("x-content-type-options"),
            "referrer_policy": headers.get("referrer-policy")
        }

        if not result["security_headers"]["csp"]:
            result["risk_signals"].append("Missing Content-Security-Policy")
        elif "unsafe-inline" in result["security_headers"]["csp"]:
            result["risk_signals"].append("Weak CSP (unsafe-inline)")

        # -------------------------
        # Server / CDN Detection
        # -------------------------
        server = headers.get("server", "").lower()
        if "cloudflare" in server:
            result["uses_cdn"] = True
            result["tech_stack"].append("cloudflare")
        if "nginx" in server:
            result["tech_stack"].append("nginx")
        if "apache" in server:
            result["tech_stack"].append("apache")

        # -------------------------
        # Cookie Signals (read-only)
        # -------------------------
        cookies = session.cookies
        result["cookie_signals"] = {
            "cookie_count": len(cookies),
            "secure_flag_possible": parsed.scheme == "https"
        }

        if len(cookies) > 0 and parsed.scheme != "https":
            result["risk_signals"].append("Cookies over non-HTTPS")

        # -------------------------
        # CORS
        # -------------------------
        cors = headers.get("access-control-allow-origin")
        if cors:
            result["cors_policy"] = cors
            if cors == "*":
                result["risk_signals"].append("Overly permissive CORS")

        # -------------------------
        # Input Surface Detection
        # -------------------------
        result["input_surfaces"] = {
            "forms": "<form" in body,
            "query_params": "?" in parsed.query or "?" in url,
            "json_responses": "application/json" in headers.get("content-type", "")
        }

        if result["input_surfaces"]["forms"]:
            result["risk_signals"].append("Form-based input surface")

        # -------------------------
        # Client-side Signals (static)
        # -------------------------
        if re.search(r"innerhtml|document\.write|eval\(", body):
            result["client_side_signals"].append("Unsafe DOM manipulation patterns")

        if "<script" in body:
            result["client_side_signals"].append("Client-side scripting present")

        # -------------------------
        # API Surface Signals (passive)
        # -------------------------
        for path in ["/api", "/v1", "/v2", "/graphql"]:
            try:
                r = session.head(parsed.scheme + "://" + parsed.netloc + path, timeout=5)
                if r.status_code < 500:
                    result["api_surface_signals"].append(path)
            except:
                pass

        if result["api_surface_signals"]:
            result["risk_signals"].append("Public API surface detected")

        # -------------------------
        # Bot / Rate-limit Signals
        # -------------------------
        if response.status_code == 429:
            result["bot_protection_signals"].append("Rate limiting active")

        if "cf-challenge" in body or "attention required" in body:
            result["bot_protection_signals"].append("Bot protection detected")

        # -------------------------
        # Risk Score Hints
        # -------------------------
        result["risk_score_hint"] = {
            "client_side": "medium" if result["client_side_signals"] else "low",
            "api": "medium" if result["api_surface_signals"] else "low",
            "infra": "low" if result["uses_cdn"] else "medium"
        }

        # -------------------------
        # Strategic Guidance
        # -------------------------
        if result["client_side_signals"]:
            result["what_is_worth_testing"].append("Client-side input handling")

        if result["api_surface_signals"]:
            result["what_is_worth_testing"].append("API authentication & authorization model")

        result["what_is_not_worth_testing"].extend([
            "Bruteforce attacks",
            "Legacy injection payloads"
        ])

        result["confidence_notes"].append(
            "Analysis based on passive observation only. No exploitation performed."
        )

    except Exception as e:
        result["confidence_notes"].append(f"Analysis failed: {str(e)}")

    return result


if __name__ == "__main__":
    target = input("Target URL (https://example.com): ").strip()
    target_intel_report = analyze_target(target)

    print("\n=== TARGET INTELLIGENCE & RISK PROFILING ===\n")
    for k, v in target_intel_report.items():
        print(f"{k}: {v}")