# 🤖 Robot Payment Testing Platform

## About The Project

**Automated payment terminal testing platform** that simulates robotic payment testing for retail environments. Built with clean architecture following Repository Pattern and Dependency Injection.

### Key Features

| Feature                   | Description                                    |
| ------------------------- | ---------------------------------------------- |
| 🔐 **JWT Authentication** | Secure login with 30-minute access tokens      |
| 🤖 **Robot Management**   | CRUD operations for T1, T4, ATM, MOBILE robots |
| 💳 **Payment Simulation** | Simulate tap, chip, and swipe payments         |
| 🐳 **Docker Compose**     | One-command development environment            |
| 📊 **CI/CD Pipeline**     | Automated linting, testing, type checking      |
| 📝 **OpenAPI Docs**       | Auto-generated Swagger UI at `/docs`           |

## Architecture

| Feature                   | Description                       |
| ------------------------- | --------------------------------- |
| **API LAYER (FastAPI)**   | Handles HTTP requests, validation |
| **SERVICE LAYER**         | Business logic, orchestration     |
| **REPOSITORY LAYER**      | Database operations, CRUD         |
| **DATABASE (PostgreSQL)** | Data persistence                  |

### Technology Stack

| Layer         | Technology   | Version |
| ------------- | ------------ | ------- |
| Web Framework | FastAPI      | 0.115.0 |
| ORM           | SQLAlchemy   | 2.0.35  |
| Database      | PostgreSQL   | 16      |
| Auth          | JWT + PBKDF2 | -       |
| Container     | Docker       | 24+     |
| Testing       | Pytest       | 9.0.3   |

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development)

### Run with Docker (Recommended)

```bash
# Clone repository
git clone git@gitlab.com:alexvlasov182/robot-payment.git
cd robot-payment

# Copy environment file
cp .env.example .env

# Edit SECRET_KEY in .env
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"

# Start everything
docker-compose up -d

# Check health
curl http://localhost:8000/health
```

## Run Locally

```bash
# Create virtual evnironment
python -m venv .venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=sqlite:///./test.db
export SECRET_KEY=your-secret-key-here

# Run
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication

| Method | Endpoint              | Description     |
| ------ | --------------------- | --------------- |
| POST   | /api/v1/auth/register | Create new user |
| POST   | /api/v1/auth/login    | Get JWT token   |

### Robots (Requires Auth)

| Method | Endpoint                   | Description         |
| ------ | -------------------------- | ------------------- |
| POST   | /api/v1/robots/            | Create robot        |
| GET    | /api/v1/robots/            | List all robots     |
| GET    | /api/v1/robots/{id}        | GET robot by ID     |
| PATCH  | /api/v1/robots/{id}/status | Update robot status |
| DELETE | /api/v1/robots/{id}        | Delete robot        |

### Terminal Testing

| Method | Endpoint                             | Description        |
| ------ | ------------------------------------ | ------------------ |
| POST   | /api/v1/terminals/test               | Simulate payment   |
| GET    | /api/v1/terminals/mcdonalds          | McDonald's test    |
| GET    | /api/v1/terminals/grocery/regression | Grocery regression |

## Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run linting
make lint

# Format code
make format

# Type checking
make type

# Run everything in Docker
make docker-quality
```

## Docker Commands

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# View API logs
docker-compose logs -f api

# Enter container
docker exec -it robot-api bash
```

## Project Structure

```bash
robot-payment/
├── app/
│   ├── api/v1/          # REST endpoints
│   │   ├── auth.py      # Authentication
│   │   ├── robots.py    # Robot CRUD
│   │   ├── terminals.py # Payment simulation
│   │   └── health.py    # Health checks
│   ├── core/            # Core infrastructure
│   │   ├── config.py    # Settings (Pydantic)
│   │   ├── database.py  # SQLAlchemy setup
│   │   └── security.py  # JWT, password hashing
│   ├── models/          # SQLAlchemy models
│   │   ├── user.py
│   │   └── robot.py
│   ├── repositories/    # Repository pattern
│   │   ├── base.py      # Generic CRUD
│   │   ├── user_repository.py
│   │   └── robot_repository.py
│   ├── schemas/         # Pydantic validation
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── robot.py
│   │   └── terminal.py
│   ├── services/        # Business logic
│   │   ├── auth_service.py
│   │   ├── robot_service.py
│   │   └── terminal_services.py
│   └── tests/           # Unit tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitlab-ci.yml
```

## Environment Variables

| Variable     | Description                  | Required |
| ------------ | ---------------------------- | -------- |
| SECRET_KEY   | JWT signing key (32+ char)   | ✅       |
| DATABASE_URL | PostgreSQL connection string | ✅       |
| APP_ENV      | development/staging/prod     | ❌       |
| DEBUG        | Enable debug mode            | ❌       |

## Design Patterns Used

### 1. Repository Pattern

```python
class BaseRepository(Generic[ModelTypeT, CreateSchemaT, UpdateSchemaT ]):
  def create(self, obj_in: CreateSchemaT) -> ModelTypeT
    # Generic CRUD operations
```

### 2. Dependency Injection

```python
async def register(
  user_data: UserRegister,
  auth_service: AuthService = Depends(get_auth_service)
):
    # FastAPI injects dependencies automatically
```

### 3. Service Layer Pattern

```python
class AuthService:
  def register_user(self, email: str, password: str) -> dict:
    # Business logic isolated from API and database
```

## Test Coverage

```bash
Name                            Stmts   Miss  Cover
---------------------------------------------------
app/api/v1/auth.py                23      8    65%
app/api/v1/robots.py              13      3    77%
app/api/v1/terminals.py           13      4    69%
app/core/security.py              14      5    64%
app/services/auth_service.py      19      5    74%
---------------------------------------------------
TOTAL                             209     49    77%
```

## CI/CD Pipeline (GitLab CI)

The pipeline runs automatically on every push

1. **Lint** - Ruff checks code style
2. **Test** - Pytest with coverage

## Main endpoints

### 1. Health check

curl http://localhost:8000/health

### 2. Register user

curl -X POST http://localhost:8000/api/v1/auth/register \
-H "Content-Type: application/json" \
-d '{"email":"interview123@test.com","password":"123456","confirm_password":"123456"}'

### 3. Login

TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
 -H "Content-Type: application/json" \
 -d '{"email":"interview@test.com","password":"123456"}' \
 | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")

### 4. Create a robot

curl -X POST http://localhost:8000/api/v1/robots \
 -H "Authorization: Bearer $TOKEN" \
 -H "Content-Type: application/json" \
 -d '{"name":"Robot T4","serial_number":"T4-001","robot_type":"T4","capabilities":"tap,chip,swipe"}'

### 5. List robots

curl -X GET http://localhost:8000/api/v1/robots/ \
 -H "Authorization: Bearer $TOKEN"

### 6. Test McDonald's terminal

curl http://localhost:8000/api/v1/terminals/mcdonalds

### 7. Simulate payment

curl -X POST http://localhost:8000/api/v1/terminals/test \
 -H "Content-Type: application/json" \
 -d '{"terminal_id":101,"amount":12.95,"payment_method":"tap"}'

### 8. Show API documentation

echo "Open http://localhost:8000/docs in your browser"

## License

MIT

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Database [PostgreSQL](https://www.postgresql.org/)
- Containerization [Docker](https://www.docker.com/)

## Contact

- Oleksandr(Sascha) Vlasov - drumlife182@gmail.com
- Project Link: [Robot Payment](https://gitlab.com/alexvlasov182/robot-payment)
- Personal web-page: [Oleksandr Vlasov](https://oleksandr-vlasov.com/)
