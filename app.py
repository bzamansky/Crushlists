import mongo, re
from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key="blah"

@app.route("/",methods = ['GET','POST'])
def home():
    return render_template("home.html",clicked=False)


"""
@app.route("/add",methods=['GET','POST'])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        meep = request.form.get("crushes")
        crushl = meep.split(",")
        mongo.addPerson(str(name),crushl)
        crushlist = name + " had crushes on " + meep
        return render_template("add.html",crush=True,crushlist=crushlist)
    return render_template("add.html",crush=False,crushlist="")
"""

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
            session['user'] = name
            name = mongo.getName(username,password)
            crushlist = ""
            if name == 0:
                return render_template("add.html",name=True,crush=False,crushlist="")
            crushlist = mongo.getPeopleYouLike(str(name))
            for item in crushlist:
                current += item + ", "
            enter = False
            return render_template("add.html",name=False,crush=True,crushlist=crushlist,person=name,current=current)
        
        elif 'usernamereg' in request.form:
            namereg = request.form.get("namereg")
            usernamereg = request.form.get("usernamereg")
            passwordreg1 = request.form.get("passwordreg1")
            passwordreg2 = request.form.get("passwordreg2")
            crushlist = ""
            current = ""
            if passwordreg1 != passwordreg2:
                return render_template("add.html",name=True,crush=False,crushlist="")
            if namereg in mongo.getAllPeople():
                test = mongo.addUserInfo(namereg,usernamereg,passwordreg1)
                if test:
                    session['user'] = namereg
                    crushlist = mongo.getPeopleYouLike(str(namereg))
                    for item in crushlist:
                        current += item + ", "
                        enter = False
                    return render_template("add.html",name=False,crush=True,crushlist=crushlist,person=name,current=current)
                else:
                    return render_template("add.html",name=True,crush=False,crushlist="")
            else:
                session['user'] = namereg
                mongo.addPerson(namereg,"",usernamereg,passwordreg1)
                return render_template("add.html",name=False,crush=True,crushlist=crushlist,person=namereg,current=current)
        else:
            meep = request.form.get("crushes")
            crushl = [x.strip() for x in meep.split(", ")]
            name = session['user']
            mongo.addPerson(str(name),crushl)
            for item in crushl:
                current += item + ", "
            return render_template("add.html",name=False,crush=True,crushlist=crushl,person=name,current=meep)
    return render_template("add.html",name=True,crush=False,crushlist="")

@app.route("/see",methods=['GET','POST'])
def see():
    l = mongo.getAllPeople()
    l.sort()
    drop = l
    if request.method == "POST":
        if "yours" in request.form:
            name = request.form.get("yours")
            words = mongo.getPeopleYouLike(str(name))
            return render_template("see.html",submitted=True,submit=False,name=name,crushes=words,drop=drop,browse=False)
        elif "likes" in request.form:
            name = request.form.get("likes")
            words = mongo.getPeopleWhoLikeYou(str(name))
            return render_template("see.html",submitted=False,submit=True,name=name,crushes=words,drop=drop,browse=False)
        else:
            name = request.form.get('name')
            words = mongo.getPeopleYouLike(str(name))
            return render_template("see.html",submitted=False,submit=False,name=name,crushes=words,drop=drop,browse=True)
            
    return render_template("see.html",submitted=False,submit=False,drop=drop)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
