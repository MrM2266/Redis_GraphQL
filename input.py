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
        person(id:1){
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
    createGroup(name:"komando")
    {
        group {
            id
            name
        }
    }
}
'''


#mutacemi pro create půjdou nastavit jen parametry, které jsou string