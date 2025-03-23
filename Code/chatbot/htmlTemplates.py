css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 100%;
  padding: 0 0rem;
  color: #fff;
}
.data-product {
    background-color: #585730;
    display: flex;
    align-items: center;
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.data-product .avatar {
  width: 20%;
  width: 100px; 
  height: 100px; 
  margin-right: 30px;
}
.data-product .avatar img{
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://inkythuatso.com/uploads/images/2022/05/anh-meo-che-anh-meo-bua-15-31-09-18-20.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://scontent.fsgn2-4.fna.fbcdn.net/v/t39.30808-1/412258273_1418807138707944_6030485564984423992_n.jpg?stp=dst-jpg_p200x200&_nc_cat=101&ccb=1-7&_nc_sid=5f2048&_nc_ohc=W6_Jp6lRNoMAb53xMbq&_nc_ht=scontent.fsgn2-4.fna&oh=00_AfCLIAVrn6UFpsmX1fNPjvUyWVINCQgqi5Vy1Z5S-REBqw&oe=662A6DC4">
    </div>    
    <div class="message">{{MSG}}</div>
    <div style="font-size: 12px; text-align: right;position: absolute; bottom: 10px; right: 20px;">{{CREATETIME}}</div>
</div>
'''

product_template = '''
<div class="data-product">
    <div class="avatar">
        <img src="{{IMAGE_URL}}">
    </div>
    <div>
        <div><a href="{{SHORT_URL}}" target="_blank">{{NAME}}</a></div>
        <div>{{DESCRIPTION}}</div>
        <div>Đánh giá: {{RATING}}</div>
        <div>Đã bán: {{QUANTITY_SOLD}}</div>
        <div>Giá: {{PRICE}} VNĐ</div>
    </div>
</div>
'''