import platform as pf
import click
import sys

from .types.OSType import OSType
from .modules.cudainstaller import CUDAInstaller
from .modules.pyenvinstaller import Pyenv

#TODO: 他のrleaseも対応する

@click.command()
@click.option("--v", default="21", help="version of ml-agents to install")
@click.option("--cuda", default=False, help="install CUDA Toolkit and use it in ml-agents")
def envinstall(v: int, cuda: bool):
    """
    Installs the necessary environment for ml-agents automatically.
    """
    # OSの種類を取得
    os_type = OSType(pf.system())
    print(f"OS: {os_type.name}")

    # 1.範囲内のPython or pyenvがあるか確かめる
    pyenv = Pyenv()
    
    if pyenv.has_pyenv() == False or sys.version_info >= (3, 9):
        print("python 3.10 or higher is required.")
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
    
    # 2. venvのアクティベーション
    if os_type == OSType.WINDOWS:
        pass
    else:
        pass


    # 3.依存ライブラリをインストール 
    if cuda:
        #pypyとCUDA
        pass
    else:
        #pypyのみ
        pass

def main():
    print(f"OS: {pf.system()} {pf.release()} {pf.version()}")

    
    