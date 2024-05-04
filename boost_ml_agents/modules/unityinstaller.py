from typing import Final as const
import subprocess
import os
import re

from ..types.OSType import OSType
class UnityInstaller:

    UNITYHUB_PATH: str|None = None

    def __init__(self, OSType: OSType):
        self.OSType = OSType
        self.set_unityhub()
        

    
    def __find_hub(self, cmd: str|list[str]) -> str | None:
        try:
            result = subprocess.check_output(cmd, text=True)
        except subprocess.CalledProcessError:
            return None
        else:
            return result.strip()
    
    def set_unityhub(self) -> None:
        """
        set the path of Unity Hub
        Returns:
            str: path of Unity Hub
        """
        default_path: str
        if self.OSType == OSType.WINDOWS:
            cmd = "where UnityHub.exe"
            default_path = "C:/Program Files/Unity Hub/Unity Hub.exe"
        elif self.OSType == OSType.MAC:
            cmd = ['find', '/Applications', '-name', 'Unity Hub', '-print']
            default_path = "/Application/Unity/Hub/Editor"
        else:
            raise Exception("Unsupported OS")
        
        if os.path.exists(default_path):
            self.UNITYHUB_PATH = default_path
        else:
            self.UNITYHUB_PATH = self.__find_hub(cmd)

    def install(self, version: str) -> tuple[str, str, str]:
        """
        install the given version
        Args:
            version (str): version to install
        Returns:
            tuple[str, str, str]: version, stdout, stderr
        """
        if self.UNITYHUB_PATH is None:
            raise Exception("Unity Hub not found. please call 'find_unityhub' first")
        
        command = f'{self.UNITYHUB_PATH} -- --headless install --version {version}'
        result = subprocess.run(command, shell=False, capture_output=True, text=True)
        return (version, result.stdout, result.stderr)
    

    def fetch_versions(self):
        """
        fetch the available versions
        Returns:
            list[str]: list of versions
        """
        if self.UNITYHUB_PATH is None:
            raise Exception("Unity Hub not found. please call 'find_unityhub' first")
        
        command = f'{self.UNITYHUB_PATH} -- --headless editors -r'
        result = subprocess.run(command, shell=False, text=True ,capture_output=True)
        if result.stderr:
            print("Error:", result.stderr)
            return []

        # バージョン情報が含まれる行を見つけるための正規表現パターン
        pattern = r'\b\d+\.\d+\.\d+[a-zA-Z0-9]+\b'
        versions = re.findall(pattern, result.stdout)

        return versions
        

#test
if __name__ == "__main__":
    unity_installer = UnityInstaller(OSType.WINDOWS)
    print(unity_installer.fetch_versions())