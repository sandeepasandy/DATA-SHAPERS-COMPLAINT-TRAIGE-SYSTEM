import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "complaints.db"

# Function to save complaints into SQL database
def save_to_database(new_complaint):
    import os
    print("Database location:", os.path.abspath("complaints.db"))
    connection = sqlite3.connect("complaints.db")
    new_complaint.to_sql(
        "complaints",
        connection,
        if_exists="append",
        index=False
    )
    connection.close()


# Load complaint dataset
df = pd.read_csv("complaints.csv")

st.title("Data Shapers - Complaint Registration and Triage System")

st.write("Welcome to the Complaint Management Dashboard!")

# Load complaint dataset
df = pd.read_csv("complaints.csv")

# Display all complaints
st.subheader("Registered Complaints")
st.dataframe(df)

# Display total complaints
st.metric("Total Complaints", len(df))

st.metric("Total Complaints", len(df))

col1, col2, col3 = st.columns(3)

col1.metric("Pending", len(df[df["Status"] == "Pending"]))
col2.metric("In Progress", len(df[df["Status"] == "In Progress"]))
col3.metric("Resolved", len(df[df["Status"] == "Resolved"]))

st.subheader("Category-wise Complaint Analysis")

category_counts = df["Category"].value_counts()

st.bar_chart(category_counts)

st.subheader("Register a New Complaint")

with st.form("complaint_form"):

    customer = st.text_input("Customer Name")

    complaint = st.text_area("Describe Your Complaint")

    category = st.selectbox(
        "Select Category",
        ["Refund", "Product", "Delivery", "Account", "Payment"]
    )

    urgency = st.selectbox(
        "Select Urgency",
        ["High", "Medium", "Low"]
    )

    submit = st.form_submit_button("Submit Complaint")

if submit:

    if customer.strip() == "" or complaint.strip() == "":
        st.warning("Please fill in all the details.")

    else:
        priority = {
            "High": "Immediate Attention",
            "Medium": "Normal Attention",
            "Low": "Low Attention"
        }

        new_complaint = pd.DataFrame([{
            "Complaint_ID": int(df["Complaint_ID"].max()) + 1,
            "Customer": customer,
            "Complaint": complaint,
            "Category": category,
            "Urgency": urgency,
            "Priority_Status": priority[urgency],
            "Status": "Pending"
        }])

        updated_df = pd.concat([df, new_complaint], ignore_index=True)
        
        updated_df.to_csv("complaints.csv", index=False)
        
        save_to_database(new_complaint)
        st.success("Complaint registered successfully in CSV and SQL!")

        st.subheader("Urgency-wise Complaint Analysis")

urgency_counts = df["Urgency"].value_counts()

st.bar_chart(urgency_counts)

def save_to_database(new_complaint):
    print("Database location:", os.path.abspath("complaints.db"))

    connection = sqlite3.connect(DB_PATH)

    new_complaint.to_sql(
        "complaints",
        connection,
        if_exists="append",
        index=False
    )
    connection.close()
