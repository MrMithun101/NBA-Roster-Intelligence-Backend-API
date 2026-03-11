"""API tests: health, teams, players, roster, cache behavior."""

from unittest.mock import patch

from httpx import AsyncClient


async def test_health_returns_200(client: AsyncClient):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


async def test_teams_returns_list(client: AsyncClient, seeded_data):
    r = await client.get("/teams")
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 1
    team = next(t for t in data["data"] if t["abbreviation"] == "TT")
    assert team["name"] == "Test Team"


async def test_teams_get_by_id_returns_item(client: AsyncClient, seeded_data):
    team_id = seeded_data["team_id"]
    r = await client.get(f"/teams/{team_id}")
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert data["data"]["id"] == team_id
    assert data["data"]["abbreviation"] == "TT"


async def test_teams_get_by_id_returns_404(client: AsyncClient):
    r = await client.get("/teams/99999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Team not found"


async def test_players_filter_position(client: AsyncClient, seeded_data):
    r = await client.get("/players", params={"position": "PG"})
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    for p in data["data"]:
        assert p["position"] == "PG"


async def test_players_filter_name(client: AsyncClient, seeded_data):
    r = await client.get("/players", params={"name": "Test"})
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert any(p["first_name"] == "Test" and p["last_name"] == "Player" for p in data["data"])


async def test_teams_roster_returns_list(client: AsyncClient, seeded_data):
    team_id = seeded_data["team_id"]
    season = seeded_data["season_year"]
    r = await client.get(f"/teams/{team_id}/roster", params={"season": season})
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert data["season"] == season
    assert data["team_id"] == team_id
    assert isinstance(data["data"], list)
    assert any(p["first_name"] == "Test" for p in data["data"])


async def test_teams_roster_404_team(client: AsyncClient):
    r = await client.get("/teams/99999/roster", params={"season": 2024})
    assert r.status_code == 404


async def test_teams_roster_404_season(client: AsyncClient, seeded_data):
    team_id = seeded_data["team_id"]
    r = await client.get(f"/teams/{team_id}/roster", params={"season": 1999})
    assert r.status_code == 404
    assert "Season" in r.json()["detail"] or "season" in r.json()["detail"].lower()


async def test_cache_teams_first_miss_second_hit(client: AsyncClient, seeded_data):
    # Patch cache: first get_json returns None (MISS), second returns cached payload (HIT)
    teams_list_key = "teams:list"
    first_response = None

    def get_json_side_effect(key):
        nonlocal first_response
        if key == teams_list_key and first_response is not None:
            return first_response
        return None

    def set_json_side_effect(key, value, ttl):
        nonlocal first_response
        if key == teams_list_key:
            first_response = value

    with patch("app.routers.teams.get_json", side_effect=get_json_side_effect), patch(
        "app.routers.teams.set_json", side_effect=set_json_side_effect
    ):
        r1 = await client.get("/teams")
        assert r1.status_code == 200
        assert r1.headers.get("x-cache") == "MISS"

        r2 = await client.get("/teams")
        assert r2.status_code == 200
        assert r2.headers.get("x-cache") == "HIT"
        assert r1.json() == r2.json()
