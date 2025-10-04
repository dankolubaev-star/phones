import re

class PhoneEntry:
    def __init__(self, raw_number: str):
        self.raw = raw_number.strip()
        self.e164 = self.normalize(self.raw)
        self.operator = self.detect_operator(self.e164)

    def normalize(self, number: str) -> str:
        num = re.sub(r"[^\d+]", "", number)

        if not num.startswith("+"):
            num = "+7" + num

        return num

    def detect_operator(self, number: str) -> str:
        if number.startswith("+7985"):
            return "МТС"
        elif number.startswith("+7926"):
            return "Мегафон"
        elif number.startswith("+7960"):
            return "Билайн"
        else:
            return "Неизвестно"
        