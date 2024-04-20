import fastapi

from topological_connect_four.api.database import GAME_SETTINGS
from topological_connect_four.api.models import ApiGravity, ApiTopology, GameSettings

app = fastapi.FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/make_new_game")
async def make_new_game(
    topology: ApiTopology = ApiTopology.NONE,
    gravity: ApiGravity = ApiGravity.BOTTOM,
    players: int = 4,
):
    new_game_id = len(GAME_SETTINGS)
    GAME_SETTINGS[new_game_id] = GameSettings(
        board_size=8, topology=topology, gravity=gravity, players=players
    )
    return {"game_id": new_game_id}


@app.get("/get_game_settings/{game_id}")
async def get_game_settings(game_id: int):
    return GAME_SETTINGS[game_id]
