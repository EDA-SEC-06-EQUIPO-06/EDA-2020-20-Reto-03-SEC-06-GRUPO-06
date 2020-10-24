"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


Afile = 'us_accidents_dis_2016.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Consultar los accidentes en una fecha por severidad")
    print("4- Consultar los accidentes anteriores a una fecha")
    print("5- Consultar los accidentes en un rango de fechas")
    print("6- Consultar los accidentes por rango de horas")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes....")
        controller.loadData(cont, Afile)
        print('Accidentes cargados: ' + str(controller.accidentesSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))

    elif int(inputs[0]) == 3:
        print("\nBuscando los accidentes en una fecha por severidad: ")
        StartDate = input("Fecha (YYYY-MM-DD): ")
        severity = input("Numero de severidad: ")
        numaccidentes = controller.getaccidentesByRangeCode(cont, StartDate, severity)
        print("\nTotal de accidentes de severidad " + "'" + severity + "'" + " en esa fecha:  " + str(numaccidentes))

    elif int(inputs[0]) == 4:
        initialDate=str(controller.minKey(cont))
        finalDate = input("Fecha (YYYY-MM-DD): ")
        total = controller.getaccidentesMByRange(cont, initialDate, finalDate)
        print("\nBuscando los accidentes anteriores a una fecha: ")
        print("\nTotal de accidentes antes de la fecha: " + str(total))

    elif int (inputs[0]) ==5:
        StartDate = input("Fecha inicial (YYYY-MM-DD): ")
        EndDate = input("Fecha final (YYYY-MM-DD): ")
        print("\nBuscando los accidentes en un rango de fechas: ")
        accidentes_rango = controller.getaccidentesRangoFechas(cont, StartDate, EndDate)
        estado = accidentes_rango[0][0]
        num_estado = accidentes_rango[0][1]
        fecha = accidentes_rango[1][0]
        num_fecha = accidentes_rango[1][1]
        print("\nEn este rango de fechas el estado con más accidentes es: "+ estado +" con "+ str(num_estado) + " accidentes ")
        print("\nLa fecha con mayor número de accidentes es: "+ fecha +" con "+ str(num_fecha) + " accidentes ")
    elif int (inputs[0]) ==6:
        Start_Time = input("Hora inicial (Ejemplo: 16:00): ")
        End_Time = input("Hora final(Ejemplo: 17:30): ")
        print("\nBuscando los accidentes en un rango de horas por severidad: ")
        accidentes_hora = controller.getaccidentesbyRangoHoras(cont, Start_Time, End_Time)
        print("\nEl total de accidentes agrupados por severidad en este rango de hora es: ")
        print("\nSeveridad 1:", accidentes_hora["1"])
        print("\nSeveridad 2:", accidentes_hora["2"])
        print("\nSeveridad 3:", accidentes_hora["3"])
        print("\nSeveridad 4:", accidentes_hora["4"]) 
    else:
        sys.exit(0)
sys.exit(0)
