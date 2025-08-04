from cs50 import get_string

text = get_string("Text: ")

count_letters = 0

# loop for conting letters
for i in range(0, len(text)):
    if text[i].isalpha():
        count_letters += 1

# conting words
count_words = 1

for b in range(0, len(text)):
    if text[b].isspace():
        count_words += 1

count_ends = 0

for a in range(0, len(text)):
    if text[a] in [".", "!", "?"]:
        count_ends += 1

L = count_letters / count_words * 100

S = count_ends / count_words * 100

grade = 0.0588 * L - 0.29 * S - 15.8
grade = round(grade)

if grade < 1:
    print("Before Grade 1")
elif grade < 16:
    print(f"Grade {grade}")
else:
    print("Grade 16+")
