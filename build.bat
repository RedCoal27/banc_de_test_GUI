rmdir /s /q dist
pyinstaller --onefile --add-data "./sources/images/*;./images" --add-data "./sources/lang/*;./lang" --icon=sources/images/xfab.jpg -F .\sources\gui.py

xcopy .\recipes .\dist\recipes /E /I /Y
copy  .\config.json .\dist\config.json