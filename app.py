
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Valuation Error Dashboard", layout="wide")

st.title("📊 Valuation Error Monitoring Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("NUTMD_Prebook_Logs.csv")

df = load_data()

# Parse JSON-like 'RESPONSE' to extract status message
df["StatusMessage"] = df["RESPONSE"].str.extract(r'"StatusMessage":"(.*?)"')
df["Agency"] = df["requestId"].str.extract(r'(\d+)-')[0]
df["Provider"] = df["requestId"].str.extract(r'-(\d+)')[0]
df["HotelId"] = df["requestBody"].str.extract(r'"hotelId":(\d+)')
df["HotelName"] = df["requestBody"].str.extract(r'"name":"(.*?)"')

# Filters
agency = st.selectbox("Select Agency", df["Agency"].dropna().unique())
df_agency = df[df["Agency"] == agency]

# Tables
st.subheader("Error Log Table")
st.dataframe(df_agency[["Agency", "Provider", "StatusMessage", "HotelId", "HotelName"]].dropna(), use_container_width=True)

# Count per StatusMessage by Provider
count_table = df_agency.groupby(["Provider", "StatusMessage"]).size().reset_index(name="ErrorCount")
st.subheader("🧮 Error Count per Provider & Status Message")
st.dataframe(count_table, use_container_width=True)

# Graphs
st.subheader("📉 Top Providers by Error Count")
provider_chart = count_table.groupby("Provider")["ErrorCount"].sum().reset_index()
fig1 = px.bar(provider_chart, x="Provider", y="ErrorCount", color="ErrorCount", height=400)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🏨 Impacted Hotels by Error Count")
hotel_chart = df_agency.groupby("HotelName").size().reset_index(name="Errors")
fig2 = px.bar(hotel_chart.sort_values("Errors", ascending=False).head(20), x="HotelName", y="Errors", height=400)
st.plotly_chart(fig2, use_container_width=True)
