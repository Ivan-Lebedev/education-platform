from typing import TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import LectureModel, ModuleModel, SectionModel

ChildModelT = TypeVar('ChildModelT', LectureModel, ModuleModel, SectionModel)


async def sync_children(
    session: AsyncSession,
    child_model: type[ChildModelT],
    current_children: list[ChildModelT],
    new_children_ids: list[UUID],
) -> None:
    """
    Синхронизирует связь обновляемой модели с её вложенными дочерними объектами.

    Удаляет дочерние объекты из обновляемой модели, которых больше нет в доменной сущности,
    и добавляет новые, которые появились в доменной сущности, но отсутствуют в модели.
    """

    current_children_ids_set = {child.id for child in current_children}
    new_children_ids_set = {str(child_id) for child_id in new_children_ids}

    children_ids_to_remove = current_children_ids_set - new_children_ids_set
    children_ids_to_add = new_children_ids_set - current_children_ids_set

    for child in list(current_children):
        if child.id in children_ids_to_remove:
            current_children.remove(child)

    for child_id in children_ids_to_add:
        child_to_add = await session.get(child_model, child_id)
        if child_to_add is not None:
            current_children.append(child_to_add)
