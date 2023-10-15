from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, SupportsIndex

if TYPE_CHECKING:
    from animator.entity.entity import Entity


def _entity_list_sort_key(entity: Entity) -> int:
    return entity.z_index


class EntityList(list['Entity']):
    """A list of entities, sorted by their z-index."""

    def append(self, entity: Entity) -> None:
        super().append(entity)
        self.sort()

    def extend(self, entities: Iterable[Entity]) -> None:
        super().extend(entities)
        self.sort()

    def sort(self) -> None:
        super().sort(key=_entity_list_sort_key)

    def insert(self, _index: SupportsIndex, _object: Entity) -> None:
        raise NotImplementedError("Use EntityList.append instead")
