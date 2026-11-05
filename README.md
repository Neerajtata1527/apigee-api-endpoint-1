# Employee Management CRUD API

A small, stateful REST API for practising Postman and later API-gateway development.

- FastAPI backend
- SQLAlchemy ORM
- PostgreSQL on Render
- SQLite by default for local quick-start
- Real database inserts, reads, updates and deletes
- OpenAPI documentation at `/docs`

> Use dummy data only. This starter project has no authentication or authorization and should not be exposed with sensitive employee information.

## 1. Run locally (SQLite)

Requires Python 3.10+.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

The local SQLite database file `employees.db` is created automatically.

## 2. Postman requests

Set a Postman environment variable:

```text
base_url = http://127.0.0.1:8000
```

For JSON requests, use **Body > raw > JSON** and the header `Content-Type: application/json`.

### Create employee

`POST {{base_url}}/employees`

```json
{
  "name": "Neeraj",
  "department": "IT",
  "salary": 35000
}
```

Expected: `201 Created`. Copy the returned `id`.

### List employees

`GET {{base_url}}/employees`

Optional pagination:

`GET {{base_url}}/employees?skip=0&limit=20`

### Get one employee

`GET {{base_url}}/employees/1`

Replace `1` with the ID returned by POST.

### Replace employee (PUT)

`PUT {{base_url}}/employees/1`

PUT requires all fields:

```json
{
  "name": "Neeraj Kumar",
  "department": "Software",
  "salary": 45000
}
```

### Partially update employee (PATCH)

`PATCH {{base_url}}/employees/1`

Only send fields to change:

```json
{
  "salary": 50000
}
```

### Delete employee

`DELETE {{base_url}}/employees/1`

Expected: `204 No Content`. A subsequent GET for that ID should return `404 Not Found`.

## 3. Deploy to Render

1. Push this folder to a GitHub repository.
2. In Render, choose **New > Blueprint** and connect the repository. Render reads `render.yaml`.
3. The Blueprint defines a FastAPI web service and a PostgreSQL database, then injects the database connection string as `DATABASE_URL`.
4. Wait for deployment. Render provides a public HTTPS URL such as `https://your-service-name.onrender.com`.
5. Test `https://your-service-name.onrender.com/health` and `/docs`.
6. In Postman, set `base_url` to your Render URL and repeat the requests above.

If Render does not offer the `free` database plan for your account/region, select an available PostgreSQL plan in the dashboard and redeploy. Check current pricing and database expiry/retention rules before relying on a free database.

### Important deployment notes

- Render free web services may spin down after inactivity, so the first request can be slow.
- Do not use SQLite on a free Render web service for persistent data; its filesystem is ephemeral. This project uses the PostgreSQL `DATABASE_URL` provided by Render.
- Free PostgreSQL offerings may have expiry, storage and usage limits. Confirm the current terms in Render's dashboard.
- Do not commit `.env` files, passwords or database credentials.
- This project intentionally has no authentication to keep API-gateway practice simple. Anyone who discovers the public URL can call the endpoints. Use dummy records only, and add authentication before any real use.

## 4. Endpoints

| Method | Path | Purpose | Success |
|---|---|---|---|
| GET | `/employees` | List employees | 200 |
| GET | `/employees/{id}` | Get one employee | 200 |
| POST | `/employees` | Create employee | 201 |
| PUT | `/employees/{id}` | Replace all editable fields | 200 |
| PATCH | `/employees/{id}` | Update supplied fields only | 200 |
| DELETE | `/employees/{id}` | Delete employee | 204 |

Common errors:

- `400`: invalid pagination or empty PATCH
- `404`: employee does not exist
- `422`: request body or path parameter failed validation

## 5. Verify persistence

Create an employee, stop and restart the local API, then GET the employee again. The record remains in `employees.db`.

For the Render deployment, PostgreSQL stores the records independently of the web-service process.
