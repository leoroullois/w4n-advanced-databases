# Advanced Databases Project

## Installation

First, you need to create a `.env` file with your credentials like :

```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=root

PGADMIN_DEFAULT_EMAIL=postgres@email.com
PGADMIN_DEFAULT_PASSWORD=root
```

Then, you need docker and you can run :

```bash
docker compose up --build
```

## Containers

There is multiple containers :

- **db** : PostgreSQL database - database is located under constant IPv4: 172.18.0.3
- **pgadmin** : Manage PostgreSQL database, run on `http://localhost:8888`
- **api** : API written in python, run on `http://localhost:5000`.

## API

- Count the number of rows in the tables :
```bash
curl --request GET \
  --url http://localhost:5000/count \
  --header 'User-Agent: insomnia/8.3.0'
```

- Delete all database data :
```bash
curl --request DELETE \
  --url http://localhost:5000/delete \
  --header 'User-Agent: insomnia/8.3.0'
```

- Task 3 (Fill database with fake data) :
```bash
curl --request PUT \
  --url http://localhost:5000/task3 \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/8.3.0' \
  --data '{ "NB_USERS": 100000, "NB_COMMENTS": 150000, "NB_POSTS": 200000, "NB_CUSTOMERS": 30000, "NB_SELLERS": 8000, "NB_EMPLOYEES": 1000, "NB_MODERATORS": 550, "NB_MANAGERS": 50, "NB_HUMAN_RESOURCES": 100, "NB_SALES_MODERATORS": 300 }'
```

- Task 4 (Monitor queries) :
```bash
curl --request PUT \
  --url http://localhost:5000/task4 \
  --header 'User-Agent: insomnia/8.3.0'
```

- Task 6 (Monitor queries with indexes) :
```bash
curl --request GET \
  --url http://localhost:5000/task5 \
  --header 'User-Agent: insomnia/8.3.0'
```
