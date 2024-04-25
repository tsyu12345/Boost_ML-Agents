import platform as pf
import click
import sys

from .types.OSType import OSType
from .modules.cudainstaller import CUDAInstaller
from .modules.pyenvinstaller import Pyenv


@click.command()
@click.option("--ver", default="21" help="環境構築するML-Agentsのバージョン")
def envinstall():
    """
    ml-agentsの開発環境を自動構築する.
    """
    # OSの種類を取得
    os_type = OSType(pf.system())
    print(f"OS: {os_type.name}")

    # OSごとの処理
    if os_type == OSType.WINDOWS:
        pass
    elif os_type == OSType.MAC:
        # 1.範囲内のPython or pyenvがあるか確かめる
        pyenv = Pyenv()
        
        if pyenv.has_pyenv() == False or 


def main():
    print(f"OS: {pf.system()} {pf.release()} {pf.version()}")

    
    