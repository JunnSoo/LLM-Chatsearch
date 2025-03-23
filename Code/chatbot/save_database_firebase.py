from firebase_admin import db
import streamlit as st
import time

def save_first_message(uid, data):
    title = data[0]['question'][:30] + '...' if len(data[0]['question']) > 30 else data[0]['question']
    # Khởi tạo cấu trúc lưu để lưu lịch sử chat
    header = {
        'title' : title,
        'createtime': time.time(),
        'data': [data[0]],
    }
    try:
        ref = db.reference(str(uid) + '/')
        history = ref.child(str(st.session_state.session_history))
        history.set(header)
    except Exception as e:
        st.error("Lỗi lưu database firebase:", e)
        
def update_conversation_message(uid, data, index):
    try:
        ref = db.reference(str(uid) + '/' + st.session_state.session_history + "/data")
        ref.child(str(index)).set(data)
    except Exception as e:
        st.error("Lỗi lưu database firebase:", e)