operators = {
    "910": "МТС",
    "912": "МТС",
    "915": "МТС",
    "916": "Tele2",  
    "917": "МТС",
    "920": "МТС",
    "925": "МТС",
    "926": "МТС",
    "985": "МТС",
    "913": "Билайн",
    "960": "Билайн",
    "961": "Билайн",
    "999": "Билайн",
    "911": "МегаФон",
    "981": "МегаФон",
    "970": "Tele2",
    "977": "Tele2",
    "919": "МТС"
}

def get_operator(prefix):
    return operators.get(prefix, "Неизвестно")

f = open("abonents.txt", "r", encoding="utf-8")
for line in f:
    number = line.strip()
    print("Номер: - abonents.py:27", number)

    digits = ""
    for character in number:
        if character.isdigit():
            digits += character

    if len(digits) == 11:
        prefix = digits[1:4] 
    elif len(digits) == 10:
        prefix = digits[0:3]
    else:
        prefix = None

    if prefix:
        print(number, "", get_operator(prefix))
    else:
        print(number, "")

f.close()
