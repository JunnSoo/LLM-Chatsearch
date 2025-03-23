import requests
import mysql.connector
import streamlit as st
import pandas as pd

# Hàm gọi API và xử lý dữ liệu trả về
def call_text2sql_api(query):
    api_url = "https://www.text2sql.ai/api/sql/generate"
    headers = {
        "Authorization": "Bearer 0b00d59ef332f221125dfcc2a4a7dfda31b8af64644021876f4abe9bb87bb1a0",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": query,
        "type": "mysql",
        "schema": "products (id, name, sku, short_description, price, list_price, price_usd, discount, discount_rate, review_count, order_count, inventory_status, short_url, rating_average, quantity_sold, brand_id, brand_name);"
    }
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# Hàm kết nối đến cơ sở dữ liệu MySQL và thực thi câu lệnh SQL

# Kết nối đến cơ sở dữ liệu MySQL
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="test",
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as error:
        print("Failed to connect to MySQL database: {}".format(error))
        
def execute_sql_query(sql_query):
    try:
        connection = connect_to_database()
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql_query)
            result = cursor.fetchall()
            return result
    except mysql.connector.Error as error:
        st.error("Failed to execute SQL query: {}".format(error))
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_max_id_from_products(cursor):
    try:
        sql_query = "SELECT MAX(id) AS max_id FROM products;"
        cursor.execute(sql_query)
        result = cursor.fetchone()
        max_id = result[0]
        return max_id
    except mysql.connector.Error as error:
        print("Error getting max ID from products table: {}".format(error))


# Đọc dữ liệu từ file CSV và append vào bảng products trong cơ sở dữ liệu
def append_data_to_database(csv_file):
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            max_id = get_max_id_from_products(cursor)
            # Đọc dữ liệu từ file CSV
            data = pd.read_csv(csv_file, encoding='utf-8')
            for index, row in data.iterrows():
                max_id += 1
                product_id = row['product_id'] if pd.notna(row['product_id']) else None
                name = row['name'] if pd.notna(row['name']) else None
                sku = row['sku'] if pd.notna(row['sku']) else 0
                short_description = row['short_description'] if pd.notna(row['short_description']) else None
                price = row['price'] if pd.notna(row['price']) else 0
                list_price = row['list_price'] if pd.notna(row['list_price']) else 0
                price_usd = row['price_usd'] if pd.notna(row['price_usd']) else 0
                discount = row['discount'] if pd.notna(row['discount']) else 0
                discount_rate = row['discount_rate'] if pd.notna(row['discount_rate']) else 0
                review_count = row['review_count'] if pd.notna(row['review_count']) else 0
                order_count = row['order_count'] if pd.notna(row['order_count']) else 0
                inventory_status = 1 if row['inventory_status'] == 'available' else 0
                short_url = row['short_url'] if pd.notna(row['short_url']) else None
                rating_average = row['rating_average'] if pd.notna(row['rating_average']) else 0
                quantity_sold = row['quantity_sold'] if pd.notna(row['quantity_sold']) else 0
                brand_id = row['brand_id'] if pd.notna(row['brand_id']) else 0
                brand_name = row['brand_name'] if pd.notna(row['brand_name']) else None
                
                # Tạo câu lệnh SQL để chèn dữ liệu
                sql = """INSERT INTO products (id, product_id, name, sku, short_description, price, list_price, price_usd, discount, discount_rate, review_count, order_count, inventory_status, short_url, rating_average, quantity_sold, brand_id, brand_name)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                        
                # Thực thi câu lệnh SQL
                cursor.execute(sql, (max_id, product_id, name, sku, short_description, price, list_price, price_usd, discount, discount_rate, review_count, order_count, inventory_status, short_url, rating_average, quantity_sold, brand_id, brand_name))
                
                # Commit thay đổi
                connection.commit()
            print("Data appended successfully.")

    except mysql.connector.Error as error:
        print("Failed to append data to MySQL database: {}".format(error))