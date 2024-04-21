param(
    [bool]$cuda= $false
)

# 仮想環境のディレクトリを指定
$envPath = ".TESTvenv"

Write-Host "Creating virtual environment... ($envPath)"
python -m venv $envPath

Write-Host "Activating virtual environment..."
. "$envPath\Scripts\Activate.ps1"

# pip install
Write-Host "Installing packages from requirements.txt..."
pip install -r requirements.txt

if ($cuda -eq $true) {
    Write-Host "Installing PyTorch with CUDA support..."
    pip install torch==1.13.1+cu116 torchaudio==0.13.1 torchvision==0.14.1+cu116 --index-url https://download.pytorch.org/whl/cu116
}


#CUDAインストーラーの起動
$installerPath = "./cuda_11.6.0_windows_network.exe"
Write-Output "Installing CUDA 11.6..."
Start-Process -FilePath $installerPath -ArgumentList "-s" -Wait
Write-Output "CUDA 11.6 installation complete."
