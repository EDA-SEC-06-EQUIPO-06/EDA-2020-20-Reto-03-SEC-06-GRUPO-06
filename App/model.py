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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config
import operator

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los accidentes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidentes': None,
                'dateIndex': None
                }

    analyzer['accidentes'] = lt.newList('SINGLE_LINKED', compareseverity)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer

# Funciones para agregar informacion al catalogo

def addaccidente(analyzer, accidente):

    lt.addLast(analyzer['accidentes'], accidente)
    updateDateIndex(analyzer['dateIndex'], accidente)
    return analyzer

def updateDateIndex(map, accidente):
    """
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de accidentes
    y se actualiza el indice de tipos de accidentes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de accidentes
    """
    occurreddate = accidente['Start_Time']
    accidentedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentedate.date())
    if entry is None:
        datentry = newDataEntry(accidente)
        om.put(map, accidentedate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accidente)
    return map


def addDateIndex(datentry, accidente):
    """
    Actualiza un indice de tipo de accidente.  Este indice tiene una lista
    de accidentes y una tabla de hash cuya llave es el tipo de accidente y
    el valor es una lista con los accidentes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidentes']
    lt.addLast(lst, accidente)
    severityIndex = datentry['severityIndex']
    severityentry = m.get(severityIndex, accidente['Severity'])
    if (severityentry is None):
        entry = newseverityEntry(accidente['Severity'], accidente)
        lt.addLast(entry['lstseverity'], accidente)
        m.put(severityIndex, accidente['Severity'], entry)
    else:
        entry = me.getValue(severityentry)
        lt.addLast(entry['lstseverity'], accidente)
    return datentry

def newDataEntry(accidente):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'severityIndex': None, 'lstaccidentes': None}
    entry['severityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareseverity)
    entry['lstaccidentes'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newseverityEntry(severity, accidente):
    """
    Crea una entrada en el indice por tipo de accidente, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    severityentry = {'severity': None, 'lstseverity': None}
    severityentry['severity'] = severity
    severityentry['lstseverity'] = lt.newList('SINGLELINKED', compareseverity)
    return severityentry

# ==============================
# Funciones de consulta
# ==============================


def accidentesSize(analyzer):
    """
    Número de accidentes leidos

    """
    return lt.size(analyzer['accidentes'])


def indexHeight(analyzer):
    """
    Altura del indice (arbol)

    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """
    Numero de nodos en el arbol

    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """
    La menor llave del arbol

    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """
    La mayor llave del arbol

    """
    return om.maxKey(analyzer['dateIndex'])



def getaccidentesByRangeCode(analyzer, StartDate, severity):
    """
    Para una fecha determinada, retorna el numero de accidentes
    de un tipo especifico.
    """
    accidentedate = om.get(analyzer['dateIndex'], StartDate)
    if accidentedate['key'] is not None:
        severitymap = me.getValue(accidentedate)['severityIndex']
        numaccidentes = m.get(severitymap, severity)
        if numaccidentes is not None:
            return m.size(me.getValue(numaccidentes)['lstseverity'])
        return 0

def informacion_accidentes(cantidad_accidentes, accidents, dicc_estados):
    for j in range(cantidad_accidentes):
        accidente = lt.getElement(accidents, j)
        if accidente["value"] is not None:
           lista_accidentes = accidente["value"]["lstseverity"]
           primer_accidente = lt.firstElement(lista_accidentes)  
           fecha = primer_accidente["Start_Time"][0:10]
           tamanio_lst = lt.size(lista_accidentes)
           for i in range(tamanio_lst):
               elemento = lt.getElement(lista_accidentes, i)
               estado = elemento["State"]
               if estado not in dicc_estados:
                  dicc_estados[estado] = 1
               else:
                  dicc_estados[estado] += 1              
    return fecha, tamanio_lst, dicc_estados
                      
def getaccidentesRangoFechas(analyzer, StartDate, EndDate):
    """
    Para una fecha inicial y final, retorna el numero de accidentes
    e indica la categoría de accidentes más reportada en ese rango.
    """
    lst = om.values(analyzer['dateIndex'], StartDate, EndDate)
    mayor = 0
    dicc_estados = {"1":0,"2":0,"3":0,"4":0}
    for i in range(lt.size(lst)):
        accidentes_dia = lt.getElement(lst, i)['severityIndex']["table"]
        cantidad_accidentes = lt.size(accidentes_dia)   
        info = informacion_accidentes(cantidad_accidentes, accidentes_dia, dicc_estados) 
        conteo = info[1] 
        if conteo > mayor:
           mayor = conteo
           fecha_mayor = info[0]
    ordenar_dicc = sorted(dicc_estados.items(), key=operator.itemgetter(1), reverse=True)
    estado_mas = ordenar_dicc[0]         
    res = [estado_mas,(fecha_mayor, mayor)] 
    return res     

def total_severidad_hora(cantidad_accidentes, accidents, Start_Time, End_Time, dicc_severidad):
    for j in range(cantidad_accidentes):
        accidente = lt.getElement(accidents, j)
        if accidente["value"] is not None:
           lista_accidentes = accidente["value"]["lstseverity"]
           tamanio_lst = lt.size(lista_accidentes)
           for i in range(tamanio_lst):
               elemento = lt.getElement(lista_accidentes, i)
               hora_inicial = elemento["Start_Time"][11:16]
               hora_final = elemento["End_Time"][11:16]
               if Start_Time < hora_inicial and End_Time > hora_final:
                  for severidad in dicc_severidad:
                      if severidad == elemento["Severity"]:
                         dicc_severidad[severidad] += 1       
    return dicc_severidad  

def getaccidentesRangoHoras(analyzer, Start_Time, End_Time):
    """
    Para una rango de horas, retorna el numero de accidentes
    agrupados por severidad y su porcentaje contra el total de
    accidentes reportados
    """    
    lst = om.values(analyzer['dateIndex'], minKey(analyzer), maxKey(analyzer))
    dicc_severidad = {"1":0,"2":0,"3":0,"4":0}
    for i in range(lt.size(lst)):
        accidentes_dia = lt.getElement(lst, i)['severityIndex']["table"]
        cantidad_accidentes = lt.size(accidentes_dia)   
        total_severidad = total_severidad_hora(cantidad_accidentes, accidentes_dia, Start_Time, End_Time, dicc_severidad)
    total_accidentes = 0
    for severidad in dicc_severidad:
        total_accidentes += dicc_severidad[severidad]
    for severidad in total_severidad:    
        porcentaje = round(int(dicc_severidad[severidad]) / total_accidentes, 2)
        dicc_severidad[severidad] = ("Cantidad accidentes: " + str(dicc_severidad[severidad]), "Porcentaje: "+str((porcentaje * 100)))  
    return dicc_severidad        

# ==============================
# Funciones de Comparacion
# ==============================

def compareIds(id1, id2):
    """
    Compara dos accidentes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareDates(date1, date2):
    """
    Compara dos ids de accidentes, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareseverity(severity1, severity2):
    """
    Compara dos ids , id es un identificador
    y entry una pareja llave-valor
    """
    severity = me.getKey(severity2)
    if (severity1 == severity):
        return 0
    elif (severity1 > severity):
        return 1
    else:
        return -1      
 