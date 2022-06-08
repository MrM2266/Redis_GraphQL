# Redis_GraphQL
Aplikace bez dockeru 
- vyžaduje běžící redis - nejlépe jako kontejner v dockeru - je třeba upravit connection string v database.py
- lze spouštět gql.py a nechat provádět jedntlivé queries (např. z input.py)

Verze s podporou FastAPI a dockeru
- ve složce Docker version je upravená verze s FastAPI - pro spuštení mimo docker:
- uvicorn gql:app --host 127.0.0.9 --port 8001
- pro spuštění v dockeru - vytvoříme podle dockerfile image gql_redis:
- docker build -t gql_redis .
- pomocí docker-compose.yml vytvoříme a spustíme kontejner:
- docker-compose -p redis_gql_DB up
- aplikace bude dostupná na http://localhost:8001/gql

Odesílnání dat do aplikace
- pro odeílání dat do FastAPI (v dockeru nebo mimo něj) lze použít send.py
- zde lze vybrat předdefinované queries a mutations z input.py
