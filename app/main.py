from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok"}

