
import pandas as pd

df = pd.read_csv("public_transactions.csv")

# Remove transaction IDs from descriptions
df["description"] = df["description"].str.replace(
    r"\s+txn_\d+$", "", regex=True
).str.strip()

# Keep only the six categories used in our project
categories = [
    "Shopping",
    "Food",
    "Travel",
    "Entertainment",
    "Bills",
    "Education"
]

df = df[df["category"].isin(categories)].copy()

# Remove exact duplicate description-category pairs
df = df.drop_duplicates(subset=["description", "category"])

# Save as a separate cleaned file
df[["description", "category"]].to_csv(
    "public_transactions_cleaned.csv",
    index=False
)

print("Cleaned dataset shape:", df.shape)
print("\nCategory counts:")
print(df["category"].value_counts())

print("\nSample cleaned descriptions:")
print(df.head(10))

print("\nSaved as public_transactions_cleaned.csv")
