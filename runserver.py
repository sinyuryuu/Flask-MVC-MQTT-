from app import app
from app import socketio
from app import migrate   #應該是可以不用匯入
from app import mqtt      #應該是可以不用匯入


socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True, debug=True) #立刻啟動伺服器 區域網路能連線


#app.run(host='0.0.0.0', port=5000,debug=True) #立刻啟動伺服器 區域網路能連線