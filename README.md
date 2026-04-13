# Django Backend Practice API

Production-style Django backend starter featuring a Notes CRUD JSON API, health checks, validation,
and automated tests. This repository is designed as a clean backend practice project that can be
extended into larger API systems.

## Features

- Django 5 project scaffold with a dedicated app (`notes`)
- JSON REST-style endpoints for create/read/update/delete flows
- Status-based filtering support (`todo`, `in_progress`, `done`)
- Input validation and clear error responses
- Django admin integration for data inspection
- Automated test suite with API-level coverage

## API Endpoints

- `GET /api/health/`
- `GET /api/notes/`
- `POST /api/notes/`
- `GET /api/notes/<id>/`
- `PUT /api/notes/<id>/`
- `DELETE /api/notes/<id>/`

## Quick Start

```bash
git clone https://github.com/sakib-maho/django-backend-practice.git
cd django-backend-practice
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open: `http://127.0.0.1:8000/api/health/`

## Run Tests

```bash
python manage.py test
```

## Project Structure

```text
django-backend-practice/
├── backend_api/
├── notes/
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── manage.py
└── requirements.txt
```

## License

MIT License. See `LICENSE`.
