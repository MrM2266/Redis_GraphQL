import graphene
import database
import input

class Person(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    surname = graphene.String()
    age = graphene.String()
    memberships = graphene.List(lambda: Membership)

    def resolve_name(parent, info):
        return str(parent.name)

    def resolve_surname(parent, info):
        return str(parent.surname)

    def resolve_age(parent, info):
        return str(parent.age)

    def resolve_memberships(parent, info):
        return parent.GetMemberships()

class CreatePerson(graphene.Mutation):
    person = graphene.Field(Person) #to co bude na výstupu mutace - to co bude vracet

    class Arguments:
        name = graphene.String()
        surname = graphene.String()
        age = graphene.String()

    def mutate(parent, info, name, surname, age):
        person = database.Person()
        if(type(name) == str): person.name = name
        if(type(surname) == str): person.surname = surname
        if(type(age) == str): person.age = age
        person.AddToDB()
        return CreatePerson(person=person)

class UpdatePerson(graphene.Mutation):
    person = graphene.Field(Person)

    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()
        surname = graphene.String()
        age = graphene.String()

    def mutate(parent, info, id, name, surname, age):
        person = database.Person()
        person.Load(int(id))
        if(type(name) == str): person.name = name
        if(type(surname) == str): person.surname = surname
        if(type(age) == str): person.age = age
        person.UpdateData()
        return UpdatePerson(person = person)

class DelPerson(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        id = graphene.ID(required = True)

    def mutate(parent, info, id):
        person = database.Person()
        person.Load(int(id))
        person.Del()
        return DelPerson(status = "ok")


class Group(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    groupType = graphene.Field(lambda:GroupType) #id odpovídající groupType
    members = graphene.List(Person)

    def resolve_name(parent, info):
        return str(parent.name)
    
    def resolve_groupType(parent, info):
        return parent.GetGroupType()

    def resolve_members(parent, info):
        return parent.GetMembers()

class CreateGroup(graphene.Mutation):
    group = graphene.Field(Group)

    class Arguments:
        name = graphene.String()
        groupTypeID = graphene.String()

    def mutate(parent, info, name, groupTypeID):
        group = database.Group()
        if(type(name) == str): group.name = name
        if(type(groupTypeID) == str): group.groupType = groupTypeID
        group.AddToDB()
        return CreateGroup(group=group)

class UpdateGroup(graphene.Mutation):
    group = graphene.Field(Group)

    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()
        groupTypeID = graphene.String()

    def mutate(root, info, id, name, groupTypeID):
        group = database.Group()
        group.Load(int(id))
        if(type(name) == str): group.name = name
        if(type(groupTypeID) == str): group.groupType = groupTypeID
        group.UpdateData()
        return UpdateGroup(group = group)

class DelGroup(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        id = graphene.ID(required = True)

    def mutate(parent, info, id):
        gr = database.Group()
        gr.Load(int(id))
        gr.Del()
        return DelGroup(status = "ok")


class GroupType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

    def resolve_name(parent, info):
        return str(parent.name)

class CreateGroupType(graphene.Mutation):
    groupType = graphene.Field(GroupType)

    class Arguments:
        name = graphene.String()

    def mutate(parent, info, name):
        groupType = database.GroupType()
        if(type(name) == str): groupType.name = name
        groupType.AddToDB()
        return CreateGroupType(groupType=groupType)

class UpdateGroupType(graphene.Mutation):
    groupType = graphene.Field(GroupType)

    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()

    def mutate(parent, info, id, name):
        gt = database.GroupType()
        gt.Load(int(id))
        if(type(name) == str): gt.name = name
        gt.UpdateData()
        return UpdateGroupType(groupType = gt)

class DelGroupType(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        id = graphene.ID(required = True)

    def mutate(parent, info, id):
        gt = database.GroupType()
        gt.Load(int(id))
        gt.Del()
        return DelGroupType(status = "ok")

class RoleType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

    def resolve_name(parent, info):
        return str(parent.name)

class CreateRoleType(graphene.Mutation):
    roleType = graphene.Field(RoleType)

    class Arguments:
        name = graphene.String()

    def mutate(parent, info, name):
        roleType = database.RoleType()
        if(type(name) == str): roleType.name = name
        roleType.AddToDB()
        return CreateRoleType(roleType=roleType)

class UpdateRoleType(graphene.Mutation):
    roleType = graphene.Field(RoleType)

    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()

    def mutate(parent, info, id, name):
        rt = database.RoleType()
        rt.Load(int(id))
        if(type(name) == str): rt.name = name
        rt.UpdateData()
        return UpdateRoleType(roleType = rt)

class DelRoleType(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        id = graphene.ID(required = True)

    def mutate(parent, info, id):
        rt = database.RoleType()
        rt.Load(int(id))
        rt.Del()
        return DelRoleType(status = "ok")

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

class RemoveUserFromGroup(graphene.Mutation):
    group = graphene.Field(Group)
    person = graphene.Field(Person)

    class Arguments:
        groupID = graphene.String()
        userID = graphene.String()

    def mutate(parent, info, groupID, userID):
        gr = database.Group()
        gr.Load(int(groupID))
        gr.RemoveMember(int(userID))
        per = database.Person()
        per.Load(int(userID))
        return RemoveUserFromGroup(group = gr, person = per)


class Query(graphene.ObjectType):
    person = graphene.Field(Person, id = graphene.ID(required=True))
    group = graphene.Field(Group, id = graphene.ID(required=True))
    groupType = graphene.Field(GroupType, id = graphene.ID(required = True))
    roleType = graphene.Field(RoleType, id = graphene.ID(required = True))

    control = graphene.String(command = graphene.String()) #pouze pro školní účely

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

    def resolve_control(root, info, command):
        if (str(command) == "PopulateDB"): 
            database.PopulateDB()
            return "db populated from data.py"

        if (str(command) == "EraseDB"): 
            database.users.table.flushall()
            return "db erased"

        return "unknown command"


class Mutations(graphene.ObjectType):
    create_person = CreatePerson.Field()
    create_group = CreateGroup.Field()
    create_group_type = CreateGroupType.Field()
    create_role_type = CreateRoleType.Field()

    add_user_to_group = AddUserToGroup.Field()
    remove_user_from_group = RemoveUserFromGroup.Field()
    
    update_person = UpdatePerson.Field()
    update_group = UpdateGroup.Field()
    update_group_type = UpdateGroupType.Field()
    update_role_type = UpdateRoleType.Field()

    del_person = DelPerson.Field()
    del_group = DelGroup.Field()
    del_group_type = DelGroupType.Field()
    del_role_type = DelRoleType.Field()



schema = graphene.Schema(query=Query, mutation=Mutations)
#print(schema)

result = schema.execute(input.ctl2)
print(result)

#result2 = schema.execute(input.query2)
#print(result2)