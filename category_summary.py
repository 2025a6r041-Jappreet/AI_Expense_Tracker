
import csv

category_totals = {}

with open("my_expenses.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        category = row["Category"]
        amount = float(row["Amount"])

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

print("\n--- Category-wise Spending ---")

for category, total in category_totals.items():
    print(category, ": Rs.", total)
