def scope_warning(target: str) -> str:
    return (
        "⚠️ SCOPE & LEGAL NOTICE\n"
        "This report is based on passive analysis only.\n\n"
        "Before active testing:\n"
        "- Verify the target is in-scope for the relevant bug bounty program\n"
        "- Avoid testing payments, real user data, or denial-of-service vectors\n"
        "- Follow program rules and local laws\n\n"
        "You are responsible for ensuring authorization before testing.\n"
    )
