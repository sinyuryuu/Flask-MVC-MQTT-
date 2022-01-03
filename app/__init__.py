# -*- coding: utf-8 -*-
import eventlet
eventlet.monkey_patch()

########### eventlet 必須在flask執行前就啟用否則會導致 用到 requests 錯誤 參考↓ ##################
#https://stackoverflow.com/questions/39969688/why-does-flask-socketio-gevent-give-me-ssl-eof-errors

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_migrate import Migrate




#eventlet.monkey_patch()   啟用會導致requests 錯誤




app = Flask(__name__,
    static_folder="static",      #靜態檔案資料夾名稱
    static_url_path="/"     #靜態檔案路徑 

) #__name__代表目前執行模組



app.config.from_object('app.setting')     #模組下的setting文件名稱，可以不用副檔名 
app.config.from_envvar('FLASKR_SETTINGS',True)   #設定環境變數，必須加 'True' 才能用

# 例如: set FLASKER_SETTINGS=C:\code\webtk\flaskproject\flaskdoorcontrol--beta3\app\setting.py


mqtt = Mqtt(app)
socketio = SocketIO(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db) 


####################  view 這裡一定要匯入不然會出問題####################

from app.model import user,token  #可以自行匯入資料庫資料表
from app.controller import app_manage #匯入contrller



################################################################



# 這個地方是在處理將呼叫模組建立實體化(變數)

