"""Entry point to start a web server of a FastAPI application."""

from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
def test():
    """Test route endpoint"""
    return {"message": "Hello World!"}
