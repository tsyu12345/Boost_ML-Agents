param(
    [bool]$cuda= $false
)

# Function to display a loading animation
function Show-LoadingAnimation {
    $chars = '|/-\'
    $current = 0
    while ($true) {
        Write-Host "`r$($chars[$current])" -NoNewline
        $current++
        if ($current -ge $chars.Length) { $current = 0 }
        Start-Sleep -Milliseconds 100
    }
}

# Check if Visual C++ Build Tools are installed
function Check-VcBuildToolsInstalled {
    # Assuming we check some registry or common installation path; here just a placeholder
    return Test-Path "C:\Path\To\VisualStudio\MSBuild.exe"
}

# Check if Pyenv is installed
function Check-PyenvInstalled {
    return Test-Path "C:\Users\$env:USERNAME\.pyenv\pyenv-win\bin\pyenv.bat"
}

# Install Pyenv if not installed
if (-not (Check-PyenvInstalled)) {
    Write-Host "Pyenv is not installed. Installing now..."
    Invoke-WebRequest -Uri "https://github.com/pyenv-win/pyenv-win/archive/refs/heads/master.zip" -OutFile "$env:TEMP\pyenv.zip"
    Expand-Archive -Path "$env:TEMP\pyenv.zip" -DestinationPath "$env:USERPROFILE\.pyenv"
    [System.Environment]::SetEnvironmentVariable("PYENV", "$env:USERPROFILE\.pyenv\pyenv-win\", "User")
    $env:Path += ";$env:USERPROFILE\.pyenv\pyenv-win\bin;$env:USERPROFILE\.pyenv\pyenv-win\shims"
    Write-Host "Pyenv installation complete."
}

# Install and set Python version using Pyenv
pyenv install 3.10.11 -s
pyenv local 3.10.11

# Install Visual C++ Build Tools if not already installed
if (-not (Check-VcBuildToolsInstalled)) {
    Write-Host "Visual C++ Build Tools not found. Initiating download and installation..."

    # Set up the parameters for downloading Build Tools
    $installerPath = "$env:TEMP\vs_buildtools.exe"
    $installerUrl = "https://aka.ms/vs/17/release/vs_buildtools.exe"

    # Download the installer
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

    # Start loading animation in a background job
    $job = Start-Job -ScriptBlock ${function:Show-LoadingAnimation}

    # Install Visual C++ Build Tools
    Start-Process -FilePath $installerPath -ArgumentList '--add Microsoft.VisualStudio.Workload.VCTools --quiet' -Wait -NoNewWindow

    # Stop the loading animation
    Stop-Job -Job $job
    Remove-Job -Job $job
    Write-Host "`r" -NoNewline

    # Clean up the installer file
    Remove-Item -Path $installerPath
    refreshenv
} else {
    Write-Host "Visual C++ Build Tools are already installed."
}


# Create and activate virtual environment
$envPath = ".venv"
Write-Host "Creating virtual environment... ($envPath)"
python -m venv $envPath

Write-Host "Activating virtual environment..."
. "$envPath\Scripts\Activate.ps1"

# Install packages from requirements.txt
Write-Host "Installing packages from requirements.txt..."
pip install -r requirements.txt

# Conditionally install PyTorch with CUDA if requested
if ($cuda -eq $true) {
    Write-Host "Installing PyTorch with CUDA support..."
    pip install torch==1.13.1+cu116 torchaudio==0.13.1 torchvision==0.14.1+cu116 --index-url https://download.pytorch.org/whl/cu116

    #CUDAインストーラーの起動
    $installerPath = "./cuda_11.6.0_windows_network.exe"
    Write-Output "Installing CUDA 11.6..."
    # Start loading animation in a background job
    $job = Start-Job -ScriptBlock ${function:Show-LoadingAnimation}

    Start-Process -FilePath $installerPath -ArgumentList "-s" -Wait

    # Stop the loading animation
    Stop-Job -Job $job
    Remove-Job -Job $job
    Write-Host "`r" -NoNewline

    Write-Output "CUDA 11.6 installation complete."
}
refreshenv



