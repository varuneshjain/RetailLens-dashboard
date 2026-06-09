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
def load_amazon():
    return pd.read_csv('data/amazon_cleaned.csv')

@st.cache_data
def load_product():
    return pd.read_csv('data/Sale Report.csv', encoding='unicode_escape')

@st.cache_data
def load_pricing():
    df = pd.read_csv('data/May-2022.csv', encoding='unicode_escape')
    for col in ['Amazon MRP', 'Flipkart MRP', 'Myntra MRP', 'Ajio MRP']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

@st.cache_data
def load_international():
    df = pd.read_csv('data/International sale Report.csv', encoding='unicode_escape')
    df['GROSS AMT'] = pd.to_numeric(df['GROSS AMT'], errors='coerce')
    df.dropna(subset=['GROSS AMT'], inplace=True)
    return df

# Sidebar filters
st.sidebar.title("🔍 Filters")
df = load_amazon()
categories = ['All'] + list(df['Category'].unique())
selected_cat = st.sidebar.selectbox("Select Category", categories)
states = ['All'] + list(df['ship-state'].unique())
selected_state = st.sidebar.selectbox("Select State", states)

filtered_df = df.copy()
if selected_cat != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_cat]
if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['ship-state'] == selected_state]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🛒 Amazon Sales", "👗 Product Analysis", "💰 Pricing", "🌍 International"])

# ── TAB 1 ──
with tab1:
    st.title("🔍 RetailLens — Amazon Sales Dashboard")
    st.markdown("**1,21,180 orders | Apr–Jun 2022 | Amazon India**")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders", f"{len(filtered_df):,}")
    col2.metric("Total Revenue", f"₹{filtered_df['Amount'].sum()/1e7:.2f} Cr")
    col3.metric("Avg Order Value", f"₹{filtered_df['Amount'].mean():.0f}")
    col4.metric("Cancellation Rate", f"{(filtered_df['Status'] == 'Cancelled').sum() / len(filtered_df) * 100:.2f}%")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Category")
        cat = filtered_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        cat.plot(kind='bar', ax=ax, color='teal')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Order Status Breakdown")
        status = filtered_df['Status'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        status.plot(kind='barh', ax=ax, color='coral')
        plt.tight_layout()
        st.pyplot(fig)

    st.divider()
    st.subheader("Top 10 States by Revenue")
    state = filtered_df.groupby('ship-state')['Amount'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 4))
    state.plot(kind='bar', ax=ax, color='steelblue')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    st.subheader("Monthly Revenue Trend")
    monthly = filtered_df.groupby('Month_Num')['Amount'].sum().reset_index()
    month_names = {4: 'April', 5: 'May', 6: 'June'}
    monthly['Month'] = monthly['Month_Num'].map(month_names)
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=monthly, x='Month', y='Amount', palette='Blues_d', ax=ax)
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    st.subheader("📋 Raw Data")
    st.dataframe(filtered_df.head(100))
    st.caption(f"Showing top 100 rows out of {len(filtered_df):,} filtered records")

# ── TAB 2 ──
with tab2:
    st.title("👗 Product Analysis")
    df_prod = load_product()
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stock by Size")
        size_sales = df_prod.groupby('Size')['Stock'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        size_sales.plot(kind='bar', ax=ax, color='teal')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Category wise Stock")
        cat_stock = df_prod.groupby('Category')['Stock'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        cat_stock.plot(kind='bar', ax=ax, color='coral')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

# ── TAB 3 ──
with tab3:
    st.title("💰 Pricing Analysis")
    df_price = load_pricing()
    st.divider()

    st.subheader("Average MRP by Platform")
    platforms = ['Amazon MRP', 'Flipkart MRP', 'Myntra MRP', 'Ajio MRP']
    avg_prices = df_price[platforms].mean().sort_values(ascending=False).round(2)
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(avg_prices.index, avg_prices.values,
                  color=['#FF9900', '#2874F0', '#FF3F6C', '#A020F0'],
                  edgecolor='white', width=0.5)
    for bar, val in zip(bars, avg_prices.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                f'₹{val:.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    st.subheader("Category wise Platform Comparison")
    cat_platform = df_price.groupby('Category')[['Amazon MRP', 'Flipkart MRP', 'Myntra MRP']].mean().round(2)
    cat_platform = cat_platform.sort_values('Amazon MRP', ascending=False).head(8)
    fig, ax = plt.subplots(figsize=(12, 5))
    cat_platform.plot(kind='bar', ax=ax, color=['#FF9900', '#2874F0', '#FF3F6C'], edgecolor='white')
    plt.xticks(rotation=45, ha='right')
    plt.legend(['Amazon', 'Flipkart', 'Myntra'])
    plt.tight_layout()
    st.pyplot(fig)

# ── TAB 4 ──
with tab4:
    st.title("🌍 International Sales")
    df_intl = load_international()
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", f"{len(df_intl):,}")
    col2.metric("Total Revenue", f"₹{df_intl['GROSS AMT'].sum()/1e7:.2f} Cr")
    col3.metric("Avg Order Value", f"₹{df_intl['GROSS AMT'].mean():.0f}")

    st.divider()
    st.subheader("Top 10 Customers by Revenue")
    top_customers = df_intl.groupby('CUSTOMER')['GROSS AMT'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 4))
    top_customers.plot(kind='bar', ax=ax, color='#2A9D8F')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    st.subheader("Top 10 Months by Revenue")
    monthly_intl = df_intl.groupby('Months')['GROSS AMT'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 4))
    monthly_intl.plot(kind='bar', ax=ax, color='#E76F51')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)