

def is_year_leap(year):
    return year % 4 == 0


test_year = 2024
result = is_year_leap(test_year)


print("год", test_year, ":", result)
