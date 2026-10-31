
import csv

total = 0

with open("my_expenses.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total = total + float(row["Amount"])

print("Total expenses: Rs.", total)
