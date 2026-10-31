
import pandas as pd

df = pd.read_csv("public_transactions.csv")

print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nCategory counts:")
print(df["category"].value_counts())

print("\nMissing values:")
print(df.isnull().sum())

print("\nUnique categories:")
print(sorted(df["category"].unique()))

print("\nSample descriptions by category:")
for category in sorted(df["category"].unique()):
    print(f"\n--- {category} ---")
    print(df[df["category"] == category]["description"].head(5).to_list())

print("\nUnique descriptions:", df["description"].nunique())

print("\nRepeated descriptions:")
print(
    df["description"]
    .value_counts()
    .head(15)
)

print("\nSame description with different categories:")
print(
    df.groupby("description")["category"]
    .nunique()
    .loc[lambda x: x > 1]
)

cleaned = pd.read_csv("public_transactions_cleaned.csv")

print("\nCleaned file columns:", cleaned.columns.tolist())
print("Cleaned file shape:", cleaned.shape)
print(cleaned.head())

original = pd.read_csv("expenses.csv")
cleaned = pd.read_csv("public_transactions_cleaned.csv")

print("\nOriginal dataset shape:", original.shape)
print("Original categories:")
print(original["category"].value_counts())

print("\nCleaned public dataset shape:", cleaned.shape)
print("Cleaned public categories:")
print(cleaned["category"].value_counts())

print("\nDescriptions appearing in both datasets:")
print(
    set(original["description"].str.lower())
    & set(cleaned["description"].str.lower())
)
