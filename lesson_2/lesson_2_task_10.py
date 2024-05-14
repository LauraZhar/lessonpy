
import math
def bank(X, Y):
    for _ in range(Y):
        X *= 1.1   
    return X
 
initial_amount = 20000
years = 5
final_amount = bank(initial_amount, years)
 
print("Сумма на счету после", years, "лет будет:", math.ceil(final_amount) )
