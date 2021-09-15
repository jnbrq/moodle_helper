import os
from functools import lru_cache

cache = lru_cache(None)

class ModuleResources:
    def __init__(self, f: str) -> None:
        dir, file = os.path.split(os.path.abspath(f))
        self.dir = dir
        module, _ = os.path.splitext(file)
        self.module = module
    
    @cache
    def text(self, resname: str) -> str:
        with open(f"{self.dir}/res/{self.module}/{resname}") as f:
            return f.read()
    
    # maybe add other types of resources
