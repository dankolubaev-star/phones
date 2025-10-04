def normalize_number(raw: str) -> str:
    digits = ""
    for ch in raw:
        if ch.isdigit() or ch == "+":
            digits += ch

    if digits.startswith("8"):
        digits = "+7" + digits[1:]
    elif not digits.startswith("+"):
        digits = "+7" + digits

    return digits