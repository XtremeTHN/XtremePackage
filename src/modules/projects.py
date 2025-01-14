from modules.utils import exec_cmd, is_installed, decide
from modules.style import info, warn, error
from modules.constants import LOCAL_BIN_DIR
from pathlib import Path

import shutil
import os

class BuildSystem:
    NUITKA=1
    MESON=2

class Project:
    build_system: BuildSystem
    path: Path
    def __init__(self, meson_required=False):
        if meson_required is True:
            if is_installed('meson') is False:
                error("Meson needs to be installed to compile vala projects", exit_code=127)

        self.meson_executable = "meson" if is_installed("arch-meson") is False else "arch-meson"

    @staticmethod
    def from_info(info):
        language = info["language"].lower()
        if language != "python" and info["alias"] is not None:
            error("Alias option is only available when installing python packages")
        
        if language == "python":
            return PythonProject(info["path"], info["name"], info["alias"])
        elif language == "vala":
            return ValaProject(info["path"], info["name"])
        
    def __compile_meson(self):
        info("Configuring meson build...")
        exec_cmd([self.meson_executable, "build"], wd=self.path)

    def setup(self):
        if self.build_system == BuildSystem.MESON:
            self.__compile_meson()

    def __install_meson(self):
        info("Installing package with meson...")
        exec_cmd(["meson", "install", "-C", "build"], wd=self.path)

    def install(self):
        if self.build_system == BuildSystem.MESON:
            self.__install_meson()
    
    def __uninstall_meson(self):
        if self.path.exists() is False:
            error("Project git directory doesn't exist. Install again the package to remove it")
            
        info("Uninstalling package with meson...")
        warn("This needs to be run as root. Continue? (y/n): ", end="")
        if decide() is False:
            return

        exec_cmd(["sudo", "ninja", "uninstall", "-C", "build"], wd=self.path)

    def uninstall(self):
        if self.build_system == BuildSystem.MESON:
            self.__uninstall_meson()

class ValaProject(Project):
    def __init__(self, path, pkg_name):
        super().__init__()
        self.package_name = pkg_name
        self.build_system = BuildSystem.MESON
        self.path = path

class PythonProject(Project):
    def __init__(self, path, pkg_name, alias=None):
        super().__init__()
        self.package_name = pkg_name
        self.alias = alias
        self.path = path

        self.build_system = self.detect_build_system()

        if self.build_system == BuildSystem.MESON and self.alias is not None:
            error("Alias option is not available when installing meson projects")
        
        if self.alias is not None:
            info("Using alias: " + (self.alias))

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
            return BuildSystem.NUITKA
    
    def __install_nuitka(self):
        info('Moving to ~/.local/bin ...')
        name = self.alias or self.package_name
        dest = LOCAL_BIN_DIR / name
        shutil.move(self.path / self.package_name, dest)
    
    def __uninstall_nuitka(self):
        info('Removing from ~/.local/bin ...')
        if (LOCAL_BIN_DIR / self.package_name).exists() is False:
            if (LOCAL_BIN_DIR / self.alias).exists() is False:
                error("Package doesn't exist on ~/.local/bin")
            else:
                self.package_name = self.alias
        os.remove(LOCAL_BIN_DIR / self.package_name)
    
    def __compile_nuitka(self):
        # TODO: Stop using nuitka in a venv
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
        if self.build_system == BuildSystem.NUITKA:
            self.__compile_nuitka()
        else:
            super().setup()
    
    def install(self):
        if self.build_system == BuildSystem.NUITKA:
            self.__install_nuitka()
        else:
            super().install()

    def uninstall(self):
        if self.build_system == BuildSystem.NUITKA:
            self.__uninstall_nuitka()
        else:
            super().uninstall()