from flask import Flask,jsonify, request
from flask_cors import CORS
from pathlib import Path
from pathlib import Path
import pickledb
import sqlite3, json, os

# アプリ
app = Flask(__name__)
CORS(app)

#画像保存位置
base_dir = Path(__file__).parent
UPLOAD_FOLDER = str(Path(base_dir, "image"))

# データベース pickledb
# アプリDBと設定
app_data = pickledb.load('app.db', False)
if not app_data.get("login_user"):
    app_data.set("login_user", "")
    app_data.set("post_id", 0)
    app_data.set("comment_id", 0)
    app_data.set("image_temp", "")
app_data.dump()

###################################################################

# データベース　sqlite3
data = sqlite3.connect('DATA')
data_cursor = data.cursor()

# アカウント情報DBとチェック
data_cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE = 'table' AND name = 'account'")#存在チェック
row = data_cursor.fetchone()
if row[0] != 1:
    data_cursor.execute("CREATE TABLE account(user_id text, password text, account_picture text, account_name text)")


# 投稿内容DBとチェック
data_cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE = 'table' AND name = 'post'")#存在チェック
row = data_cursor.fetchone()
if row[0] != 1:
    data_cursor.execute("CREATE TABLE post(post_id int, post_content text, post_picture text, account_name text)")


# コメントDBとチェック
data_cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE = 'table' AND name = 'comment'")#存在チェック
row = data_cursor.fetchone()
if row[0] != 1:
    data_cursor.execute("CREATE TABLE comment(comment_id int, post_id int, comment_content text, account_name text)")


# いいねDBとチェック
data_cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE = 'table' AND name = 'like'") #存在チェック
row = data_cursor.fetchone()
if row[0] != 1:
    data_cursor.execute("CREATE TABLE like(post_id int, account_name text)")

# データベースをコミットし、閉じる
data.commit()
data.close()

###################################################################

# URL「/」に対応して処理する関数
@app.route("/")
def index():
    # 戻り値がそのままWebサイトに表示される。
    return jsonify({"result":"This is Backend API Server!"})

# 画像アップロード
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['picture']

    # 画像名変更
    extension = file.filename.split('.')
    file.filename = "temp." + extension[1]
    app_data.set("image_temp", file.filename)

    # 画像を一時的に保存
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"picture" : file.filename})

# 新規登録
@app.route("/signup/<user_id>/<password>/<account_picture>/<user_name>")
def signup(user_id, password, account_picture, user_name):
    data = sqlite3.connect('DATA') #データベースに接続
    data_cursor = data.cursor()

    # アカウントが存在しているかどうかをチェック account(user_id text, password text, account_picture text, account_name text)
    boolean = True
    sql = "SELECT count(*) FROM account WHERE user_id = '" + user_id + "' OR account_name = '" + user_name + "'"
    data_cursor.execute(sql)
    result = data_cursor.fetchall()
    if result[0][0]:
        return jsonify({"result":"failure"})
    
    # 新規登録
    sql = "INSERT INTO account VALUES('" + user_id + "', '" + password + "', '" + account_picture + "', '" + user_name + "')" # SQLコマンド
    data.execute(sql) # SQL実行
    data.commit()

    # TEST account(user_id text, password text, account_picture text, account_name text)
    data_json = []
    for row in data.execute("SELECT * FROM account"):
        temp = {"user_id":row[0], "password":row[1], "account_picture":row[2], "account_name":row[3]}
        data_json.append(temp)

    data.close() #データベースを閉じる
    return jsonify(data_json)

# ログイン
@app.route("/login/<user_id>/<password>")
def login(user_id, password):
    data = sqlite3.connect('DATA') #データベースに接続
    PASS = ""
    USER = ""
    # パスワード取得 account(user_id text, password text, account_picture text, account_name text)
    for row in data.execute("SELECT * FROM account WHERE user_id = '" + user_id + "'"):
        PASS = row[1]
        USER = row[0]
    
    if password == PASS:
        app_data.set("login_user", str(USER)) # ログインしているものをアプリに登録
        app_data.dump()
        return jsonify({"login_user":app_data.get("login_user"), "result":"true", "password": password})
    
    # test ############################ 無効化
    app_data.set("login_user", "")
    app_data.dump()

    data.close() #データベースを閉じる
    return jsonify({"login_user":app_data.get("login_user"), "result":"false", "password":password})

# ログアウト
@app.route("/logout")
def logout():
    app_data.set("login_user", "")
    app_data.dump()
    return jsonify({"login_user":app_data.get("login_user")})

# アカウント情報取得
def account_info(user_id):
    data = sqlite3.connect('DATA') #データベースに接続
    data_cursor = data.cursor()

    account_data = {}
    sql = "SELECT count(*) FROM account WHERE user_id = '" + user_id + "'"
    data_cursor.execute(sql)
    result = data_cursor.fetchall()
    # ユーザ数が１以上なら、情報取得 account(user_id text, password text, account_picture text, account_name text)
    if result[0][0]: 
        for row in data.execute("SELECT * FROM account WHERE user_id = '" + user_id + "'"):
            account_data["user_id"] = row[0]
            account_data["account_picture"] = row[2]
            account_data["account_name"] = row[3]

    data.close() #データベースを閉じる
    return account_data

# ログインしている情報を習得 Json
@app.route("/login_info")
def login_info():
    user_id = app_data.get("login_user")
    return jsonify(account_info(user_id))

# メニュー画面の投稿内容を取得
# <全ての投稿を取得する>
# 引数:なし
# 返り値:これまでの投稿全て(?)のリスト
#       ->  ok投稿したユーザーの名前
#           ok投稿したユーザーのプロフィール画像のパス
#           ok投稿id
#           ok投稿文章
#           ok投稿画像のパス
#           ok投稿についたいいねの数
@app.route("/all_post")
def post_content():
    data = sqlite3.connect('DATA') #データベースに接続
    data_cursor = data.cursor()
    json_data = []

    # 投稿内容取得 post(post_id int, post_content text, post_picture text, account_name text)
    for row in data.execute("SELECT * FROM post"):
        # 投稿id, 投稿文章, 投稿画像のパス, 投稿したユーザーの名前
        temp = {"post_id":row[0], "post_content":row[1], "post_picture":row[2], "account_name":row[3]}

        # プロフィール画像のパス
        for row_2 in data.execute("SELECT * FROM account WHERE account_name = '" + row[3] + "'"):
            #account(user_id text, password text, account_picture text, account_name text)
            temp["account_picture"] = row_2[2]

        # 投稿についたいいねの数 like(post_id int, account_name text)
        data_cursor.execute("SELECT count(*) FROM like WHERE post_id = " + str(row[0]))
        result = data_cursor.fetchall()
        temp["like_number"] = result[0][0]

        json_data.append(temp)

    data.close() #データベースを閉じる
    return jsonify(json_data)

# 投稿
@app.route("/post/<content>/<post_picture>")
def post(content, post_picture):
    data = sqlite3.connect('DATA') #データベースに接続

    user_id = app_data.get("login_user")
    account = account_info(user_id)
    # 投稿ID取得と新たな設定
    post_id = app_data.get("post_id") + 1
    app_data.set("post_id", post_id)
    app_data.dump()

    # 投稿写真処理
    if post_picture != "null":
        file_name = app_data.get("image_temp") # 一時保存したファイル名を取得
        extension = file_name.split(".") # ファイルの拡張子
        # 投稿に合わせて画像ファイル名を変更
        file_name = str(post_id) + extension[1] 
        new_name = str(Path(base_dir, file_name)) 
        os.rename(post_picture, new_name)
        # 一時保存した画像情報を削除
        app_data.set("image_temp", "")
        app_data.dump()
    
    # 投稿登録 post(post_id int, post_content text, post_picture text, account_name text)
    sql = "INSERT INTO post VALUES(" + str(post_id) + ", '" + content + "', '" + new_name + "', '" + account["account_name"] + "')"
    data.execute(sql)
    data.commit()

    data.close() #データベースを閉じる
    return post_content()

# 投稿内容取得
@app.route("/post1/<post_id>")
def take_post(post_id):
    data = sqlite3.connect('DATA') #データベースに接続

    # post(post_id int, post_content text, post_picture text, account_name text)
    post_data = {}
    sql = "SELECT * FROM post WHERE post_id = " + str(post_id)
    for row in data.execute(sql):
        post_data["post_id"] = row[0]
        post_data["post_content"] = row[1]
        post_data["post_picture"] = row[2]
        post_data["account_name"] = row[3]
        # プロフィール写真
        account = account_info(app_data.get("login_user"))
        post_data["account_picture"] = account["account_picture"]
    
    # コメント情報取得 comment(comment_id int, post_id int, comment_content text, account_name text)
    comment_data = []
    sql = "SELECT * FROM comment WHERE post_id = " + str(post_id)
    for row in data.execute(sql):
        # プロフィール写真を取得
        sql = "SELECT * FROM account WHERE account_name = '" + row[3] + "'"
        account_picture = ""
        for row_2 in data.execute(sql): # account(user_id text, password text, account_picture text, account_name text)
            account_picture = row_2[2]
        temp = {"comment_id":row[0], "comment_content":row[2], "account_name":row[3], "account_picture":account_picture}
        comment_data.append(temp)
    
    # いいね情報取得 like(post_id int, account_name text)
    like_data = []
    sql = "SELECT * FROM like WHERE post_id = " + str(post_id)
    for row in data.execute(sql):
        temp = {"account_name" : row[1]}
        like_data.append(temp)

    data.close()#データベースを閉じる
    
    return jsonify({"post":post_data, "comment":comment_data, "like":like_data})

# <あるユーザーの投稿を取得する>(ついでに名前とプロフィール画像も)
# 引数:ユーザーid
# 返り値:okそのidのユーザーの名前,
#       okプロフィール画像のパス, 
#       そのユーザーのこれまでの投稿のリスト
#       ->  ok投稿id
#           ok投稿文章
#           ok投稿画像のパス
#           ok投稿についたいいねの数
@app.route("/post2/<user_id>")
def post2(user_id):
    data = sqlite3.connect('DATA') #データベースに接続
    data_cursor = data.cursor()

    # account(user_id text, password text, account_picture text, account_name text)
    json_data = {}
    account = account_info(user_id)
    json_data["account_name"] = account["account_name"]
    json_data["account_picture"] = account["account_picture"]
    # そのユーザーのこれまでの投稿のリスト
    post_data = []
    sql = "SELECT * FROM post WHERE account_name = '" + account["account_name"] + "'"
    for row in data.execute(sql): # post(post_id int, post_content text, post_picture text, account_name text)
        temp = {}
        temp["post_id"] = row[0]
        temp["post_content"] = row[1]
        temp["post_picture"] = row[2]
        # いいね数
        data_cursor.execute("SELECT count(*) FROM like WHERE post_id = " + str(row[0]))
        result = data_cursor.fetchall()
        temp["like_number"] = result[0][0]

        post_data.append(temp)
    
    # 投稿リスト追加
    json_data["post_list"] = post_data

    data.close()#データベースを閉じる
    return jsonify(json_data)


# アカウント情報をすべて取得
@app.route("/account_data")
def account_data():
    data = sqlite3.connect('DATA') #データベースに接続

    json_data = []
    # account(user_id text, password text, account_picture text, account_name text)
    for row in data.execute("SELECT * FROM account"):
        temp = {"user_id":row[0], "password":row[1], "account_picture":row[2], "account_name":row[3]}
        json_data.append(temp)
    data.close() #データベースを閉じる

    return jsonify(json_data)

# コメントDBを取得
@app.route("/comment_data")
def comment_data():
    data = sqlite3.connect('DATA') #データベースに接続

    json_data = []
    # コメント情報をすべて取得 comment(comment_id int, post_id int, comment_content text, account_name text)
    for row in data.execute("SELECT * FROM comment"):
        temp = {"comment_id":row[0], "post_id":row[1], "comment_content":row[2], "account_name":row[3]}
        json_data.append(temp)

    data.close() #データベースを閉じる

    return jsonify(json_data)

# コメント投稿
@app.route("/comment/<post_id>/<content>")
def comment(post_id, content):
    data = sqlite3.connect('DATA') #データベースに接続

    user_id = app_data.get("login_user")
    account = account_info(user_id)
    # コメント投稿ID取得と新たな設定
    comment_id = app_data.get("comment_id") + 1
    app_data.set("comment_id", comment_id)
    app_data.dump()

    # コメント投稿登録 comment(comment_id int, post_id int, comment_content text, account_name text)
    sql = "INSERT INTO comment VALUES (" + str(comment_id) + ", " + str(post_id) + ", '" + content + "', '" + account["account_name"] + "')"
    data.execute(sql)
    data.commit()

    # test ############ 無効化
    json_data = comment_data()

    data.close() #データベースを閉じる
    return json_data

#
# <ある投稿についているコメントを取得する>
# 引数:投稿id
# 返り値: そのidの投稿についているコメントのリスト
#       ->  コメントしたユーザーの名前
#           コメントしたユーザーのプロフィール画像のパス
#           コメント文章
@app.route("/comment/<post_id>")
def take_comment(post_id):
    data = sqlite3.connect('DATA') #データベースに接続
    json_data = []

    # コメント情報取得  comment(comment_id int, post_id int, comment_content text, account_name text)
    sql = "SELECT * FROM comment WHERE post_id = " + str(post_id)
    for row in data.execute(sql):
        temp = {}
        temp["account_name"] = row[3]
        temp["comment_content"] = row[2]
        # account(user_id text, password text, account_picture text, account_name text)
        for row_2 in data.execute("SELECT * FROM account WHERE account_name = '" + row[3] + "'"):
            temp["account_picture"] = row_2[2]
        json_data.append(temp)

    data.close()#データベースを閉じる
    return jsonify(json_data)

# いいねDBを取得
@app.route("/like_data")
def like_data():
    data = sqlite3.connect('DATA') #データベースに接続

    json_data = []
    # いいねの情報をすべて取得 like(post_id int, account_name text)
    for row in data.execute("SELECT * FROM like"):
        temp = {"post_id":row[0], "account_name":row[1]}
        json_data.append(temp)

    data.close() #データベースを閉じる

    return jsonify(json_data) 

# いいね
@app.route("/like/<post_id>")
def like(post_id):
    data = sqlite3.connect('DATA') #データベースに接続
    data_cursor = data.cursor()

    # いいねをしたかどうかをチェック
    user_id = app_data.get("login_user")
    account = account_info(user_id)
    sql = "SELECT count(*) FROM like WHERE post_id = " + str(post_id) + " AND account_name = '" + account["account_name"] + "'"
    data_cursor.execute(sql)
    result = data_cursor.fetchall()
    print("------------------", result[0][0])

    # いいねを登録または削除
    if not result[0][0]: # 登録 like(post_id int, account_name text)
        sql = "INSERT INTO like VALUES(" + str(post_id) + ", '" + account["account_name"] + "')"
    else: #削除
        sql = "DELETE FROM like WHERE post_id = " + str(post_id) + " AND account_name = '" + account["account_name"] + "'"

    data.execute(sql) # SQL実行
    data.commit()

    data.close() #データベースを閉じる

    return like_data()

# ユーザ情報変更
@app.route("/change_info/<info>/<change_text>")
def change_info(info, change_text):
    data = sqlite3.connect('DATA') #データベースに接続
    user_id = app_data.get("login_user")

    # sql コマンド　account(user_id text, password text, account_picture text, account_name text)
    sql = "UPDATE account SET "
    if info == "user_name":
        sql += "account_name = '" + change_text
    if info == "password":
        sql += "password = '" + change_text
    sql += "' WHERE user_id = '" + user_id + "'"
    print(sql)

    data.execute(sql) # SQL実行
    data.commit()

    data.close() #データベースを閉じる
    return account_data()

# プロフィール写真変更
@app.route("/change_profile_picture/<profile_picture>")
def change_profile_picture(profile_picture):
    # ログインしているアカウント情報取得
    user_id = app_data.get("login_user")
    account = account_info(user_id)

    # 前のプロフィール写真を削除 
    os.remove(account["account_picture"])

    # プロフィール写真名変更
    file_name = app_data.get("image_temp") # 一時保存したファイル名を取得
    extension = file_name.split(".") # ファイルの拡張子
    file_name = account["user_id"] + extension[1] 
    new_name = str(Path(base_dir, account["user_id"])) 
    os.rename(profile_picture, new_name)

    # プロフィール写情報更新 account(user_id text, password text, account_picture text, account_name text)
    data = sqlite3.connect('DATA') #データベースに接続
    sql = "UPDATE account set account_picture = '" + new_name + "' WHERE user_id = '" + account["user_id"] + "'"
    data.execute(sql)
    data.close() #データベースを閉じる

    return jsonify({"result" : "success"})


# アカウント削除
@app.route("/delete_account")
def delete_account():
    data = sqlite3.connect('DATA') #データベースに接続 
    user_id = app_data.get("login_user")
    account = account_info(user_id)
    account_name = account["account_name"]

    #アカウントを削除 account(user_id text, password text, account_picture text, account_name text)
    sql = "DELETE FROM account WHERE account_name = '" + account_name +"'"
    data.execute(sql) # SQL実行

    # アカウントに関する情報を削除
    # アカウントに関する画像
    os.remove(account["account_picture"]) # プロフィール写真
    sql = "SELECT * FROM post WHERE account_name = '" + account_name +"'"
    for row in data.execute(sql):
        if row[2] != "null":
            os.remove(row[2]) # 投稿写真
    # コメント
    sql = "DELETE FROM comment WHERE account_name = '" + account_name +"'"
    data.execute(sql)
    # 投稿内容
    sql = "DELETE FROM post WHERE account_name = '" + account_name +"'"
    data.execute(sql)
    # いいね
    sql = "DELETE FROM like WHERE account_name = '" + account_name +"'"
    data.execute(sql)

    data.commit()
    data.close() #データベースを閉じる
    return account_data()

# デバッグ用
ret=[]
for i in range(10):
    ret.append({"id":i, "content":"debug"})
@app.route("/debug_getpost")
def debug_get_post():
    #ret.append({"id":100, "content":"first"})
    #ret.append({"id":200, "content":
    #            "secsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"
    #            })
    for i in range(0):
        ret.append({"id":i, "content":"debug"})
    return jsonify(ret)        # JSON形式で表示する

@app.route("/debug_addpost/<id>/<content>")
def debug_add_post(id,content):
    ret.append({"id":id, "content":content})
    return jsonify(ret)        # JSON形式で表示する

@app.route("/debug_getpost/<id>")
def debug_get_mypost(id):
    ret = []
    #ret.append({"id":100, "content":"first"})
    #ret.append({"id":200, "content":
    #            "secsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"
    #            })
    for i in range(10):
        ret.append({"id":id, "content":"debug"})
    return jsonify(ret)        # JSON形式で表示...

###################################################################
# ここから定型文、触らなくて良い
if __name__ == "__main__":
    app.run(debug=True)
