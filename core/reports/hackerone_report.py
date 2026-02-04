def generate_hackerone_report(final_report: dict) -> str:
    """
    Generates a HackerOne / Bugcrowd ready vulnerability report
    based on passive intelligence only.
    """

    target = final_report.get("target", "Unknown target")
    modules = final_report.get("modules", {})
    strategic = final_report.get("strategic_summary", {})
    signals = strategic.get("global_risk_signals", [])

    lines = []

    # =========================
    # Title
    # =========================
    lines.append(f"# Security Assessment Report for {target}\n")

    # =========================
    # Summary
    # =========================
    lines.append("## Summary\n")

    if signals:
        lines.append(
            "Passive reconnaissance identified multiple security-relevant signals "
            "that may indicate exploitable weaknesses. No active exploitation was "
            "performed.\n"
        )
    else:
        lines.append(
            "Passive reconnaissance did not identify any immediately exploitable "
            "high-risk vulnerabilities.\n"
        )

    # =========================
    # Potential Findings
    # =========================
    lines.append("## Potential Vulnerability Areas\n")

    # ---- IDOR ----
    authz = modules.get("authorization", {})
    if authz.get("worth_deeper_testing"):
        lines.append("### 1. Possible Broken Access Control (IDOR)\n")
        lines.append(
            "**Description**  \n"
            "The application appears to expose object identifiers directly. "
            "If proper authorization checks are missing, this could allow users "
            "to access or modify resources belonging to other users.\n"
        )

        urls = authz.get("suspicious_object_urls") or authz.get("object_urls") or []

        if urls:
            lines.append("**Affected URLs / Endpoints**")
            for u in urls[:5]:
                lines.append(f"- {u}")

        lines.append(
            "\n**Attack Scenario**\n"
            "1. Attacker authenticates as a low-privileged user\n"
            "2. Attacker captures a request containing an object ID\n"
            "3. Attacker modifies the ID to reference another user's resource\n"
            "4. Server returns unauthorized data or allows unauthorized actions\n"
        )

        lines.append(
            "**Impact**  \n"
            "- Unauthorized data disclosure  \n"
            "- Account or resource takeover\n"
        )

        lines.append(
            "**Severity (Suggested)**: High\n"
        )

    # ---- API ----
    api = modules.get("api_surface", {})
    if api.get("worth_deeper_testing"):
        lines.append("\n### 2. Public or Weakly Protected API Endpoints\n")
        lines.append(
            "**Description**  \n"
            "Publicly accessible or weakly protected API endpoints were detected. "
            "These endpoints may expose sensitive business logic or data.\n"
        )

        endpoints = api.get("unauthenticated_api_signals") or api.get("api_endpoints_detected") or []

        if endpoints:
            lines.append("**Affected Endpoints**")
            for e in endpoints[:5]:
                lines.append(f"- {e}")

        lines.append(
            "\n**Attack Scenario**\n"
            "- Call API endpoints without authentication\n"
            "- Remove or tamper with authorization headers\n"
            "- Modify user-controlled parameters\n"
        )

        lines.append(
            "**Impact**  \n"
            "- Sensitive data exposure  \n"
            "- Business logic abuse\n"
        )

        lines.append(
            "**Severity (Suggested)**: Medium–High\n"
        )

    # =========================
    # Testing Notes
    # =========================
    lines.append("\n## Testing Notes\n")
    lines.append(
        "- All findings are based on passive analysis only\n"
        "- No exploitation or brute-force activity was performed\n"
        "- Further manual verification is recommended\n"
    )

    # =========================
    # Footer
    # =========================
    lines.append(
        "\n---\n"
        "Report generated automatically via passive security analysis.\n"
        "All testing should remain within program scope and authorization.\n"
    )

    return "\n".join(lines)
