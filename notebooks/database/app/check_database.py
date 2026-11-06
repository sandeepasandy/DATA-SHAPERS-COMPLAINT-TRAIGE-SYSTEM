import sqlite3
import os
connection = sqlite3.connect(
    os.path.abspath("complaints.db")
)
print("Database location:", os.path.abspath("complaints.db"))

cursor = connection.cursor()

cursor.execute("""
SELECT Complaint_ID, Customer, Complaint, Status
FROM complaints
ORDER BY Complaint_ID DESC
LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

connection.close()