import datetime
import time


divisors = [1,2,3,4,5,0,9,8,7,6]

for i in range(len(divisors)):
    try:
        divisors[i] = 1/divisors[i]
    except ZeroDivisionError:
        divisors[i] = 0
print(divisors)

d = len(divisors)
i = 0
print(f'Do not abort the process -> grab a coffee :)')
for el in divisors:
    elstrong = f'Progress: {str(10*i)}%'
    print("$"*i+"-"*(d-i) +' '+ elstrong)
    i += 1
print('$'*len(divisors) + ' Loading complete!')






