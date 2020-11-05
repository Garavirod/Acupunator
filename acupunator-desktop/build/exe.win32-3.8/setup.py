import sys
from cx_Freeze import setup, Executable
#LAS LIBRERIAS SE INSTALAN CON OTRO.PY
include_files = [
        'Acupunator.py',
        'requirements.txt',
        'setup.py',
        'templates/','img/','packages/']
setup( name = "Acupunator", version = "1.0",
       description = "Sistema de realidad virtual para estudiar acupuntura",
       options = {'build_exe': {'include_files':include_files}},
       author = 'Rodrigo García Ávila, Luis Enrique Hernández Tapia',
       executables = [Executable("Acupunator.py",base = "Win32GUI", icon="acupunator.ico")])
