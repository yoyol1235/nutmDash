
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("NUTMD_Prebook_logs_cleaned.csv")
    df["EVENT_CREATED_AT"] = pd.to_datetime(df["EVENT_CREATED_AT"])
    return df

df = load_data()

st.title("🛠️ Error Monitoring Dashboard - Agency & Provider Drilldown")

st.sidebar.header("🔍 Filters")
unique_agencies = sorted(df["Agency_ID"].dropna().unique())
selected_agency = st.sidebar.selectbox("Select Agency", unique_agencies)

filtered_df = df[df["Agency_ID"] == selected_agency]
unique_providers = sorted(filtered_df["Provider_ID"].dropna().unique())
selected_provider = st.sidebar.selectbox("Select Provider", unique_providers)

final_df = filtered_df[filtered_df["Provider_ID"] == selected_provider]

st.subheader(f"📊 Daily Errors - Agency {selected_agency} / Provider {selected_provider}")
daily_counts = final_df.groupby(final_df["EVENT_CREATED_AT"].dt.date).size().reset_index(name="Error Count")
fig = px.line(daily_counts, x="EVENT_CREATED_AT", y="Error Count", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("📄 Raw Error Logs")
st.dataframe(final_df[["EVENT_CREATED_AT", "Agency_ID", "Provider_ID", "REQUEST"]].reset_index(drop=True))
