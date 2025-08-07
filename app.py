import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("🚗 Vehicle Registration Dashboard")

# Load Data
df = pd.read_csv("vehicle_data.csv")
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['quarter'] = df['date'].dt.to_period('Q')

# Sidebar Filters
vehicle_types = df['vehicle_type'].unique()
manufacturers = df['manufacturer'].unique()

selected_type = st.sidebar.selectbox("Select Vehicle Type", vehicle_types)
selected_manufacturer = st.sidebar.selectbox("Select Manufacturer", manufacturers)

start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

# Filter Data
mask = (
    (df['vehicle_type'] == selected_type) &
    (df['manufacturer'] == selected_manufacturer) &
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date))
)

filtered_df = df[mask]

# Grouped Data
yearly_data = filtered_df.groupby('year')['registrations'].sum().reset_index()
yearly_data['YoY Growth %'] = yearly_data['registrations'].pct_change() * 100

# Display Table
st.subheader("📈 Yearly Registrations and Growth")
st.dataframe(yearly_data)

# Bar Chart
fig = px.bar(yearly_data, x='year', y='registrations', title="Yearly Registrations")
st.plotly_chart(fig)
