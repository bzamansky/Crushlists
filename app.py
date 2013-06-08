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
        name = ""
        current = ""
        if 'name' in request.form:
            name = request.form.get("name")
            session['user'] = name
            crushlist = mongo.getPeopleYouLike(str(name))
            for item in crushlist:
                current += item + ", "
            enter = False
            return render_template("add.html",name=False,crush=True,crushlist=crushlist,person=name,current=current)

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
