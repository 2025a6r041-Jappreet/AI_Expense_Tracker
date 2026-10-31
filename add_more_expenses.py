
import pandas as pd

data = pd.read_csv("expenses.csv")

new_rows = [
    # Shopping
    ("Bought a pair of sandals", "Shopping"),
    ("Purchased a new bedsheet", "Shopping"),
    ("Ordered a power bank", "Shopping"),
    ("Bought a water purifier", "Shopping"),
    ("Purchased a school bag", "Shopping"),
    ("Bought a pair of gloves", "Shopping"),
    ("Ordered a phone cover", "Shopping"),
    ("Purchased a new monitor", "Shopping"),
    ("Bought kitchen utensils", "Shopping"),
    ("Purchased a table fan", "Shopping"),

    # Food
    ("Paid for a bowl of soup", "Food"),
    ("Ordered a cheese pizza", "Food"),
    ("Bought fresh apples", "Food"),
    ("Paid for a takeaway meal", "Food"),
    ("Purchased bread rolls", "Food"),
    ("Bought a packet of biscuits", "Food"),
    ("Ordered a vegetable sandwich", "Food"),
    ("Bought yogurt from a store", "Food"),
    ("Paid for a cup of tea", "Food"),
    ("Purchased rice and lentils", "Food"),

    # Travel
    ("Bought a local train pass", "Travel"),
    ("Paid for a ride to the office", "Travel"),
    ("Booked a bus for a trip", "Travel"),
    ("Paid for a cycle rental", "Travel"),
    ("Bought an intercity train ticket", "Travel"),
    ("Paid for a taxi to the market", "Travel"),
    ("Purchased a travel pass", "Travel"),
    ("Paid for a parking ticket", "Travel"),
    ("Booked a ride to the railway station", "Travel"),
    ("Paid for a car journey", "Travel"),

    # Entertainment
    ("Bought tickets for a football match", "Entertainment"),
    ("Paid for a bowling game", "Entertainment"),
    ("Purchased a cinema ticket", "Entertainment"),
    ("Subscribed to a streaming platform", "Entertainment"),
    ("Paid for a museum visit", "Entertainment"),
    ("Bought tickets for a music concert", "Entertainment"),
    ("Paid for a board game cafe", "Entertainment"),
    ("Rented a film for the weekend", "Entertainment"),
    ("Paid for a live music event", "Entertainment"),
    ("Bought a ticket to a magic show", "Entertainment"),

    # Bills
    ("Paid the monthly electricity charges", "Bills"),
    ("Paid the internet service invoice", "Bills"),
    ("Paid the monthly phone charges", "Bills"),
    ("Paid the apartment water invoice", "Bills"),
    ("Paid the heating bill", "Bills"),
    ("Paid the monthly rent invoice", "Bills"),
    ("Paid a waste disposal charge", "Bills"),
    ("Paid a household service bill", "Bills"),
    ("Paid a gas utility invoice", "Bills"),
    ("Paid the broadband bill", "Bills"),

    # Education
    ("Purchased a physics textbook", "Education"),
    ("Paid for a maths tutoring session", "Education"),
    ("Bought a notebook for lectures", "Education"),
    ("Paid for a science workshop", "Education"),
    ("Purchased a digital learning course", "Education"),
    ("Bought a dictionary for class", "Education"),
    ("Paid a school examination fee", "Education"),
    ("Purchased an academic workbook", "Education"),
    ("Paid for a coding tutorial", "Education"),
    ("Bought drawing supplies for class", "Education"),
]

extra = pd.DataFrame(
    new_rows, columns=["description", "category"]
)

data = pd.concat([data, extra], ignore_index=True)
data = data.drop_duplicates(
    subset=["description", "category"]
).reset_index(drop=True)

data.to_csv("expenses.csv", index=False)

print("Additional examples processed!")
print("Dataset shape:", data.shape)
print("\nCategory counts:")
print(data["category"].value_counts())
print("\nDuplicate rows:", data.duplicated().sum())
