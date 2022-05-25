import graphene
import database

class Person(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    surname = graphene.String()
    groups = graphene.List(lambda: Group)

    def resolve_name(parent, info):
        #print(parent)
        return parent["name"]

    def resolve_surname(parent, info):
        return parent["surname"]

    def resolve_groups(parent, info):
        #print(database.RelationMN(database.users, database.groups, database.users_groups, parent["id"]))
        #return [{'id': 1, 'name': 'FVT', 'groupType': '1'}, {'id': 2, 'name': 'FVL', 'groupType': '1'}]
        #očekává se, že bude vracet list skupin - stejných datových struktur, jako jsou na vstupu do class Group
        return database.RelationMN(database.users, database.groups, database.users_groups, int(parent["id"]))

class Group(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    groupType = graphene.Field(lambda:GroupType)

    def resolve_name(parent, info):
        return parent["name"]
    
    def resolve_groupType(parent, info):
        return database.GetGroupType(database.group_types, int(parent["groupType"]))

class GroupType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

    def resolve_name(parent, info):
        return parent["name"]

class Query(graphene.ObjectType):
    person = graphene.Field(Person, id = graphene.ID(required=True))
    group = graphene.Field(Group, id = graphene.ID(required=True))
    groupType = graphene.Field(GroupType, id = graphene.ID(required = True))

    def resolve_person(root, info, id):
        return database.GetUser(database.users, id) #toto je parent pro fci resolve_name v class person - je to string - tzn. do person jsem si poslal str id
        #tady bych potřeboval dostat z databáze strukturu (objekt?), který bude reprezentovat osobu se zadaným id

    def resolve_group(root, info, id):
        return database.GetGroup(database.groups, id)

    def resolve_groupType(root, info, id):
        return database.GetGroupType(database.group_types, id)

schema = graphene.Schema(query=Query)
#print(schema)

query = '''
    query
    { 
        group(id:5){
        id
        name
        groupType{
            id
            name
        }
        }
    }
    '''

query2 = '''
    query
    { 
        person(id:2){
        name
        surname
        groups{
            id
            name
            groupType{
                name
            }
        }
        }
    }
'''

query3 = '''
    query
    { 
        groupType(id:2){
        id
        name
        }
    }
'''

result = schema.execute(query2)
print(result)