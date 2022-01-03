from flask import Flask, render_template,request, jsonify

####################################################
from lotify.client import Client
import uuid
from app import app,db
#這裡會呼叫lotify功能必要模組
#以及匯入 flask app 跟 db 變數
##############匯入資料庫model########################
from app.model.token import token
##############匯入資料庫model########################



lotify = Client(client_id="yOYt2Juy9kZFfm16Ns4uzB", client_secret="6WlWeKVdV5EueVDVJqLu4ByD6czYEMx5BiJvzSP4Utb", redirect_uri="http://localhost:5000/callback")

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
    #from app import db
    #from app.model.token import token
    

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
