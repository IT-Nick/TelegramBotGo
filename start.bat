@echo off

call %~dp0\tgvenv\Scripts\activate

cd %~dp0

set TOKEN=

python main.py

pause
