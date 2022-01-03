from app import db


class token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    linetoken = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, linetoken):
        self.linetoken = linetoken

    def __repr__(self):
        return '<token %r>' % self.linetoken


# 若初次建立完實體(Model)請回到執行檔案的目錄，執行 flask shell 建立資料庫實體模型

# from app import db  #匯入資料庫模組操作  from * ← 這是看你的專案是甚麼名子修改


# db.create_all()     #建立資料庫模型

# 可以透過db指令寫入資料但還是用圖形化介面操作會比較好...

#linetoken = token.query.first()           #回傳token 資料表第一個資料
#linetoken = token.query.get(1)            #回傳token 資料表第一個資料
#linetoken = token.query.get(1).linetoken  #回傳token 資料表 linetoken第一個資料




# 這裡呢是所謂資料庫的實體(Model)，編輯的話可以增加資料表(請執行flask db migrate與flask db upgrade指令)等操作

#第一次使用 設定Migrate時環境變數回到執行檔案的目錄 執行 set FLASK_APP=app.py  或是 MCV(MTV)架構的話 set FLASK_APP=runserver.py

# flask db init  #  初始化資料庫
# flask db migrate -m "這裡可以打字"  #建置新版
# flask db upgrade  #  更新
# flask db downgrade  # 資料庫降版，如果沒有指令就以上版還原
# flask db stamp
# flask db current 顯示當前版本
# flask db history 顯示歷史歷程
# flask db show 顯示當前版本詳細資訊
# flask db merge 合併兩個版本
# flask db heads 顯示目前版本號
# flask db branches 顯示當前分支點

# !!!Flask-Migrate不支援將表格刪除，可以用降版方式移除!!!





