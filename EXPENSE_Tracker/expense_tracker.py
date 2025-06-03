import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Initialize Database
conn = sqlite3.connect('expenses.db')
c = conn.cursor()

# Create Table
c.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    type TEXT,
    amount REAL,
    notes TEXT
)
''')
conn.commit()

def add_transaction(date, category, t_type, amount, notes=""):
    c.execute("INSERT INTO transactions (date, category, type, amount, notes) VALUES (?, ?, ?, ?, ?)",
              (date, category, t_type, amount, notes))
    conn.commit()

def view_transactions():
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    print(df)

def plot_pie_with_label(data, title, colors=None):
    plt.figure(figsize=(6,6))
    patches, texts, autotexts = plt.pie(data, labels=data.index, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title(title)
    plt.axis('equal')
    plt.text(0, 0, title, horizontalalignment='center', verticalalignment='center',
             fontsize=12, weight='bold', alpha=0.6)
    plt.show()

def monthly_summary(month):
    query = "SELECT * FROM transactions WHERE date LIKE ?"
    df = pd.read_sql_query(query, conn, params=[f"{month}%"])

    if df.empty:
        print("No records found for the specified month.")
        return

    expense_df = df[df['type'] == 'Expense']
    income_df = df[df['type'] == 'Income']

    if not expense_df.empty:
        expense_cat = expense_df.groupby('category')['amount'].sum()
        plot_pie_with_label(expense_cat, 'Expense Distribution by Category')

    if not income_df.empty:
        income_cat = income_df.groupby('category')['amount'].sum()
        colors = plt.cm.Greens(np.linspace(0.3, 0.7, len(income_cat)))
        plot_pie_with_label(income_cat, 'Income Distribution by Category', colors)

    if not expense_df.empty:
        expense_day = expense_df.groupby('date')['amount'].sum()
        # Remove date labels on pie charts but keep indices for display
        # So here, pass the original date indices but don't show labels on pie
        plot_pie_with_label(expense_day, 'Expense Distribution by Day')

    if not income_df.empty:
        income_day = income_df.groupby('date')['amount'].sum()
        colors = plt.cm.Greens(np.linspace(0.3, 0.7, len(income_day)))
        plot_pie_with_label(income_day, 'Income Distribution by Day', colors)

def statistics_summary():
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    if df.empty:
        print("No data available.")
        return
    df['amount'] = df['amount'].astype(float)
    expenses = df[df['type'] == 'Expense']['amount']
    income = df[df['type'] == 'Income']['amount']
    print("\nStatistical Insights:")
    print(f"Total Income: {income.sum():.2f}")
    print(f"Total Expenses: {expenses.sum():.2f}")
    print(f"Average Expense: {expenses.mean():.2f}")
    print(f"Standard Deviation in Expenses: {np.std(expenses):.2f}")

def export_to_csv():
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    df['date'] = pd.to_datetime(df['date'])  # Ensure proper date formatting
    df.to_csv("transactions_export.csv", index=False)
    print("Exported full transactions to transactions_export.csv")

def run_default_actions():
    # Adding demo transactions
    add_transaction("2025-06-01", "Food", "Expense", 25.50, "Lunch")
    add_transaction("2025-06-02", "Salary", "Income", 3000.00, "Monthly salary")
    add_transaction("2025-06-03", "Rent", "Expense", 850.00, "June rent")
    add_transaction("2025-06-04", "Transport", "Expense", 40.00, "Taxi fare")
    add_transaction("2025-06-05", "Freelance", "Income", 600.00, "Project work")

    print("\nAll Transactions:")
    view_transactions()
    print("\nMonthly Summary for 2025-06:")
    monthly_summary("2025-06")
    statistics_summary()
    export_to_csv()

if __name__ == '__main__':
    run_default_actions()
    conn.close()
