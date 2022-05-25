import redis
import data

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
        data = self.table.hgetall(id)
        data["id"] = id
        return data

    def GetItem(self, id, item): #vrací string
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


def Relation11(table1, table2, table1_id): #1:1 relace
    return table1.GetLine(table2.GetItem(table1_id, table1.GetTableName() + "_id")) #když je klic u user - tzn, user má car_id


def Relation1N(table1, table2, table1_id): #1:N relace - klíč je na straně N
    ids = table2.GetKeys()
    output = []

    for id in ids:
        entity_id = int(table2.GetItem(id, table1.GetTableName() + "_id"))

        if (entity_id == table1_id):
            line = table2.GetLine(id)
            line["id"] = id
            output.append(line)

    if (len(output) != 0): return output
    else: return None


def RelationMN(table1, table2, interTable, table1_id): #M:N přes pomocnou tabulku - vrací list dictionaries - každý dictionary je řádek z table2, která je v relaci
    #s prvkem z table1 s table1_id např. [{'id': 1, 'name': 'FVT', 'groupType': '1'}, {'id': 2, 'name': 'FVL', 'groupType': '1'}]
    line_ids = interTable.GetKeys()
    output = []

    for line_id in line_ids:
        if (int(interTable.GetItem(line_id, table1.GetTableName() + "_id")) == table1_id):
            output.append(table2.GetLine(str(interTable.GetItem(line_id, table2.GetTableName() + "_id"))))

    if (len(output) != 0): return output
    else: return None


def GetUser(table, id):
    data = {
        "id":id,
        "name":table.GetItem(id, "name"),
        "surname":table.GetItem(id, "surname"),
        "age":table.GetItem(id, "age"),
        "roles":table.GetItem(id, "roles")
    }
    return data

def GetGroup(table, id):
    data = {
        "id":id,
        "name":table.GetItem(id, "name"),
        "groupType":table.GetItem(id, "groupType")
    }
    return data

def GetGroupType(table, id):
    data = {
        "id":id,
        "name":table.GetItem(id, "name"),
    }
    return data


users = CTable("users", 0)
groups = CTable("groups", 1)
users_groups = CTable("users_groups", 2)
group_types = CTable("group_types", 3)
role_types = CTable("role_types", 4)

users.Populate(data.data_users)
groups.Populate(data.data_groups)
users_groups.Populate(data.data_users_groups)
group_types.Populate(data.data_groupTypes)
role_types.Populate(data.data_roleTypes)

#print(GetGroup(groups, 1))
#data = GetUser(users, 1)
#print(RelationMN(users, groups, users_groups, 1))
#print(groups.GetLine(1))
#print(users.GetItem("1", "roles"))