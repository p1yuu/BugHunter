import os

def export_markdown(target: str, content: str) -> str:
    safe = target.replace("https://", "").replace("/", "_")
    path = f"attack_guide_{safe}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.abspath(path)
