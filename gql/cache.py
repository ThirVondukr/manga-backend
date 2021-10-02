from typing import Awaitable, Callable

_SENTINEL = object()


class AsyncCache:
    def __init__(self, awaitable: Callable[[], Awaitable]):
        self._awaitable = awaitable
        self._cached = _SENTINEL

    async def __call__(self):
        if self._cached is _SENTINEL:
            self._cached = await self._awaitable()
        return self._cached

    def __await__(self):
        return self().__await__()

