import platform as pf
import click
import sys
import os
import subprocess
import shlex

from .types.OSType import OSType
from .modules.cudainstaller import CUDAInstaller
from .modules.pyenvinstaller import Pyenv
from .modules.utils import LoadingSpinner

#TODO: 他のrleaseも対応する

def run_command_in_venv(venv_path: str, command: str):
    # 仮想環境内の Python インタプリタへのパスを指定
    python_executable = f"{venv_path}/bin/python" if sys.platform != 'win32' else f"{venv_path}\\Scripts\\python.exe"
    
    # コマンド文字列をリストに変換（安全なコマンドライン解析のため）
    command_list = [python_executable] + shlex.split(command)
    print(command_list)
    # コマンドを実行
    result = subprocess.run(command_list, capture_output=True, text=True)

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
            loading = LoadingSpinner("Installing pyenv...")
            loading.start(p_async=True)
            #os毎にdistributionが異なるので、それぞれの処理を行う
            if os_type == OSType.WINDOWS:
                pyenv.install_win()
                loading.stop()
            elif os_type == OSType.MAC:
                pyenv.install_mac()
                loading.stop()
        else:
            print("this command need pyenv. please install pyenv and try again.")
            return
    else:
        print("you have already installed pyenv.")
    
    pyenv.pin_python_ver("3.10.11")
    if os.path.exists(venv):
        print(f"virtual environment already exists: {venv}")
        print("resuming vertial environment...")
    else:
        loading = LoadingSpinner("Creating virtual environment...")
        loading.start(p_async=True)
        subprocess.call(f'python -m venv {venv}', shell=True)
        loading.stop()
        print("pinned python version to 3.10.11 and created virtual environment.")
    
    
    # 2.依存ライブラリをインストール 
    loading = LoadingSpinner("Installing dependencies packages...")
    loading.start(p_async=True)
    if cuda:
        #pypy
        run_command_in_venv(venv, "-m pip install -r ./requirements-cuda.txt")
        run_command_in_venv(venv, "-m pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118")
        
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
        else:
            print("you have already downloaded CUDA Installer.")

        loading_cuda = LoadingSpinner("Installing CUDA Toolkit...")
        loading_cuda.start(p_async=True)
        installer.download_cuda(cuda_installer)
        loading_cuda.stop()
        print("CUDA Toolkit installation completed.")
    else:
        #pypyのみ
        run_command_in_venv(venv, "-m pip install -r ./requirements.txt")
        run_command_in_venv(venv, "-m pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0")

    loading.stop()

    print("\n ===========Next Step=============")
    print("ml-agents installation completed. let's start training your agents!")
    print("1. open Unity Project on './MLAgentsTemplate'")
    print("2. run 'mlagents-learn --force' to start mlagents backend system.")
    print("3. run your Unity Project and start training your agents.")
    

if __name__ == "__main__":
    
    try:
        install()
    except Exception as e:
        print("An error occurred during the installation process.")
        print(e)
        sys.exit(1)
