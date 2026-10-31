
import joblib

model = joblib.load("expense_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

expense = input("Enter your expense: ")

expense_vector = vectorizer.transform([expense])
category = model.predict(expense_vector)

print("Predicted category:", category[0])
