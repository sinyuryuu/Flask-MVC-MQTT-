
#from flask.templating import render_template_string
#import requests #requests 模組
import json
import uuid
import os
from flask import Flask, render_template ,request, jsonify
import requests

#app 導入後才能import (從__int__匯入app)
from app import app,db,socketio,migrate,mqtt
from app.controller.login import login_required,getnowuser     #這裡只用到flask_login的登入功能驗證
from app.controller.mqtt import bmqtt               #這裡只用到mqtt 解析後 bmqtt這個串列
from app.controller.linenotify import lotify        #這裡只用到lotify這個變數

##############匯入資料庫model########################
from app.model.user import user
from app.model.token import token

app.secret_key = 'dd06be55a06c03312b2ab109b5f8f6ab'
#secret_key = 'dd06be55a06c03312b2ab109b5f8f6ab'
################################# 網頁功能 #############################################

import datetime

app.jinja_env.globals['nowts'] = datetime.datetime.now()   #設定jinja2 時間模板

# UTC時間自動更新
@app.context_processor 
def inject_template_globals(): 
    return { 
     'nowts': datetime.datetime.utcnow(), 
    } 


# 前端放入 {{ nowts.strftime('%Y') }}

def lineNotifyMessage(token, msg):

    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg }
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code



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
    token = 'ctupVqalWzuKbaw72AWqKcl2tKXftiT5YhGiBR0v0jL'
    message = getnowuser()+'開門!!!!!'
    lineNotifyMessage(token, message)
    return render_template("arduino.html")


@app.route("/ledoff", methods=['GET', 'POST'])
def ledoff():        
    mqtt.publish('esp/son', 'soff') 
    token = 'ctupVqalWzuKbaw72AWqKcl2tKXftiT5YhGiBR0v0jL'
    message = getnowuser()+'閉門！！！'
    lineNotifyMessage(token, message)
    return render_template("arduino.html")







@app.route("/show")
def show():
    name=request.args.get("n","")
    
    return render_template ("index.html",name =name)




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
        



        

    
@app.route("/token1")
def token1():
    #from app import db
    #from app.model.token import  token
    alltoken = token.query.all()
    #linetoken = token.query.first() #回傳token 資料表第一個資料
    #linetoken = token.query.get(1) #回傳token 資料表第一個資料
    linetoken = token.query.get(1).linetoken  #回傳token 資料表 linetoken第一個資料

    return render_template("line.html", token=linetoken,alltoken=alltoken)



################################# 網頁路由 #############################################



#建立"/" 處理函式
#預設get方法
@app.route("/") #函式的裝飾 (decorator) 以提供為基礎，提供附加功能
def index():
    db.session.commit()
    return render_template("index.html")
    

@app.route("/page")
@login_required
def page():
    return render_template ("page.html")

@app.route("/line")
@login_required
def line():
    # LINK 由CLIENT_ID、SECRET、URI組成
     link = lotify.get_auth_link(state=uuid.uuid4())
     return render_template("line.html", auth_url=link)


@app.route("/arduino")
@login_required
def arduino(): 
    
  
    return render_template("arduino.html",nowuser = getnowuser())


@app.route('/top')
def top():
  return render_template('top.html')

@app.route('/member')
@login_required
def member():
  return render_template('member.html')









#https://www.coder.work/article/7620724  flask 即時顯示狀態
