import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

TIMEOUT = 10

RISK_KEYWORDS = [
    "search", "query", "q", "s",
    "redirect", "return", "next", "url",
    "id", "user", "account",
    "comment", "message", "feedback",
    "file", "upload"
]


def analyze_input_handling(target_url):
    result = {
        "url": target_url,
        "query_parameters": [],
        "forms": [],
        "input_fields": [],
        "client_side_controls": [],
        "risk_indicators": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        response = requests.get(
            target_url,
            headers=HEADERS,
            timeout=TIMEOUT,
            allow_redirects=True
        )

        soup = BeautifulSoup(response.text, "html.parser")

        # --- Query parameters ---
        parsed = urlparse(response.url)
        query_params = parse_qs(parsed.query)

        for param, values in query_params.items():
            param_info = {
                "name": param,
                "example_value": values[0] if values else None
            }
            result["query_parameters"].append(param_info)

            for kw in RISK_KEYWORDS:
                if kw in param.lower():
                    result["risk_indicators"].append(
                        f"Query parameter '{param}' may warrant input validation review"
                    )

        # --- Forms & inputs ---
        for form in soup.find_all("form"):
            form_info = {
                "action": urljoin(target_url, form.get("action")) if form.get("action") else target_url,
                "method": form.get("method", "get").lower(),
                "inputs": []
            }

            for inp in form.find_all("input"):
                field = {
                    "name": inp.get("name"),
                    "type": inp.get("type", "text"),
                    "maxlength": inp.get("maxlength"),
                    "pattern": inp.get("pattern"),
                    "required": inp.has_attr("required"),
                    "autocomplete": inp.get("autocomplete")
                }

                form_info["inputs"].append(field)
                result["input_fields"].append(field)

                # --- Validation signals ---
                if field["maxlength"] is None and field["type"] in ["text", "search"]:
                    result["client_side_controls"].append(
                        f"Input '{field['name']}' has no maxlength constraint"
                    )

                if field["pattern"] is None and field["type"] == "text":
                    result["client_side_controls"].append(
                        f"Input '{field['name']}' has no pattern validation"
                    )

                for kw in RISK_KEYWORDS:
                    if field["name"] and kw in field["name"].lower():
                        result["risk_indicators"].append(
                            f"Input field '{field['name']}' may warrant validation review"
                        )

            result["forms"].append(form_info)

    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))

    # --- Decision logic ---
    if (
        len(result["query_parameters"]) > 0
        or len(result["input_fields"]) > 0
        or len(result["risk_indicators"]) > 0
    ):
        result["worth_deeper_testing"] = True

    # Deduplicate
    result["risk_indicators"] = list(set(result["risk_indicators"]))
    result["client_side_controls"] = list(set(result["client_side_controls"]))

    return result

if __name__ == "__main__":
    target = input("Target URL (https://example.com): ").strip()
    input_handling_report = analyze_input_handling(target)

    print("\n=== INPUT HANDLING & VALIDATION INTELLIGENCE ===\n")
    for k, v in input_handling_report.items():
        print(f"{k}: {v}")
