import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="Customer Revenue Analysis Dashboard",
    layout="wide"
)

st.title("Customer Revenue Analysis Dashboard")
st.markdown("Analyze customer revenue, churn risk, and satisfaction patterns.")

# -------------------------------
# Load data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")

    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Fill missing satisfaction values
    df["satisfaction_level"] = df["satisfaction_level"].fillna(
        df["satisfaction_level"].mode()[0]
    )

    # Create customer spend segment
    df["customer_segment"] = pd.qcut(
        df["total_spend"],
        q=3,
        labels=["Low", "Medium", "High"]
    )

    # Create churn risk
    def classify_churn(row):
        if row["days_since_last_purchase"] > 60:
            return "High"
        elif row["days_since_last_purchase"] > 30 and row["satisfaction_level"] == "Unsatisfied":
            return "High"
        elif row["days_since_last_purchase"] > 30:
            return "Medium"
        else:
            return "Low"

    df["churn_risk"] = df.apply(classify_churn, axis=1)

    # Optional feature
    df["avg_spend_per_item"] = df["total_spend"] / df["items_purchased"]

    return df


df = load_data()

# -------------------------------
# Sidebar filters
# -------------------------------
st.sidebar.header("Filters")

selected_city = st.sidebar.multiselect(
    "Select City",
    options=sorted(df["city"].unique()),
    default=sorted(df["city"].unique())
)

selected_membership = st.sidebar.multiselect(
    "Select Membership Type",
    options=sorted(df["membership_type"].unique()),
    default=sorted(df["membership_type"].unique())
)

selected_churn = st.sidebar.multiselect(
    "Select Churn Risk",
    options=["Low", "Medium", "High"],
    default=["Low", "Medium", "High"]
)

filtered_df = df[
    (df["city"].isin(selected_city)) &
    (df["membership_type"].isin(selected_membership)) &
    (df["churn_risk"].isin(selected_churn))
]

# -------------------------------
# KPI metrics
# -------------------------------
total_customers = filtered_df["customer_id"].nunique()
total_revenue = filtered_df["total_spend"].sum()
avg_spend = filtered_df["total_spend"].mean()
high_churn_pct = (
    (filtered_df["churn_risk"] == "High").mean() * 100
    if len(filtered_df) > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers}")
col2.metric("Total Revenue", f"${total_revenue:,.2f}")
col3.metric("Average Spend", f"${avg_spend:,.2f}" if pd.notnull(avg_spend) else "$0.00")
col4.metric("High Churn %", f"{high_churn_pct:.1f}%")

st.markdown("---")

# -------------------------------
# Row 1: Membership spend and churn distribution
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Spend by Membership Type")
    membership_spend = (
        filtered_df.groupby("membership_type")["total_spend"]
        .mean()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    membership_spend.plot(kind="bar", ax=ax)
    ax.set_xlabel("Membership Type")
    ax.set_ylabel("Average Total Spend")
    ax.set_title("Membership Type vs Spend")
    plt.xticks(rotation=0)
    st.pyplot(fig)

with col2:
    st.subheader("Customer Count by Churn Risk")
    churn_counts = filtered_df["churn_risk"].value_counts().reindex(["Low", "Medium", "High"], fill_value=0)

    fig, ax = plt.subplots(figsize=(7, 4))
    churn_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Churn Risk")
    ax.set_ylabel("Customer Count")
    ax.set_title("Churn Risk Distribution")
    plt.xticks(rotation=0)
    st.pyplot(fig)

# -------------------------------
# Row 2: Churn vs spend and spend distribution
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Spend by Churn Risk")
    churn_spend = (
        filtered_df.groupby("churn_risk")["total_spend"]
        .mean()
        .reindex(["Low", "Medium", "High"])
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    churn_spend.plot(kind="bar", ax=ax)
    ax.set_xlabel("Churn Risk")
    ax.set_ylabel("Average Total Spend")
    ax.set_title("Churn Risk vs Spend")
    plt.xticks(rotation=0)
    st.pyplot(fig)

with col2:
    st.subheader("Total Spend Distribution")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(filtered_df["total_spend"], bins=20)
    ax.set_xlabel("Total Spend")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Total Spend")
    st.pyplot(fig)

# -------------------------------
# Row 3: Satisfaction vs segment
# -------------------------------
st.subheader("Satisfaction Level by Customer Segment")

satisfaction_segment = pd.crosstab(
    filtered_df["customer_segment"],
    filtered_df["satisfaction_level"]
)

st.dataframe(satisfaction_segment, use_container_width=True)

fig, ax = plt.subplots(figsize=(8, 4))
satisfaction_segment.plot(kind="bar", stacked=True, ax=ax)
ax.set_xlabel("Customer Segment")
ax.set_ylabel("Customer Count")
ax.set_title("Customer Segment vs Satisfaction Level")
plt.xticks(rotation=0)
st.pyplot(fig)

# -------------------------------
# Optional detailed table
# -------------------------------
st.subheader("Filtered Customer Data")
st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# Business insights section
# -------------------------------
st.markdown("---")
st.subheader("Key Business Insights")

if len(filtered_df) > 0:
    top_membership = membership_spend.idxmax() if not membership_spend.empty else "N/A"
    lowest_churn_spend_group = churn_spend.idxmin() if not churn_spend.dropna().empty else "N/A"

    st.markdown(
        f"""
        - **{top_membership} members** have the highest average spending in the current filtered view.
        - Customers in the **{lowest_churn_spend_group} churn-risk group** contribute the lowest average spend.
        - Customer satisfaction appears strongly related to spend segment, especially among higher-value customers.
        - Retention and membership-upgrade strategies could improve both engagement and revenue.
        """
    )
else:
    st.warning("No data available for the selected filters.")