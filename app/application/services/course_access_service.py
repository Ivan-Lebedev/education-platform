from uuid import UUID

from app.application.exceptions import (
    CourseNotFoundError,
    ModuleNotFoundError,
    PermissionDeniedError,
    SectionNotFoundError,
)
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities import Course, Module, Section, User


class CourseAccessService:
    """
    Сервис проверки прав доступа к управлению курсом и его содержимым.

    Инкапсулирует правила авторизации для иерархии сущностей 'Курс' → 'Модуль' → 'Раздел',
    делегируя проверку прав от дочерних сущностей к родительскому курсу.
    """

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def ensure_can_manage_course(
        self,
        actor: User,
        course_id: UUID,
    ) -> Course:
        """
        Проверяет право пользователя управлять курсом и возвращает курс.

        Загружает курс из БД и проверяет, имеет ли пользователь право
        управлять им согласно правилам доступа.

        Правила предоставления доступа:
            - Администратор платформы может управлять любым курсом.
            - Автор курса может управлять своим курсом.

        Args:
            actor (User): Пользователь, выполняющий действие.
            course_id (UUID): УИН курса для проверки.

        Returns:
            Course: Загруженный курс, если проверка пройдена.

        Raises:
            CourseNotFoundError: Если курс с указанным УИН не найден.
            PermissionDeniedError: Если пользователь не является
                ни администратором платформы, ни автором курса.
        """

        course = await self.uow.courses.get_by_id(course_id)
        if course is None:
            raise CourseNotFoundError('Course not found.')

        if not actor.can_manage_platform() and not course.is_owned_by(actor.id):
            raise PermissionDeniedError('User cannot manage this course.')

        return course

    async def ensure_can_manage_module(
        self,
        actor: User,
        module_id: UUID,
    ) -> Module:
        """
        Проверяет право пользователя управлять модулем и возвращает модуль.

        Загружает модуль из БД и делегирует проверку прав родительскому курсу
        через ensure_can_manage_course.

        Args:
            actor (User): Пользователь, выполняющий действие.
            module_id (UUID): УИН модуля для проверки.

        Returns:
            Module: Загруженный модуль, если проверка пройдена.

        Raises:
            ModuleNotFoundError: Если модуль с указанным УИН не найден.
            CourseNotFoundError: Если родительский курс модуля не найден.
            PermissionDeniedError: Если пользователь не имеет права
                управлять родительским курсом модуля.
        """

        module = await self.uow.modules.get_by_id(module_id)
        if module is None:
            raise ModuleNotFoundError('Module not found.')

        await self.ensure_can_manage_course(actor, module.course_id)
        return module

    async def ensure_can_manage_section(
        self,
        actor: User,
        section_id: UUID,
    ) -> Section:
        """
        Проверяет право пользователя управлять разделом и возвращает раздел.

        Загружает раздел из БД и делегирует проверку прав родительскому модулю
        через ensure_can_manage_module, который, в свою очередь,
        делегирует проверку родительскому курсу.

        Args:
            actor (User): Пользователь, выполняющий действие.
            section_id (UUID): УИН раздела для проверки.

        Returns:
            Section: Загруженный раздел, если проверка пройдена.

        Raises:
            SectionNotFoundError: Если раздел с указанным УИН не найден.
            ModuleNotFoundError: Если родительский модуль раздела не найден.
            CourseNotFoundError: Если родительский курс родительского модуля не найден.
            PermissionDeniedError: Если пользователь не имеет права
                управлять родительским курсом раздела.
        """

        section = await self.uow.sections.get_by_id(section_id)
        if section is None:
            raise SectionNotFoundError('Section not found.')

        await self.ensure_can_manage_module(actor, section.module_id)
        return section
