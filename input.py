query1 = '''
    query
    { 
        group(id:1){
        id
        name
        groupType{
            name
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
            groups
            {
                id
                name
                groupType
                {
                    name
                }
            }
        }
    }
'''

query3 = '''
    query
    { 
        groupType(id:3){
        id
        name
        }
    }
'''

query4 = '''
    query
    { 
        roleType(id:3){
        id
        name
        }
    }
'''

query5 = '''
    query
    { 
        person(id:2){
        name
        surname
        roles
        {
            group
            {
                name
            }
            roleType{
                name
            }
        }
        }
    }
'''

query6 = '''
    query
    { 
        person(id:2){
        name
        surname
        age
        roles
        {
            group
            {
                name
                groupType{
                    name
                }
            }
            roleType{
                name
            }
        }
        groups{
            name
        }
        }
    }
'''

mut = '''
   mutation {
    createPerson(name:"Peter", surname:"Veliky"){
        person {
            name
            surname
        }
    }
}
    '''

mut1 = '''
mutation
{ 
    createGrouptype(name:"komando")
    {
        output {
            name
        }
    }
}
'''

mut1 = '''
mutation
{ 
    createGrouptype(name:"komando")
    {
        output {
            name
        }
    }
}
'''


mut2 = '''
mutation
{ 
    createGroup(name:"komando")
    {
        group {
            name
        }
    }
}
'''