import mongo
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
            crushl = meep.split(", ")
            name = session['user']
            mongo.addPerson(str(name),crushl)
            for item in crushl:
                if item[0] == " ":
                    item = item[1:]
                current += item + ", "
            return render_template("add.html",name=False,crush=True,crushlist=crushl,person=name,current=current)

    return render_template("add.html",name=True,crush=False,crushlist="")

@app.route("/see",methods=['GET','POST'])
def see():
    if request.method == "POST":
        if "yours" in request.form:
            name = request.form.get("yours")
            words = mongo.getPeopleYouLike(str(name))
            return render_template("see.html",submitted=True,submit=False,name=name,crushes=words)
        elif "likes" in request.form:
            name = request.form.get("likes")
            words = mongo.getPeopleWhoLikeYou(str(name))
            return render_template("see.html",submitted=False,submit=True,name=name,crushes=words)
    return render_template("see.html",submitted=False,submit=False)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
