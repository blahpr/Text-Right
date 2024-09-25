@echo off
pyinstaller --onefile --icon=images\D.ico --name="Text Right v1.0" --distpath="Text Right v1.0" --add-data="images;images" --add-data "C:\Users\Bobzer\AppData\Local\Programs\Python\Python312\Lib\site-packages\tkdnd\tkdnd\win64;tkdnd" --upx-dir "C:\upx-4.2.4-win64" D.pyw 
"C:\upx-4.2.4-win64\upx.exe" --brute --force "Text Right v1.0\Text Right v1.0.exe"
echo.
pause.
