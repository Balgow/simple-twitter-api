# Twitter Data API

RESTful API service for retrieving Twitter/X data. Built with **Python 3.11+ and FastAPI**.

## Features

- ✅ RESTful API with hashtag search and user timeline endpoints
- ✅ FastAPI with automatic interactive documentation
- ✅ Custom X API v2 implementation (no public SDK)
- ✅ Mock service for development (works without API keys)
- ✅ Real X API integration (production-ready)
- ✅ Comprehensive unit tests (38 tests)
- ✅ Clean architecture with service layer pattern

## Requirements

- Python 3.11, 3.12, or 3.13
- pip for package management

## Quick Start

### 1. Clone and Install

```bash
git clone <repository-url>
cd anymind-twitter-api
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Application

```bash
python run.py
```

The API will start at `http://localhost:5000`

**Access:**
- API Endpoints: `http://localhost:5000`
- Interactive Docs: `http://localhost:5000/docs`
- Alternative Docs: `http://localhost:5000/redoc`

### 3. Test Endpoints

```bash
# Get tweets by hashtag
curl http://localhost:5000/hashtags/python?limit=5

# Get user tweets
curl http://localhost:5000/users/elonmusk?limit=5

# Health check
curl http://localhost:5000/health
```

## API Endpoints

### 1. GET /hashtags/{hashtag}

Get tweets containing a specific hashtag.

**Parameters:**
- `hashtag` (path, required): Hashtag to search (without #)
- `limit` (query, optional): Number of tweets (default: 30, min: 1, max: 100)

**Example:**
```bash
curl http://localhost:5000/hashtags/python?limit=10
```

**Response:**
```json
[
  {
    "account": {
      "fullname": "Raymond Hettinger",
      "href": "/raymondh",
      "id": 14159138
    },
    "date": "12:57 PM - 7 Mar 2018",
    "text": "Historically, bash filename pattern matching...",
    "replies": 13,
    "retweets": 27,
    "likes": 169,
    "hashtags": ["#python"]
  }
]
```

### 2. GET /users/{username}

Get tweets from a user's timeline.

**Parameters:**
- `username` (path, required): Twitter username (without @)
- `limit` (query, optional): Number of tweets (default: 30, min: 1, max: 100)

**Example:**
```bash
curl http://localhost:5000/users/twitter?limit=10
```

**Response:** Same format as hashtag endpoint

## Architecture

### Clean Architecture Pattern

```
┌─────────────────────────────────────┐
│      FastAPI Layer (Routers)        │
│   - Hashtags Router                 │
│   - Users Router                    │
│   - Automatic Validation            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        Service Layer                │
│   - TwitterService (Interface)      │
│   - TwitterMockService              │
│   - TwitterAPIService (X API v2)    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Data Models                 │
│   - Tweet                           │
│   - Account                         │
└─────────────────────────────────────┘
```

### Project Structure

```
anymind-twitter-api/
├── app/
│   ├── __init__.py           # FastAPI app factory
│   ├── models/
│   │   └── tweet.py          # Data models
│   ├── routes/
│   │   ├── hashtags.py       # Hashtag endpoint
│   │   └── users.py          # User endpoint
│   ├── services/
│   │   ├── twitter_service.py         # Abstract interface
│   │   ├── twitter_mock_service.py    # Mock implementation
│   │   └── twitter_api_service.py     # Real X API v2
│   └── utils/
│       └── validators.py     # Input validation
├── tests/                    # Unit tests
├── config.py                 # Configuration
├── run.py                    # Entry point
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Testing

### Run Tests

```bash
# All tests
pytest

# Verbose output
pytest -v

# With coverage
pytest --cov=app
```

### Test Coverage

- ✅ 38 tests passing
- ✅ API endpoint tests (success and error cases)
- ✅ Service layer tests
- ✅ Data model tests
- ✅ Input validation tests

## Configuration

The application automatically switches between mock and real data:

### Mock Mode (Default)
- No setup required
- Uses realistic sample data
- Perfect for development/testing

### Real X API Mode (Optional)

To use real Twitter/X data:

1. **Get X API Bearer Token:**
   - Sign up at [developer.x.com](https://developer.x.com)
   - Create an app
   - Get Bearer Token from "Keys and tokens" section

2. **Set Environment Variable:**

Create `.env` file:
```bash
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

Or export directly:
```bash
export TWITTER_BEARER_TOKEN="your_bearer_token_here"
```

3. **Run Application:**
```bash
python run.py
```

The app automatically detects the token and uses real X API!

**Note:** Free tier has 100 reads/month. [Learn more](https://developer.x.com/en/docs/x-api)

## Implementation Details

### X API v2 Integration

- ✅ Custom implementation (no public SDK per requirements)
- ✅ Bearer Token authentication (OAuth 2.0)
- ✅ Endpoints used:
  - `/2/tweets/search/recent` - Search tweets
  - `/2/users/by/username/:username` - User lookup
  - `/2/users/:id/tweets` - User timeline
- ✅ Comprehensive error handling (401, 403, 429, 500)
- ✅ Rate limit detection

### Design Patterns

- **Factory Pattern**: Automatic service selection
- **Strategy Pattern**: Swappable implementations
- **Dependency Inversion**: Routes depend on abstractions
- **Repository Pattern**: Service layer abstracts data access

### Code Quality

- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ PEP 8 compliant
- ✅ SOLID principles
- ✅ Clean code practices

## Dependencies

```
fastapi==0.104.1          # Web framework
uvicorn[standard]==0.24.0 # ASGI server
requests==2.31.0          # HTTP client
pytest==7.4.3             # Testing framework
httpx==0.25.1             # Async HTTP (for tests)
python-dotenv==1.0.0      # Environment variables
```

## Production Deployment

```bash
# Using uvicorn directly
uvicorn run:app --host 0.0.0.0 --port 8000 --workers 4

# Or using the run script
export PORT=8000
export FLASK_ENV=production
python run.py
```

## License

This project is created for the AnyMind Group technical assessment.

## Author

Developed for the Python Engineer position application at AnyMind Group.
