from modules.utils import exec_cmd, is_installed
from modules.style import info, warn, error
from modules.constants import LOCAL_BIN_DIR
from pathlib import Path

import shutil
import os

class BuildSystem:
    DEFAULT=1
    MESON=2

class Project:
    def __init__(self):
        pass

    @staticmethod
    def from_info(info):
        if info["language"] == "python":
            return PythonProject(info["path"], info["name"])
        elif info["language"] == "vala":
            return ValaProject(info["path"], info["name"])

    def setup(self):
        pass

    def install(self):
        pass

class ValaProject(Project):
    def __init__(self, path, pkg_name):
        super().__init__()
        self.package_name = pkg_name
        self.path = path

        if is_installed('meson') is False:
            error("Meson needs to be installed to compile vala projects", exit_code=127)

        self.meson_executable = "meson" if is_installed("arch-meson") is False else "arch-meson"
    
    def setup(self):
        info("Configuring vala project...")
        exec_cmd([self.meson_executable, "setup", "build"], wd=self.path)

    def install(self):
        info("Installing package with meson...")
        exec_cmd([self.meson_executable, "install", "-C", "build"], wd=self.path)

class PythonProject(Project):
    def __init__(self, path, pkg_name):
        super().__init__()
        self.package_name = pkg_name
        self.path = path

        self.build_system = self.detect_build_system()
        self.meson_executable = "meson" if is_installed("arch-meson") is False else "arch-meson"

    def get_main_file_python(self, path: Path) -> str:
        files = [str(p) for p in path.glob("**/*.py") if p.name == "main.py"]
        if len(files) > 1:
            # Gets the size of all file paths on project root
            k = [len(x.split("/")) for x in files]

            # Return the root main file
            return files[k.index(min(k))]
        
        return files[0]

    def exec_on_venv(self, args: list, venv_path: str, wd: str, executable=None):
        _env = {
            "VIRTUAL_ENV": venv_path,
            "PATH": f"{venv_path}/bin:{os.environ['PATH']}"
        }
        
        exec_cmd(args, wd, env=_env)
    
    def detect_build_system(self):
        if (self.path / "meson.build").exists():
            if is_installed("meson") is False:
                error("Meson needs to be installed to compile meson projects", exit_code=127)
                
            info("Using meson build system...")
            return BuildSystem.MESON
        else:
            info("Using nuitka...")
            return BuildSystem.DEFAULT
    
    def __install_default(self):
        info('Moving to ~/.local/bin ...')
        shutil.move(self.path / self.package_name, LOCAL_BIN_DIR / self.package_name)
    
    def __install_meson(self):
        info("Installing package with meson...")
        exec_cmd([self.meson_executable, "install", "-C", "build"], wd=self.path)
    
    def __compile_meson(self):
        info("Configuring meson build...")
        exec_cmd([self.meson_executable, "setup", "build"], wd=self.path)
    
    def __compile_default(self):
        venv_dir = self.path / ".venv"
        requirements_path = self.path / "requirements.txt"
        
        if venv_dir.exists() is False:
            info("Making virtual environment...")
            exec_cmd(["python3", "-m", "venv", str(venv_dir)], self.path)
            
        info("Installing nuitka to the venv...")
        self.exec_on_venv(["python3", "-m", "pip", "install", "nuitka"], venv_dir, self.path)
        
        if requirements_path.exists():
            info("Installing dependencies...")
            self.exec_on_venv(["python3", "-m", "pip", "install", "-r", f'{self.path}/requirements.txt'], venv_dir, self.path)
        else:
            warn("No requirements file found. Maybe the compilation will fail")
        
        info("Detecting entry file...")
        entry_file = self.get_main_file_python(self.path)
        info("Compiling python project with nuitka...")
        self.exec_on_venv(["python3", "-m", "nuitka", "--follow-imports", entry_file, '--output-dir=build', f'--output-file={self.package_name}'], venv_dir, self.path)
        info("Successfully compiled")

    def setup(self):
        if self.build_system == BuildSystem.DEFAULT:
            self.__compile_default()
        else:
            self.__compile_meson()
    
    def install(self):
        if self.build_system == BuildSystem.DEFAULT:
            self.__install_default()
        else:
            self.__install_meson()
