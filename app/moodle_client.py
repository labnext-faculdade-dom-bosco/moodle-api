import httpx

from app.config import settings

REST_ENDPOINT = "/webservice/rest/server.php"


async def call_moodle_function(wsfunction: str, **params) -> dict | list:
    """Chama a wsfunction indicada no Moodle e devolve o JSON de resposta."""
    query = {
        "wstoken": settings.moodle_token,
        "wsfunction": wsfunction,
        "moodlewsrestformat": "json",
        **params,
    }

    async with httpx.AsyncClient(base_url=settings.moodle_base_url, timeout=10) as client:
        response = await client.get(REST_ENDPOINT, params=query)
        response.raise_for_status()
        return response.json()
