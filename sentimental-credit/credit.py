from cs50 import get_string
import sys

while True:
    n = get_string("Number: ")
    if len(n) > 0 and len(n) <= 16:
        break

if len(n) < 13:
    print("INVALID")

sumnum = 0
sumnum2 = 0
for a in range(len(n) - 2, -1, -2):
    num = n[a]
    num = int(num)
    if num * 2 > 9:
        nu = str(num * 2)
        sumnum += int(nu[0]) + int(nu[1])
    else:
        sumnum += num * 2

for b in range(len(n) - 1, -1, -2):
    num2 = n[b]
    num2 = int(num2)
    sumnum2 += num2

num_total = str(sumnum + sumnum2)

if num_total[len(num_total) - 1] != '0':
    print("INVALID")
    sys.exit(1)

if n[0:2] == '34' or n[0:2] == '37':
    print("AMEX")
elif n[0:2] == '51' or n[0:2] == '52' or n[0:2] == '53' or n[0:2] == '54' or n[0:2] == '55':
    print("MASTERCARD")
elif n[0] == '4':
    print("VISA")
else:
    print("INVALID")
