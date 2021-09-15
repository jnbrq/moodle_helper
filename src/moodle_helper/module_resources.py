import os

class ModuleResources:
    def __init__(self, f: str) -> None:
        dir, file = os.path.split(os.path.abspath(f))
        self.dir = dir
        module, _ = os.path.splitext(file)
        self.module = module
    
    def text(self, resname: str) -> str:
        with open(f"{self.dir}/res/{self.module}/{resname}") as f:
            return f.read()
    
    # maybe add other types of resources
