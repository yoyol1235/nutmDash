
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("NUTMD_Prebook_logs_cleaned_v2.csv", parse_dates=["EVENT_CREATED_AT"])

df = load_data()

st.title("📊 Agency & Provider Prebook Error Dashboard")

# Sidebar filter
st.sidebar.header("🔍 Filters")
agencies = df["Agency_ID"].dropna().unique()
selected_agency = st.sidebar.selectbox("Select Agency", sorted(agencies))

# Filtered data
filtered_df = df[df["Agency_ID"] == selected_agency]

st.subheader(f"📈 Provider Breakdown for Agency {selected_agency}")

# Count errors by provider
provider_counts = filtered_df["Provider_ID"].value_counts().reset_index()
provider_counts.columns = ["Provider_ID", "Error Count"]

# Show table
st.dataframe(provider_counts)

# Plot
fig = px.bar(provider_counts, x="Provider_ID", y="Error Count", title="Error Count by Provider",
             labels={"Provider_ID": "Provider", "Error Count": "Error Count"})
st.plotly_chart(fig)

# Optional raw logs
with st.expander("📄 Raw Logs"):
    st.dataframe(filtered_df)
