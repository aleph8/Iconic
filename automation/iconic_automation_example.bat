@echo off

echo [!] Cleaning ...

del /q ..\release\Loader.exe
del ..\iconCreator\assembly.dll

echo [!] Compiling the payload ...
echo:

cd ..\payloads\assembly\
dotnet build

copy bin\Debug\net9.0\win-x64\assembly.dll ..\..\iconCreator\
cd ..\..\iconCreator

echo:
echo [!] Making the stego ICO file and hiding the payload ...
echo:

call .\.venv\Scripts\activate.bat
python.exe .\example_auto_hide_dll.py .\image_samples\vtlogo.png .\assembly.dll iconic.ico
move iconic.ico ..\loaders\loader_example

echo:
echo [!] Compiling the loader with the icon ...
echo:

cd ..\loaders\loader_example
dotnet publish --property WarningLevel=0

copy bin\Release\net9.0\win-x64\publish\Loader.exe ..\..\release
cd ..\..

echo:
echo [0] DONE! Press any key to finish...
pause > nul