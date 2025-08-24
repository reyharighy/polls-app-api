"""Configuration for the API."""

APPLICATION_METADATA = {
    "title": "Poll API",
    "description": "A simple polling application using FastAPI.",
    "version": "0.1.0",
    "openapi_tags": [
        {
            "name": "polls",
            "description": "All HTTP endpoints related to the poll model."
        }
    ],
    "contact": {
        "name": "Muhammad Reyhan Arighy",
        "url": "https://github.com/reyharighy/polls-app-api",
        "email": "arighymoch@gmail.com"
    }
}