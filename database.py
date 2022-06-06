import redis
import data

class CTable:
    def __init__(self, name, db_no):
        self.name = name
        self.next_id = 1 #první volné id pro nový záznam
        self.lines = 0 #počet řádků v tabulce
        self.db_no = db_no
        self.table = redis.Redis(host="localhost", port=6379, db = db_no, charset="utf-8", decode_responses=True)

    def AddLine(self, id, data): #pod dane id ulozi dic v data
        self.table.hset(id, mapping=data)
        self.lines += 1

    def AddRecord(self, record): #přidá záznam do tabulky - přiřadí mu první volné id
        id = self.next_id
        self.table.hset(id, mapping=record)
        self.next_id += 1
        self.lines += 1
        return id
        #record je dict, který obsahuje stringy - roles je string - json

    def GetTableName(self):
        return self.name

    def GetKeys(self):
        keys = self.table.keys()

        for i in range(0, len(keys)):
            keys[i] = int(keys[i])
        return keys

    def GetLine(self, id):
        data = self.table.hgetall(id)
        data["id"] = id
        return data

    def GetItem(self, id, item): #vrací string
        return self.table.hget(id, item)

    def UpdateItem(self, id, item, new_value): #pokud neexistuje, tak vytvoří
        self.table.hset(id, item, new_value)

    def DelItem(self, id, item): #vymaže položku na zadaném řádku
        self.table.hdel(id, item)

    def DelLine(self, id):
        self.table.delete(id)
        self.lines -=1
    
    def Populate(self, data): #bere data, dic, kde v každé položce je na prvním místě id
        for line in data:
            del line["id"]
            self.AddRecord(line)

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


def RelationMN(table1, table2, interTable, table1_id):
    #sestaví si název klíče podle table1.name
    #vrací všechny řádky z interTable, které jako value pro sestavený klíč obsahují table1_id
    #pro RelationMN(groups, users_groups, 1) vrací
    #[{'users_id': '2', 'groups_id': '1', 'id': 4}, {'users_id': '3', 'groups_id': '1', 'id': 6}, {'users_id': '4', 'groups_id': '1', 'id': 8}, {'users_id': '1', 'groups_id': '1', 'id': 1}]
    line_ids = interTable.GetKeys()
    output = []

    for line_id in line_ids:
        if (int(interTable.GetItem(line_id, table1.GetTableName() + "_id")) == table1_id):
            output.append(interTable.GetLine(line_id))

    if (len(output) != 0): return output
    else: return None


class Group:
    def __init__(self, name = None, groupType = None):
        #to co není list lze nastavit přes konstruktor
        #ke stringům se přistupuje přímo - k listům pomocí fcí
        self.id = None #toto budou jen stringy - obsah databáze
        self.name = name
        self.groupType = groupType
        #members - pomocí GetMembers()
        #groupType - pomocí GetGroupType

    def AddToDB(self): #musíme popsat všechny sloupce tabulky v db kromě id (automaticky tvořeno)
        #přidá tuto skupinu do databáze pod nové id
        data = {
            "name":str(self.name),
            "groupType": str(self.groupType)}
        self.id = groups.AddRecord(data)

    def Load(self, group_id):
        self.id = group_id
        self.name = groups.GetItem(group_id, "name")
        self.groupType = groups.GetItem(group_id, "groupType")

    def LoadMembers(self):
        #vrací pole stringů - jde o id uživatelů, kteří patří do této skupiny
        #např. ['4', '2', '3', '1'] pro skupinu 1
        data = RelationMN(groups, users, users_groups, int(self.id))

        if (data != None):
            out = []
            for member in data:
                out.append(str(member["users_id"]))
            return out
        else: return []

    def UpdateData(self): #aktualizuje všechny string položky - uloží do databáze
        groups.UpdateItem(self.id, "name", self.name)
        groups.UpdateItem(self.id, "groupType", self.groupType)

    def GetGroupType(self):
        #v proměnné self.groupType mám teď objekt groupType - chtěl bych tam mít string
        # který bude obsahovat id příslušného objektu GroupType
        #vrací objekt GroupType pro tuto skupinu - lze na něm volat name atd.
        gt = GroupType()
        gt.Load(int(self.groupType))
        return gt

    def GetMembers(self):
        #vrací list objektů Person, kteří jsou členy této skupiny
        #TODO: prázdná skupina - members = [""]
        membersIDs = self.LoadMembers()
        out = []
        for id in membersIDs:
            tmp = Person()
            tmp.Load(int(id))
            out.append(tmp)

        return out

    def AddMember(self, member_id, roleType_id):
        users_groups.AddRecord({"users_id":str(member_id), "groups_id":str(self.id), "roleType_id":roleType_id})


class Membership: #relace mezi uživatelem a skupinou
    def __init__(self, roleType_id = None, group_id = None):
        self.roleType_id = roleType_id #string
        self.group_id = group_id #string

    def GetGroup(self):
        gr = Group()
        gr.Load(int(self.group_id))
        return gr

    def GetRoleType(self):
        roleType = RoleType()
        roleType.Load(int(self.roleType_id))
        return roleType


class Person:
    def __init__(self, name = None, surname = None, age = None):
        self.id = None
        self.name = name
        self.surname = surname
        self.age = age
        #memberships - pomocí GetMemberships()

    def AddToDB(self):
        data = {
            "name":str(self.name),
            "surname":str(self.surname),
            "age":str(self.age)}

        self.id = users.AddRecord(data)

    def Load(self, user_id): #načte data z databáze
        self.id = user_id
        self.name = users.GetItem(user_id, "name")
        self.surname = users.GetItem(user_id, "surname")
        self.age = users.GetItem(user_id, "age")

    def UpdateData(self): #aktualizuje všechny string položky - uloží do databáze
        users.UpdateItem(self.id, "name", self.name)
        users.UpdateItem(self.id, "surname", self.surname)
        users.UpdateItem(self.id, "age", self.age)
        #TODO: update memberships

    def GetMemberships(self):
        data = RelationMN(users, groups, users_groups, int(self.id))
        out = []

        for mem in data:
            tmp = Membership()
            tmp.group_id = mem["groups_id"]
            tmp.roleType_id = mem["roleType_id"]
            out.append(tmp)

        return out

    def AddToGroup(self, group_id, roleType_id):
        users_groups.AddRecord({"users_id":self.id, "groups_id":group_id, "roleType_id":roleType_id})


class GroupType:
    def __init__(self, name = None):
        self.id = None
        self.name = name

    def AddToDB(self):
        data = {
            "name":str(self.name)}

        self.id = group_types.AddRecord(data)

    def Load(self, groupType_id):
        self.id = int(groupType_id)
        self.name = group_types.GetItem(self.id, "name")

    def UpdateData(self): #aktualizuje všechny string položky - uloží do databáze
        group_types.UpdateItem(self.id, "name", self.name)

class RoleType:
    def __init__(self, name = None):
        self.id = None
        self.name = name

    def AddToDB(self):
        data = {"name":str(self.name)}
        self.id = role_types.AddRecord(data)

    def Load(self, roleType_id):
        self.id = roleType_id
        self.name = role_types.GetItem(self.id, "name")

    def UpdateData(self):
        role_types.UpdateItem(self.id, "name", self.name)



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

#gr = Group()
#gr.Load(3)
#
#usr = Person()
#usr.Load(1)
#
#mem = usr.GetMemberships()
#
#for m in mem:
#    print(m.GetGroup().GetGroupType().name)

#gt = GroupType(name = "specialni skupina")
#gt.AddToDB()
#
#gr = Group()
#gr.name = "komando"
#gr.groupType = gt.id
#gr.AddToDB()
#
#rt = RoleType(name = "clen skupiny")
#rt.AddToDB()
#
#
#usr = Person(name = "Jan", surname = "Novak", age = "36")
#usr.AddToDB()
#usr.AddToGroup(gr.id, rt.id)
#
#usr2 = Person(name = "Richard", surname = "Hammond")
#usr2.AddToDB()
#
#gr.AddMember(usr2.id, "1")
#
#members = gr.GetMembers()
#
#for m in members:
#    print(m.surname)
#