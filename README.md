# Semantic Document Search

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

API available at `http://127.0.0.1:8000`

## Endpoints

- `POST /documents` — store a document (`title`, `content`)
- `GET /documents/search?q=<query>&top_k=<n>` — search by semantic similarity (`top_k` optional, default 5)
- `DELETE /documents/{id}` — delete a document by ID

## Run tests

```bash
python3 -m pytest -v
```