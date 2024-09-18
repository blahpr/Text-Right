@echo off
pyinstaller --onefile --icon=images\D.ico --name="Text Right v1.0" --distpath="Text Right v1.0" --add-data="images;images" --add-data "C:\Users\Bobzer\AppData\Local\Programs\Python\Python312\Lib\site-packages\tkdnd\tkdnd\win64;tkdnd" --hidden-import=tkdnd D.pyw
pause.
