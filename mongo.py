from pymongo import Connection

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
    r = [x for x in db.students.find({'name':name})]
    print r
    if len(r) > 0:
        db.students.update({'name':name},d)
    else:
        db.students.insert(d)

def getPeopleYouLike(name):
    db = conn()
    r = [x for x in db.students.find({'name':name})]
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
        if name in person['crushlist']:
            yours.append(person['name'])
    if len(yours) == 0:
        return ["No one has put you on their crushlist", "Or you might need to type your name differently or try capitalizing/uncapitalizing the name"]
    return yours
