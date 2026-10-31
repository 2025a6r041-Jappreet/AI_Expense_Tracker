

import sqlite3
import os
import pandas as pd
import bcrypt


def create_connection():
    folder = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(folder, "expenses.db")
    return sqlite3.connect(database_path)


def create_table():
    connection = create_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            monthly_budget REAL NOT NULL
        )
    """)
    # Users table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    connection.commit()
    connection.close()

def migrate_to_multi_user():
    connection = create_connection()

    try:
        connection.execute("BEGIN")

        # Check expenses table
        expense_columns = [
            row[1] for row in
            connection.execute("PRAGMA table_info(expenses)").fetchall()
        ]

        if "user_id" not in expense_columns:
            connection.execute("""
                ALTER TABLE expenses
                ADD COLUMN user_id INTEGER REFERENCES users(id)
            """)

        # Rebuild settings table to allow one budget per user
        connection.execute("""
            ALTER TABLE settings RENAME TO settings_old
        """)

        connection.execute("""
            CREATE TABLE settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monthly_budget REAL NOT NULL,
                user_id INTEGER UNIQUE REFERENCES users(id)
            )
        """)

        connection.execute("""
            INSERT INTO settings (id, monthly_budget, user_id)
            SELECT id, monthly_budget, user_id
            FROM settings_old
        """)

        connection.execute("DROP TABLE settings_old")

        connection.commit()
        print("Multi-user database migration successful!")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

        
def register_user(name, email, username, password):
    connection = create_connection()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        connection.execute("BEGIN")

        # Check whether this is the first account
        user_count = connection.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

        cursor = connection.execute("""
            INSERT INTO users (name, email, username, password)
            VALUES (?, ?, ?, ?)
        """, (name, email, username, hashed_password))

        new_user_id = cursor.lastrowid

        # Assign existing data to the first registered user
        if user_count == 0:
            connection.execute("""
                UPDATE expenses
                SET user_id = ?
                WHERE user_id IS NULL
            """, (new_user_id,))

            connection.execute("""
                UPDATE settings
                SET user_id = ?
                WHERE user_id IS NULL
            """, (new_user_id,))

        connection.commit()
        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        connection.rollback()
        return False, "Email or username already exists."

    finally:
        connection.close()


def verify_user(username, password):
    connection = create_connection()

    cursor = connection.execute(
        "SELECT id, name, username, password FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    connection.close()

    if user is None:
        return None

    stored_password = user[3].encode("utf-8")

    if bcrypt.checkpw(password.encode("utf-8"), stored_password):
        return {
            "id": user[0],
            "name": user[1],
            "username": user[2]
        }

    return None

def reset_password(username, new_password):
    conn = create_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    cursor.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (hashed_password, username)
    )

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0

def update_username(old_username, new_username):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE users SET username = ? WHERE username = ?",
            (new_username, old_username)
        )
        conn.commit()
        return cursor.rowcount > 0

    except Exception:
        return False

    finally:
        conn.close()

def update_name(username, new_name):
    conn = create_connection()

    cursor = conn.execute(
        "UPDATE users SET name = ? WHERE username = ?",
        (new_name, username)
    )

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0

def save_budget(amount, user_id):
    connection = create_connection()

    connection.execute("""
        INSERT INTO settings (monthly_budget, user_id)
        VALUES (?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET monthly_budget = excluded.monthly_budget
    """, (float(amount), user_id))

    connection.commit()
    connection.close()

def get_budget(user_id):
    connection = create_connection()

    cursor = connection.execute(
        "SELECT monthly_budget FROM settings WHERE user_id = ?",
        (user_id,)
    )

    result = cursor.fetchone()
    connection.close()

    return result[0] if result else 0.0

def add_expense(description, category, amount, user_id):
    connection = create_connection()

    connection.execute("""
        INSERT INTO expenses (description, category, amount, user_id)
        VALUES (?, ?, ?, ?)
    """, (description, category, amount, user_id))

    connection.commit()
    connection.close()


def view_expenses(user_id):
    connection = create_connection()

    cursor = connection.execute(
        "SELECT * FROM expenses WHERE user_id = ?",
        (user_id,)
    )

    expenses = cursor.fetchall()
    connection.close()

    return expenses


def delete_expense(expense_id, user_id):
    connection = create_connection()

    connection.execute(
        "DELETE FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, user_id)
    )

    connection.commit()
    connection.close()


def migrate_csv_to_database():
    csv_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "my_expenses.csv"
    )

    if not os.path.exists(csv_path):
        print("CSV file not found.")
        return

    df = pd.read_csv(csv_path)
    connection = create_connection()

    cursor = connection.execute("SELECT COUNT(*) FROM expenses")
    total = cursor.fetchone()[0]

    if total == 0:
        for _, row in df.iterrows():
            connection.execute("""
                INSERT INTO expenses (description, category, amount)
                VALUES (?, ?, ?)
            """, (
                str(row["Description"]),
                str(row["Category"]),
                float(row["Amount"])
            ))

        connection.commit()
        print("CSV expenses transferred successfully!")
    else:
        print("Database already contains data. Nothing transferred.")

    connection.close()


if __name__ == "__main__":
    create_table()
    migrate_csv_to_database()
    print("Current database records:")
    print(view_expenses())
