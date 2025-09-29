import sqlite3
import os

DB_FOLDER = "data"
DB_FILE = os.path.join(DB_FOLDER, "expenses.db")
os.makedirs(DB_FOLDER, exist_ok=True)

class Storage:
    @staticmethod
    def initialize_db():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def save_expense(amount, category, description, date_str):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
            (amount, category, description, date_str)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def load_expenses():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def update_expense(expense_id, amount=None, category=None, description=None, date_str=None):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        fields, values = [], []
        if amount is not None:
            fields.append("amount=?")
            values.append(amount)
        if category is not None:
            fields.append("category=?")
            values.append(category)
        if description is not None:
            fields.append("description=?")
            values.append(description)
        if date_str is not None:
            fields.append("date=?")
            values.append(date_str)
        values.append(expense_id)
        cursor.execute(f"UPDATE expenses SET {', '.join(fields)} WHERE id=?", values)
        conn.commit()
        conn.close()

    @staticmethod
    def delete_expense(expense_id):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search_by_category(category):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE category LIKE ?", ('%' + category + '%',))
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def search_by_date(date_str):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE date=?", (date_str,))
        rows = cursor.fetchall()
        conn.close()
        return rows
=======
import sqlite3
import os

DB_FOLDER = "data"
DB_FILE = os.path.join(DB_FOLDER, "expenses.db")
os.makedirs(DB_FOLDER, exist_ok=True)

class Storage:
    @staticmethod
    def initialize_db():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def save_expense(amount, category, description, date_str):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
            (amount, category, description, date_str)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def load_expenses():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def update_expense(expense_id, amount=None, category=None, description=None, date_str=None):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        fields, values = [], []
        if amount is not None:
            fields.append("amount=?")
            values.append(amount)
        if category is not None:
            fields.append("category=?")
            values.append(category)
        if description is not None:
            fields.append("description=?")
            values.append(description)
        if date_str is not None:
            fields.append("date=?")
            values.append(date_str)
        values.append(expense_id)
        cursor.execute(f"UPDATE expenses SET {', '.join(fields)} WHERE id=?", values)
        conn.commit()
        conn.close()

    @staticmethod
    def delete_expense(expense_id):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search_by_category(category):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE category LIKE ?", ('%' + category + '%',))
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def search_by_date(date_str):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE date=?", (date_str,))
        rows = cursor.fetchall()
        conn.close()
        return rows
>>>>>>> 28a87a2 (First commit)
