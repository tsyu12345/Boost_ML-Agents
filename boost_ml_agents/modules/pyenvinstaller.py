from typing import Final as const
import requests
import subprocess
from tqdm import tqdm
import os 
import shutil

class Pyenv:

    def __has_homebrew(self) -> bool:
        try:
            subprocess.run("brew --version", shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def __install_homebrew(self) -> str:
        result = subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True, check=True)
        return result.stdout.decode("utf-8")
    
    def has_pyenv(self) -> bool:
        """
        Checks if pyenv is installed.
        """
        try:
            subprocess.run("pyenv --version", shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def install_mac(self) -> str:
        """
        Installs pyenv on a Mac using Homebrew.
    
        Returns:
            str: The output of the installation process.
        """

        #Chack homebrew installation
        if not self.__has_homebrew():
            #ユーザーにインストールするかどうかを尋ねる
            print("[Pyenv Installer] Homebrew is not installed. Do you want to install it? (y/n)")
            user_input = input()
            if user_input == "y":
                print("[Pyenv Installer] Installing Homebrew...")
                brewinstall = self.__install_homebrew()
                print("[Pyenv Installer] Homebrew installation completed.", brewinstall)
            else:
                print("[Pyenv Installer] Homebrew is not installed. Please install Homebrew and try again.")
                return ""
        print("[Pyenv Installer] Installing pyenv...")
        running_process = subprocess.run(["brew", "install", "pyenv"], check=True)
        return running_process.stdout.decode("utf-8")
    
    def install_win(self) -> None:
        """
        Installs pyenv on a Windows machine.(pyenv-win)
        """
        response = requests.get("https://github.com/pyenv-win/pyenv-win/archive/refs/heads/master.zip")
        
        if response.status_code != 200:
            raise Exception(f"Failed to download pyenv-win: {response.status_code}")

        with open(f"{os.environ['TEMP']}\\pyenv.zip", 'wb') as f:
            f.write(response.content)
        shutil.unpack_archive(f"{os.environ['TEMP']}\\pyenv.zip", f"{os.environ['USERPROFILE']}\\.pyenv")
        os.environ["PYENV"] = f"{os.environ['USERPROFILE']}\\.pyenv\\pyenv-win\\"
        os.environ["PATH"] += f";{os.environ['PYENV']}bin;{os.environ['PYENV']}shims"
        
        print("[Pyenv Installer] pyenv-win installation completed.")


    def pin_python_ver(self, version: str):
        """
        Pins the specified Python version to pyenv.
        """
        try:
            subprocess.run(f"pyenv install {version}", shell=True, check=True)
            subprocess.run(f"pyenv local {version}", shell=True, check=True)
            subprocess.run(f"pyenv rehash", shell=True, check=True)
        except subprocess.CalledProcessError:
            raise Exception(f"Failed to pin Python {version} to pyenv.")
        
        print(f"[Pyenv Installer] Python {version} is now pinned to pyenv.")
    
