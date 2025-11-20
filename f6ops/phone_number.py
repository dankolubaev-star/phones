def normalize_number(raw):
    clean = ""

    for ch in raw:
        if ch.isdigit() or ch == "+":
            clean += ch
        elif ch == "*":
            clean += "0"

    if clean.startswith("8"):
        clean = "+7" + clean[1:]
    elif not clean.startswith("+"):
        clean = "+7" + clean

    return clean