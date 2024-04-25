from typing import Final as const
import requests
import subprocess
import os
from tqdm import tqdm

class CUDAInstaller:
    """
    本クラスはWindowsのみのサポート
    """

    #CUDA installerのURL
    InstallerURLs: const = {
        '11.8': "https://developer.download.nvidia.com/compute/cuda/11.8.0/network_installers/cuda_11.8.0_windows_network.exe"
    }

    def __init__(self, version: str):
        """"""
        self.version = version
        enable_vers = self.InstallerURLs.keys()
        if version not in enable_vers:
            raise ValueError(f"Unsupported version: {version}")
        self.InstallerURL = self.InstallerURLs[version]
    
    def download_installer(self, save_path: str) -> str:
        """"""
        response = requests.get(self.InstallerURL, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in tqdm(response.iter_content(chunk_size=8192)):
                    file.write(chunk)
            print("[CUDA Installer] Download completed: ", save_path)
        else:
            raise Exception(f"Failed to download CUDA installer: {self.InstallerURL} : {response.status_code}")
        return save_path
    
    def download_cuda(self, installer:str) -> None:
        """"""
        print(f"[CUDA Installer] Start installing CUDA {self.version} from {installer}")

        cmd = f"\"{installer}\" -s"  # Assuming '-s' is the correct flag for silent install
        print(f"Executing command: {cmd}")

        try:
            result = subprocess.Popen(cmd, shell=True, capture_output=True, text=True)
        except KeyboardInterrupt:
            pid = result.pid

        # Print stdout and stderr from the subprocess
        if result.stdout:
            print("Installation output:", result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
        
#test
if __name__ == "__main__":
    installer = CUDAInstaller("11.8")
    cuda_installer = installer.download_installer("./cuda_11.8.0_windows_network.exe")
    installer.download_cuda(cuda_installer)