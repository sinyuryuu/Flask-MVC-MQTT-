
from app import app,db
import glob
##############匯入資料庫model########################

from app.model.user import user

###################################################
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

#這裡會匯入 flask login 功能必要模組
#匯入 app 跟 db 變數

#users = {'bob': {'password': '123'},'zzz':{'password':'zzz'}}   #多層字典 key對應value
#users = {'bob': '123','zzz': '999'}  #字典 key對應value

g =[]
alluser =[]
allpwd =[]





# 取得帳號密碼函式只要有呼叫該函式就會刷新字典
def getupwd():
    
    global newus     #定義全域變數
    alluser.clear()  #清空帳號串列
    allpwd.clear()   #清空密碼串列


    #迴圈將所有指定資料表全部輸出    
    for u in user.query.all():
        #gw = f"{u.username} : {'password'} : {u.password}"  #取得user資料表特定資料
        key_user = f"{u.username}"                           #取得目前資料庫最新的帳號串列
        key_password = f"{u.password}"                       #取得目前資料庫最新的密碼串列
        #g.append(gw)
        alluser.append(key_user)                             #每筆帳號加入key_user串列
        #alluser.append(key_password)
        allpwd.append(key_password)                          #每筆密碼加入key_password串列
        #print (gw)
        #print(alluser)
        db.session.commit()                                  #更新資料庫

    
    newus = dict(zip(alluser, allpwd))   #將key_user 與 key_password list轉換成字典

getupwd()      #初次呼叫(更新)
users =newus   #承接字典
#print(users)  #print users目前資料




""" 
table = user.query.all()
for row in table:

    row_as_dict = {column: str(getattr(row, column)) for column in row.__table__.c.keys()}
    users.update(row_as_dict)

    print(row_as_dict)
print(users)
 """


app.secret_key = 'dd06be55a06c03312b2ab109b5f8f6ab'
#secret_key = 'dd06be55a06c03312b2ab109b5f8f6ab'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請登入後再操作!'


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(user_id):
    getupwd()
    users = newus
    if user_id not in users:
        return

    user = User()
    user.id = user_id
    return user


@login_manager.request_loader
def request_loader(request):
    getupwd()
    users = newus
    user_id = request.form.get('user_id')
    if user_id not in users:
        return

    user = User()
    user.id = user_id

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[user_id]

    

    return user
myname =''
from flask import request, render_template, url_for, redirect, flash
@app.route('/login', methods=['GET', 'POST'])



def login(): 
    getupwd()                #取得目前最新帳密字典
    users = newus
    #print('1之前',users)
    #print('2之前',newus)
    
    
    if request.method == 'GET':
        return render_template("login.html")
    
    
    user_id = request.form['user_id']
    user_pwd = request.form['password']
    if (user_id in users) and (user_pwd in users[user_id]):  #找目前輸入id 的 pwd

        

        

        user = User()
        user.id = user_id
        user.pwd = user_pwd
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
