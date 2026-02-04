def write_anti_duplicate(cvss: dict, chains: list) -> str:
    lines = []

    lines.append("## Why this is NOT a duplicate")
    lines.append(
        "This report is not a low-impact configuration issue. "
        "It demonstrates a concrete attack path with security impact."
    )

    lines.append(
        f"The issue was assessed as **{cvss['severity']} severity** "
        f"with a CVSS score of **{cvss['cvss_score']}**, based on impact "
        "and exploitability."
    )

    if chains:
        lines.append(
            "Additionally, the issue can be chained into broader impact scenarios:"
        )
        for c in chains:
            lines.append(f"- {c['title']}: {c['impact']}")

    return "\n".join(lines)
