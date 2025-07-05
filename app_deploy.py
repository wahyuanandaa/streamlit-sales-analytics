import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
from io import StringIO

# Set page config
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data from CSV
@st.cache_data
def load_data():
    try:
        # Try to load from CSV file
        if os.path.exists('sales_data.csv'):
            df = pd.read_csv('sales_data.csv')
            # Convert order_date to datetime
            df['order_date'] = pd.to_datetime(df['order_date'])
            return df
        else:
            # If CSV doesn't exist, create sample data
            st.warning("File sales_data.csv tidak ditemukan. Membuat data sample...")
            return create_sample_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return create_sample_data()

def create_sample_data():
    """Create sample sales data for demonstration"""
    import numpy as np
    from datetime import datetime, timedelta
    
    # Generate sample data
    np.random.seed(42)
    n_records = 1000
    
    # Date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = [start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days)) for _ in range(n_records)]
    
    # Sample data
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports']
    products = {
        'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera'],
        'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Shoes', 'Jacket'],
        'Books': ['Fiction', 'Non-Fiction', 'Science', 'History', 'Biography'],
        'Home & Garden': ['Furniture', 'Kitchen', 'Garden Tools', 'Decor', 'Lighting'],
        'Sports': ['Football', 'Basketball', 'Tennis', 'Gym Equipment', 'Outdoor Gear']
    }
    
    data = []
    for i in range(n_records):
        category = np.random.choice(categories)
        product = np.random.choice(products[category])
        
        data.append({
            'order_id': i + 1,
            'order_date': np.random.choice(dates),
            'customer_id': np.random.randint(1000, 9999),
            'customer_name': f"Customer {np.random.randint(1, 100)}",
            'product_id': np.random.randint(100, 999),
            'product_names': product,
            'categories': category,
            'quantity': np.random.randint(1, 10),
            'price': round(np.random.uniform(10, 500), 2)
        })
    
    df = pd.DataFrame(data)
    df['total'] = df['quantity'] * df['price']
    return df

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

# Date range filter
min_date = df['order_date'].min().date()
max_date = df['order_date'].max().date()

col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Start Date", min_date)
with col2:
    end_date = st.date_input("End Date", max_date)

# Category filter
categories = ['All Categories'] + sorted(df['categories'].unique().tolist())
selected_category = st.sidebar.selectbox("Category", categories)

# Filter data based on selections
def filter_data(df, start_date, end_date, category):
    filtered_df = df[
        (df['order_date'].dt.date >= start_date) &
        (df['order_date'].dt.date <= end_date)
    ]
    
    if category != 'All Categories':
        filtered_df = filtered_df[filtered_df['categories'] == category]
    
    return filtered_df

filtered_df = filter_data(df, start_date, end_date, selected_category)

# Main dashboard
st.title("📊 Sales Analytics Dashboard")
st.markdown("---")

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = filtered_df['total'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.2f}")

with col2:
    total_orders = filtered_df['order_id'].nunique()
    st.metric("Total Orders", f"{total_orders:,}")

with col3:
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    st.metric("Avg Order Value", f"${avg_order_value:,.2f}")

with col4:
    top_category = filtered_df.groupby('categories')['total'].sum().idxmax() if not filtered_df.empty else "N/A"
    st.metric("Top Category", top_category)

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue Over Time")
    
    # Daily revenue
    daily_revenue = filtered_df.groupby(filtered_df['order_date'].dt.date)['total'].sum().reset_index()
    daily_revenue.columns = ['date', 'revenue']
    
    if not daily_revenue.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(daily_revenue['date'], daily_revenue['revenue'], marker='o', linewidth=2, markersize=4)
        ax.set_xlabel('Date')
        ax.set_ylabel('Revenue ($)')
        ax.set_title('Daily Revenue Trend')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("No data available for the selected date range")

with col2:
    st.subheader("🏷️ Revenue by Category")
    
    # Category revenue
    category_revenue = filtered_df.groupby('categories')['total'].sum().sort_values(ascending=False)
    
    if not category_revenue.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(category_revenue.index, category_revenue.values, color='skyblue')
        ax.set_xlabel('Category')
        ax.set_ylabel('Revenue ($)')
        ax.set_title('Revenue by Category')
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:,.0f}', ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("No data available for the selected category")

# Top products
st.subheader("🏆 Top 10 Products")
top_products = filtered_df.groupby('product_names')['total'].sum().sort_values(ascending=False).head(10)

if not top_products.empty:
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(top_products.index, top_products.values, color='lightgreen')
    ax.set_xlabel('Revenue ($)')
    ax.set_title('Top 10 Products by Revenue')
    ax.grid(True, alpha=0.3)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
               f'${width:,.0f}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("No data available for the selected filters")

# Raw data table
st.subheader("📋 Raw Data")
st.markdown(f"Showing {len(filtered_df)} records")

# Add pagination
records_per_page = 100
total_pages = (len(filtered_df) - 1) // records_per_page + 1

if total_pages > 1:
    page = st.selectbox("Page", range(1, total_pages + 1))
    start_idx = (page - 1) * records_per_page
    end_idx = start_idx + records_per_page
    display_df = filtered_df.iloc[start_idx:end_idx]
else:
    display_df = filtered_df

# Display the data
if not display_df.empty:
    # Format the display
    display_df_formatted = display_df.copy()
    display_df_formatted['order_date'] = display_df_formatted['order_date'].dt.strftime('%Y-%m-%d')
    display_df_formatted['price'] = display_df_formatted['price'].apply(lambda x: f"${x:.2f}")
    display_df_formatted['total'] = display_df_formatted['total'].apply(lambda x: f"${x:.2f}")
    
    st.dataframe(display_df_formatted, use_container_width=True)
else:
    st.info("No data available for the selected filters")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📊 Sales Analytics Dashboard | Built with Streamlit</p>
    <p>Data source: CSV file | Last updated: {}</p>
</div>
""".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True) 