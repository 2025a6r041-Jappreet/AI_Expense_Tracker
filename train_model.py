
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Read the dataset
data = pd.read_csv("expenses.csv")

# Input and output
X = data["description"]
y = data["category"]

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", C=2.0))
])

model.fit(X_train, y_train)

print("Model training completed successfully!")
print("Training examples:", len(X_train))


# Test with a new expense
new_expense = ["Ordered pizza from Zomato"]

# Convert the new expense into TF-IDF numbers
prediction = model.predict(new_expense)

print("\nNew expense:", new_expense[0])
print("Predicted category:", prediction[0])


from sklearn.metrics import accuracy_score

# Convert testing descriptions into numbers
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nActual categories:")
print(list(y_test))

print("\nPredicted categories:")
print(list(y_pred))

print("\nModel accuracy:", round(accuracy * 100, 2), "%")


from sklearn.metrics import confusion_matrix

categories = [
    "Bills",
    "Education",
    "Entertainment",
    "Food",
    "Shopping",
    "Travel"
]

cm = confusion_matrix(y_test, y_pred, labels=categories)

print("\nConfusion Matrix:")
print(cm)


from sklearn.metrics import classification_report

categories = [
    "Bills",
    "Education",
    "Entertainment",
    "Food",
    "Shopping",
    "Travel"
]

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    labels=categories,
    zero_division=0
))

# Show incorrectly predicted test examples
results = pd.DataFrame({
    "Description": X_test.values,
    "Actual": y_test.values,
    "Predicted": y_pred
})

print("\nIncorrect Food Predictions:")
print(
    results[
        (results["Actual"] == "Food") &
        (results["Predicted"] != "Food")
    ].to_string(index=False)
)

print("\nIncorrect Travel Predictions:")
print(
    results[
        (results["Actual"] == "Travel") &
        (results["Predicted"] != "Travel")
    ].to_string(index=False)
)

import joblib

joblib.dump(model.named_steps["classifier"], "expense_model.pkl")
joblib.dump(model.named_steps["tfidf"], "tfidf_vectorizer.pkl")

print("\nModel and vectorizer saved successfully!")
