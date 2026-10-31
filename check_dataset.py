
import pandas as pd
from sklearn.model_selection import train_test_split

# Read the dataset
data = pd.read_csv("expenses.csv")

print("FIRST 5 ROWS")
print(data.head())

print("\nDATASET SHAPE:", data.shape)

# Check required columns
print("\nCOLUMNS:", data.columns.tolist())

# Clean extra spaces from text fields
data["description"] = data["description"].astype("string").str.strip()
data["category"] = data["category"].astype("string").str.strip()

# Check missing and empty values
print("\nMISSING VALUES:")
print(data.isnull().sum())

print("\nEMPTY DESCRIPTIONS:",
      (data["description"] == "").sum())

print("\nEMPTY CATEGORIES:",
      (data["category"] == "").sum())

# Check category balance
print("\nCATEGORY COUNTS:")
print(data["category"].value_counts())

# Check exact duplicate rows
print("\nEXACT DUPLICATE ROWS:",
      data.duplicated().sum())

# Check repeated descriptions with conflicting labels
label_counts = data.groupby("description")["category"].nunique()
conflicts = label_counts[label_counts > 1].index

print("\nCONFLICTING DESCRIPTIONS:", len(conflicts))

if len(conflicts) > 0:
    print(data[data["description"].isin(conflicts)]
          .sort_values("description")
          .to_string(index=False))

# Show examples from every category
print("\nSAMPLE DESCRIPTIONS BY CATEGORY:")
for category in sorted(data["category"].dropna().unique()):
    print(f"\n{category}:")
    examples = data.loc[
        data["category"] == category, "description"
    ].head(5)

    for example in examples:
        print("-", example)

# Stratified train-test split
X = data["description"]
y = data["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTRAINING EXAMPLES:", len(X_train))
print("TESTING EXAMPLES:", len(X_test))

print("\nTRAINING CATEGORY COUNTS:")
print(y_train.value_counts())

print("\nTESTING CATEGORY COUNTS:")
print(y_test.value_counts())

import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Read dataset
data = pd.read_csv("expenses.csv")

print("DATASET SHAPE:", data.shape)
print("COLUMNS:", data.columns.tolist())

# 2. Check required columns
required = {"description", "category"}

if not required.issubset(data.columns):
    raise ValueError("Dataset must contain description and category columns.")

# 3. Clean text fields
data["description"] = data["description"].astype("string").str.strip()
data["category"] = data["category"].astype("string").str.strip()

# 4. Check missing and empty values
print("\nMISSING VALUES:")
print(data[["description", "category"]].isna().sum())

empty_description = data["description"].fillna("").eq("").sum()
empty_category = data["category"].fillna("").eq("").sum()

print("\nEMPTY DESCRIPTIONS:", empty_description)
print("EMPTY CATEGORIES:", empty_category)

# Stop if essential data is invalid
if data[["description", "category"]].isna().any().any():
    raise ValueError("Missing values found. Fix them before training.")

if empty_description > 0 or empty_category > 0:
    raise ValueError("Empty descriptions/categories found.")

# 5. Check categories and duplicates
print("\nCATEGORY COUNTS:")
print(data["category"].value_counts())

print("\nEXACT DUPLICATE ROWS:", data.duplicated().sum())

conflicts = (
    data.groupby("description")["category"]
    .nunique()
)
conflicts = conflicts[conflicts > 1]

print("\nCONFLICTING DESCRIPTIONS:", len(conflicts))

if len(conflicts) > 0:
    print(conflicts)

# 6. Check repeated descriptions
print("\nREPEATED DESCRIPTIONS:")
print(
    data["description"]
    .value_counts()
    .loc[lambda counts: counts > 1]
)

# 7. Stratified split
X = data["description"]
y = data["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTRAINING EXAMPLES:", len(X_train))
print("TESTING EXAMPLES:", len(X_test))

print("\nTRAINING CATEGORY COUNTS:")
print(y_train.value_counts())

print("\nTESTING CATEGORY COUNTS:")
print(y_test.value_counts())
