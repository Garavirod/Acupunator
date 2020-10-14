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

# import sys
# from cx_Freeze import setup, Executable

# include_files = [
#         'cfdi.log',
#         'conf.py',
#         'credenciales.txt',
#         'Descarga.py',
#         'Hola.png',
#         'invoices.sqlite',
#         'main.py',
#         'Parametros.py',
#         'requirements.txt',
#         'settings.py',
#         'setup.py',
#         'templates/','png/','bin/','sat/']
 #includes = ["click",'pillow','python-dateutil','pyOpenSSL','PyQt5','requests','Logbook']
 #packages = ["PIL"]
 #excludes = ["tkinter"]
# zip_include_packages=["*"],
# zip_exclude_packages: [""]
        #"cx-freeze",
        #click
        #"Pillow"
        #"python-dateutil",
        #"pyOpenSSL",
        #"PyQt5",
        #"requests",
        #"peewee",
        #"Logbook"
# setup(
#     name = 'Murgati SAT',
#     version = '0.1',
#     description = 'Brought to you by xxx',
#     author = 'Rodrigo, Tapia',
#     author_email = 'tapia641@gmail.com',
#     options = {'build_exe': {'include_files':include_files}}, 
#     executables = [Executable('main.py')]
# )