
import joblib
import csv
import os

model = joblib.load("expense_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

expense = input("Enter your expense: ")
amount = float(input("Enter amount (Rs.): "))

expense_vector = vectorizer.transform([expense])
category = model.predict(expense_vector)[0]

file_exists = os.path.isfile("my_expenses.csv")

with open("my_expenses.csv", "a", newline="") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow(["Description", "Category", "Amount"])

    writer.writerow([expense, category, amount])

print("Predicted category:", category)
print("Amount: Rs.", amount)
print("Expense saved successfully!")
