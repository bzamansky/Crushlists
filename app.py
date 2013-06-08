import mongo, re
import json
from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key="blah"

@app.route("/",methods = ['GET','POST'])
def home():
    return render_template("home.html",clicked=False)

@app.route("/add",methods=['GET','POST'])
def add():
    if request.method == "POST":

        username = ""
        password = ""
        current = ""
        name = ""
        if 'username' in request.form:
            username = request.form.get("username")
            password = request.form.get("password")
            name = mongo.getName2(username,password)
            session['user'] = name
            crushlist = ""
            if name == 0:
                return render_template("add.html",name=True,crush=False,crushlist="")
            crushl = mongo.getPeopleYouLike2(str(name))
            return render_template("add.html",name=False,crush=True,crushlist=crushl,person=name,current=current)

        elif 'usernamereg' in request.form:
            namereg = request.form.get("namereg")
            usernamereg = request.form.get("usernamereg")
            passwordreg1 = request.form.get("passwordreg1")
            passwordreg2 = request.form.get("passwordreg2")
            crushlist = ""
            current = ""
            if passwordreg1 != passwordreg2:
                return render_template("add.html",name=True,crush=False,crushlist="")
            mongo.addUser(namereg,usernamereg,passwordreg1)
            session['user'] = namereg
            crushlist = mongo.getPeopleYouLike2(str(namereg))
            return render_template("add.html",name=False,crush=True,crushlist=crushlist,person=namereg,current=current)


        elif 'remove' in request.form:
            name = session['user']
            mongo.removeUser(name)
            return render_template("add.html",name=True,crush=False,crushlist="")
        elif 'add' in request.form:
            meep = request.form.get("crushes")
            crushl = [x.strip() for x in meep.split('\n')]
            name = session['user']
            for item in crushl:
                item.strip()
                x = item.split(", ")
                print x
                print len(x)
                if len(x)>2:
                    mongo.addPerson2(str(name),x[0],x[1],x[2])
                elif len(x) == 1:
                    continue
                else:
                    mongo.addPerson2(str(name),x[0],x[1],"")
            crushl = mongo.getPeopleYouLike2(str(name))
            return render_template("add.html",name=False,crush=True,crushlist=crushl,person=name,current=meep)
        else:
            name = session['user']
            crush = request.form[0]
            mongo.removeCrush(name,crush)
            crushl = mongo.getPeopleYouLike2(str(name))
            return render_template("add.html",name=False,crush=True,crushlist=crushl,person=name)

    return render_template("add.html",name=True,crush=False,crushlist="")

@app.route("/see",methods=['GET','POST'])
def see():
    l = mongo.getAllPeople2()
    l.sort()
    drop = l
    if request.method == "POST":
        if "yours" in request.form:
            name = request.form.get("yours")
            words = mongo.getPeopleYouLike2(str(name))
            return render_template("see.html",submitted=True,submit=False,name=name,crushes=words,drop=drop,browse=False)
        elif "likes" in request.form:
            name = request.form.get("likes")
            words = mongo.getPeopleWhoLikeYou2(str(name))
            return render_template("see.html",submitted=False,submit=True,name=name,crushes=words,drop=drop,browse=False)
        else:
            name = request.form.get('name')
            w = mongo.getPeopleYouLike2(str(name))
            words = []
            for item in w:
                if item[2] != "":
                    x = item[0] + ", " + item[1] + ", "+item[2]
                else:
                    x = item[0]+", "+item[1]
                words.append(x)
            return render_template("see.html",submitted=False,submit=False,name=name,crushes=words,drop=drop,browse=True)

    return render_template("see.html",submitted=False,submit=False,drop=drop)

####################  Z ####################
@app.route("/addAjax")
def addAjax():
    crusher = session['user']
    year = request.args.get('cyear',"")
    crush = request.args.get('ccrush',"")
    hm = request.args.get('chm','')
    if len(crush)>0:
        mongo.addPerson2(str(crusher),crush,year,hm)
    crushl = mongo.getPeopleYouLike2(str(crusher))
    return render_template("crushonly.html",name=False,crush=True,crushlist=crushl,person=crusher)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
