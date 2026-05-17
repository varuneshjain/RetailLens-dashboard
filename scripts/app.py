import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="RetailLens",
    page_icon="🔍",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv('data/amazon_cleaned.csv')

df = load_data()

st.title("🔍 RetailLens — Amazon Sales Dashboard")
st.markdown("**1,21,180 orders | Apr–Jun 2022 | Amazon India**")

st.divider()

# Metrics row
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", f"{len(df):,}")
col2.metric("Total Revenue", f"₹{df['Amount'].sum()/1e7:.2f} Cr")
col3.metric("Avg Order Value", f"₹{df['Amount'].mean():.0f}")
col4.metric("Cancellation Rate", f"{(df['Status'] == 'Cancelled').sum() / len(df) * 100:.2f}%")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Category")
    cat = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    cat.plot(kind='bar', ax=ax, color='teal')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Order Status Breakdown")
    status = df['Status'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    status.plot(kind='barh', ax=ax, color='coral')
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()

st.subheader("Top 10 States by Revenue")
state = df.groupby('ship-state')['Amount'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 4))
state.plot(kind='bar', ax=ax, color='steelblue')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

st.divider()

st.subheader("Monthly Revenue Trend")
monthly = df.groupby('Month_Num')['Amount'].sum().reset_index()
month_names = {4: 'April', 5: 'May', 6: 'June'}
monthly['Month'] = monthly['Month_Num'].map(month_names)
fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(data=monthly, x='Month', y='Amount', palette='Blues_d', ax=ax)
plt.tight_layout()
st.pyplot(fig)

st.sidebar.title("🔍 Filters")

# Category filter
categories = ['All'] + list(df['Category'].unique())
selected_cat = st.sidebar.selectbox("Select Category", categories)

# State filter
states = ['All'] + list(df['ship-state'].unique())
selected_state = st.sidebar.selectbox("Select State", states)

# Filter apply karo
filtered_df = df.copy()
if selected_cat != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_cat]
if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['ship-state'] == selected_state]

st.divider()
st.subheader("📊 Filtered Data Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Filtered Orders", f"{len(filtered_df):,}")
col2.metric("Filtered Revenue", f"₹{filtered_df['Amount'].sum()/1e7:.2f} Cr")
col3.metric("Avg Order Value", f"₹{filtered_df['Amount'].mean():.0f}")

st.divider()

st.subheader("📋 Raw Data")
st.dataframe(filtered_df.head(100))

st.caption(f"Showing top 100 rows out of {len(filtered_df):,} filtered records")