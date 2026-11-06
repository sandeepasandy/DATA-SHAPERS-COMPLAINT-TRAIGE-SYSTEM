import pandas as pd

print("Data Shapers Project Started!")

# Create complaint data
data = {
    "Customer": ["Ravi", "Priya", "Kiran", "Sneha", "Arjun"],

    "Complaint": [
        "Refund not received",
        "Product damaged",
        "Delivery delayed",
        "Password reset issue",
        "Payment deducted twice"
    ],

    "Category": [
        "Refund", "Product", "Delivery", "Account", "Payment"
    ],

    "Urgency": [
        "High", "High", "Medium", "Low", "High"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Display dataset
print(df)

# Save dataset as CSV
df.to_csv("complaints.csv", index=False)

print("Dataset saved successfully!")

# Basic Data Analysis

print("\nTotal Complaints:")
print(len(df))

print("\nComplaints by Category:")
print(df["Category"].value_counts())

print("\nComplaints by Urgency:")
print(df["Urgency"].value_counts())

# Assign priority status

def assign_priority(urgency):
    if urgency == "High":
        return "Immediate Attention"
    elif urgency == "Medium":
        return "Normal Attention"
    else:
        return "Low Attention"

df["Priority_Status"] = df["Urgency"].apply(assign_priority)

print("\nComplaints with Priority Status:")
print(df)

# Generate Complaint IDs

df.insert(0, "Complaint_ID", range(1001, 1001 + len(df)))

print("\nComplaint Records with IDs:")
print(df)

df.to_csv("complaints.csv", index=False)
print("Updated CSV saved successfully!")

# Add complaint status

df["Status"] = [
    "Pending",
    "In Progress",
    "Pending",
    "Resolved",
    "In Progress"
]

print("\nComplaint Status:")
print(df[["Complaint_ID", "Customer", "Complaint", "Status"]])

# Save updated dataset
df.to_csv("complaints.csv", index=False)

print("\nComplaint dataset updated successfully!")

# Complaint Status Analysis

print("\nComplaint Status Summary:")

status_count = df["Status"].value_counts()

print(status_count)

print("\nTotal Resolved Complaints:")
print((df["Status"] == "Resolved").sum())

print("\nTotal Pending Complaints:")
print((df["Status"] == "Pending").sum())

print(df["Status"].value_counts())