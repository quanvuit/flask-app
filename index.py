from flask import Flask,render_template,request,redirect,session
import psycopg2
from db import connection,cursor
import os
import json
#import request

app = Flask(__name__)
app.secret_key = "abc"

@app.route('/')
def index():
    if "username" in session:
        #sql = "select * from sinhvien"

        # Executing a SQL query
        #cursor.execute(sql)
        # Fetch result
        #record = cursor.fetchall()

        #s = "<h1 style='color:red'>Xin chào</h1>"
        
        return render_template("index.html",us=session["username"])
    else: 
        return redirect("/login")
#-------------------------------------khách sạn-----------------------------------------------------
@app.route('/hotel')
def hotel():
    if "username" in session:
        sql = "select id_hotel,name,image,phone,acreage,area,address,hotel,money,published from hotel ORDER BY id_hotel ASC"
        #sql = "select * from hotel ORDER BY id_hotel ASC"

        # Executing a SQL query
        cursor.execute(sql)
        # Fetch result
        record = cursor.fetchall()

        #s = "<h1 style='color:red'>Xin chào</h1>"

        return render_template("hotel.html",r=record,us=session["username"])
    else:
        return redirect("/login")
    

@app.route("/insert")
def insert():
    return render_template("insert.html")

@app.route("/search_hotel",methods=["POST"])
def search_hotel():
    # print("1")
    # where_area = ""
    # where_key = ""
    # area = request.form.get("area")

    #print(area)
    # if(area):
    #     where_area = f"and area like '%{area}%'"
    # else:
    #     where_area = ""

    #print(where_area)


    key = request.form.get("key")
    # if(key):
    #     where_key = f"and name = '%{key}%'"
    # else:
    #     where_key = ""


    sql = f"select id_hotel,name,image,phone,acreage,area,address,hotel,money,published from hotel where (published = 1 or published = 0) and (name LIKE '%{key}%' or area LIKE '%{key}%') ORDER BY id_hotel ASC"

    # Executing a SQL query
    cursor.execute(sql)

    record = cursor.fetchall()

    #fetchall : lay tat ca

    connection.commit()

    return render_template("search_hotel.html",r=record,k=key)

@app.route("/themmoi",methods=["POST"])
def themmoi():
    
    name = request.form.get("name")
    phone = request.form.get("phone")
    money = request.form.get("money")
    acreage = request.form.get("acreage")
    area = request.form.get("area")
    address_hotel = request.form.get("address_hotel")
    hotel = request.form.get("hotel")
    img = ""
    published = 1
    for uploaded_file in request.files.getlist("file"):
        if uploaded_file.filename != "":
            img = uploaded_file.filename
            print(uploaded_file.filename)
            uploaded_file.save(os.path.join("static/images", uploaded_file.filename))


    content = request.form.get("content")

    #sql = "insert into hotel(name,phone,money,image,acreage,area,address,hotel,content) values('"+name+"',"+phone+",'"+money+"','../static/images/"+img+"','"+acreage+"','"+area+"','"+address_hotel+"','"+hotel+"','"+content+"')"

    sql = f"insert into hotel(name,phone,money,image,acreage,area,address,hotel,content,published) values('{name}','{phone}','{money}','../static/images/{img}','{acreage}','{area}','{address_hotel}','{hotel}','{content}','{published}')"

    # Executing a SQL query
    cursor.execute(sql)
    
    connection.commit()

    return redirect("/hotel")

@app.route("/delete/<id>")
def delete(id):
    i = {id}
    sql = "delete from hotel where id_hotel = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/hotel")

@app.route("/update/<id>")
def update(id):
    i = {id}
    sql = "select * from hotel where id_hotel = " + id

    cursor.execute(sql)
    # Fetch result
    record = cursor.fetchone()

    #fetchone: chir lay 1

    return render_template("update.html",r=record)
    # Executing a SQL query

@app.route("/update_hotel",methods=["POST"])
def update_hotel():
    id_hotel = request.form.get("id_hotel")
    name = request.form.get("name")
    phone = request.form.get("phone")
    money = request.form.get("money")
    acreage = request.form.get("acreage")
    area = request.form.get("area")
    address_hotel = request.form.get("address_hotel")
    hotel = request.form.get("hotel")
    img = request.form.get("img")
    img = ""
    published = 1
    for uploaded_file in request.files.getlist("file"):
        if uploaded_file.filename != "":
            img = uploaded_file.filename
            print(uploaded_file.filename)
            uploaded_file.save(os.path.join("static/images", uploaded_file.filename))

    content = request.form.get("content")

    #sql = "insert into hotel(name,phone,money,image,acreage,area,address,hotel,content) values('"+name+"',"+phone+",'"+money+"','../static/images/"+img+"','"+acreage+"','"+area+"','"+address_hotel+"','"+hotel+"','"+content+"')"

    #sql = f"insert into hotel(name,phone,money,image,acreage,area,address,hotel,content) values('{name}','{phone}','{money}','../static/images/{img}','{acreage}','{area}','{address_hotel}','{hotel}','{content}')"
    sql = f"Update hotel set name = '{name}',phone = {phone},image = '../static/images/{img}',address = '{address_hotel}',hotel = '{hotel}',money = {money},acreage = '{acreage}',area = '{area}',content = '{content}' where id_hotel = {id_hotel}"
    # Executing a SQL query
    cursor.execute(sql)

    connection.commit()

    return redirect("/hotel")

@app.route("/pls_hotel/<id>")
def pls_hotel(id):
    i = {id}
    sql = "Update hotel set published = 1 where id_hotel = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/hotel")

@app.route("/unpls_hotel/<id>")
def unpls_hotel(id):
    i = {id}
    sql = "Update hotel set published = 0 where id_hotel = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/hotel")

#------------------------------------------------------------Login-------------------------------------------------------------------
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_dn",methods=["POST"])
def login_dn():
    us = request.form.get("us")
    pa = request.form.get("pa")

    sql = f"select * from user_member where user_name = '{us}' and pass='{pa}'"
    #sql = f"select * from user_member where user_name = '{us}' and pass='{pa}'"
    cursor.execute(sql)
    # Fetch result
    record = cursor.fetchall()
    if(len(record)==1):
        session["username"] = us
        return redirect("/")
    else:
        return render_template("login.html")
#-----------------------------------------------------register-------------------------------------------------------
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    #session.pop('user_name', None)
    #session.delete()
    #request.session['user_name'] = ''
    return redirect('/login')
    
@app.route("/add_register",methods=["POST"])
def add_register():
    us = request.form.get("us")
    phone = request.form.get("phone")
    email = request.form.get("email")
    pa = request.form.get("pa")
    published = 0
    sql = f"insert into user_member(user_name,email,pass,phone,published) values('{us}','{email}','{pa}','{phone}','{published}')"
    #sql = "insert into user_member(user_name,email,pass) values('"+us+"','"+email+"','"+pa+"')"

    # sql = "insert into sinhvien(ten_sv,email,dia_chi) values(N'"+us+"','"+email+"',N'"+pa+"')"
    # Executing a SQL query
    cursor.execute(sql)
    
    connection.commit()

    return redirect("/login")


#-------------------------------------Tin tức-----------------------------------------------------
@app.route('/news')
def news():
    if "username" in session:
        sql = "select * from news ORDER BY id_news ASC"

        # Executing a SQL query
        cursor.execute(sql)
        # Fetch result
        record = cursor.fetchall()

        #s = "<h1 style='color:red'>Xin chào</h1>"

        return render_template("news.html",r=record,us=session["username"])
    else:
        return redirect("/login")

@app.route("/insert_news")
def insert_news():
    return render_template("insert_news.html")

@app.route("/themmoi_news",methods=["POST"])
def themmoi_news():
    name = request.form.get("name")
    date = request.form.get("date")
    tomtat = request.form.get("tomtat")

    img = ""
    published = 1
    for uploaded_file in request.files.getlist("file"):
        if uploaded_file.filename != "":
            img = uploaded_file.filename
            print(uploaded_file.filename)
            uploaded_file.save(os.path.join("static/images", uploaded_file.filename))


    content = request.form.get("content")

    #sql = "insert into hotel(name,phone,money,image,acreage,area,address,hotel,content) values('"+name+"',"+phone+",'"+money+"','../static/images/"+img+"','"+acreage+"','"+area+"','"+address_hotel+"','"+hotel+"','"+content+"')"

    sql = f"insert into news(title,time,image,content,published,tomtat) values('{name}','{date}','../static/images/{img}','{content}','{published}','{tomtat}')"

    # Executing a SQL query
    cursor.execute(sql)

    connection.commit()

    return redirect("/news")

@app.route("/delete_news/<id>")
def delete_news(id):
    i = {id}
    sql = "delete from news where id_news = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/news")

@app.route("/update_news/<id>")
def update_news(id):
    i = {id}
    sql = "select * from news where id_news = " + id

    cursor.execute(sql)
    # Fetch result
    record = cursor.fetchone()

    return render_template("update_news.html",r=record)

@app.route("/save_news",methods=["POST"])
def save_news():
    id_news = request.form.get("id_news")
    name = request.form.get("name")
    date = request.form.get("date")
    tomtat = request.form.get("tomtat")

    img = ""

    for uploaded_file in request.files.getlist("file"):
        if uploaded_file.filename != "":
            img = uploaded_file.filename
            print(uploaded_file.filename)
            uploaded_file.save(os.path.join("static/images", uploaded_file.filename))

    content = request.form.get("content")

    #sql = "insert into hotel(name,phone,money,image,acreage,area,address,hotel,content) values('"+name+"',"+phone+",'"+money+"','../static/images/"+img+"','"+acreage+"','"+area+"','"+address_hotel+"','"+hotel+"','"+content+"')"

    #sql = f"insert into hotel(name,phone,money,image,acreage,area,address,hotel,content) values('{name}','{phone}','{money}','../static/images/{img}','{acreage}','{area}','{address_hotel}','{hotel}','{content}')"
    sql = f"Update news set title = '{name}',time = '{date}',tomtat = '{tomtat}',image = '../static/images/{img}',content = '{content}' where id_news = {id_news}"
    # Executing a SQL query
    cursor.execute(sql)

    connection.commit()

    return redirect("/news")

@app.route("/pls_news/<id>")
def pls_news(id):
    i = {id}
    sql = "Update news set published = 1 where id_news = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/news")

@app.route("/unpls_news/<id>")
def unpls_news(id):
    i = {id}
    sql = "Update news set published = 0 where id_news = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/news")

#----------------------------------------------------recruitment--------------------------------------------------------

@app.route('/recruitment')
def recruitment():
    if "username" in session:
        sql = "select * from recruitment ORDER BY id_re ASC"

        # Executing a SQL query
        cursor.execute(sql)
        # Fetch result
        record = cursor.fetchall()

        #s = "<h1 style='color:red'>Xin chào</h1>"

        return render_template("recruitment.html",r=record,us=session["username"])
    else:
        return redirect("/login")

@app.route("/insert_recruitment")
def insert_recruitment():

    sql = "select * from hotel ORDER BY id_hotel ASC"
    # Executing a SQL query
    cursor.execute(sql)
    # Fetch result
    record = cursor.fetchall()
    return render_template("insert_recruitment.html",r=record)

@app.route("/themmoi_recruitment",methods=["POST"])
def themmoi_recruitment():
    name = request.form.get("name")
    date = request.form.get("date")
    hotel = request.form.get("hotel")
    img = ""
    published = 1

    sql_hotel = "select id_hotel,name from hotel where id_hotel = " + hotel

    cursor.execute(sql_hotel)
    # Fetch result
    record_hotel = cursor.fetchone()

    name_hotel = record_hotel[1]


    content = request.form.get("content")

    #sql = "insert into hotel(name,phone,money,image,acreage,area,address,hotel,content) values('"+name+"',"+phone+",'"+money+"','../static/images/"+img+"','"+acreage+"','"+area+"','"+address_hotel+"','"+hotel+"','"+content+"')"

    sql = f"insert into recruitment(title,date,content,published,id_hotel,name_hotel) values('{name}','{date}','{content}','{published}','{hotel}','{name_hotel}')"

    # Executing a SQL query
    cursor.execute(sql)

    connection.commit()

    return redirect("/recruitment")

@app.route("/delete_recruitment/<id>")
def delete_recruitment(id):
    i = {id}
    sql = "delete from recruitment where id_re = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/recruitment")

@app.route("/update_recruitment/<id>")
def update_recruitment(id):
    i = {id}
    sql = "select * from recruitment where id_re = " + id

    cursor.execute(sql)
    # Fetch result
    record = cursor.fetchone()

    sql_hotel = "select * from hotel ORDER BY id_hotel ASC"
    # Executing a SQL query
    cursor.execute(sql_hotel)
    # Fetch result
    record_hotel = cursor.fetchall()

    return render_template("update_recruitment.html",r=record,list=record_hotel)

@app.route("/save_recruitment",methods=["POST"])
def save_recruitment():
    id_re = request.form.get("id_re")
    name = request.form.get("name")
    date = request.form.get("date")
    hotel = request.form.get("hotel")
    sql_hotel = "select id_hotel,name from hotel where id_hotel = " + hotel

    cursor.execute(sql_hotel)
    # Fetch result
    record_hotel = cursor.fetchone()

    name_hotel = record_hotel[1]



    content = request.form.get("content")

    #sql = "insert into hotel(name,phone,money,image,acreage,area,address,hotel,content) values('"+name+"',"+phone+",'"+money+"','../static/images/"+img+"','"+acreage+"','"+area+"','"+address_hotel+"','"+hotel+"','"+content+"')"

    #sql = f"insert into hotel(name,phone,money,image,acreage,area,address,hotel,content) values('{name}','{phone}','{money}','../static/images/{img}','{acreage}','{area}','{address_hotel}','{hotel}','{content}')"
    sql = f"Update recruitment set title = '{name}',date = '{date}',id_hotel= {hotel},name_hotel = '{name_hotel}',content = '{content}' where id_re = {id_re}"
    # Executing a SQL query
    cursor.execute(sql)

    connection.commit()

    return redirect("/recruitment")

@app.route("/pls_recruitment/<id>")
def pls_recruitment(id):
    i = {id}
    sql = "Update recruitment set published = 1 where id_re = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/recruitment")

@app.route("/unpls_recruitment/<id>")
def unpls_recruitment(id):
    i = {id}
    sql = "Update recruitment set published = 0 where id_re = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/recruitment")

#----------------------------------------Đơn hàng--------------------------------------------

@app.route('/donhang')
def donhang():
    if "username" in session:
        sql = "select * from order_hotel ORDER BY id_order ASC"
        # Executing a SQL query
        cursor.execute(sql)
        # Fetch result
        record = cursor.fetchall()

        #s = "<h1 style='color:red'>Xin chào</h1>"

        return render_template("donhang.html",r=record,us=session["username"])
    else:
        return redirect("/login")


#----------------------------------------User----------------------------------------------------------

@app.route('/user')
def user():
    if "username" in session:
        sql = "select * from user_member ORDER BY id_user ASC"
        # Executing a SQL query
        cursor.execute(sql)
        # Fetch result
        record = cursor.fetchall()

        #s = "<h1 style='color:red'>Xin chào</h1>"

        return render_template("user.html",r=record,us=session["username"])
    else:
        return redirect("/login")

@app.route("/pls_order/<id>")
def pls_order(id):
    i = {id}
    sql = "Update user_member set published = 1 where id_user = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/user")

@app.route("/unpls_order/<id>")
def unpls_order(id):
    i = {id}
    sql = "Update user_member set published = 0 where id_user = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/user")

@app.route("/delete_order/<id>")
def delete_order(id):
    i = {id}
    sql = "delete from user_member where id_user = " + id

    # Executing a SQL query
    cursor.execute(sql)
    connection.commit()
    return redirect("/user")

#------------------------------------------------Trang chủ ---------------------------------------------

@app.route('/home')
def home():
    if "username" in session:
        sql = "select * from hotel where published = 1 ORDER BY id_hotel ASC LIMIT 3"
        cursor.execute(sql)
        record = cursor.fetchall()

        sql_news = "select title,published,time,image,tomtat,id_news from news where published = 1 ORDER BY id_news ASC LIMIT 4"
        cursor.execute(sql_news)
        record_news = cursor.fetchall()

        #s = "<h1 style='color:red'>Xin chào</h1>"

        return render_template("home.html",r=record,list_news=record_news,us=session["username"])
    else:
        return redirect("/login")

#------------------------------------------------khách sạn------------------------------------------

@app.route('/khach-san')
def khachsan():
    if "username" in session:
        sql = "select * from hotel where published = 1 ORDER BY id_hotel DESC"
        cursor.execute(sql)
        record = cursor.fetchall()

        return render_template("khach-san.html",r=record,us=session["username"])
    else:
        return redirect("/login")

@app.route("/tim-kiem-khach-san",methods=["POST"])
def timkiemks():

    key = request.form.get("key")

    sql = f"select * from hotel where published = 1 and (name LIKE '%{key}%' or area LIKE '%{key}%') ORDER BY id_hotel ASC"

    cursor.execute(sql)

    record = cursor.fetchall()

    connection.commit()

    return render_template("search_ks.html",r=record,k=key)

@app.route("/chitietkhachsan/<id>")
def chitietkhachsan(id):
    i = {id}
    sql = "select * from hotel where id_hotel = " + id

    cursor.execute(sql)
    # Fetch result
    record = cursor.fetchone()

    return render_template("chitietkhachsan.html",r=record)

@app.route("/order",methods=["POST"])
def order():
    id_hotel = request.form.get("id")
    title = request.form.get("title")
    name = request.form.get("name")
    phone = request.form.get("phone")
    date = request.form.get("date")
    note = request.form.get("note")



    #sql = "insert into hotel(name,phone,money,image,acreage,area,address,hotel,content) values('"+name+"',"+phone+",'"+money+"','../static/images/"+img+"','"+acreage+"','"+area+"','"+address_hotel+"','"+hotel+"','"+content+"')"

    sql = f"insert into order_hotel(id_hotel,title,name,phone,date,note) values('{id_hotel}','{title}','{name}','{phone}','{date}','{note}')"

    # Executing a SQL query
    cursor.execute(sql)

    connection.commit()

    return redirect("/khach-san")



#----------------------------------------Tin tức--------------------------------------------

@app.route('/tin-tuc')
def tintuc():
    if "username" in session:
        sql = "select * from news where published = 1 ORDER BY id_news ASC"
        cursor.execute(sql)
        record = cursor.fetchall()

        return render_template("tintuc.html",list_news=record,us=session["username"])
    else:
        return redirect("/login")


@app.route("/chitiettintuc/<id>")
def chitiettintuc(id):

    sql = "select * from news where id_news = " + id

    cursor.execute(sql)
    # Fetch result
    record = cursor.fetchone()

    sql_news = "select title,published,time,image,tomtat,id_news from news where published = 1 and not id_news = " + id + "ORDER BY id_news ASC LIMIT 2"
    cursor.execute(sql_news)
    record_news = cursor.fetchall()

    return render_template("chitiettintuc.html",r=record,list=record_news)

#----------------------------------------Bản đồ--------------------------------------------

@app.route('/ban-do')
def bando():
    if "username" in session:
        #cur = conn.cursor()
        sql = "SELECT nane,ST_AsGeoJSON(geom) from map"
        cursor.execute(sql)
        version = cursor.fetchall()
        geo_json = []
        for row in version:
            geo_json.append({
                    "type": "Feature",
                    "name": row[0],
                    "properties": {"Tên":row[0]}, #Thông tin thuộc tính khi ấn popup sẽ hiện thị
                    "geometry":json.loads(row[1]) # type: là kiểu  coor: là tọa độ
            })

        return render_template("json.html",data=json.dumps(geo_json))
    else:
        return redirect("/login")

#----------------------------------------Tuyển dụng--------------------------------------------

@app.route('/tuyen-dung')
def tuyendung():
    if "username" in session:
        sql = "select * from recruitment where published = 1 ORDER BY id_re ASC"
        cursor.execute(sql)
        record = cursor.fetchall()

        return render_template("tuyendung.html",r=record,us=session["username"])
    else:
        return redirect("/login")

@app.route("/chitiettuyendung/<id>")
def chitiettuyendung(id):

    sql = "select * from recruitment where id_re = " + id

    cursor.execute(sql)
    # Fetch result
    record = cursor.fetchone()

    return render_template("chitiettuyendung.html",r=record)

#----------------------------------------Giới thiệu--------------------------------------------

@app.route('/gioi-thieu')
def about():
    if "username" in session:


        return render_template("about.html",us=session["username"])
    else:
        return redirect("/login")


#f có nghĩa là:  Các biểu thức được trích xuất từ ​​chuỗi được đánh giá trong ngữ cảnh xuất hiện chuỗi f.
# Điều này có nghĩa là biểu thức có toàn quyền truy cập vào các biến cục bộ và toàn cầu.
# Bất kỳ biểu thức hợp lệ Python đều có thể được sử dụng, bao gồm các lệnh gọi hàm và phương thức.