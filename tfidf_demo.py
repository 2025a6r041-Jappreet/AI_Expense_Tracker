
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Read the dataset
data = pd.read_csv("expenses.csv")

# Get expense descriptions
X = data["description"]

# Create the TF-IDF tool
vectorizer = TfidfVectorizer()

# Convert text into numbers
X_tfidf = vectorizer.fit_transform(X)

# Show the results
print("Original description:")
print(X.iloc[0])

print("\nWords learned by TF-IDF:")
print(vectorizer.get_feature_names_out())

print("\nTF-IDF matrix shape:")
print(X_tfidf.shape)

print("\nNumbers for the first expense:")
print(X_tfidf.toarray()[0])
