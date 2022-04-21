import redis

users = redis.Redis(host="localhost", port=6379, db = 0, charset="utf-8", decode_responses=True)
cars = redis.Redis(host="localhost", port=6379, db = 1)

users.hset("1", "name", "Pavel")
users.hset("1", "age", "55")

users.hset("2", "name", "Petr")




jan = {"name":"Jan", "surname":"Veliky", "age":"99"}

users.hset("3", mapping=jan)
users.hset("3", "address", "Brno")


test = users.hgetall("3")



car0 = {"id":"5", "brand":"BMW", "type":"450d"}
car1 = {"id":"10", "brand":"Audi", "type":"A4"}

cars.hset(car0["id"], mapping=car0)

cars.hset(5, "fuel", "diesel")

keys = users.keys()

for i in range(0, len(keys)):
    keys[i] = int(keys[i])

print(users.hgetall(keys[0]))