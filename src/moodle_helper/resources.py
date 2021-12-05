from abc import abstractmethod
import os
from functools import lru_cache

cache = lru_cache(None)


class GlobalResourceManager:
    """
    A global cache for resources.
    """

    @cache
    def text(self, respath: str) -> str:
        with open(respath, "r") as f:
            return f.read()

    @cache
    def binary(self, respath: str) -> bytes:
        with open(respath, "rb") as f:
            return f.read()


_global_resource_manager = GlobalResourceManager()


class ResourcesBase:
    @abstractmethod
    def respath(self, resname: str) -> str:
        pass

    @abstractmethod
    def resdir(self) -> str:
        pass

    def text(self, resname: str) -> str:
        return _global_resource_manager.text(self.respath(resname))

    def binary(self, resname: str) -> bytes:
        return _global_resource_manager.binary(self.respath(resname))


class Resources(ResourcesBase):
    """
    Resources relative to module directory.

    Usage:

        resources = Resources(__file__)

    """

    def __init__(self, f: str, ) -> None:
        dir, rest = os.path.split(os.path.abspath(f))
        self._dir = dir

    def respath(self, resname: str) -> str:
        return f"{self._dir}/{resname}"

    def resdir(self) -> str:
        return self._dir


class ModuleResources(ResourcesBase):
    """
    Resources relative to `res/{module}`.

    Usage:

        module_resources = ModuleResources(__file__)

    """

    def __init__(self, f: str, ) -> None:
        dir, file = os.path.split(os.path.abspath(f))
        self._dir = dir
        module, _ = os.path.splitext(file)
        self._module = module

    def respath(self, resname: str) -> str:
        return f"{self._dir}/res/{self._module}/{resname}"

    def resdir(self) -> str:
        return f"{self._dir}/res/{self._module}"


class UninitializedResources(ResourcesBase):
    """
    An uninitialized resources object signals that something is wrong.
    """

    def __init__(self, error_msg) -> None:
        self._error_msg = error_msg

    def respath(self, resname: str) -> str:
        raise RuntimeError(self._error_msg)

    def resdir(self) -> str:
        raise RuntimeError(self._error_msg)
