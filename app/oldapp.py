# from types import MethodType
# from typing import Collection
from threading import local
import eventlet
import builtins
import json
from flask.templating import render_template_string
import requests #requests 模組
from lotify.client import Client
import uuid
import os
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask import Flask, render_template, Request , redirect ,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
#app 導入後才能import 
from app import User, token, Category


# flask Request模組 HTTP 請求 #requests 模組 # redirect載入導向網址物件

########################## 這裡是未將flask MVC(MTV)化的地方，可以看到很長...的程式碼  ##########################


#  取得目前文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

eventlet.monkey_patch()

doorstatus =""



#開發者
CLIENT_ID = os.getenv("yOYt2Juy9kZFfm16Ns4uzB")
SECRET = os.getenv("6WlWeKVdV5EueVDVJqLu4ByD6czYEMx5BiJvzSP4Utb")
URI = os.getenv("http://localhost:5000/callback")
lotify = Client(client_id="yOYt2Juy9kZFfm16Ns4uzB", client_secret="6WlWeKVdV5EueVDVJqLu4ByD6czYEMx5BiJvzSP4Utb", redirect_uri="http://localhost:5000/callback")


app = Flask(__name__,
    static_folder="static",      #靜態檔案資料夾名稱
    static_url_path="/"     #靜態檔案路徑 

) #__name__代表目前執行模組





app.secret_key = 'dd06be55a06c03312b2ab109b5f8f6ab'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請登入後再操作!'




# app.config['SECRET'] = 'my secret key'
# app.config['MQTT_BROKER_URL'] = '192.168.0.144'
# app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_USERNAME'] = 'bob01'
# app.config['MQTT_PASSWORD'] = '123456'
# app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds

app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_CLEAN_SESSION'] = True


#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置sqlite檔案路徑
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(pjdir, 'data.sqlite')


app.secret_key = 'dd06be55a06c03312b2ab109b5f8f6ab'



mqtt = Mqtt(app)
socketio = SocketIO(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db) # this


from app.model import user, token



#  users 使用者清單
users = {'bob': {'password': '123'}}      


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(user_id):
    if user_id not in users:
        return

    user = User()
    user.id = user_id
    return user


@login_manager.request_loader
def request_loader(request):
    user_id = request.form.get('user_id')
    if user_id not in users:
        return

    user = User()
    user.id = user_id

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[user_id]['password']

    return user




@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('esp/test')

bmqtt = ['123']
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global sg 
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    doorstatus =  message.payload.decode('utf-8') # 轉換編碼utf-8才看得懂中文
    socketio.emit('mqtt_message', data=data)
    bmqtt.append(doorstatus)
    sg = doorstatus
    print(sg) 
    print("成功",*g) 
    return sg


""" @mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf) """



@app.route('/top')
def top():
  return render_template('top.html')

@app.route('/member')
@login_required
def member():
  return render_template('member.html')


from flask import request, render_template, url_for, redirect, flash
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    user_id = request.form['user_id']
    if (user_id in users) and (request.form['password'] == users[user_id]['password']):
        user = User()
        user.id = user_id
        login_user(user)
        
        #return redirect(url_for('from_start'))
        #return render_template('login.html')
        return render_template ("index.html",name =user_id)

    flash('登入失敗了...')
    return render_template('login.html')

@app.route('/logout')
def logout():
    user_id = current_user.get_id()
    logout_user()
    flash(f'{user_id}！歡迎下次再來！')
    return render_template('login.html') 


@app.route("/mqtt")
def mqttz():
    
    
    if  bmqtt[-1] == "yes" and len(bmqtt) > 1  :
        print(len(bmqtt))
        now = "yes"
        bmqtt.clear() 
        bmqtt.append("null")   
        return render_template("arduino.html",doorstatus = now)
    
        
        
    elif bmqtt[-1] == "no" and len(bmqtt) > 1 :
        now = "no"
        bmqtt.clear()
        bmqtt.append("null")  
        return render_template("arduino.html",doorstatus = now)   

    else:
        # return render_template("arduino.html",doorstatus = "残念")
        return render_template("arduino.html",doorstatus = "残念")


   
    
@app.route("/ledon", methods=['GET', 'POST'])
def ledon():        
    mqtt.publish('esp/son', 'on') 
    return render_template("arduino.html")


@app.route("/ledoff", methods=['GET', 'POST'])
def ledoff():        
    mqtt.publish('esp/son', 'soff') 
    return render_template("arduino.html")
   



@app.route("/arduino")
@login_required
def arduino(): 
  
    return render_template("arduino.html")

#要求字串   max=

@app.route("/keisan")
@login_required
def keisan():  #1+2+3+...max

    minn = request.args.get("minn","")  #("",預設值)
    maxn = request.args.get("maxn","")  #("",預設值)
    suzi = 0
    if len(minn) == 0 or len(maxn) == 0:

      return "無"  
    else:

  
        maxn=int(maxn)
        minn=int(minn)   
        result = 0
        print("最大數",maxn)
        for z in range(minn,maxn+1):
            result+=z

       
        print("答案",result)
        suzi = result
        print("答案",suzi)
        return render_template("page.html", suzi=suzi)



        


g=[]

@app.route("/line")
@login_required
def line():
    # LINK 由CLIENT_ID、SECRET、URI組成
     link = lotify.get_auth_link(state=uuid.uuid4())
     return render_template("line.html", auth_url=link)
    
@app.route("/token1")
def token1():
    from app import db
    from app import token
    alltoken = token.query.all()
    #linetoken = token.query.first() #回傳token 資料表第一個資料
    #linetoken = token.query.get(1) #回傳token 資料表第一個資料
    linetoken = token.query.get(1).linetoken  #回傳token 資料表 linetoken第一個資料

    return render_template("line.html", token=linetoken,alltoken=alltoken)

#拿個人的token(每次綁定會變化)  拿一次就可以了 
#"RUhm4gpuamZC1JwFS09Txr4t5ioeGtGeYRgwprDNwZP"
#回傳index.html token 帶值
# callbacl → token 有數值 → 前端token都可以抓到這個變數
#http://localhost:5000/callback?code=YIt5cxBgpq0Igr2MSZSzr4&state=70a58a1a-ebf8-4dce-ae06-c8260f024c8c
#↑ 會藉由lotify 解析 "code" 得到token
#一個人可以有複數個token?
@app.route("/callback")
def confirm():

    oktoken = lotify.get_access_token(code=request.args.get("code"))
    from app import db
    from app import token
    

    #token資料新增到資料庫
    addtoken = token(linetoken= oktoken)
    db.session.add(addtoken)
    db.session.commit()
    print("寫入成功")
    return render_template("line.html", token=oktoken)
    



#可以將個人token寫入資料庫再執行
@app.route("/notify/send", methods=["POST"])
def send():
    payload = request.get_json()
    response = lotify.send_message(
        access_token=payload.get("token"), message=payload.get("message")
    )
    return jsonify(result=response.get("message")), response.get("status")

# 貼圖設定 https://developers.line.biz/en/docs/messaging-api/sticker-list/
@app.route("/notify/send/sticker", methods=["POST"])
def send_sticker():
    payload = request.get_json()
    response = lotify.send_message_with_sticker(
        access_token=payload.get("token"),
        message=payload.get("message"),
        sticker_id=630,
        sticker_package_id=4,
    )
    return jsonify(result=response.get("message")), response.get("status")


#建立"/" 處理函式
#預設get方法
@app.route("/") #函式的裝飾 (decorator) 以提供為基礎，提供附加功能
def index():
    db.session.commit()
    # print("請求的方法", request.method)
    # print("通訊協定", request.scheme)
    # print("主機名稱", request.host)
    # print("路徑", request.path)
    # print("完整網址", request.url)
    # return "hello word2"
    # print("瀏覽器和作業系統", request.headers.get("user-agent"))
    # print("使用者語言偏好",request.headers.get("accept-language"))
    # print("引薦網址",request.headers.get("referrer"))
    # lang=request.headers.get("accept-language") 
    # if lang.startswith("zh-TW"):
    #     return json.dumps({
    #         "staus":"OK",
    #         "text":"どうもtw！"
    #          },ensure_ascii=False)      #指示不要用ascii處理中文
    # else:     
    #     return json.dumps({
    #         "staus":"OK",
    #         "text":"どうもjp！"
    #          },ensure_ascii=False)
    return render_template("index.html")




@app.route("/show")
def show():
    name=request.args.get("n","")
    
    return render_template ("index.html",name =name)



@app.route("/page")
@login_required
def page():
    return render_template ("page.html")

# @app.route("/user/<username>")
# def getname(username):
#     if username == "bob":
#         return "どうも "+username
#     elif username =="aa":
#         return "hello "+username
#     else:
#         return "知りません "+username

socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True, debug=True) #立刻啟動伺服器 區域網路能連線
#app.run(host='0.0.0.0', port=5000,debug=True) #立刻啟動伺服器 區域網路能連線


#https://www.coder.work/article/7620724  flask 即時顯示狀態
