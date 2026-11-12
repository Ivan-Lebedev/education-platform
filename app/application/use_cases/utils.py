from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities import Course, Module, Section


async def delete_section_lectures(section: Section, uow: UnitOfWork) -> None:
    "Удаление всех лекций указанного раздела."
    # TODO: Рассмотреть каскадное удаление вопросов и связанных с ними сущностей, принадлежащих разделу.  # noqa: E501

    for lecture_id in section.lecture_ids:
        lecture = await uow.lectures.get_by_id(lecture_id)
        if lecture is not None:
            await uow.lectures.remove(lecture_id)


async def delete_module_sections(module: Module, uow: UnitOfWork) -> None:
    "Удаление всех разделов с входящими в них лекциями указанного модуля."

    for section_id in module.section_ids:
        section = await uow.sections.get_by_id(section_id)
        if section is not None:
            await delete_section_lectures(section=section, uow=uow)
            await uow.sections.remove(section_id)


async def delete_course_modules(course: Course, uow: UnitOfWork) -> None:
    "Удаление всех модулей с входящими в них разделами и лекциями указанного курса."

    for module_id in course.module_ids:
        module = await uow.modules.get_by_id(module_id)
        if module is not None:
            await delete_module_sections(module=module, uow=uow)
            await uow.modules.remove(module_id)
