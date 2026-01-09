def truncate_text(text: str, max_chars: int) -> str:
    if len(text) > max_chars:
        return text[:max_chars] + "\n[context truncated]"
    return text
