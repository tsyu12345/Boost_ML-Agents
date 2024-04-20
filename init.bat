@echo off
setlocal

REM 仮想環境のディレクトリを指定
set "ENV_PATH=.TESTvenv"

echo Creating virtual environment... (%ENV_PATH%)
python -m venv %ENV_PATH%
echo Virtual environment created.

echo Activating virtual environment...
call "%ENV_PATH%\Scripts\activate.bat"
echo Virtual environment activated.

endlocal
