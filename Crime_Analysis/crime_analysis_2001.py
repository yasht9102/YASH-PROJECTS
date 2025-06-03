import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

# Load the dataset (make sure the CSV file is in the same directory)
file_path = 'NCRB_2001_Table_28.csv'
df = pd.read_csv(file_path)

# -------------------- Step 1: Data Cleaning --------------------
df.dropna(how='all', inplace=True)
df.fillna(0, inplace=True)

# -------------------- Step 2: Save to SQLite --------------------
db_path = 'rape_cases_2001.db'
conn = sqlite3.connect(db_path)
df.to_sql("rape_cases", conn, if_exists="replace", index=False)

# -------------------- Step 3: SQL Analysis --------------------
top_states_query = """
    SELECT "States/UTs/Cities", "No. of Cases Reported (Total Rape Cases)" AS Total_Cases
    FROM rape_cases
    WHERE Category = 'State'
    ORDER BY Total_Cases DESC
    LIMIT 5;
"""
top_states_df = pd.read_sql_query(top_states_query, conn)

age_group_query = """
    SELECT 
        SUM("No. of Victims (Total Rape Cases) upto 10 Years") AS "0-10",
        SUM("No. of Victims (Total Rape Cases) - 10-14 Years") AS "10-14",
        SUM("No. of Victims (Total Rape Cases) - 14 - 18 Years") AS "14-18",
        SUM("No. of Victims (Total Rape Cases) - 18 - 30 Years") AS "18-30",
        SUM("No. of Victims (Total Rape Cases) - 30 - 50 Years") AS "30-50",
        SUM("No. of Victims (Total Rape Cases) above 50 Years") AS "50+"
    FROM rape_cases;
"""
age_group_df = pd.read_sql_query(age_group_query, conn)

rape_type_query = """
    SELECT 
        SUM("No. of Cases Reported (Incest Rape Cases)") AS Incest,
        SUM("No. of Cases Reported (Other Rape Cases)") AS Other
    FROM rape_cases;
"""
rape_type_df = pd.read_sql_query(rape_type_query, conn)

conn.close()

# -------------------- Step 4: Visualization --------------------
# Bar chart: Top 5 states by total rape cases
plt.figure(figsize=(10, 6))
plt.bar(top_states_df["States/UTs/Cities"], top_states_df["Total_Cases"], color='crimson')
plt.title("Top 5 States by Total Rape Cases (2001)", fontsize=14)
plt.xlabel("State")
plt.ylabel("Total Rape Cases")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Pie chart: Victims by Age Group
age_group_data = age_group_df.iloc[0]
labels = age_group_data.index
sizes = age_group_data.values

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Reds(np.linspace(0.3, 1, len(labels))))
plt.title("Victim Age Group Distribution (2001)", fontsize=14)
plt.tight_layout()
plt.show()

# Bar chart: Incest vs Other rape cases
plt.figure(figsize=(6, 4))
plt.bar(['Incest', 'Other'], rape_type_df.iloc[0], color=['orange', 'purple'])
plt.title("Incest vs Other Rape Cases (2001)", fontsize=14)
plt.ylabel("Number of Cases")
plt.tight_layout()
plt.show()
