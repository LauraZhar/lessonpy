 
def month_to_season(month):
    if 3 <= month <= 5:
        return "Весна"
    elif 6 <= month <= 8:
        return "Лето"
    elif 9 <= month <= 11:
        return "Осень"
    elif month == 12 or 1 <= month <= 2:
        return "Зима"
    else:
        return "Некорректный номер месяца"

 
test_month = 6
result = month_to_season(test_month)
print("Месяц", test_month, "относится к сезону:", result)
