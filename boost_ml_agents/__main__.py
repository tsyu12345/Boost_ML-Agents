import platform as pf
import click
import sys
import os
import subprocess

from .types.OSType import OSType
from .modules.cudainstaller import CUDAInstaller
from .modules.pyenvinstaller import Pyenv

#TODO: 他のrleaseも対応する

@click.command()
@click.option("--v", default="21", help="version of ml-agents to install")
@click.option("--venv", default=".venv", help="location of the virtual environment")
@click.option("--cuda", default=False, help="install CUDA Toolkit and use it in ml-agents")
def install(v: int, venv:str, cuda: bool):
    """
    Installs the necessary environment for ml-agents automatically.
    """
    # OSの種類を取得
    os_type = OSType(pf.system())
    print(f"OS: {os_type.name}")
    print(f"OS: {pf.system()} {pf.release()} {pf.version()}")

    # 1.範囲内のPython or pyenvがあるか確かめる

    if  sys.version_info <= (3, 9):
        print("python 3.10.x or higher")
        print("chcking pyenv installed...")

    pyenv = Pyenv()
    has_pyenv = pyenv.has_pyenv()
    print(f"has Pyenv: {has_pyenv}")
    if has_pyenv == False:
        print("do you want to install pyenv? (y/n)")
        user_input = input()
        if user_input == "y":
            #os毎にdistributionが異なるので、それぞれの処理を行う
            if os_type == OSType.WINDOWS:
                pyenv.install_win()
            elif os_type == OSType.MAC:
                pyenv.install_mac()
        else:
            print("this command need pyenv. please install pyenv and try again.")
            return
    else:
        print("you have already installed pyenv.")
    
    pyenv.pin_python_ver("3.10.11")
    subprocess.call(f'python -m venv {venv}', shell=True)
    print("pinned python version to 3.10.11 and created virtual environment.")
    # 2. venvのアクティベーション
    if os_type == OSType.WINDOWS:
        subprocess.call(f'{venv}\\Scripts\\activate', shell=True)
    elif os_type == OSType.MAC:
        subprocess.call(f'{venv}/bin/activate', shell=True)

    # 3.依存ライブラリをインストール 
    print("installing dependencies...")
    if cuda:
        #pypyとCUDA
        subprocess.call("pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118", shell=True)
        #カレントディレクトリにCUDA installer.exeの存在を確認
        installer = CUDAInstaller("11.8")
        cuda_installer = "./cuda_11.8.0_windows_network.exe"
        if os.path.exists(cuda_installer) == False:
            print("CUDA Installer was not found. Do you want to install it? (y/n)")
            user_input = input()
            if user_input == "y":
                installer.download_installer(cuda_installer)
            else:
                print("this command need CUDA Toolkit. please install CUDA Toolkit and try again.")
                return
        print("installing CUDA Toolkit...")
        installer.download_cuda(cuda_installer)
        print("CUDA Toolkit installation completed.")
    else:
        subprocess.call('pip install -r ./requirements.txt', shell=True)
    
    print("ml-agents installation completed. let's start training your agents!")
    print("1. open Unity Project on './MLAgentsTemplate'")
    print("2. run 'mlagents-learn --force' to start training.")
    

if __name__ == "__main__":
    install()