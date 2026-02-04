"""
SecAI Tool Registry
------------------
Defines available intelligence tools and
the conditions under which they should be considered.

Rule-based (Phase 1)
LLM-based orchestration will wrap this later (Phase 2)
"""

TOOLS_REGISTRY = [
    {
        "name": "recon_surface_intel",
        "module": "tools.recon_intel_pro",
        "description": "Initial surface reconnaissance and application mapping",
        "triggers": [
            "new target",
            "unknown application",
            "first look",
            "recon",
            "surface"
        ],
        "outputs": [
            "subdomains",
            "technology clues",
            "application surface"
        ],
        "risk_domains": [
            "attack surface expansion",
            "exposed components"
        ]
    },

    {
        "name": "auth_session_intel",
        "module": "tools.auth_session_intel_pro",
        "description": "Authentication and session handling intelligence",
        "triggers": [
            "login",
            "authentication",
            "session",
            "account",
            "authorization"
        ],
        "outputs": [
            "auth mechanisms",
            "session handling signals",
            "access control hints"
        ],
        "risk_domains": [
            "broken authentication",
            "session management weaknesses"
        ]
    },

    {
        "name": "input_handling_intel",
        "module": "tools.input_handling_intel_pro",
        "description": "User input handling and validation intelligence",
        "triggers": [
            "forms",
            "input",
            "search",
            "parameters",
            "user supplied data"
        ],
        "outputs": [
            "input points",
            "validation signals",
            "encoding / filtering clues"
        ],
        "risk_domains": [
            "injection classes",
            "input trust boundaries"
        ]
    },

    {
        "name": "file_handling_intel",
        "module": "tools.file_handling_intel_pro",
        "description": "File upload and download handling intelligence",
        "triggers": [
            "file upload",
            "attachment",
            "media",
            "download",
            "export"
        ],
        "outputs": [
            "upload forms",
            "download endpoints",
            "client-side controls"
        ],
        "risk_domains": [
            "file handling risks",
            "content validation gaps"
        ]
    },

    {
        "name": "api_surface_and_emerging_intel",
        "module": "tools.api_surface_and_emerging_intel_pro_max",
        "description": "API surface discovery and emerging risk signals",
        "triggers": [
            "api",
            "graphql",
            "backend",
            "integration",
            "mobile app",
            "future risk"
        ],
        "outputs": [
            "api endpoints",
            "openapi signals",
            "backend technology clues",
            "non-CVE risk indicators"
        ],
        "risk_domains": [
            "api security",
            "authorization boundaries",
            "emerging technology risks"
        ]
    }
]


def suggest_tools(context_text: str):
    """
    Returns a list of tool definitions that MAY be relevant
    based on simple keyword matching (Phase 1 logic).
    """

    context = context_text.lower()
    suggested = []

    for tool in TOOLS_REGISTRY:
        for trigger in tool["triggers"]:
            if trigger in context:
                suggested.append(tool)
                break

    return suggested
