import os

DEBUG = True

#############################  SQlite資料庫 設定檔  #####################################


pjdir = os.path.abspath(os.path.dirname(__file__))




#  新版本的部份預設為none，會有異常，再設置True即可。
SQLALCHEMY_TRACK_MODIFICATIONS = True
#  設置sqlite檔案路徑
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(pjdir, 'data.sqlite')





#############################  MQTT 設定檔  #####################################

# app.config['SECRET'] = 'my secret key'
# app.config['MQTT_BROKER_URL'] = '192.168.0.144'
# app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_USERNAME'] = 'bob01'
# app.config['MQTT_PASSWORD'] = '123456'
# app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds

SECRET = 'my secret key'
TEMPLATES_AUTO_RELOAD = True
MQTT_BROKER_URL = 'broker.hivemq.com'
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = ''
MQTT_PASSWORD = ''
MQTT_KEEPALIVE = 5
MQTT_TLS_ENABLED = False
MQTT_CLEAN_SESSION = True




# 找不到環境變數的話 請注意是否已經設定  set FLASKR_SETTINGS=C:\code\webtk\flaskproject\flaskdoorcontrol--beta3\app\setting.py