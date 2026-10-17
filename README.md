# JokeStore
**Django + PostgreSQL**
Microservice app that lets you create, get random and like a joke in PostgreSQL db

##To run:
```bash
docker compose up --build
```

- **WEB** `http://localhost:8000/`
- **Swagger UI:** `http://localhost:8000/swagger/`
- **OpenAPI:** `http://localhost:8000/api/schema/`

## API:
- `GET /api/story/random/` — Get random joke.
- `POST /api/story/create/` — Create new joke (`{"text": "joke"}`).
- `POST /api/story/<id>/rank/` — Increment the like counter for a specific story by its ID.