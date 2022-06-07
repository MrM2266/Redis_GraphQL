query1 = '''
    query
    { 
        group(id:5){
        id
        name
        groupType{
            name
            }
        members{
            name
            surname
        }
        }
    }
    '''

query2 = '''
    query
    { 
        person(id:1)
        {
            name
            surname
            age
            memberships{
                roleType{name}
                group{name}
            }
        }
    }
'''

query3 = '''
    query
    { 
        groupType(id:1){
        id
        name
        }
    }
'''

query4 = '''
    query
    { 
        roleType(id:1){
        id
        name
        }
    }
'''

query5 = '''
    query
    { 
        person(id:1){
        name
        surname
        memberships{
            group{
                name
                groupType{name}
            }
            roleType{
                id
                name
            }
        }
        }
    }
'''

query6 = '''
    query
    { 
        person(id:1){
        name
        surname
        age
        memberships
        {
            group
            {
                name
                groupType{
                    name
                }
                members{
                    name
                    surname}
            }
            roleType{
                name
            }
        }
        }
    }
'''

mut = '''
   mutation {
    createPerson(name:"Peter", surname:"Veliky", age:"50"){
        person {
            id
            name
            surname
            age
        }
    }
}
    '''

mut1 = '''
mutation
{ 
    createGroupType(name:"ceta")
    {
        groupType {
            id
            name
        }
    }
}
'''


mut2 = '''
mutation
{ 
    createGroup(name:"komando", groupTypeID:"3")
    {
        group {
            id
            name
            groupType{name}
        }
    }
}
'''

mut3 = '''
mutation
{ 
    createRoleType(name:"velitel")
    {
        roleType {
            id
            name
        }
    }
}
'''


mut4 = '''
mutation
{ 
    addUserToGroup(groupID:"5", userID:"2", roleTypeID:"1")
    {
        group {
            name
            members{
                name
                surname
            }
        }
    }
}
'''


mut5 = '''
mutation
{ 
    addUserToGroup(groupID:"5", userID:"2", roleTypeID:"1")
    {
        person {
            name
            surname
            memberships{
                group{name}
            }
        }

        group{name}
    }
}
'''


mut6 = '''
mutation
{ 
    updatePerson(id:"5", name:"Honza", surname:"Maly")
    {
        person {
            id
            name
            surname
            age
            memberships{
                group{
                    id
                    name
                }
                roleType{name}
            }
        }
    }
}
'''

mut7 = '''
mutation
{ 
    updateGroup(id:"1", name:"Fakulta vojenskych technologii")
    {
        group {
            id
            name
            groupType{name}
        }
    }
}
'''

mut8 = '''
mutation
{ 
    updateGroupType(id:"2", name:"department")
    {
        groupType {
            id
            name
        }
    }
}
'''

mut9 = '''
mutation
{ 
    updateRoleType(id:"2", name:"teacher")
    {
        roleType {
            id
            name
        }
    }
}
'''

err1 = '''
mutation
{ 
    createGroup(groupTypeID:"3")
    {
        group {
            id
            name
            groupType{name}
            members{
                name
                surname
                }
        }
    }
}
'''

err2 = '''
mutation
{ 
    createPerson(name:"Max", surname:"Payne")
    {
        person{
            id
            name
            surname
            age
            memberships{
                roleType{name}
                group{
                    id
                    name
                    members{name
                    surname
                    }
                    }
            }
        }
    }
}
'''

err3 = '''
mutation
{ 
    createRoleType(name:"test")
    {
        roleType {
            id
            name
        }
    }
}
'''

err4 = '''
query
{ 
    person(id:"99")
    {
        name
        surname
        memberships{
            group{name}
        }
    }
}
'''

del1 = '''
mutation
{ 
    delPerson(id:"1")
    {
        status
    }
}
'''

del2 = '''
mutation
{ 
    delGroup(id:"1")
    {
        status
    }
}
'''

del3 = '''
mutation
{ 
    delGroupType(id:"1")
    {
        status
    }
}
'''

del4 = '''
mutation
{ 
    delRoleType(id:"2")
    {
        status
    }
}
'''

rem1 = '''
mutation
{ 
    removeUserFromGroup(groupID:"1", userID:"1")
    {
        person{
            name
            surname
            memberships{
                group{name}
            }
        }

        group{
            name
            members{
                name
                surname
            }
        }
    }
}
'''

ctl1 = '''
query
{ 
    control(command:"PopulateDB")
}
'''

ctl2 = '''
query
{ 
    control(command:"EraseDB")
}
'''

#mutacemi pro create půjdou nastavit jen parametry, které jsou string