def generate_poc_examples(final_report: dict = None) -> str:
    """
    Generates clear, copy-paste-ready Proof of Concept examples
    for common bug bounty scenarios (IDOR / API abuse).
    """

    lines = []

    # -------------------------
    # Generic IDOR PoC (always useful)
    # -------------------------
    lines.append("## Proof of Concept (PoC)\n")
    lines.append("### Example PoC – IDOR / Broken Access Control\n")
    lines.append("```http")
    lines.append("GET /api/v1/resource/12345 HTTP/1.1")
    lines.append("Host: target.com")
    lines.append("Authorization: Bearer <your-valid-user-token>")
    lines.append("```")
    lines.append(
        "➡ Change `12345` to another ID (e.g. `12346`) and resend the request.\n"
        "➡ If data belonging to another user is returned, this confirms an IDOR issue.\n"
    )

    # -------------------------
    # Context-aware PoC (from scan results, if available)
    # -------------------------
    if final_report:
        modules = final_report.get("modules", {})
        authz = modules.get("authorization", {})

        urls = (
            authz.get("suspicious_object_urls")
            or authz.get("object_urls")
            or []
        )

        if urls:
            lines.append("### Context-Specific PoC Based on Discovered Endpoints\n")
            example_url = urls[0]

            lines.append("```bash")
            lines.append(f"curl -i '{example_url}' \\")
            lines.append("  -H 'Authorization: Bearer <your-valid-user-token>'")
            lines.append("```")
            lines.append(
                "➡ Modify object identifiers or user references in the URL.\n"
                "➡ Observe whether unauthorized resources become accessible.\n"
            )

    # -------------------------
    # Notes for Triagers
    # -------------------------
    lines.append(
        "---\n"
        "**Note:** This PoC does not rely on brute force, fuzzing, or race conditions.\n"
        "It demonstrates a direct authorization logic flaw using a single modified request.\n"
    )

    return "\n".join(lines)
