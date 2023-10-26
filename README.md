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

**WARNING** : Yet the API is useless, just edit the python files and run them when you're finish, I'll develop this later
