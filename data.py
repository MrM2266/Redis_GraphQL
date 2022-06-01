data_users = [
{"id":"1", "name":"Timmy", "surname":"Trumpet", "age":"35", "roles": '[{"id":"1", "roletype":"1", "group":"1"}, {"id":"2", "roletype":"2", "group":"2"}]'},
{"id":"2", "name":"Ava", "surname":"Max", "age":"25", "roles": '[{"id":"1", "roletype":"1", "group":"1"}, {"id":"2", "roletype":"1", "group":"3"}]'},
{"id":"3", "name":"Becky", "surname":"Hill", "age":"30", "roles": '[{"id":"1", "roletype":"1", "group":"1"}, {"id":"2", "roletype":"1", "group":"6"}]'},
{"id":"4", "name":"Dua", "surname":"Lipa", "age":"28", "roles": '[{"id":"1", "roletype":"3", "group":"6"}]'},
{"id":"5", "name":"Jan", "surname":"Veliky", "age":"60", "roles": '[{"id":"1", "roletype":"2", "group":"2"}, {"id":"2", "roletype":"2", "group":"1"}]'},
{"id":"10", "name":"Petr", "surname":"Maly", "age":"25", "roles": '[{"id":"1", "roletype":"1", "group":"5"}, {"id":"2", "roletype":"1", "group":"3"}]'},
{"id":"19", "name":"Pavel", "surname":"Novotny", "age":"42", "roles": '[{"id":"1", "roletype":"2", "group":"6"}, {"id":"2", "roletype":"2", "group":"4"}]'},
{"id":"20", "name":"David", "surname":"Guetta", "age":"40", "roles": '[{"id":"1", "roletype":"3", "group":"5"}, {"id":"2", "roletype":"2", "group":"1"}, {"id":"2", "roletype":"2", "group":"3"}]'}]

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
    {"id":"1", "users_id":"1", "groups_id":"1"},
    {"id":"2", "users_id":"1", "groups_id":"3"},
    {"id":"3", "users_id":"1", "groups_id":"5"},
    {"id":"4", "users_id":"2", "groups_id":"1"},
    {"id":"5", "users_id":"2", "groups_id":"6"},
    {"id":"6", "users_id":"3", "groups_id":"1"},
    {"id":"7", "users_id":"3", "groups_id":"3"},
    {"id":"8", "users_id":"4", "groups_id":"1"},
    {"id":"9", "users_id":"4", "groups_id":"4"},
    {"id":"10", "users_id":"5", "groups_id":"5"},
    {"id":"11", "users_id":"10", "groups_id":"5"},
    {"id":"12", "users_id":"19", "groups_id":"5"},
    {"id":"13", "users_id":"20", "groups_id":"2"},
]