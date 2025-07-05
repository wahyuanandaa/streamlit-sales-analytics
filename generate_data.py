import polars as pl
import numpy as np
from datetime import datetime, timedelta

# Function to generate data

def generate(nrows: int, filename: str):
    names = np.asarray([
        "Laptop", "Smartphone", "Desk", "Chair", "Monitor", "Printer",
        "Paper", "Pen", "Notebook", "Coffee Maker", "Cabinet", "Plastic Cups"
    ])
    categories = np.asarray([
        "Electronics", "Electronics", "Office", "Office", "Electronics", "Electronics",
        "Stationery", "Stationery", "Stationery", "Electronics", "Office", "Sundry"
    ])
    product_id = np.random.randint(len(names), size=nrows)
    quantity = np.random.randint(1, 11, size=nrows)
    price = np.random.randint(199, 10000, size=nrows) / 100
    
    # Generate random order dates between 2010 and 2023
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = (end_date - start_date).days
    
    # Create order dates as np.array and convert to string format
    order_dates = np.array([
        (start_date + timedelta(days=np.random.randint(0, date_range))).strftime('%Y-%m-%d')
        for _ in range(nrows)
    ])
    columns = {
        "order_id": np.arange(nrows),
        "order_date": order_dates,
        "customer_id": np.random.randint(100, 1000, size=nrows),
        "customer_name": [f"Customer_{i}" for i in np.random.randint(2**15, size=nrows)],
        "product_id": product_id + 200,
        "product_names": names[product_id],
        "categories": categories[product_id],
        "quantity": quantity,
        "price": price,
        "total": price * quantity,
    }
    
    # Create DataFrame and write to CSV
    df = pl.DataFrame(columns)
    df.write_csv(filename, separator=',', include_header=True)

if __name__ == "__main__":
    generate(100_000, "sales_data.csv") 