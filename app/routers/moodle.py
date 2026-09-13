from fastapi import APIRouter

from app.moodle_client import call_moodle_function

router = APIRouter(prefix="/moodle", tags=["moodle"])


@router.get("/site-info")
async def site_info():
    """Dados gerais do site: nome, versão, usuário do token, funções disponíveis."""
    return await call_moodle_function("core_webservice_get_site_info")


@router.get("/courses")
async def list_courses():
    """Lista os cursos cadastrados no Moodle."""
    return await call_moodle_function("core_course_get_courses")
