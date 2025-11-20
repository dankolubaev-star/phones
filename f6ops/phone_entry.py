import re
from f6ops.operators import get_operator_by_def

class PhoneEntry:
    def __init__(self, raw_number):
        self.raw = raw_number.strip()
        self.e164 = self.normalize(self.raw)
        self.def_code = self.get_def_code(self.e164)
        self.operator = get_operator_by_def(self.def_code)

    def normalize(self, num):
        cleaned = re.sub(r"[^\d+]", "", num)

        if cleaned.startswith("8"):
            cleaned = "+7" + cleaned[1:]

        if not cleaned.startswith("+"):
            cleaned = "+7" + cleaned

        return cleaned

    def get_def_code(self, e164):
        if e164.startswith("+7") and len(e164) >= 5:
            return e164[2:5]
        else:
            return None