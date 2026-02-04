import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

TIMEOUT = 10

FILE_KEYWORDS = [
    "upload", "file", "attachment", "import",
    "document", "image", "media", "avatar",
    "profile picture", "resume"
]


def analyze_file_handling(target_url):
    result = {
        "url": target_url,
        "file_inputs_detected": [],
        "upload_forms": [],
        "client_side_constraints": [],
        "textual_indicators": [],
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
        html_lower = response.text.lower()

        # --- Textual hints ---
        for kw in FILE_KEYWORDS:
            if kw in html_lower:
                result["textual_indicators"].append(
                    f"Keyword '{kw}' present in page content"
                )

        # --- File inputs & forms ---
        for form in soup.find_all("form"):
            file_inputs = form.find_all("input", {"type": "file"})
            if not file_inputs:
                continue

            form_info = {
                "action": urljoin(target_url, form.get("action")) if form.get("action") else target_url,
                "method": form.get("method", "get").lower(),
                "file_fields": []
            }

            for inp in file_inputs:
                field = {
                    "name": inp.get("name"),
                    "accept": inp.get("accept"),
                    "multiple": inp.has_attr("multiple")
                }

                form_info["file_fields"].append(field)
                result["file_inputs_detected"].append(field)

                if field["accept"] is None:
                    result["client_side_constraints"].append(
                        f"File input '{field['name']}' has no 'accept' restriction"
                    )

                if field["multiple"]:
                    result["client_side_constraints"].append(
                        f"File input '{field['name']}' allows multiple files"
                    )

            result["upload_forms"].append(form_info)

        # --- Risk logic ---
        if result["file_inputs_detected"]:
            result["risk_indicators"].append(
                "File upload surface detected — file handling controls may warrant review"
            )

        if result["client_side_constraints"]:
            result["risk_indicators"].append(
                "Client-side file restrictions appear limited or absent"
            )

    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))

    if (
        result["file_inputs_detected"]
        or result["textual_indicators"]
        or result["risk_indicators"]
    ):
        result["worth_deeper_testing"] = True

    result["client_side_constraints"] = list(set(result["client_side_constraints"]))
    result["risk_indicators"] = list(set(result["risk_indicators"]))
    result["textual_indicators"] = list(set(result["textual_indicators"]))

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print({
            "tool": "file_upload_surface_intel",
            "module": "file_upload_surface_intel_pro_max",
            "status": "error",
            "error": "No target URL provided"
        })
        sys.exit(1)

    target = sys.argv[1].strip()
    data = analyze_file_handling(target)

    print({
        "tool": "file_upload_surface_intel",
        "module": "file_upload_surface_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": data
    })
