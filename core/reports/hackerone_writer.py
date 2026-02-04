def generate_hackerone_report(
    target: str,
    narrative: str,
    cvss: dict,
    decision: dict,
    duplicate: dict,
    chains: list,
    poc: str,
    anti_dup: str
) -> str:
    lines = []

    lines.append(f"# {cvss['severity']} Severity Security Vulnerability\n")

    # =========================
    # Summary
    # =========================
    lines.append("## Summary")
    lines.append(
        f"A passive security assessment of **{target}** identified a "
        f"potential {cvss['severity']} severity vulnerability. "
        f"The issue appears exploitable under realistic conditions."
    )

    # =========================
    # Severity
    # =========================
    lines.append("\n## Severity & Impact")
    lines.append(f"- CVSS Score: {cvss['cvss_score']}")
    lines.append(f"- Severity: {cvss['severity']}")
    lines.append(f"- Impact Justification:")
    for j in cvss["justification"]:
        lines.append(f"  - {j}")

    # =========================
    # Technical Details
    # =========================
    lines.append("\n## Technical Analysis")
    lines.append(narrative)

    # =========================
    # Attack Chains
    # =========================
    if chains:
        lines.append("\n## Attack Scenarios")
        for c in chains:
            lines.append(f"### {c['title']}")
            lines.append(f"- Impact: {c['impact']}")
            lines.append(f"- Why it matters: {c['why_it_matters']}")

    # =========================
    # PoC
    # =========================
    if poc:
        lines.append("\n## Proof of Concept")
        lines.append(poc)

    # =========================
    # Duplicate Analysis
    # =========================
    if duplicate:
        lines.append("\n## Duplicate Risk Assessment")
        lines.append(f"- Likelihood: {duplicate.get('likelihood')}")
        lines.append(f"- Reasoning: {duplicate.get('reason')}")

    if anti_dup:
        lines.append("\n" + anti_dup)

    # =========================
    # Final Recommendation
    # =========================
    lines.append("\n## Reporting Recommendation")
    lines.append(f"- Should Report: {'YES' if decision['should_report'] else 'NO'}")
    lines.append(f"- Confidence: {decision['confidence']}")

    # =========================
    # Footer
    # =========================
    lines.append(
        "\n---\n"
        "_This report was generated from passive analysis only. "
        "All testing should remain within program scope._"
    )

    return "\n".join(lines)
