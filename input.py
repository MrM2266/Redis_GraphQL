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
        person(id:2)
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
                id
                name
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
    createGrouptype(name:"ceta")
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
    createRoletype(name:"velitel")
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

#mutacemi pro create půjdou nastavit jen parametry, které jsou string