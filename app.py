from flask import Flask,render_template,request,url_for,redirect,session
import requests
import sqlite3 as sql

app=Flask(__name__)

app.secret_key="key"

url="https://api.mfapi.in/mf/"

@app.route('/',methods=["POST","GET"])
def home():
    if "ID" in session:
     conn=sql.connect("finance.db")
     conn.row_factory=sql.Row
     cur=conn.cursor()
     cur.execute("Select * from finance_details where ID=?",(session["ID"],))
     data=cur.fetchall()   
     return render_template("home.html",data=data)
    return redirect(url_for("login"))

@app.route("/add",methods=["GET","POST"])
def add_user():
    if request.method=="POST":
     Name=request.form.get("Name")
     Fund_Code=request.form.get("Fund_Code")
     Invested_Amount=request.form.get("Invested_Amount")
     Unit_Held=request.form.get("Unit_Held")
     req=requests.get(url+Fund_Code)
     data=req.json()
     Fund_house=data["meta"]["fund_house"]
     nav=data["data"][0]["nav"]
     current_value=float(nav)*int(Invested_Amount)
     growth=float(current_value)-int(Unit_Held)
     conn=sql.connect("finance.db")
     cur=conn.cursor()
     cur.execute("Insert into finance_details(NAME,FUND_CODE,INVESTED_AMOUNT,UNIT_HELD,FUND_HOUSE,NAV,GROWTH,CURRENT_VALUE) values(?,?,?,?,?,?,?,?)",
         (Name,Fund_Code,Invested_Amount,Unit_Held,Fund_house,nav,growth,current_value)) 
     conn.commit() 
     return redirect(url_for("home"))
    return render_template("add_user.html")

@app.route("/edit/<string:id>",methods=["POST","GET"])
def edit(id):
       if request.method=="POST":
        Name=request.form.get("Name")
        Fund_Code=request.form.get("Fund_Code")
        Invested_Amount=request.form.get("Invested_Amount")
        Unit_Held=request.form.get("Unit_Held")
        req=requests.get(url+Fund_Code)
        data=req.json()
        Fund_house=data["meta"]["fund_house"]
        nav=data["data"][0]["nav"]
        current_value=float(nav)*int(Invested_Amount)
        growth=float(current_value)-int(Unit_Held)
        conn=sql.connect("finance.db")
        cur=conn.cursor()
        cur.execute("Update finance_details set Name=?, Fund_Code=?,Invested_Amount=?,Unit_Held=?,Fund_house=?,nav=?,growth=?,current_value=? where ID=?",
                (Name,Fund_Code,Invested_Amount,Unit_Held,Fund_house,nav,growth,current_value,id)) 
        conn.commit() 
        return redirect(url_for("home"))

       conn=sql.connect("finance.db")
       conn.row_factory=sql.Row
       cur=conn.cursor()
       cur.execute("Select * from finance_details where ID=?",(id,))
       data=cur.fetchone()   
       return render_template("edit.html",datum=data)  

@app.route("/delete/<string:id>",methods=["GET","POST"])
def delete(id):
      conn=sql.connect("finance.db")
      cur=conn.cursor()
      cur.execute("Delete from finance_details where ID=?",(id,))
      conn.commit()
      return redirect(url_for("home"))

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        Name=request.form.get("Name")
        Password=request.form.get("Password")
        conn=sql.connect("finance.db")
        conn.row_factory=sql.Row
        cur=conn.cursor()
        cur.execute("select * from login_table")
        data=cur.fetchall()
        for i in data:
         if str(i["Name"])==Name and str(i["Password"])==Password:
            session["ID"]=Password
            return redirect(url_for('home'))          
    return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.pop("Name",None)
    return redirect(url_for("login"))

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":
       Name=request.form.get("Name")
       Password=request.form.get("Password")
       conn=sql.connect("finance.db")
       conn.row_factory=sql.Row
       cur=conn.cursor()
       cur.execute("insert into login_table (Name,Password) values(?,?)",(Name,Password))
       conn.commit() 
       return redirect(url_for("home"))
    return render_template("signup.html")

if __name__=="__main__":
    app.run(debug=True)



