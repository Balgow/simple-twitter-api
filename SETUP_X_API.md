# Setting Up Real X (Twitter) API Integration

This guide will walk you through setting up real X API access for this application.

## Overview

The application automatically detects if you have X API credentials configured:
- **With credentials**: Uses real X API v2
- **Without credentials**: Uses mock service (for development/testing)

## Step 1: Create X Developer Account

1. Go to [X Developer Portal](https://developer.x.com)
2. Sign in with your X (Twitter) account
3. Apply for a developer account (usually instant approval for Free tier)

## Step 2: Choose Access Level

Select the tier that fits your needs:

| Tier | Cost | Reads/Month | Best For |
|------|------|-------------|----------|
| **Free** | $0 | 100 | Testing only |
| **Basic** | $200/month | 10,000 | Hobbyists/Prototypes |
| **Pro** | $5,000/month | 1,000,000 | Startups/Production |
| **Enterprise** | Custom | Unlimited | Large scale |

📖 [More details on access levels](https://developer.x.com/en/docs/x-api)

## Step 3: Create an App

1. In the [X Developer Portal](https://developer.x.com), navigate to **Projects & Apps**
2. Click **Create App** or **Create Project**
3. Fill in the required information:
   - **App name**: Choose a unique name (e.g., "twitter-data-api")
   - **Description**: Describe your application
   - **Use case**: Select appropriate category

## Step 4: Get Your Bearer Token

After creating your app:

1. Go to your app's **Keys and tokens** section
2. Under **Authentication Tokens**, find **Bearer Token**
3. Click **Generate** or **Regenerate** if needed
4. **Copy the Bearer Token** (you won't see it again!)

⚠️ **Important**: Keep your token secure. Never commit it to version control.

## Step 5: Configure the Application

### Option A: Using Environment Variable (Recommended)

```bash
# Linux/Mac
export TWITTER_BEARER_TOKEN="your_bearer_token_here"

# Windows (Command Prompt)
set TWITTER_BEARER_TOKEN=your_bearer_token_here

# Windows (PowerShell)
$env:TWITTER_BEARER_TOKEN="your_bearer_token_here"
```

### Option B: Using .env File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your token:
   ```bash
   TWITTER_BEARER_TOKEN=your_actual_bearer_token_here
   ```

3. Install python-dotenv (if not already):
   ```bash
   pip install python-dotenv
   ```

4. Load environment variables in `run.py`:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Step 6: Test Your Configuration

### Test with curl:

```bash
curl -X GET "https://api.twitter.com/2/tweets/search/recent?query=python&max_results=10" \
  -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```

### Test the Application:

```bash
# Start the application
python run.py

# Test hashtag endpoint
curl http://localhost:5000/hashtags/python?limit=5

# Test user endpoint  
curl http://localhost:5000/users/twitter?limit=5
```

If configured correctly, you'll get real data from X!

## API Endpoints Used

This application uses the following X API v2 endpoints:

### 1. Recent Search
- **Endpoint**: `GET /2/tweets/search/recent`
- **Purpose**: Search tweets by hashtag
- **Access**: Free tier has access (with limits)
- **Docs**: https://developer.x.com/en/docs/twitter-api/tweets/search/api-reference

### 2. User Lookup
- **Endpoint**: `GET /2/users/by/username/:username`
- **Purpose**: Get user ID from username
- **Access**: Available on all tiers
- **Docs**: https://developer.x.com/en/docs/twitter-api/users/lookup/api-reference

### 3. User Timeline
- **Endpoint**: `GET /2/users/:id/tweets`
- **Purpose**: Get tweets from user timeline
- **Access**: Available on all tiers
- **Docs**: https://developer.x.com/en/docs/twitter-api/tweets/timelines/api-reference

## Rate Limits

### Free Tier Limits:
- 100 reads per month (total across all endpoints)
- Resets monthly

### Basic Tier Limits:
- 10,000 reads per month
- Rate limit: Variable based on endpoint

### Handling Rate Limits:

The application automatically detects rate limit errors (HTTP 429) and returns helpful messages.

To check your rate limit status:
```bash
curl -X GET "https://api.twitter.com/2/tweets/search/recent?query=test" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -I
```

Look for headers:
- `x-rate-limit-limit`: Your rate limit
- `x-rate-limit-remaining`: Requests remaining
- `x-rate-limit-reset`: When limit resets (Unix timestamp)

## Troubleshooting

### Error: "Authentication failed"
- ✅ Check that your Bearer Token is correct
- ✅ Ensure token is properly set in environment variable
- ✅ Verify token hasn't been revoked in Developer Portal

### Error: "Access forbidden" (HTTP 403)
- ✅ Endpoint may require higher access tier
- ✅ Recent search requires at least Free tier
- ✅ Some features only available on Pro/Enterprise

### Error: "Rate limit exceeded" (HTTP 429)
- ✅ You've hit your monthly/per-minute limit
- ✅ Wait for rate limit to reset
- ✅ Consider upgrading to higher tier

### Getting Mock Data Instead of Real Data
- ✅ Verify `TWITTER_BEARER_TOKEN` is set: `echo $TWITTER_BEARER_TOKEN`
- ✅ Restart the application after setting environment variable
- ✅ Check application logs for authentication errors

## Switching Between Mock and Real API

The application automatically switches based on token availability:

```python
# In app/services/__init__.py
def get_twitter_service():
    if os.getenv('TWITTER_BEARER_TOKEN'):
        return TwitterAPIService()  # Real API
    else:
        return TwitterMockService()  # Mock data
```

### Force Mock Service (Even with Token):

Edit `app/services/__init__.py`:
```python
def get_twitter_service():
    return TwitterMockService()  # Always use mock
```

### Force Real API (Development/Testing):

```python
# For testing with real API
service = TwitterAPIService(bearer_token="your_token")
tweets = service.get_tweets_by_hashtag("python", limit=5)
```

## Security Best Practices

1. ✅ **Never commit tokens** to version control
2. ✅ Add `.env` to `.gitignore` (already done)
3. ✅ Use environment variables in production
4. ✅ Rotate tokens periodically
5. ✅ Use different tokens for dev/staging/production
6. ✅ Monitor token usage in Developer Portal

## Production Deployment

### Environment Variables on Common Platforms:

**Heroku:**
```bash
heroku config:set TWITTER_BEARER_TOKEN=your_token
```

**AWS Lambda/Elastic Beanstalk:**
Set in AWS Console → Configuration → Environment Properties

**Docker:**
```bash
docker run -e TWITTER_BEARER_TOKEN=your_token your_image
```

**Kubernetes:**
```yaml
env:
  - name: TWITTER_BEARER_TOKEN
    valueFrom:
      secretKeyRef:
        name: twitter-secrets
        key: bearer-token
```

## Additional Resources

- 📖 [X API Documentation](https://developer.x.com/en/docs/x-api)
- 📖 [X API v2 Migration Guide](https://developer.x.com/en/docs/twitter-api/migrate)
- 📖 [Rate Limits Guide](https://developer.x.com/en/docs/twitter-api/rate-limits)
- 💬 [X Developer Community Forums](https://twittercommunity.com/)
- 🐙 [X API Sample Code](https://github.com/xdevplatform)
- 📮 [Postman Collection for X API](https://www.postman.com/twitter)

## Support

If you encounter issues:

1. Check the [X API Status Page](https://api.twitterstat.us/)
2. Review [X Developer Forums](https://twittercommunity.com/)
3. Check application logs for detailed error messages
4. Verify your access tier supports the endpoints you're using

## Cost Estimation

### Example Usage Scenarios:

**Scenario 1: Testing/Development**
- Tier: Free
- Usage: 100 reads/month
- Cost: $0

**Scenario 2: Small App**
- Tier: Basic
- Usage: ~300 requests/day (9,000/month)
- Cost: $200/month

**Scenario 3: Production App**
- Tier: Pro
- Usage: ~33,000 requests/day (1M/month)
- Cost: $5,000/month

**Each API call to your application makes these X API requests:**
- `GET /hashtags/{tag}`: 1 X API call (search)
- `GET /users/{username}`: 2 X API calls (user lookup + timeline)

Plan your tier accordingly!

