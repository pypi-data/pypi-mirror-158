# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

from asyncio import Queue
from contextlib import contextmanager, asynccontextmanager

from hagworm.extend.base import Utils


class ObjectPool:
    """对象池实现
    """

    def __init__(self, maxsize):

        self._queue = Queue(maxsize=maxsize)

        for _ in range(maxsize):
            self._queue.put_nowait(self._create_obj())

        Utils.log.info(f'ObjectPool {type(self)} initialized: {self._queue.qsize()}')

    def _create_obj(self):

        raise NotImplementedError()

    @asynccontextmanager
    async def get(self):

        Utils.log.debug(f'ObjectPool {type(self)} size: {self._queue.qsize()}')

        obj = await self._queue.get()

        try:
            yield obj
        except Exception as err:
            raise err
        finally:
            self._queue.put_nowait(obj)

    @contextmanager
    def get_nowait(self):

        Utils.log.debug(f'ObjectPool {type(self)} size: {self._queue.qsize()}')

        obj = self._queue.get_nowait()

        try:
            yield obj
        except Exception as err:
            raise err
        finally:
            self._queue.put_nowait(obj)


