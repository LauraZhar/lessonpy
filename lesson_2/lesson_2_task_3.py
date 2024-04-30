
import math


def square(side):
    area = side * side
    return math.ceil(area)


test_side = 3.5
result = square(test_side)


print("Площадь квадрата со стороной", test_side, "равна", result)
