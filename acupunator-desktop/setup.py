import sys
from cx_Freeze import setup, Executable
#LAS LIBRERIAS SE INSTALAN CON OTRO.PY
include_files = [
        'main.py',
        'requirements.txt',
        'setup.py',
        'templates/','img/','packages/']
setup( name = "Acupunator", version = "1.0",
       description = "Sistema de realidad virtual para estudiar acupuntura",
       options = {'build_exe': {'include_files':include_files}},
       author = 'Rodrigo García Ávila, Luis Enrique Hernández Tapia',
       executables = [Executable("main.py",base = "Win32GUI", icon="acupunator.ico")])
