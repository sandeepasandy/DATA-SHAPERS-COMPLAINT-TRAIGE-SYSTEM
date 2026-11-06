import sqlite3
import pandas as pd

# Connect to database
connection = sqlite3.connect("complaints.db")

# Create cursor
cursor = connection.cursor()

# Create complaints table
cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    Complaint_ID INTEGER PRIMARY KEY,
    Customer TEXT,
    Complaint TEXT,
    Category TEXT,
    Urgency TEXT,
    Priority_Status TEXT,
    Status TEXT
)
""")

# Reopen database connection
connection = sqlite3.connect("complaints.db")

# Retrieve data
query = "SELECT * FROM complaints"

result = pd.read_sql_query(query, connection)

print("\nComplaint Data Retrieved from SQL:")
print(result)

# SQL Analysis 1: Count complaints by category

query = """
SELECT Category, COUNT(*) AS Total_Complaints
FROM complaints
GROUP BY Category
"""

result = pd.read_sql_query(query, connection)

print("\nComplaints Category-wise:")
print(result)

# SQL Analysis 2: Count complaints by urgency

query = """
SELECT Urgency, COUNT(*) AS Total_Complaints
FROM complaints
GROUP BY Urgency
"""

result = pd.read_sql_query(query, connection)

print("\nUrgency-wise Complaint Analysis:")
print(result)

# SQL Analysis 3: High Priority Complaints

query = """
SELECT Customer, Complaint, Category, Urgency
FROM complaints
WHERE Urgency = 'High'
"""

result = pd.read_sql_query(query, connection)

print("\nHigh Priority Complaints:")
print(result)

# SQL Analysis 4: Total Complaints

query = """
SELECT COUNT(*) AS Total_Complaints
FROM complaints
"""

result = pd.read_sql_query(query, connection)

print("\nTotal Number of Complaints:")
print(result)

# SQL Analysis 5: Sort complaints by urgency

query = """
SELECT Customer, Complaint, Category, Urgency
FROM complaints
ORDER BY Urgency ASC
"""

result = pd.read_sql_query(query, connection)

print("\nComplaints Sorted by Urgency:")
print(result)

# SQL Analysis 6: Status-wise Complaint Analysis

query = """
SELECT Status, COUNT(*) AS Total_Complaints
FROM complaints
GROUP BY Status
"""

result = pd.read_sql_query(query, connection)

print("\nStatus-wise Complaint Analysis:")
print(result)
      
# SQL Analysis 7: Resolution Percentage

query = """
SELECT
    COUNT(*) AS Total,
    SUM(CASE WHEN Status = 'Resolved' THEN 1 ELSE 0 END) AS Resolved
FROM complaints
"""

result = pd.read_sql_query(query, connection)

total = result["Total"][0]
resolved = result["Resolved"][0]

percentage = (resolved / total) * 100

print("\nComplaint Resolution Percentage:")
print(percentage, "%")


query = """
SELECT Complaint_ID, Customer, Category, Urgency, Status
FROM complaints
ORDER BY Complaint_ID DESC
"""

result = pd.read_sql_query(query, connection)

print("Latest Registered Complaints:")
print(result.head())

connection.close()