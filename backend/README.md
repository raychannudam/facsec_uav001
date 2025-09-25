# Minimal Backend Setup Guide

This guide will help you set up and run the minimal backend application from scratch after cloning from GitHub.

## Prerequisites
- Python 3.12+
- PostgreSQL
- (Optional) Docker & Docker Compose

## 1. Clone the Repository
```sh
git clone <your-repo-url>
cd minimal-backend-setup
```

## 2. Install Python Dependencies
It is recommended to use a virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Environment Variables
Copy `.env.example` to `.env` and update values as needed:
```sh
cp .env.example .env
# Edit .env with your database and secret settings
```

## 4. Configure Database
- Ensure PostgreSQL is running and accessible.
- (Optional) Use Docker Compose:
  ```sh
  docker-compose up -d
  ```

## 5. Run Database Migrations
If using Alembic:
```sh
alembic upgrade head
```

## 6. Seed the Database
Run the seeding script to create default users and roles:
```sh
python db_seeding.py
```

## 7. Start the Application
```sh
uvicorn main:app --reload
```

## 8. API Usage
- Access the API at: `http://localhost:8000/api/v1/`
- Swagger docs: `http://localhost:8000/docs`

## 9. Default Credentials
- **Admin:**
  - Username: `admin`
  - Password: `adminpass`
- **User:**
  - Username: `user`
  - Password: `userpass`

---

## Troubleshooting
- Ensure your database is running and accessible.
- Check environment variables and connection strings.
- For Docker, ensure ports are not blocked.

---

## License
MIT
