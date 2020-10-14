import os
from os import remove

# ACTUALIZACIÓN DE PIP
def updatePIP():
    print("----------------------Actualizando PIP--------------------------")
    try:
        os.system('python -m pip install --user --upgrade pip')
        return True
    except:
        print("Error al actualzar pip")
        return False

# INSTALACIÓN DE DEPENDENCIAS
def installDependencies():
    try:
        print("----------------------Instalando dependencias--------------------------")
        os.system('python -m pip install --user -r requirements.txt')
        return True
    except:
        print("Error al instalr dependencias")
        return False

# CREADOR DEL INSTALADOR
def createBuildProduction():
    try:
        print("----------------------Creando instalador--------------------------")
        os.system('python setup.py build')
        return True
    except:
        print("Error al crear el instalador de produción")
        return False

if __name__ == "__main__":
    is_pip = updatePIP()
    is_dep = installDependencies()

    if is_dep and is_pip:
        is_build = createBuildProduction()
        if is_build:
            print("¡Instalación terminada exitosamente!")
        else:
            print("No se pudo realizar la instalación")
    
    print("----------------------Proceso terminado--------------------------")

