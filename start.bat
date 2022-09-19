@echo off

call %~dp0\tgvenv\Scripts\activate

cd %~dp0

set TOKEN=5737568872:AAHNw4VyrniXNPx3mUZgbZojHKdHlicmOiA

python main.py

pause