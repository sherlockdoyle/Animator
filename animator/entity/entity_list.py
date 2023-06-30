from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, SupportsIndex

if TYPE_CHECKING:
    from animator.entity.entity import Entity


class EntityList(list['Entity']):
    """A list of entities, sorted by their z-index."""

    def append(self, entity: Entity) -> None:
        super().append(entity)
        self.sort(key=lambda e: e.z_index)

    def extend(self, entities: Iterable[Entity]) -> None:
        super().extend(entities)
        self.sort(key=lambda e: e.z_index)

    def insert(self, _index: SupportsIndex, _object: Entity) -> None:
        raise NotImplementedError("Use EntityList.append instead")
