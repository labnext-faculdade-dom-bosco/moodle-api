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


@router.get("/courses/{course_id}/completion")
async def get_course_completion(course_id: int, user_id: int):
    """
    Retorna o status de conclusão do curso para um aluno específico.
    Mapeia a wsfunction nativa: core_completion_get_course_completion_status
    """
    return await call_moodle_function(
        "core_completion_get_course_completion_status",
        courseid=course_id,
        userid=user_id
    )


@router.get("/users/search")
async def search_users(field: str = "username", value: str = ""):
    """Busca utilizadores no Moodle por um campo específico (ex: username, email)."""
    return await call_moodle_function(
        "core_user_get_users_by_field",
        field=field,
        **{"values[0]": value}
    )

@router.get("/courses/{course_id}/users")
async def get_enrolled_users(course_id: int):
    """
    Consulta e trás de volta todos os usuários (alunos e professores) matriculados em um curso específico.
     Pega e mapeia  a wsfunction nativa: core_enrol_get_enrolled_users
    """
    return await call_moodle_function(
        "core_enrol_get_enrolled_users",
        courseid=course_id
    )

@router.get("/courses/{course_id}/users/{user_id}/activities-completion")
async def get_activities_completion_status(course_id: int, user_id: int):
    """Retorna o status detalhado de conclusão de cada atividade do curso."""
    return await call_moodle_function(
        "core_completion_get_activities_completion_status",
        courseid=course_id,
        userid=user_id
    )

@router.get("/courses/{course_id}/users/{user_id}/grades")
async def get_user_grades(course_id: int, user_id: int):
    """Retorna o relatório de notas do aluno no curso."""
    return await call_moodle_function(
        "gradereport_user_get_grade_items",
        courseid=course_id,
        userid=user_id
    )

@router.get("/quizzes/{quiz_id}/users/{user_id}/attempts")
async def get_user_quiz_attempts(quiz_id: int, user_id: int):
    """Retorna as tentativas e notas do aluno em um questionário (quiz)."""
    return await call_moodle_function(
        "mod_quiz_get_user_attempts",
        quizid=quiz_id,
        userid=user_id
    )