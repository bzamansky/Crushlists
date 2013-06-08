from pymongo import Connection
import re

def conn():
    connection = Connection('mongo2.stuycs.org')
    db = connection.admin
    res = db.authenticate('ml7','ml7')
    db = connection['crushlists']
    return db

def clearDB():
    db = conn()
    db.students.remove()


def addPerson(name,crushlist):
    db = conn()
    d = {'name':name, 'crushlist':crushlist}
    regx = re.compile("^"+name,re.IGNORECASE)
    r = [x for x in db.students.find({'name':regx})]
    print r
    if len(r) > 0:
        db.students.update({'name':name},d)
    else:
        db.students.insert(d)


def addPerson2(name,crush,year):
    db = conn()
    d = {'name':name,'crush':crush,'year':year}
    r = [x for x in db.students.find({'name':name})]
    print r


def getPeopleYouLike(name):
    db = conn()
    regx = re.compile("^"+name,re.IGNORECASE)
    r = [x for x in db.students.find({'name':regx})]
    if len(r) == 0:
        return ["You have not submitted a crushlist","Or you might need to add a last name or try capitalizing/uncapitalizing the name"]
    else:
        a = r[0]
        return a['crushlist']
        
def getPeopleWhoLikeYou(name):
    db = conn()
    r = [x for x in db.students.find()]
    yours = []
    for person in r:
        for x in person['crushlist']:
            if x.lower() == name.lower():
                yours.append(person['name'])
    if len(yours) == 0:
        return ["No one has put you on their crushlist", "Or you might need to type your name differently or try capitalizing/uncapitalizing the name"]
    return yours


def getAllPeople():
    db = conn()
    r = [x for x in db.students.find()]
    l = [x['name'] for x in r]
    return l

def printAll():
    db = conn()
    r = [x for x in db.students.find()]
    l = [[x['name'],x['crushlist']] for x in r]
    for x in l:
        print x[0]
        print x[1]

#printAll()
