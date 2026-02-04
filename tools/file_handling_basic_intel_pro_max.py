import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "SecAI-Research-Agent/1.0"
}

TIMEOUT = 10

UPLOAD_KEYWORDS = [
    "upload", "file", "attachment", "media", "image", "document"
]

DOWNLOAD_KEYWORDS = [
    "download", "export", "file", "attachment", "media"
]


def analyze_file_handling(url):
    result = {
        "url": url,
        "upload_forms_detected": [],
        "file_inputs": [],
        "download_endpoints": [],
        "client_side_controls": [],
        "risk_signals": [],
        "analysis_notes": [],
        "worth_deeper_testing": False
    }

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        soup = BeautifulSoup(response.text, "html.parser")

        # --- Forms ---
        forms = soup.find_all("form")
        for form in forms:
            enctype = (form.get("enctype") or "").lower()
            method = (form.get("method") or "get").lower()
            action = form.get("action") or ""

            file_inputs = form.find_all("input", {"type": "file"})

            if file_inputs:
                form_info = {
                    "action": action,
                    "method": method,
                    "enctype": enctype,
                    "file_input_count": len(file_inputs)
                }

                result["upload_forms_detected"].append(form_info)

                if enctype != "multipart/form-data":
                    result["risk_signals"].append(
                        "File upload form without multipart/form-data"
                    )

                for inp in file_inputs:
                    accept = inp.get("accept")
                    if accept:
                        result["client_side_controls"].append(
                            f"Accept attribute: {accept}"
                        )
                    else:
                        result["risk_signals"].append(
                            "File input without accept attribute"
                        )

        # --- Download links ---
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"].lower()
            if any(k in href for k in DOWNLOAD_KEYWORDS):
                full_url = urljoin(url, link["href"])
                result["download_endpoints"].append(full_url)

        # --- Client-side validation clues ---
        scripts = soup.find_all("script")
        for script in scripts:
            content = (script.string or "").lower()
            if any(k in content for k in ["filesize", "extension", "mime"]):
                result["client_side_controls"].append(
                    "Client-side file validation logic detected"
                )

    except requests.exceptions.RequestException as e:
        result["analysis_notes"].append(str(e))

    if (
        result["upload_forms_detected"]
        or result["download_endpoints"]
        or result["risk_signals"]
    ):
        result["worth_deeper_testing"] = True

    result["download_endpoints"] = list(set(result["download_endpoints"]))
    result["client_side_controls"] = list(set(result["client_side_controls"]))

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print({
            "tool": "file_handling_intel",
            "status": "error",
            "error": "No target URL provided"
        })
        sys.exit(1)

    target = sys.argv[1].strip()
    data = analyze_file_handling(target)

    print({
        "tool": "file_handling_intel",
        "module": "file_handling_intel_pro_max",
        "target": target,
        "status": "completed",
        "data": data
    })
