import graphene
import database
import input


class CreatePerson(graphene.Mutation):
    person = graphene.Field(lambda: Person) #to co bude na výstupu mutace - to co bude vracet

    class Arguments:
        name = graphene.String()
        surname = graphene.String()
        age = graphene.String()

    def mutate(root, info, name, surname, age):
        person = database.Person(name = name, surname = surname, age=age)
        person.AddToDB()
        return CreatePerson(person=person)

class Person(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    surname = graphene.String()
    age = graphene.String()
    memberships = graphene.List(lambda: Membership)

    def resolve_name(parent, info):
        return parent.name

    def resolve_surname(parent, info):
        return parent.surname

    def resolve_age(parent, info):
        return parent.age

    def resolve_memberships(parent, info):
        return parent.GetMemberships()

class Group(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    groupType = graphene.Field(lambda:GroupType) #id odpovídající groupType
    members = graphene.List(Person)

    def resolve_name(parent, info):
        return parent.name
    
    def resolve_groupType(parent, info):
        return parent.GetGroupType()

    def resolve_members(parent, info):
        return parent.GetMembers()

class CreateGroup(graphene.Mutation):
    group = graphene.Field(Group)

    class Arguments:
        name = graphene.String()
        groupTypeID = graphene.String()

    def mutate(root, info, name, groupTypeID):
        group = database.Group(name = name, groupType = groupTypeID)
        group.AddToDB()
        return CreateGroup(group=group)


class GroupType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

    def resolve_name(parent, info):
        return parent.name

class CreateGroupType(graphene.Mutation):
    groupType = graphene.Field(GroupType)

    class Arguments:
        name = graphene.String()

    def mutate(parent, info, name):
        groupType = database.GroupType(name=name)
        groupType.AddToDB()
        return CreateGroupType(groupType=groupType)

class RoleType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

    def resolve_name(parent, info):
        return parent.name

class CreateRoleType(graphene.Mutation):
    roleType = graphene.Field(RoleType)

    class Arguments:
        name = graphene.String()

    def mutate(parent, info, name):
        roleType = database.RoleType(name=name)
        roleType.AddToDB()
        return CreateRoleType(roleType=roleType)

class Membership(graphene.ObjectType):
    roleType = graphene.Field(RoleType)
    group = graphene.Field(Group)

    def resolve_group(parent, info):
        return parent.GetGroup()

    def resolve_roleType(parent, info):
        return parent.GetRoleType()

class AddUserToGroup(graphene.Mutation):
    group = graphene.Field(Group)
    person = graphene.Field(Person)

    class Arguments:
        groupID = graphene.String()
        userID = graphene.String()
        roleTypeID = graphene.String()

    def mutate(parent, info, groupID, userID, roleTypeID):
        group = database.Group()
        group.Load(int(groupID))
        group.AddMember(userID, roleTypeID)
        user = database.Person()
        user.Load(int(userID))
        return AddUserToGroup(group = group, person = user)

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


class Mutations(graphene.ObjectType):
    create_person = CreatePerson.Field()
    create_group = CreateGroup.Field()
    create_groupType = CreateGroupType.Field()
    create_roleType = CreateRoleType.Field()

    add_user_to_group = AddUserToGroup.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutations)
#print(schema)

result = schema.execute(input.mut5)
print(result)