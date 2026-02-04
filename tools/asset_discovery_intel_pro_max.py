import sys
import requests
import socket
import re
from collections import defaultdict

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}


def get_ct_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subs = set()

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            data = r.json()
            for entry in data:
                name = entry.get("name_value", "")
                for sub in name.split("\n"):
                    if "*" not in sub:
                        subs.add(sub.strip().lower())
    except Exception:
        pass

    return subs


def resolve_dns(subdomain):
    try:
        return socket.gethostbyname(subdomain)
    except Exception:
        return None


def analyze_subdomains(domain):
    result = {
        "domain": domain,
        "total_discovered": 0,
        "subdomains": [],
        "risk_summary": defaultdict(list),
        "what_is_worth_testing": [],
        "what_is_not_worth_testing": [],
        "confidence_notes": []
    }

    subs = get_ct_subdomains(domain)
    result["total_discovered"] = len(subs)

    for sub in subs:
        entry = {
            "subdomain": sub,
            "resolves": False,
            "ip": None,
            "risk_signals": [],
            "likely_role": "unknown"
        }

        ip = resolve_dns(sub)
        if ip:
            entry["resolves"] = True
            entry["ip"] = ip
        else:
            entry["risk_signals"].append("Does not resolve")

        # Heuristic role detection
        if re.search(r"(api|graphql|v1|v2)", sub):
            entry["likely_role"] = "api"
            entry["risk_signals"].append("API surface indicator")

        if re.search(r"(dev|test|staging|beta)", sub):
            entry["likely_role"] = "non-production"
            entry["risk_signals"].append("Non-production environment")

        if re.search(r"(admin|internal|manage)", sub):
            entry["likely_role"] = "sensitive"
            entry["risk_signals"].append("Sensitive naming pattern")

        if entry["resolves"]:
            result["subdomains"].append(entry)
            for signal in entry["risk_signals"]:
                result["risk_summary"][signal].append(sub)

    # Strategic guidance
    if result["risk_summary"].get("Non-production environment"):
        result["what_is_worth_testing"].append(
            "Non-production subdomains (often weaker controls)"
        )

    if result["risk_summary"].get("API surface indicator"):
        result["what_is_worth_testing"].append(
            "API authorization and object-level access"
        )

    result["what_is_not_worth_testing"].extend([
        "Subdomains that do not resolve",
        "Marketing or static-only hosts"
    ])

    result["confidence_notes"].append(
        "Subdomains collected via certificate transparency logs only. No brute-force used."
    )

    # defaultdict → normal dict (JSON safe)
    result["risk_summary"] = dict(result["risk_summary"])

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print({
            "tool": "asset_discovery",
            "status": "error",
            "error": "No root domain provided"
        })
        sys.exit(1)

    target = sys.argv[1].replace("https://", "").replace("http://", "").strip("/")

    output = analyze_subdomains(target)

    print({
        "tool": "asset_discovery",
        "module": "asset_discovery_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": output
    })
