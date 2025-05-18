
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("🔍 Prebook Error Monitoring Dashboard")

# Load data
provider_df = pd.read_csv("provider_error_summary.csv")
hotel_df = pd.read_csv("hotel_error_summary.csv")

# Provider Error Summary
st.header("📊 Top Providers Causing Errors")
top_providers = (
    provider_df.groupby("providerId")["errorCount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1, ax1 = plt.subplots()
sns.barplot(data=top_providers, x="providerId", y="errorCount", ax=ax1)
ax1.set_title("Top 10 Providers by Error Count")
ax1.set_xlabel("Provider ID")
ax1.set_ylabel("Error Count")
st.pyplot(fig1)

# Hotel Error Summary
st.header("🏨 Top Hotels Causing Errors")
top_hotels = (
    hotel_df.groupby("HOTEL_NAME")["hotelErrorCount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2, ax2 = plt.subplots()
sns.barplot(data=top_hotels, x="hotelErrorCount", y="HOTEL_NAME", ax=ax2)
ax2.set_title("Top 10 Hotels by Error Count")
ax2.set_xlabel("Error Count")
ax2.set_ylabel("Hotel Name")
st.pyplot(fig2)

# Display raw tables
st.subheader("📄 Provider Error Table")
st.dataframe(provider_df)

st.subheader("📄 Hotel Error Table")
st.dataframe(hotel_df)
