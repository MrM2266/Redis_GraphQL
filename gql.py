import graphene
import database
import input


class CreatePerson(graphene.Mutation):
    person = graphene.Field(lambda: Person) #to co bude na výstupu mutace - to co bude vracet

    class Arguments:
        name = graphene.String()
        surname = graphene.String()


    def mutate(root, info, name, surname):
        person = Person(name = name, surname = surname)
        return CreatePerson(person=person)

class Person(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    surname = graphene.String()
    age = graphene.String()
    groups = graphene.List(lambda: Group)
    roles = graphene.List(lambda: Role)

    def resolve_name(parent, info):
        return parent.name

    def resolve_surname(parent, info):
        return parent.surname

    def resolve_age(parent, info):
        return parent.age

    def resolve_groups(parent, info):
        #return [{'id': 1, 'name': 'FVT', 'groupType': '1'}, {'id': 2, 'name': 'FVL', 'groupType': '1'}]
        #očekává se, že bude vracet list skupin - stejných datových struktur, jako jsou na vstupu do class Group
        #to co vrací return se dává jako vstup do class Group
        #print(database.RelationMN(database.users, database.groups, database.users_groups, int(parent["id"])))
        #return database.RelationMN(database.users, database.groups, database.users_groups, parent.id)
        #bude muset vracet list objektů database.group
        return parent.groups

    def resolve_roles(parent, info):
        return parent.roles

class Group(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    groupType = graphene.Field(lambda:GroupType)

    def resolve_name(parent, info):
        return parent.name
    
    def resolve_groupType(parent, info):
        return parent.groupType

class CreateGroup(graphene.Mutation):
    group = graphene.Field(Group)

    class Arguments:
        name = graphene.String()

    def mutate(root, info, name):
        group = Group(name = name)
        return CreateGroup(group=group)


class GroupType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

    def resolve_name(parent, info):
        return parent.name

class CreateGroupType(graphene.Mutation):
    output = graphene.Field(GroupType)

    class Arguments:
        name = graphene.String()

    def mutate(parent, info, name):
        groupType = GroupType(name=name)
        return CreateGroupType(groupType)

class RoleType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

    def resolve_name(parent, info):
        return parent.name

class Role(graphene.ObjectType):
    id = graphene.ID()
    roleType = graphene.Field(RoleType)
    group = graphene.Field(Group)

    def resolve_group(parent, info):
        return parent.group

    def resolve_roleType(parent, info):
        return parent.roleType

class Query(graphene.ObjectType):
    person = graphene.Field(Person, id = graphene.ID(required=True))
    group = graphene.Field(Group, id = graphene.ID(required=True))
    groupType = graphene.Field(GroupType, id = graphene.ID(required = True))
    roleType = graphene.Field(RoleType, id = graphene.ID(required = True))

    def resolve_person(root, info, id):
        person = database.Person()
        person.Load(id)
        return person

    def resolve_group(root, info, id):
        group = database.Group()
        group.Load(id)
        return group

    def resolve_groupType(root, info, id):
        groupType = database.GroupType()
        groupType.Load(id)
        return groupType

    def resolve_roleType(root, info, id):
        roleType = database.RoleType()
        roleType.Load(id)
        return roleType


class MyMutations(graphene.ObjectType):
    create_person = CreatePerson.Field()
    create_group = CreateGroup.Field()
    

schema = graphene.Schema(query=Query, mutation=MyMutations)
#print(schema)

result = schema.execute(input.query6)
print(result)

#TODO ke groups přidat roles - aby šlo zobrazit roli ve skupině