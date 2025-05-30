
## 🎬 VideoFlix Backend– Django Video Platform

VideoFlix is a Django REST API for managing and providing videos. The app uses PostgreSQL as a database and is fully containerized with Docker.

---

## 🚀 Features

- Upload videos, trailers & screenshots
- Genre-based video categorization
- Automatic deletion of video files when removed from the database
- Modern API with OpenAPI specification (Swagger)
- Fully executable in Docker

---

## 🛠️ Technologies
- Django & Django REST Framework
- PostgreSQL
- Docker & docker-compose
- pytest + pytest-django + coverage
- Swagger / OpenAPI for API-documentation

---

## 📦 `.env`-configuration

```env
# Django Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=adminpassword
DJANGO_SUPERUSER_EMAIL=admin@example.com

# Django Settings
SECRET_KEY="django-insecure-lp6h18zq4@z30symy*oz)+hp^uoti48r_ix^qc-m@&yfxd7&hn"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# PostgreSQL-Database
DB_NAME=videoflix
DB_USER=postgres
DB_PASSWORD=supersecret
DB_HOST=db
DB_PORT=5432

# Redis Cache
REDIS_HOST=redis
REDIS_LOCATION=redis://redis:6379/1
REDIS_PORT=6379
REDIS_DB=0

# E-Mail-configuration
EMAIL_HOST=your_email_host
EMAIL_PORT=your_email_port
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=default_from_email
```

---

## ⚠️ Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.10+ (if running locally)
- Git (optional, for cloning the repository)
- Internet connection (for package installation for the Docker build)
- Frontend: https://github.com/KevinMuellerDev/videoflix_frontend

---

## 🐳 Docker Quickstart

1. Clone project

    
```bash
    git clone https://github.com/dein-benutzername/videoflix.git
    cd videoflix
```

2. Start Container

    
```bash
    docker-compose up --build
```

3. Access to the app (standard port: 8000)

    [http://localhost:8000](http://localhost:8000)

---

## 🧪 Tests

Open container shell:

```bash
docker-compose up -d db web
docker-compose exec web /bin/sh
```

Then execute the following commands in the shell:
```bash
coverage run -m pytest
coverage report -m
```

---

## 📄 API-documentation

The API is documented on SwaggerHub:  
🔗 [https://app.swaggerhub.com/apis-docs/selfemployed-50f/videoflix/1.0.1](https://app.swaggerhub.com/apis-docs/selfemployed-50f/videoflix/1.0.1)

---

## 📁 Project structure
```
videoflix/
│
├── content_app/       # Django App with Models, Views, Signals ...
├── media/             # Video-Uploads
├── static/            # Static files
├── templates/         # HTML-Templates
├── manage.py          # Django Entrypoint
├── Dockerfile         # Web-App Dockerfile
├── docker-compose.yml # Docker-Services (App + DB)
└── README.md
```

---

## 📬 Contact

For questions or contributions:
**info@kevin-mueller-dev.de**
