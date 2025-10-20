import re
from f6ops.operators import get_operator_by_def  

class PhoneEntry:
    def __init__(self, raw_number: str):
        self.raw = raw_number.strip()
        self.e164 = self.normalize(self.raw)
        self.def_code = self.extract_def(self.e164)   
        self.operator = get_operator_by_def(self.def_code)

    def normalize(self, number: str) -> str:
        num = re.sub(r"[^\d+]", "", number)
        if num.startswith("8"):
            num = "+7" + num[1:]
        elif not num.startswith("+"):
            num = "+7" + num
        return num

    def extract_def(self, e164: str) -> str | None:
        if e164.startswith("+79") and len(e164) >= 5:
            return e164[2:5] 
        return None