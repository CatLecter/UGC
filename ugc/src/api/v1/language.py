import logging
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.requests import Request

from ...schemas import LanguageMovie
from ...services import LanguageService
from ...services.getters import get_language_service

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/movies/{movie_id}/language")
async def language_movies(
    msg: LanguageMovie,
    movie_id: UUID,
    request: Request,
    language_service: LanguageService = Depends(get_language_service),
):
    """Add language movie."""
    language = msg.language_movie
    value = {
        "user_uuid": request.state.user_uuid,
        "movie_id": movie_id,
        "language_movie": language,
        "language_client": request.state.language,
        "datetime": msg.datetime,
    }
    await language_service.send(message=value)
    return {
        "success": {
            "User UUID": request.state.user_uuid,
            "Movie UUID": movie_id,
            "Movie language": language,
            "Client language": request.state.language,
        }
    }
