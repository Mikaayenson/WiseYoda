"""Toy 'Yoda voice' transform — fun, not linguistically serious."""


def to_yoda_speak(text: str) -> str:
    """
    Rough clause shuffle for a fortune-cookie vibe.

    If there is a comma, swap the two sides. Otherwise split the sentence
    roughly in half and swap halves.
    """
    s = text.strip()
    if not s:
        return s
    trailing = ""
    if s.endswith((".", "!", "?")):
        trailing = s[-1]
        s = s[:-1].strip()

    if "," in s:
        left, right = s.split(",", 1)
        body = f"{right.strip()}, {left.strip()}"
    else:
        words = s.split()
        if len(words) <= 4:
            body = s
        else:
            mid = max(1, len(words) // 2)
            first = " ".join(words[:mid])
            second = " ".join(words[mid:])
            body = f"{second}, {first}"

    out = body[0].upper() + body[1:] if body else body
    return f"{out}{trailing if trailing else '.'}"
