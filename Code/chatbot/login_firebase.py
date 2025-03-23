import firebase_admin
from firebase_admin import credentials, auth
import streamlit as sl;
import requests
import json
import os

#from model.user import save_user_to_cookie

FIREBASE_WEB_API_KEY = "AIzaSyCwsCJ5Y4rffHyfKmc0iq3v-lyTzixjmO8"
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        if user:
            auth_user,error = sign_in_with_email_and_password(email,password)
            print(auth_user)
            if error is None:
                return auth_user, None
            else:
                return None, {'error': 'Login failed'}
        else: 
            return None, {'error': 'Login failed'}
    except Exception as e:
        return None, str(e)
    
def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
    if not FIREBASE_WEB_API_KEY:
        return {'error': 'Missing API key'}, None
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })
    try:
        r = requests.post(rest_api_url,
                          params={"key": FIREBASE_WEB_API_KEY},
                          data=payload)
        
        if r.status_code == 200 and 'localId' in r.json():
            return r.json(), None
        else:
            return None, {'error': 'Login failed'}
    except Exception as e:
        return None, {'error': str(e)}
    
def login_page():
    sl.title("Đăng nhập",)
    email = sl.text_input("Email")
    password = sl.text_input("Password", type="password")

    if sl.button("Đăng nhập"):
        if email and password:
            user, error = login(email, password)
            if user and error == None:
                return user
            else:
                sl.error("Đăng nhập thất bại: " + str(error))
                return None
        else:
            sl.warning("Vui lòng nhập email và password.")
            return None
    else:
        return None
            
def update_user_info():
    sl.warning("Vui lòng cập nhật thông tin của bạn")
    display_name = sl.text_input("Tên", key='display_name_input')
    photo_url = sl.text_input("URL hình ảnh", key='photo_url_input')

    if sl.button("Cập nhật"):
        # if display_name:
        #     user['displayName'] = display_name
        # if photo_url:
        #     user['photo_url'] = photo_url
        
        # # Cập nhật thông tin người dùng lên Firebase
        # user_record = auth.update_user(
        #     uid = user["idToken"],
        #     display_name=user["displayName"],
        #     photo_url=user["photo_url"]
        # )
        # print("Sau khi update" + user_record)
        
        sl.success("Thông tin đã được cập nhật.")
