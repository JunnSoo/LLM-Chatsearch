import firebase_admin
from firebase_admin import credentials

def initialize_firebase(service_account_key_path, database_url):
    if not firebase_admin._apps:
        try:
            assert service_account_key_path is not None and database_url is not None
            
            cred = credentials.Certificate(service_account_key_path)
            
            firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })
            
            print("Kết nối Firebase thành công!")
            return True
        except Exception as e:
            print("Lỗi khi kết nối Firebase:", e)
            return False
    else:
        print("Ứng dụng Firebase đã được khởi tạo trước đó.")
        return True