import redis
import data
import json

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


class Group:
    def __init__(self, id = None, name = None, groupType = None):
        self.id = id
        self.name = name
        self.groupType = groupType

    def Load(self, group_id):
        self.id = group_id
        self.name = groups.GetItem(group_id, "name")
        self.groupType = self.LoadGroupType()

    def LoadGroupType(self):
        #vrací objekt GroupType pro tuto skupinu
        gt = GroupType()
        gt.Load(int(groups.GetItem(self.id, "groupType")))
        return gt

class Person:
    def __init__(self, id = None, name = None, surname = None, age = None, roles = None, groups = None):
        self.id = id
        self.name = name
        self.surname = surname
        self.age = age
        self.roles = roles
        self.groups = groups

    def Load(self, user_id):
        self.id = user_id
        self.name = users.GetItem(user_id, "name")
        self.surname = users.GetItem(user_id, "surname")
        self.age = users.GetItem(user_id, "age")
        self.roles = self.LoadRoles() #list objektů role
        self.groups = self.LoadGroups() #je to list objektů Group

    def LoadGroups(self):
        data = RelationMN(users, groups, users_groups, int(self.id))
        out = []
        if (data == None):
            out.append(Group())
            return out
        
        for group in data:
            tmp = Group()
            tmp.Load(int(group["id"]))
            out.append(tmp)
        if (len(out) != 0): return out
        else:
            out.append(Group())
            return out

    def LoadRoles(self): #TODO: vyřešit prázdné role - co tam má být, když není ve skupině
        data = users.GetItem(self.id, "roles")
        out = []
        if (data == None):
            out.append(Role())
            return out
        
        data = json.loads(data)

        for role in data:
            tmp = Role()
            tmp.Load(role)
            out.append(tmp)

        if (len(out) != 0): return out
        else:
            out.append(Role())
            return out
           
    def PrintGroups(self):
        for group in self.groups:
            print(f"ID: {group.id}")
            print(f"Nazev: {group.name}")
            print(f"groupType: {group.groupType}\n")

class GroupType:
    def __init__(self, id = None, name = None):
        self.id = id
        self.name = name

    def Load(self, groupType_id):
        self.id = int(groupType_id)
        self.name = group_types.GetItem(self.id, "name")

class RoleType:
    def __init__(self, id = None, name = None):
        self.id = id
        self.name = name

    def Load(self, roleType_id):
        self.id = roleType_id
        self.name = role_types.GetItem(self.id, "name")

class Role:
    def __init__(self, id = None, roleType=None, group = None):
        self.id = id
        self.roleType = roleType
        self.group = group
        #self.user_id = user_id #id uživatele, kterému tato role patří

    def Load(self, data): #data = dic jedné role - této role - dic dostanu z person LoadRoles
        self.id = data["id"]
        self.roleType = self.LoadRoleType(data["roletype"])
        self.group = self.LoadGroup(data["group"])
        
    def LoadRoleType(self, roleType_id):
        tmp = RoleType()
        tmp.Load(int(roleType_id))
        return tmp

    def LoadGroup(self, group_id):
        tmp = Group()
        tmp.Load(int(group_id))
        return tmp



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
#print(type(GetRolesFromUser(1)))
#print(GetRolesFromUser(1))

#p = Person()
#p.Load(2)
#print(p.roles[1].group.name)

#r = Role()
#r.Load(json.loads('{"id":"10", "roletype":"1", "group":"1"}'))
#print(r.group.groupType.name)
