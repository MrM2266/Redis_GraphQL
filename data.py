data_users = [
{"id":"1", "name":"Timmy", "surname":"Trumpet", "age":"35"},
{"id":"2", "name":"Ava", "surname":"Max", "age":"25"},
{"id":"3", "name":"Becky", "surname":"Hill", "age":"30"},
{"id":"4", "name":"Dua", "surname":"Lipa", "age":"28"},
{"id":"5", "name":"Jan", "surname":"Veliky", "age":"60"},
{"id":"6", "name":"Petr", "surname":"Maly", "age":"25"},
{"id":"7", "name":"Pavel", "surname":"Novotny", "age":"42"},
{"id":"8", "name":"David", "surname":"Guetta", "age":"40"}]

data_groups = [{"id":"1", "name":"FVT", "groupType":"1"},
{"id":"2", "name":"FVL", "groupType":"1"},
{"id":"3", "name":"23-5KB", "groupType":"3"},
{"id":"4", "name":"21-5TPVO", "groupType":"3"},
{"id":"5", "name":"Katedra informatiky a kybernetickych operaci", "groupType":"2"},
{"id":"6", "name":"Katedra radiolokace", "groupType":"2"}]

data_groupTypes = [{"id":"1", "name":"fakulta"},
{"id":"2", "name":"katedra"},
{"id":"3", "name":"ucebni skupina"}
]

data_roleTypes = [{"id":"1", "name":"student"},
{"id":"2", "name":"ucitel"},
{"id":"3", "name":"vedouci katedry"}]

data_users_groups = [
    {"id":"1", "users_id":"1", "groups_id":"1", "roleType_id":"1"},
    {"id":"2", "users_id":"1", "groups_id":"3", "roleType_id":"2"},
    {"id":"3", "users_id":"1", "groups_id":"5", "roleType_id":"1"},
    {"id":"4", "users_id":"2", "groups_id":"1", "roleType_id":"1"},
    {"id":"5", "users_id":"2", "groups_id":"6", "roleType_id":"1"},
    {"id":"6", "users_id":"3", "groups_id":"1", "roleType_id":"2"},
    {"id":"7", "users_id":"3", "groups_id":"3", "roleType_id":"1"},
    {"id":"8", "users_id":"4", "groups_id":"1", "roleType_id":"1"},
    {"id":"9", "users_id":"4", "groups_id":"4", "roleType_id":"3"},
    {"id":"10", "users_id":"5", "groups_id":"5", "roleType_id":"1"},
    {"id":"11", "users_id":"6", "groups_id":"5", "roleType_id":"2"},
    {"id":"12", "users_id":"7", "groups_id":"5", "roleType_id":"1"},
    {"id":"13", "users_id":"8", "groups_id":"2", "roleType_id":"2"}
]

#zbývá vyřešit zápis do data_users_groups - jinak do všeho vše lze zapsat