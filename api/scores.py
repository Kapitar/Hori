import requests
from os import getenv

headers = {
    "Authorization": f'Bearer {getenv("OSU_TOKEN")}'
}


async def get_recent_score(user_id: int, mode: str, scores_count: int) -> list:
    """
    Returning user's most recent scores
    :param user_id: User's osu id.
    :param mode: Gamemode type.
    :param scores_count: Count of scores that needs to be requested.
    """

    payload = {
        "mode": mode,
        "limit": scores_count
    }
    response = requests.get(f'{getenv("OSU_BASE_URL")}/users/{user_id}/scores/recent', params=payload, headers=headers)
    return response.json()
