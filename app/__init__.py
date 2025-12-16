"""
FastAPI application factory
"""
from fastapi import FastAPI
from config import config


def create_app(config_name='default'):
    """
    Application factory pattern for creating FastAPI app instances
    
    Args:
        config_name: Configuration name (development, testing, production)
        
    Returns:
        FastAPI application instance
    """
    app = FastAPI(
        title="Twitter Data API",
        description="RESTful API service for Twitter data retrieval",
        version="1.0.0"
    )
    
    # Store config in app state
    app.state.config = config[config_name]
    
    # Register routers
    from app.routes.hashtags import router as hashtags_router
    from app.routes.users import router as users_router
    
    app.include_router(hashtags_router)
    app.include_router(users_router)
    
    # Health check endpoint
    @app.get('/health')
    async def health_check():
        return {'status': 'healthy'}
    
    return app
