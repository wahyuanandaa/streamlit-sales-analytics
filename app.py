import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Load data from CSV
@st.cache_data
def load_data():
    df = pd.read_csv('sales_data.csv', parse_dates=['order_date'])
    return df

def get_date_range(df):
    return df['order_date'].min(), df['order_date'].max()

def get_unique_categories(df):
    return sorted(df['categories'].dropna().unique())

# Function to get dashboard stats
def get_dashboard_stats(df, start_date, end_date, category):
    dff = df[(df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))]
    if category != 'All Categories':
        dff = dff[dff['categories'] == category]
    total_revenue = (dff['price'] * dff['quantity']).sum()
    total_orders = dff['order_id'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    top_category = dff.groupby('categories').apply(lambda x: (x['price'] * x['quantity']).sum()).sort_values(ascending=False)
    top_category = top_category.index[0] if not top_category.empty else 'N/A'
    return total_revenue, total_orders, avg_order_value, top_category

def get_plot_data(df, start_date, end_date, category):
    dff = df[(df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))]
    if category != 'All Categories':
        dff = dff[dff['categories'] == category]
    plot_df = dff.copy()
    plot_df['revenue'] = plot_df['price'] * plot_df['quantity']
    return plot_df.groupby('order_date').agg({'revenue': 'sum'}).reset_index().rename(columns={'order_date': 'date'})

def get_revenue_by_category(df, start_date, end_date, category):
    dff = df[(df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))]
    if category != 'All Categories':
        dff = dff[dff['categories'] == category]
    dff['revenue'] = dff['price'] * dff['quantity']
    return dff.groupby('categories').agg({'revenue': 'sum'}).reset_index().sort_values('revenue', ascending=False)

def get_top_products(df, start_date, end_date, category):
    dff = df[(df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))]
    if category != 'All Categories':
        dff = dff[dff['categories'] == category]
    dff['revenue'] = dff['price'] * dff['quantity']
    return dff.groupby('product_names').agg({'revenue': 'sum'}).reset_index().sort_values('revenue', ascending=False).head(10)

def get_raw_data(df, start_date, end_date, category):
    dff = df[(df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))]
    if category != 'All Categories':
        dff = dff[dff['categories'] == category]
    dff = dff.copy()
    dff['revenue'] = dff['price'] * dff['quantity']
    return dff.sort_values(['order_date', 'order_id'])

def plot_data(data, x_col, y_col, title, xlabel, ylabel, orientation='v'):
    fig, ax = plt.subplots(figsize=(10, 6))
    if not data.empty:
        if orientation == 'v':
            ax.bar(data[x_col], data[y_col])
        else:
            ax.barh(data[x_col], data[y_col])
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=45)
    else:
        ax.text(0.5, 0.5, "No data available", ha='center', va='center')
    return fig

# Streamlit App
st.title("Sales Performance Dashboard")

# Load data
df = load_data()

# Filters
with st.container():
    col1, col2, col3 = st.columns([1, 1, 2])
    min_date, max_date = get_date_range(df)
    start_date = col1.date_input("Start Date", min_date)
    end_date = col2.date_input("End Date", max_date)
    categories = get_unique_categories(df)
    category = col3.selectbox("Category", ["All Categories"] + list(categories))

# Custom CSS for metrics
st.markdown("""
    <style>
    .metric-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .metric-container {
        flex: 1;
        padding: 10px;
        text-align: center;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin: 0 5px;
    }
    .metric-label {
        font-size: 14px;
        color: #555;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 18px;
        font-weight: bold;
        color: #0e1117;
    }
    </style>
""", unsafe_allow_html=True)

# Metrics
st.header("Key Metrics")
total_revenue, total_orders, avg_order_value, top_category = get_dashboard_stats(df, start_date, end_date, category)

# Custom metrics display
metrics_html = f"""
<div class="metric-row">
    <div class="metric-container">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">${total_revenue:,.2f}</div>
    </div>
    <div class="metric-container">
        <div class="metric-label">Total Orders</div>
        <div class="metric-value">{total_orders:,}</div>
    </div>
    <div class="metric-container">
        <div class="metric-label">Average Order Value</div>
        <div class="metric-value">${avg_order_value:,.2f}</div>
    </div>
    <div class="metric-container">
        <div class="metric-label">Top Category</div>
        <div class="metric-value">{top_category}</div>
    </div>
</div>
"""
st.markdown(metrics_html, unsafe_allow_html=True)

# Visualization Tabs
st.header("Visualizations")
tabs = st.tabs(["Revenue Over Time", "Revenue by Category", "Top Products"])


# Revenue Over Time Tab
with tabs[0]:
    st.subheader("Revenue Over Time")
    revenue_data = get_plot_data(df, start_date, end_date, category)
    st.pyplot(plot_data(revenue_data, 'date', 'revenue', "Revenue Over Time", "Date", "Revenue"))

# Revenue by Category Tab
with tabs[1]:
    st.subheader("Revenue by Category")
    category_data = get_revenue_by_category(df, start_date, end_date, category)
    st.pyplot(plot_data(category_data, 'categories', 'revenue', "Revenue by Category", "Category", "Revenue"))

# Top Products Tab
with tabs[2]:
    st.subheader("Top Products")
    top_products_data = get_top_products(df, start_date, end_date, category)
    st.pyplot(plot_data(top_products_data, 'product_names', 'revenue', "Top Products", "Revenue", "Product Name", orientation='h'))

st.header("Raw Data")
raw_data = get_raw_data(df, start_date, end_date, category)
raw_data = raw_data.reset_index(drop=True)
st.dataframe(raw_data, hide_index=True)
st.write("")