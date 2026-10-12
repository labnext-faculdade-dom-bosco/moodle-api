from fastapi import APIRouter

from app.moodle_client import call_moodle_function

router = APIRouter(prefix="/moodle", tags=["moodle"])


@router.get("/site-info")
async def get_site_info():
    """Dados gerais do site: nome, versão, usuário do token, funções disponíveis."""
    return await call_moodle_function("core_webservice_get_site_info")


@router.get("/courses")
async def get_courses():
    """Retorna as disciplinas cadastradas no Moodle."""
    return await call_moodle_function("core_course_get_courses")

@router.get("/course-content")
async def get_course_content(course_id: int):
    """Retorna as atividades de uma disciplina cadastradas no Moodle."""
    return await call_moodle_function("core_course_get_contents", courseid=course_id)
