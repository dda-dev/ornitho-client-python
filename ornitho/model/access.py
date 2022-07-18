from typing import Optional

from ornitho.model.observer import Observer


class Access:
    def __init__(self, id_observer: int, anonymous: bool, id_access: int) -> None:
        """Access constructor
        :param id_observer: Observer ID
        :param anonymous: Anonymous Observer
        :param id_access: Access ID
        :type id_observer: int
        :type anonymous: bool
        :type id_access: int
        """
        self.id_observer: int = id_observer
        self.anonymous: bool = anonymous
        self.id_access: int = id_access
        self._observer: Optional[Observer] = None

    @property
    def observer(self) -> Observer:
        """Observing user"""
        if self._observer is None:
            self._observer = Observer.get(id_=self.id_observer)
        return self._observer
