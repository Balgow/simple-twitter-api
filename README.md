# Twitter Data API

A RESTful API service that provides Twitter data through two main endpoints: hashtag search and user timeline retrieval. Built with Python and FastAPI, following best practices for production-ready applications.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Future Enhancements](#future-enhancements)

## Features

- ✅ **RESTful API** with two main endpoints
- ✅ **FastAPI Framework**: Modern, fast, high-performance web framework
- ✅ **Automatic API Documentation**: Interactive docs (Swagger UI & ReDoc)
- ✅ **Hashtag Search**: Retrieve tweets by hashtag
- ✅ **User Timeline**: Get tweets from a specific user
- ✅ **Configurable Limits**: Customizable number of tweets returned (default: 30)
- ✅ **Comprehensive Testing**: Unit tests with pytest
- ✅ **Clean Architecture**: Separation of concerns with service layer pattern
- ✅ **Extensible Design**: Easy to swap implementations (mock → real scraping → API)
- ✅ **Input Validation**: Pydantic models and automatic validation
- ✅ **Type Hints**: Full type annotations for better code quality
- ✅ **Production Ready**: Configuration management for different environments
- ✅ **Async Support**: Built-in async capabilities for better performance

## Architecture

The application follows a layered architecture pattern:

```
┌─────────────────────────────────────┐
│      FastAPI Layer (Routers)        │
│   - Hashtags Router                 │
│   - Users Router                    │
│   - Automatic Validation            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Business Logic Layer           │
│   - Input Validation (Pydantic)     │
│   - Error Handling                  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        Service Layer                │
│   - TwitterService (Interface)      │
│   - TwitterMockService (Impl)       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Data Models                 │
│   - Tweet                           │
│   - Account                         │
└─────────────────────────────────────┘
```

### Design Principles

1. **Dependency Inversion**: Service layer uses abstract interfaces
2. **Single Responsibility**: Each module has a clear, focused purpose
3. **Open/Closed**: Easy to extend without modifying existing code
4. **Testability**: All components are independently testable

## Requirements

- **Python**: 3.11, 3.12, or 3.13
- **pip**: For package management
- **Virtual environment**: Recommended for isolation

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure X API (Optional)

The application works in two modes:

**Mock Mode (Default)**: Uses sample data, no API keys needed
- Perfect for development and testing
- No costs or rate limits
- Works out of the box

**Real API Mode**: Connects to actual X (Twitter) API v2
- Requires X Developer account and Bearer Token
- See [SETUP_X_API.md](SETUP_X_API.md) for detailed setup guide
- Get credentials at [developer.x.com](https://developer.x.com)

To enable real API mode:

```bash
# Set your X API Bearer Token
export TWITTER_BEARER_TOKEN="your_bearer_token_here"

# The app automatically detects the token and switches to real API
```

**Quick Setup:**
1. Sign up at [developer.x.com](https://developer.x.com)
2. Create an app and get your Bearer Token
3. Set environment variable: `export TWITTER_BEARER_TOKEN="your_token"`
4. Run the application - it will automatically use real data!

For complete setup instructions, see [SETUP_X_API.md](SETUP_X_API.md)

## Running the Application

### Development Mode

```bash
python run.py
```

The application will start on `http://localhost:5000`

You can access:
- API endpoints at `http://localhost:5000`
- Interactive API documentation (Swagger UI) at `http://localhost:5000/docs`
- Alternative API documentation (ReDoc) at `http://localhost:5000/redoc`

### Production Mode

```bash
export FLASK_ENV=production
export PORT=8000
uvicorn run:app --host 0.0.0.0 --port 8000
```

Or using the run.py script:

```bash
export FLASK_ENV=production
export PORT=8000
python run.py
```

### Using Custom Port

```bash
export PORT=8080
python run.py
```

## API Endpoints

### 1. Get Tweets by Hashtag

Retrieve tweets containing a specific hashtag.

**Endpoint**: `GET /hashtags/<hashtag>`

**Parameters**:
- `hashtag` (path, required): The hashtag to search for (without # symbol)
- `limit` (query, optional): Number of tweets to retrieve (default: 30, min: 1, max: 100)

**Example Request**:
```bash
curl -H "Accept: application/json" -X GET http://localhost:5000/hashtags/Python?limit=40
```

**Example Response**:
```json
[
  {
    "account": {
      "fullname": "Raymond Hettinger",
      "href": "/raymondh",
      "id": 14159138
    },
    "date": "12:57 PM - 7 Mar 2018",
    "hashtags": ["#python"],
    "likes": 169,
    "replies": 13,
    "retweets": 27,
    "text": "Historically, bash filename pattern matching was known as \"globbing\". Hence, the #python module called \"glob\"."
  }
]
```

**Error Responses**:
- `400 Bad Request`: Invalid parameters
- `422 Unprocessable Entity`: Validation error (FastAPI automatic validation)
- `500 Internal Server Error`: Service error

### 2. Get User Tweets

Retrieve tweets from a specific user's timeline.

**Endpoint**: `GET /users/<username>`

**Parameters**:
- `username` (path, required): Twitter username (without @ symbol)
- `limit` (query, optional): Number of tweets to retrieve (default: 30, min: 1, max: 100)

**Example Request**:
```bash
curl -H "Accept: application/json" -X GET http://localhost:5000/users/twitter?limit=20
```

**Example Response**:
```json
[
  {
    "account": {
      "fullname": "Twitter",
      "href": "/Twitter",
      "id": 783214
    },
    "date": "2:54 PM - 8 Mar 2018",
    "hashtags": ["#InternationalWomensDay"],
    "likes": 287,
    "replies": 17,
    "retweets": 70,
    "text": "Powerful voices. Inspiring women.\n\n#InternationalWomensDay"
  }
]
```

**Error Responses**:
- `400 Bad Request`: Invalid parameters
- `422 Unprocessable Entity`: Validation error (FastAPI automatic validation)
- `500 Internal Server Error`: Service error

### 3. Health Check

Check if the service is running.

**Endpoint**: `GET /health`

**Example Request**:
```bash
curl http://localhost:5000/health
```

**Example Response**:
```json
{
  "status": "healthy"
}
```

## Testing

The project includes comprehensive unit tests covering all components.

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

This generates a coverage report in `htmlcov/index.html`

### Run Specific Test Files

```bash
# Test API endpoints
pytest tests/test_api.py

# Test services
pytest tests/test_services.py

# Test models
pytest tests/test_models.py

# Test validators
pytest tests/test_validators.py
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Test Coverage

The test suite covers:
- ✅ All API endpoints (success and error cases)
- ✅ Service layer implementations
- ✅ Data models and serialization
- ✅ Input validation logic
- ✅ Error handling
- ✅ Edge cases and boundary conditions

## Project Structure

```
├── app/
│   ├── __init__.py              # FastAPI application factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── tweet.py             # Tweet and Account data models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── hashtags.py          # Hashtag router
│   │   └── users.py             # User router
│   ├── services/
│   │   ├── __init__.py          # Service factory (auto-selects mock vs real)
│   │   ├── twitter_service.py   # Service interface (abstract)
│   │   ├── twitter_mock_service.py      # Mock implementation
│   │   └── twitter_api_service.py       # Real X API v2 implementation
│   └── utils/
│       ├── __init__.py
│       └── validators.py        # Input validation utilities
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration (FastAPI TestClient)
│   ├── test_api.py              # API endpoint tests
│   ├── test_models.py           # Model tests
│   ├── test_services.py         # Service tests (mock)
│   ├── test_twitter_api_service.py  # Service tests (real API)
│   └── test_validators.py       # Validator tests
├── config.py                    # Configuration management
├── run.py                       # Application entry point (Uvicorn)
├── requirements.txt             # Python dependencies
├── env.example                  # Environment variables template
├── SETUP_X_API.md              # Complete X API setup guide
├── .gitignore                   # Git ignore rules
└── README.md                    # This file (main documentation)
```

## Configuration

The application supports multiple configuration environments:

- **Development**: Debug mode enabled, verbose logging
- **Testing**: Isolated configuration for tests
- **Production**: Optimized for production deployment

Configuration is managed in `config.py` and can be changed via environment variables:

```bash
# Set environment
export FLASK_ENV=development  # or testing, production

# Set port
export PORT=8000

# Set request timeout
export REQUEST_TIMEOUT=10
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `DEFAULT_TWEET_LIMIT` | Default number of tweets | 30 |
| `MAX_TWEET_LIMIT` | Maximum tweets per request | 100 |
| `MIN_TWEET_LIMIT` | Minimum tweets per request | 1 |
| `REQUEST_TIMEOUT` | HTTP request timeout (seconds) | 10 |

## Implementation Notes

### Service Architecture - Mock vs Real API

The application includes **two service implementations**:

#### 1. TwitterMockService (Default)
- ✅ **No setup required** - works out of the box
- ✅ **No API costs** - completely free
- ✅ **No rate limits** - unlimited requests
- ✅ **Realistic data** - generates sample tweets with proper structure
- ✅ **Perfect for development** and testing
- ⚠️ **Mock data only** - not connected to real X/Twitter

#### 2. TwitterAPIService (Production)
- ✅ **Real X API v2 integration** - actual live data
- ✅ **Official API** - reliable and supported
- ✅ **Recent tweets** - real-time data
- ⚠️ **Requires Bearer Token** from [developer.x.com](https://developer.x.com)
- ⚠️ **Has rate limits** based on your tier (Free: 100 reads/month, Basic: 10K/month, Pro: 1M/month)
- ⚠️ **May have costs** ($0 for Free tier, $200+ for paid tiers)

### Automatic Service Selection

The application **automatically switches** between services:

```python
# In app/services/__init__.py
def get_twitter_service():
    if os.getenv('TWITTER_BEARER_TOKEN'):
        return TwitterAPIService()  # ← Real X API v2
    else:
        return TwitterMockService()  # ← Mock data
```

**How it works:**
- 🔍 Checks if `TWITTER_BEARER_TOKEN` environment variable is set
- ✅ **With token**: Uses real X API v2 → live data
- ❌ **Without token**: Uses mock service → sample data
- 🔄 **No code changes needed** - same API interface

### Setting Up Real X API

See [SETUP_X_API.md](SETUP_X_API.md) for complete setup guide.

**Quick start:**
```bash
# 1. Get your token from https://developer.x.com
# 2. Set environment variable
export TWITTER_BEARER_TOKEN="your_bearer_token_here"

# 3. Run application - it automatically uses real API!
python run.py
```

### X API Access Levels

| Tier | Cost | Reads/Month | Best For |
|------|------|-------------|----------|
| **Free** | $0 | 100 | Testing |
| **Basic** | $200/mo | 10,000 | Small apps |
| **Pro** | $5,000/mo | 1,000,000 | Production |
| **Enterprise** | Custom | Unlimited | Enterprise |

📖 More info: [developer.x.com/en/docs/x-api](https://developer.x.com/en/docs/x-api)

## FastAPI Features

This application leverages FastAPI's powerful features:

### Automatic Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: Available at `/docs`
  - Try out API calls directly from the browser
  - See request/response schemas
  - Test different parameters

- **ReDoc**: Available at `/redoc`
  - Alternative documentation interface
  - Clean, three-panel design
  - Easy to navigate

### Automatic Request Validation

FastAPI automatically validates:
- Path parameters (e.g., `hashtag`, `username`)
- Query parameters (e.g., `limit` with min/max constraints)
- Request body (if needed in future)
- Response models

Invalid requests return clear error messages with details about what went wrong.

### Type Safety

- Full type hints throughout the codebase
- IDE auto-completion and error detection
- Runtime type validation
- Better code maintainability

## Future Enhancements

Potential features for future development:

- [ ] **Authentication**: Add API key authentication (FastAPI security utilities)
- [ ] **Rate Limiting**: Implement request throttling
- [ ] **Caching**: Cache responses to reduce load
- [ ] **Database**: Store tweets for historical analysis
- [ ] **Pagination**: Add cursor-based pagination
- [ ] **Filtering**: Advanced filtering (date range, engagement metrics)
- [ ] **WebSocket Support**: Real-time updates for live tweets (FastAPI native support)
- [ ] **Background Tasks**: Async data fetching with FastAPI BackgroundTasks
- [ ] **Analytics**: Aggregate statistics and trending data
- [ ] **Docker**: Containerization for easy deployment
- [ ] **CI/CD**: Automated testing and deployment pipeline
- [ ] **Monitoring**: Logging and metrics (Prometheus, Grafana)

## Development Guidelines

### Code Style

- Follow **PEP 8** style guide
- Use **type hints** for all functions
- Write **docstrings** for all public methods
- Keep functions **small and focused**

### Testing Guidelines

- Maintain **high test coverage** (>80%)
- Test both **success and failure** cases
- Use **meaningful test names**
- Keep tests **independent** and **idempotent**

### Git Workflow

1. Create feature branch from `main`
2. Make changes with descriptive commits
3. Run tests before committing
4. Create pull request with description
5. Merge after review and passing CI

## Troubleshooting

### Port Already in Use

If port 5000 is already in use:
```bash
export PORT=8080
python run.py
```

### Import Errors

Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Test Failures

Run tests with verbose output to see details:
```bash
pytest -v -s
```

## License

This project is created for the AnyMind Group technical assessment.

## Author

Developed as part of the Python Engineer position application for AnyMind Group.

## Contact

For questions or issues, please open an issue in the repository.

