import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

TIMEOUT = 10


def analyze_input_surface(url):
    result = {
        "url": url,
        "query_parameters": {},
        "forms": [],
        "risk_signals": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    if query_params:
        result["query_parameters"] = {
            k: len(v) for k, v in query_params.items()
        }
        result["analysis_notes"].append(
            f"{len(query_params)} query parameter(s) detected"
        )

        if len(query_params) >= 3:
            result["risk_signals"].append(
                "Multiple query parameters increase logic/injection surface"
            )

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")

        for idx, form in enumerate(forms, start=1):
            form_info = {
                "form_id": idx,
                "method": form.get("method", "GET").upper(),
                "action": form.get("action"),
                "inputs": [],
                "notes": []
            }

            inputs = form.find_all("input")

            for inp in inputs:
                input_type = inp.get("type", "text")
                name = inp.get("name")

                form_info["inputs"].append({
                    "name": name,
                    "type": input_type
                })

                if input_type in ["hidden", "password"]:
                    form_info["notes"].append(
                        f"Sensitive input type detected: {input_type}"
                    )

            if len(form_info["inputs"]) >= 4:
                form_info["notes"].append(
                    "Form has many inputs — complex validation likely"
                )
                result["risk_signals"].append(
                    "Complex form logic surface"
                )

            if form_info["method"] == "POST":
                result["analysis_notes"].append(
                    "POST-based form detected (server-side handling)"
                )

            result["forms"].append(form_info)

        if forms:
            result["analysis_notes"].append(
                f"{len(forms)} form(s) discovered on page"
            )

    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(f"Connection issue: {str(e)}")

    # Decision logic
    if (
        len(result["risk_signals"]) >= 2
        or len(result["forms"]) >= 1
        or len(result["query_parameters"]) >= 2
    ):
        result["worth_deeper_testing"] = True

    return result


if __name__ == "__main__":
    target = input("Target URL (https://example.com): ").strip()
    input_surface_report = analyze_input_surface(target)

    print("\n=== INPUT SURFACE & PARAMETER INTELLIGENCE ===\n")
    for k, v in input_surface_report.items():
        print(f"{k}: {v}")