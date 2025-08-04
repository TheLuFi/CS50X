from cs50 import get_int

while True:
    n = get_int("Height: ")
    if n > 0 and n <= 8:
        break

for a in range(n):

    print(" " * (n - a - 1), end="")
    print("#" * (a + 1), end="")
    print("  ", end="")
    print("#" * (a + 1))
