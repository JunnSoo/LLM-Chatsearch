import os
import streamlit as st
import pandas
import docx
import pickle
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain
from call_api_sql import append_data_to_database, call_text2sql_api, execute_sql_query
from check_api_openai import call_openai_create_sql, check_openai_api_key
from htmlTemplates import css, user_template, bot_template, product_template
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db, firestore
import json
import time

from initialize_firebase import initialize_firebase
from load_file_name import load_vector_store
from login_firebase import login_page
from process_text_file import process_text_file
from save_database_firebase import save_first_message, update_conversation_message
from save_vector_store import save_vector_store
import random
import string

# Ramdom id saving id history => Firebase
def generate_random_id(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def get_data(uid):
    try:
        ref = db.reference(f"{uid}")
        data = ref.get()
        return data
    except Exception as e:
        st.error("Lỗi get database firebase:", e)
        return None

def main():
    # Setup env
    load_dotenv()
    # firebase
    # Đường dẫn đến serviceAccountKey.json
    service_account_key_path = "D:/ai/ChatBot-LLM/credentials.json"

    # URL của Realtime Database của bạn
    database_url = 'https://chatbot-llm-b4175-default-rtdb.firebaseio.com/'
    # Khởi tạo Firebase
    if not firebase_admin._apps:
        st.session_state.is_initialize_firebase = initialize_firebase(service_account_key_path, database_url)
    st.set_page_config(page_title="Project Chat MySQL", page_icon=":sunflower:")
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
        visible = True
    if "session_history" not in st.session_state:
        st.session_state.session_history = generate_random_id()
        
    st.header("Project - Find Products TikiShop by CNN :sunflower:")
    
    # Screen Login
    if st.session_state.user_info == None:
        user_info = login_page()
        if user_info:
            st.session_state.user_info = user_info
            st.warning("Đăng nhập thành công. Đợi xíu nhó")
            st.write(st.session_state.user_info)
            visible = False
            time.sleep(2)
            st.rerun()
        else:
            visible = True
    else:
        visible = False

    with st.sidebar:
        st.subheader("File sản phẩm")
        uploadedFiles = st.file_uploader(
            label="Tải lên tài liệu bằng button dưới đây (pdf,csv,doc)",
            type=['.csv'],
            accept_multiple_files=True,
            help="Đây là phiên bản test nên đôi khi bị lỗi thông cảm ạ",
            disabled=visible
        )
        
        if (uploadedFiles != []):
            if st.button("Xử lý"):
                with st.spinner("Đang xử lý File"):
                    for file in uploadedFiles:
                        append_data_to_database(file)
        
        if st.button("Migrate Data Crawl",disabled=visible):
            with st.spinner("Đang upload"):
                save_first_message(st.session_state.user_info['localId'], st.session_state.chat_history)
        
        if st.session_state.user_info is not None:
            st.subheader("Lịch sử trò chuyện")
            data = get_data(st.session_state.user_info['localId'])
            if data is not None:
                for key, value in data.items():
                    if st.button(value['title'], key=key):
                        st.session_state.chat_history = value['data']
                        st.session_state.session_history = key
            if st.sidebar.button("Tạo mới"):
                st.session_state.chat_history = []
                st.session_state.session_history = generate_random_id()
                st.rerun()
    if visible == False:
        query = st.text_input("Vui lòng nhập yêu cầu về sản phẩm:",disabled=visible)
        if query:
            result = call_openai_create_sql("sk-proj-rHW9a0sdyIn3IJwoGszVT3BlbkFJouHgh2dbynYMNI2msgXO", query)
            if result is not None:
                sql_query = result["choices"][0]["message"]["content"]
                print(sql_query)
                sql_result = execute_sql_query(sql_query)
                if (sql_result is not None):
                    createtime = time.time()
                    # Lưu session 1 đoạn hội thoại vào database
                    index = len(st.session_state.chat_history)
                    if st.session_state.chat_history == []:
                        st.session_state.chat_history.append({
                            'question': query,
                            'response': sql_result,
                            'createtime': createtime
                        })
                        save_first_message(st.session_state.user_info['localId'], st.session_state.chat_history)
                    else:
                        message = {
                            'question': query,
                            'response': sql_result,
                            'createtime': createtime
                        }
                        update_conversation_message(st.session_state.user_info['localId'], message, index)
                        st.session_state.chat_history.append(message)
                        
            
        # result = call_text2sql_api(query)
        # temp = {'output': "SELECT * \nFROM products \nWHERE name LIKE '%áo thun%' AND price BETWEEN 100000 AND 150 AND rating_average > 4 \nLIMIT 10;", 'generation': {'count': 1}}
        # if temp is not None:
        #     sql_query = temp["output"]
        #     print(sql_query)
        #     sql_result = execute_sql_query(sql_query)
        #     st.write(sql_result)  # In kết quả truy vấn SQL lên giao diện Streamlit
        # else:
        #     st.error("Error occurred while fetching data from API")
        # response = []
        # st.session_state.chat_history.append({
        #     'question': query,
        #     'response': response
        # })
        # for i, message in enumerate(st.session_state.chat_history):
        #     if i % 2 == 0:
        #         st.write(user_template.replace(
        #             "{{MSG}}", message['question']), unsafe_allow_html=True)
        #     else:
        #         st.write(bot_template.replace(
        #             "{{MSG}}", message['response']), unsafe_allow_html=True)
        # st.write(user_template.replace("{{MSG}}", query), unsafe_allow_html=True)
        # st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True) 
        # st.divider()

    for i, products in enumerate(reversed(st.session_state.chat_history)):
        createtime_formatted = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(products['createtime']))
        
        st.write(user_template.replace(
            '{{MSG}}', products['question']).replace('{{CREATETIME}}', createtime_formatted), unsafe_allow_html=True)
        if 'response' not in products or not products['response']:
            st.write(bot_template.replace("{{MSG}}", "Thử lại cậu ơi data tui hong có cái cậu tìm òi =))) "), unsafe_allow_html=True) 
        else:
            for product in products['response']:
                #html = product_template.replace("{{IMAGE_URL}}", product["image_url"])
                html = product_template.replace("{{IMAGE_URL}}", "https://scontent.fsgn2-9.fna.fbcdn.net/v/t39.30808-1/341707090_157803910563043_6586752251395047829_n.jpg?stp=c50.0.200.200a_dst-jpg_p200x200&_nc_cat=103&ccb=1-7&_nc_sid=5f2048&_nc_ohc=wsT-iEPxtlcAb4AqvRU&_nc_ht=scontent.fsgn2-9.fna&oh=00_AfCOAI_5a0cgiET5mEKp0fnWcl7__0Sj3-QTWbSvd7icfQ&oe=662A7C7C")   
                html = html.replace("{{SHORT_URL}}", product["short_url"])
                html = html.replace("{{NAME}}", product["name"])
                html = html.replace("{{DESCRIPTION}}", product["short_description"])
                html = html.replace("{{RATING}}", str(product["rating_average"]))
                html = html.replace("{{QUANTITY_SOLD}}", str(product["quantity_sold"]))
                html = html.replace("{{PRICE}}", str(product["price"]))
                st.markdown(html, unsafe_allow_html=True)
        st.divider()
if __name__ == '__main__':
    main()
