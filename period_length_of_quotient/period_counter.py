from decimal import Decimal, getcontext
import time
import math
from fractions import Fraction


def find_period_length(decimal_part):

    start_time = time.time()
    iteration_count = 0

    # First loop searching for the pattern in the first 1000 digits
    d=0
    for i in range(1, 1000):
        iteration_count += 1
        if decimal_part[d:i+d] == decimal_part[i+d:2*i+d]:
            if decimal_part[i+d:2*i+d] == decimal_part[2*i+d:3*i+d]:
                return i

        if time.time() - start_time >= 60:  # Check if a minute has passed
            print(f"Number of iterations per minute: {iteration_count}")
            iteration_count = 0
            start_time = time.time()

    return -1

# Create a Fraction object using a float for the denominator
numerator = Decimal(input("Enter numerator "))
denominator = Decimal(input("Enter denominator "))


getcontext().prec = 100000000  # Количество знаков после запятой
zeroes=1
try:
    fraction = Decimal(numerator / denominator)
    result_str = str(fraction)

    #if the result is an integer
    if '.' not in result_str:
        print("integer")
    else:
        decimal_part=result_str.split('.')[1]
        if len(decimal_part)<100:
            print(f"terminal fraction or integer, {result_str} ")
        else:   #removing 0s from the beginning of a decimal part
            while decimal_part[0]=='0':
                zeroes+=1
                decimal_part=decimal_part[1:]
            next_number=0

            while find_period_length(decimal_part)==-1:
            #decimal_length=len(decimal_part)
                decimal_part=decimal_part[1:]
                #print("checking with next digit")
                next_number+=1

            period_length = find_period_length(decimal_part)
            ending=2+zeroes+period_length*2
            print(f"Period length={period_length}, period=({decimal_part[:period_length]}), begins with {zeroes+next_number} digit, {result_str[:ending]}")
except ZeroDivisionError:
    print("0 Division")
