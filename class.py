import redis

class CTable:
    def __init__(self, name, db_no):
        self.name = name
        self.lines = 0
        self.db_no = db_no
        self.table = redis.Redis(host="localhost", port=6379, db = db_no, charset="utf-8", decode_responses=True)

    def GetTableName(self):
        return self.name

    def GetKeys(self):
        keys = self.table.keys()

        for i in range(0, len(keys)):
            keys[i] = int(keys[i])
        return keys

    def AddLine(self, id, data): #pod dane id ulozi dic v data
        self.table.hset(id, mapping=data)
        self.lines += 1

    def GetLine(self, id):
        return self.table.hgetall(id)

    def GetItem(self, id, item):
        return self.table.hget(id, item)

    def UpdateItem(self, id, item, new_value): #pokud neexistuje, tak vytvoří
        self.table.hset(id, item, new_value)
    
    def Populate(self, data): #bere data, dic, kde v každé položce je na prvním místě id
        for line in data:
            id = line["id"]
            del line["id"]
            self.AddLine(id, line)

    def ShowLine(self, id):
        print(self.GetLine(id))


def GetCarByUserID(cars, users, user_id): #1:1 relace
    return cars.GetLine(users.GetItem(user_id, "car_id")) #když je klic u user - tzn, user má car_id

def GetCarsByUserID(users, cars, user_id): #1:N relace
    ids = cars.GetKeys()
    output = []

    for id in ids:
        owner_id = int(cars.GetItem(id, users.GetTableName() + "_id"))

        if (owner_id == user_id):
            line = cars.GetLine(id)
            line["id"] = id
            output.append(line)

    if (len(output) != 0): return output
    else: return None

def GetGroupsByUserID(users, groups, users_groups, target_user_id): #M:N přes pomocnou tabulku
    line_ids = users_groups.GetKeys()
    output = []

    for line_id in line_ids:
        if (int(users_groups.GetItem(line_id, users.GetTableName() + "_id")) == target_user_id):
            output.append(groups.GetLine(str(users_groups.GetItem(line_id, groups.GetTableName() + "_id"))))

    if (len(output) != 0): return output
    else: return None



data_users = [
{"id":"1", "name":"Timmy", "surname":"Trumpet", "age":"35"},
{"id":"2", "name":"Ava", "surname":"Max", "age":"25"},
{"id":"3", "name":"Becky", "surname":"Hill", "age":"30"},
{"id":"4", "name":"Dua", "surname":"Lipa", "age":"28"},
{"id":"5", "name":"Jan", "surname":"Veliky", "age":"60"},
{"id":"10", "name":"Petr", "surname":"Maly", "age":"25"},
{"id":"19", "name":"Pavel", "surname":"Novotny", "age":"42"},
{"id":"20", "name":"David", "surname":"Guetta", "age":"40"}]

data_cars = [{"id":"5", "brand":"BMW", "type":"450d", "users_id":"5"},
{"id":"10", "brand":"Audi", "type":"A4", "users_id":"10"},
{"id":"1", "brand":"Skoda", "type":"Superb", "users_id":"19"},
{"id":"2", "brand":"Porsche", "type":"GT3 RS", "users_id":"20"},
{"id":"3", "brand":"Rolls Royce", "type":"Phantom", "users_id":"20"},
{"id":"4", "brand":"Audi", "type":"RS4", "users_id":"20"}]

data_groups = [{"id":"1", "name":"singers"},
{"id":"2", "name":"DJs"},
{"id":"3", "name":"America"},
{"id":"4", "name":"Europe"},
{"id":"5", "name":"employees"}]

data_users_groups = [
    {"id":"1", "users_id":"1", "groups_id":"1"},
    {"id":"2", "users_id":"1", "groups_id":"3"},
    {"id":"3", "users_id":"1", "groups_id":"2"},
    {"id":"4", "users_id":"2", "groups_id":"1"},
    {"id":"5", "users_id":"2", "groups_id":"3"},
    {"id":"6", "users_id":"3", "groups_id":"1"},
    {"id":"7", "users_id":"3", "groups_id":"3"},
    {"id":"8", "users_id":"4", "groups_id":"1"},
    {"id":"9", "users_id":"4", "groups_id":"4"},
    {"id":"10", "users_id":"5", "groups_id":"5"},
    {"id":"11", "users_id":"10", "groups_id":"5"},
    {"id":"12", "users_id":"19", "groups_id":"5"},
    {"id":"13", "users_id":"20", "groups_id":"1"},
    {"id":"14", "users_id":"20", "groups_id":"2"},
    {"id":"15", "users_id":"20", "groups_id":"3"}
]


users = CTable("users", 0)
cars = CTable("cars", 1)
groups = CTable("groups", 2)
users_groups = CTable("users_groups", 3)

users.Populate(data_users)
cars.Populate(data_cars)
groups.Populate(data_groups)
users_groups.Populate(data_users_groups)

#cars.ShowLine(5)
#cars.ShowLine(10)
#cars.ShowLine(1)
#print(GetCarByUserID(cars, users, 5)) #nyní nefunguje - klíč je na druhé straně

#print(GetCarsByUserID(users, cars, 5))

print(GetGroupsByUserID(users, groups, users_groups, 20))

#TODO: zobecnit fce - aby byly obecně pro N:M a 1:M pro jakékoliv tabulky