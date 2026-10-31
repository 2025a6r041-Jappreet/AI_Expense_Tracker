
import pandas as pd

# Read the existing dataset
data = pd.read_csv("expenses.csv")

categories = [
    "Shopping", "Food", "Travel",
    "Entertainment", "Bills", "Education"
]

# Remove invalid rows and clean existing data
data = data[data["category"].isin(categories)]
data = data.dropna(subset=["description", "category"])
data["description"] = data["description"].astype(str).str.strip()
data = data[data["description"] != ""]

# Add new expense examples
new_rows = [
    # Shopping: 11 examples
    ("Bought a phone charger", "Shopping"),
    ("Purchased a handbag at the mall", "Shopping"),
    ("Bought a tablet online", "Shopping"),
    ("Purchased a water bottle", "Shopping"),
    ("Bought sunglasses from a shop", "Shopping"),
    ("Ordered a wallet online", "Shopping"),
    ("Purchased a computer mouse", "Shopping"),
    ("Bought a jacket at a clothing store", "Shopping"),
    ("Purchased a desk lamp", "Shopping"),
    ("Bought a travel suitcase", "Shopping"),
    ("Ordered a keyboard online", "Shopping"),

    # Food: 10 examples
    ("Bought takeaway pasta", "Food"),
    ("Paid for ice cream", "Food"),
    ("Ordered sushi for dinner", "Food"),
    ("Bought eggs and cheese", "Food"),
    ("Purchased flour and rice", "Food"),
    ("Paid for a meal delivery", "Food"),
    ("Bought a pastry from a bakery", "Food"),
    ("Ordered fried chicken", "Food"),
    ("Bought cooking oil", "Food"),
    ("Purchased frozen vegetables", "Food"),

    # Travel: 10 examples
    ("Paid for a ferry ride", "Travel"),
    ("Bought a weekly transit pass", "Travel"),
    ("Booked a shuttle to campus", "Travel"),
    ("Paid for a bicycle taxi", "Travel"),
    ("Paid for a car rental", "Travel"),
    ("Bought a bus pass", "Travel"),
    ("Paid for train fare to work", "Travel"),
    ("Booked a rideshare to the station", "Travel"),
    ("Paid for an airport transfer", "Travel"),
    ("Purchased a subway ticket", "Travel"),

    # Entertainment: 10 examples
    ("Bought a theater ticket", "Entertainment"),
    ("Paid for a movie rental", "Entertainment"),
    ("Subscribed to an audiobook service", "Entertainment"),
    ("Paid for mini golf", "Entertainment"),
    ("Bought a festival pass", "Entertainment"),
    ("Paid for an escape room", "Entertainment"),
    ("Visited an amusement arcade", "Entertainment"),
    ("Bought a ticket to a live show", "Entertainment"),
    ("Paid for a dance event", "Entertainment"),
    ("Rented a console game", "Entertainment"),

    # Bills: 10 examples
    ("Paid the monthly garbage collection fee", "Bills"),
    ("Paid property tax", "Bills"),
    ("Paid apartment water charges", "Bills"),
    ("Renewed the home internet plan", "Bills"),
    ("Paid for a cooking gas refill", "Bills"),
    ("Paid the mobile postpaid invoice", "Bills"),
    ("Paid the sewerage bill", "Bills"),
    ("Paid the household maintenance fee", "Bills"),
    ("Paid for home security service", "Bills"),
    ("Paid the monthly utility charges", "Bills"),

    # Education: 10 examples
    ("Paid tuition for mathematics lessons", "Education"),
    ("Bought a laboratory manual", "Education"),
    ("Paid college library membership", "Education"),
    ("Purchased exam preparation flashcards", "Education"),
    ("Paid for a language learning course", "Education"),
    ("Paid the university application fee", "Education"),
    ("Purchased a chemistry workbook", "Education"),
    ("Paid for an educational webinar", "Education"),
    ("Bought an engineering reference book", "Education"),
    ("Purchased a computer science textbook", "Education"),
]

extra_data = pd.DataFrame(
    new_rows, columns=["description", "category"]
)

# Combine data and remove repeated entries
data = pd.concat([data, extra_data], ignore_index=True)
data = data.drop_duplicates(
    subset=["description", "category"]
).reset_index(drop=True)

# Save the improved dataset
data.to_csv("expenses.csv", index=False)

print("Dataset updated successfully!")
print("\nDataset shape:", data.shape)
print("\nCategory counts:")
print(data["category"].value_counts())
print("\nMissing values:")
print(data.isnull().sum())
print("\nDuplicate rows:", data.duplicated().sum())
