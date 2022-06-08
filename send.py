import requests
import input


payload = {'query': input.ctl1}
#r = requests.post("http://127.0.0.9:8001/gql", json=payload) #mimo docker
r = requests.post("http://localhost:8001/gql", json=payload) #v dockeru


print(r.json())