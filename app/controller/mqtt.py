from app import socketio,mqtt

#這裡是mqtt功能必要模組
#匯入 socketio 跟 db 變數


#mqtt 訂閱的頻道
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('esp/test')


#接收mqtt訊息，並解析
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
    print("成功",*bmqtt) 
    return sg


############  取消註解會顯示log  #########################

""" @mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf) """

############  取消註解會顯示log  #########################