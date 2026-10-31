
import csv
import os

filename = "my_expenses.csv"
temp_file = "temp.csv"

with open(filename, "r", newline="") as file:
    reader = csv.reader(file)
    rows = list(reader)

with open(temp_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Description", "Category", "Amount"])

    for row in rows[1:]:
        if len(row) == 2:
            writer.writerow([row[0], row[1], 0])
        elif len(row) >= 3:
            writer.writerow(row[:3])

os.replace(temp_file, filename)

print("CSV file fixed successfully!")

with open(filename, "r", newline="") as file:
    for row in csv.reader(file):
        print(row)
