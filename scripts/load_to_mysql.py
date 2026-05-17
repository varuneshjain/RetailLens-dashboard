import pandas as pd
import mysql.connector

# MySQL se connect karo
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Varunesh@10',  
    database='retailens'
)

df = pd.read_csv('data/amazon_cleaned.csv')

cursor = conn.cursor()

# Table banao
cursor.execute("""
    CREATE TABLE IF NOT EXISTS amazon_sales (
        order_id VARCHAR(50),
        date DATE,
        status VARCHAR(50),
        fulfilment VARCHAR(50),
        sales_channel VARCHAR(50),
        ship_service_level VARCHAR(50),
        style VARCHAR(50),
        sku VARCHAR(50),
        category VARCHAR(50),
        size VARCHAR(20),
        courier_status VARCHAR(50),
        qty INT,
        currency VARCHAR(10),
        amount FLOAT,
        ship_city VARCHAR(50),
        ship_state VARCHAR(50),
        ship_postal_code VARCHAR(20),
        ship_country VARCHAR(10),
        b2b BOOLEAN,
        month VARCHAR(20),
        month_num INT
    )
""")

# Data insert karo
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO amazon_sales VALUES 
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(row))

conn.commit()
print(f"Done! {len(df)} rows inserted.")
cursor.close()
conn.close()