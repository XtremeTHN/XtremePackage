import json

from typing import TypedDict
from pathlib import Path

CONFIG_DIR=Path.home() / ".config" / "xtremepkg"
CONFIG_DIR.mkdir(exist_ok=True)

class PkgsConfig(TypedDict):
    installed: list
    
class PythonCConfig(TypedDict):
    make_venv: bool

class CompilationConfig(TypedDict):
    python: PythonCConfig

class Config(TypedDict):
    def default():
        return {"packages": {"installed": []}, "compilation":{"python":{"make_venv":True}}}
    packages: PkgsConfig
    compilation: CompilationConfig

class XConfig:
    def __init__(self):
        self.config_file = CONFIG_DIR / "xconfig.json"
        if self.config_file.exists() is False:
            with self.config_file.open("w") as file:
                json.dump(Config.default(), file, indent=4)
            
        self.config: Config = json.loads(self.config_file.read_text())
    
    def save(self):
        self.config_file.write_text(json.dumps(self.configs, indent=4))