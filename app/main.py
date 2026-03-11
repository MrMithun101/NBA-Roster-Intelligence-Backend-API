from fastapi import FastAPI

from app.routers import players, teams

app = FastAPI(title="NBA Roster Intelligence API")

app.include_router(teams.router)
app.include_router(players.router)


@app.get("/health")
def health():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok"}

