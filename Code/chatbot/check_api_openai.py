import openai
import streamlit as st

def check_openai_api_key(api_key):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "system", "content": "Hello, OpenAI!"}]
        )

        if response and response['id']:
            return True, "API key hợp lệ và hoạt động với OpenAI."
        else:
            return False, "API key không hợp lệ hoặc không hoạt động với OpenAI."
    except Exception as e:
        return False, f"Lỗi khi kiểm tra API key: {e}"
    
def call_openai_create_sql(api_key, query):
    openai.api_key = api_key
    temp = "Viết sql cho tôi khi tôi có bảng products chứa thông tin sản phẩm\nid int(11): id key\nproduct_id\tint(11): id sản phẩm\nname\tvarchar(255) Tên sản phẩm (Tìm theo LIKE %) gần giống tên\nsku\tvarchar(255)\tMã sản phẩm\nshort_description\ttext\tMô tả\t\nprice\tfloat: Giá bán\nlist_price\tfloat: Giá gốc\nprice_usd\tfloat: quy ra tiền USD\ndiscount\tfloat : Số tiền giảm\ndiscount_rate\tfloat : Số phần trăm giảm giá\nreview_count\tint(11): số lượt đánh giá\norder_count\tint(11): \ninventory_status\tint(11) : 1 là có , 0 là hết hàng\nshort_url\tvarchar(255): link sản phẩm\nrating_average \tfloat: Đánh giá\nquantity_sold\tint(11): Số lượt  bán\nbrand_id\tint(11): id cửa hàng\nbrand_name\tvarchar(255): nhãn hiệu\n\nHãy viết sql không cần giải thích gì thêm"
    query = temp + " " + query
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "system", "content": query}]
        )
        if response and response['id']:
            return response
        else:
            st.error("Lỗi lấy dữ liệu vui lòng liên hệ quản trị viên")
            return None
    except Exception as e:
        st.error(f"Lỗi khi kiểm tra API key: {e}")
        return None