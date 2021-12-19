import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import fitnessProxy 
import csv


# Imprime una población:
def printPoblacion(poblacion):
    for i in range(len(poblacion)):
        print("individuo", i, " ", end="")
        for j in range(len(poblacion[0])):
            print(poblacion[i][j], end = "")
        print("")

def inicializacion(m, size):
    # Se inicializa una matriz con las dimensiones que recibe como parámetros
    # Aquí guardaremos los individuos
    poblacion = [[0 for x in range(size)] for y in range(m)] 
    for i in range(m):
        for j in range(size):
            # A cada bit de cada individuo se le asignará un 0 o un 1 con un 50% de probabilidad
            poblacion[i][j] = random.randint(0,1)
    return poblacion

def evaluacion(m, size, poblacion, mejorSolucion, generacion):
    valores = [] # Aquí guardaremos los valores de evaluación de cada individuo
    for i in range(m):
        chromosome = ""
        for j in range(size):
            chromosome = chromosome + str(poblacion[i][j])
        num = float(fitnessProxy.getFitness("agente_gen.py", chromosome,"."))
        #r = requests.get(website + chromosome)
        #num = float(r.text)
        # Guardando el valor de evaluación de cada individuo en una lista:
        valores.append(num)
        # Comprobar si es la mejor solución encontrada hasta ahora y en ese caso actualizarla:
        if (num < mejorSolucion[1]):
            mejorSolucion[0] = poblacion[i]
            mejorSolucion[1] = num
            mejorSolucion[2] = generacion
    return valores

def seleccionMejores(poblacion, valores, k):
    valoresCopy = copy.copy(valores)
    # Se ordena la lista de valores de menor a mayor y se eligen los índices de los k primeros (los mejores):
    mejoresIndex = np.argsort(valoresCopy)[:k]
    # Los individuos de la población que se corresponden con esos índices se guardan en 'mejores':
    mejores = []
    for i in range(k):
        mejores.append(copy.deepcopy(poblacion[mejoresIndex[i]]))
    return mejores

def seleccionTorneos(m, t, k, poblacion, valores):
    # Se realiza un número de torneos igual al número de individuos - k, es decir, aquellos que sí serán reemplazados:
    nuevaPoblacion = []
    for i in range(m-k):
        smallestVal = 9999999999
        smallestIndex = 0
        # En cada torneo se elije un t% random de individuos:
        for j in range(int(t*m/100)):
            elegido = random.randint(0,m-1)
            # Se busca el índice del menor valor:
            if valores[elegido] < smallestVal:
                smallestVal = valores[elegido]
                smallestIndex = elegido
        nuevaPoblacion.append(poblacion[smallestIndex])
    return nuevaPoblacion

def cruce(m, k, size, nuevaPoblacion):
    #Se "desordena" la población para aleatorizar el emparejamiento:
    random.shuffle(nuevaPoblacion)
    #Se atraviesa el array en orden y se emparejan los individuos de dos en dos:
    for i in range(int((m-k)/2)):
        for j in range(size):
            #Se realiza una recombinación uniforme.
            #Se analizan los bits homólogos (en la misma posición j) de ambos progenitores.
            #Solo si los bits son distintos (la distancia de Hamming no es 0)
            #se considera intercambiarlos con una probabilidad del 50%:   
            if (nuevaPoblacion[2*i][j] != nuevaPoblacion[2*i+1][j]):
                swap = random.randint(0,1)
                if (swap):
                    aux = nuevaPoblacion[2*i][j]
                    nuevaPoblacion[2*i][j] = nuevaPoblacion[2*i+1][j]
                    nuevaPoblacion[2*i+1][j] = aux

def mutacion(m, k, size, nuevaPoblacion, f):
    # Ir individuo por individuo, bit por bit, y con una probabilidad muy baja (f%) cambiar ese bit
    for i in range(m-k):
        for j in range(size):
            mutar = random.uniform(0,1)
            if (mutar <= f):
                nuevaPoblacion[i][j] = 1 - nuevaPoblacion[i][j]

def main():
    #       Características del problema:
    # Número de bits que requiere la codificación de los individuos (en nuestro caso 11 bits):
    size = 14

    #       Parámetros elegidos:
    # El tamaño de la población será de 100 individuos:
    m = 20
    # Porcentaje de elitismo (porcentaje de individuos con mejor fitness
    # que no serán reemplazados al final de la generación):
    p = 10 
    # Porcentaje de individuos que competirán en cada torneo:
    t = 15
    # Factor de mutación:
    f = 0.05
    # Límite de generaciones sin mejora (criterio de parada):
    parada = 10
    # Número de individuos que no serán reemplazados 
    k = int((p*m)/100) 

    #       Variables de utilidad:
    # Contador de generaciones:
    generacion = 0
    # Variable que guardará el mejor individuo, su valor de evaluación, y su índice en el array población
    mejorSolucion = [[],9999999999.999999, 0]
    # Aquí guardaremos los mejores valores de evaluación de cada generación, con el objetivo de graficar la evolución:
    plot = []
    # Contador utilizado para el criterio de parada:
    # El algoritmo se detiene cuando pasen 50 generaciones consecutivas sin que se encuentre un mejor individuo
    generacionesSinMejora = 0

    #       Algoritmo:

    # Inicialización aleatoria de la población:
    
    poblacion = inicializacion(m, size)
    

    # Bucle principal:
    #while(generacionesSinMejora < parada and mejorSolucion[1] != 0):
    while(generacion < 30):
        ### EVALUACIÓN ###
        # Guardamos el mejor valor que teníamos hasta ahora:
        aux = mejorSolucion[1]
        valores = evaluacion(m, size, poblacion, mejorSolucion, generacion)
        # Si tras la evaluación, el valor de evaluación en mejorSolucion ha cambiado,
        # entonces se ha encontrado un mejor individuo, así que ha habido mejora
        if (aux != mejorSolucion[1]):
            # Si se ha encontrado un individuo mejor, se reinicia el contador,
            # dando oportunidad al algoritmo a que siga mejorando:
            generacionesSinMejora = 0
        else:
            # Si no se ha encontrado un individuo mejor, se aumenta el contador,
            # y si este llega a un valor muy alto es indicador de que el algoritmo puede haberse estancado
            # y ya no sea capaz obtener resultados más óptimos:
            generacionesSinMejora += 1
        # Imprimir el mejor fitness de esta iteración:
        indexMin = valores.index(min(valores))
        print("Mejor valor de evaluación de la generación #", generacion, ": ", valores[indexMin])
        myFile = open('evaluaciones.csv', 'a')
        with myFile:
            writer = csv.writer(myFile)
            if(generacion == 0):
                writer.writerow(["Generacion","Fitness", "Individuo","Mejor de generación"])
            writer.writerows([str(generacion), str(mejorSolucion[1]), str(mejorSolucion[0]),str(valores[indexMin])])
        print("Mejor valor obtenido por ahora: ", mejorSolucion[1], "en la generación #", mejorSolucion[2])
        # Guardar su valor en la lista 'plot' para graficarlo al final del algoritmo:
        plot.append(valores[indexMin])

        ### SELECCIÓN ###
        # Los k mejores individuos se guardan en la lista 'mejores':
        mejores = seleccionMejores(poblacion, valores, k)
        # El resto se seleccionan por torneos:
        nuevaPoblacion = seleccionTorneos(m, t, k, poblacion, valores)
        
        ### CRUCE ###
        cruce(m, k, size, nuevaPoblacion)

        ### MUTACIÓN ###
        mutacion(m, k, size, nuevaPoblacion, f)

        ### REEMPLAZO ###
        # La nueva población estará formada por los m-k individuos que pasaron por el proceso de selección, cruce y mutación
        # y los k mejores de la anterior ronda sin modificación
        poblacion = [row[:] for row in nuevaPoblacion]
        for i in range(k):
            poblacion.append(mejores[i])

        # Incrementamos el contador de generaciones:
        generacion += 1

    # Finalmente se imprime el mejor individuo al finalizar la ejecución del algoritmo:
    f = open("demofile2.txt", "a")
    f.write("Mejor solución encontrada:"+str(mejorSolucion[0])+"fitness"+str(mejorSolucion[1])+"\n")
    f.close()
    print("Mejor solución encontrada: ", mejorSolucion[0], "con fitness = ", mejorSolucion[1])
    # Y se grafica la evolución del fitness a lo largo de las generaciones:
    plt.plot(plot)
    plt.ylabel("Mejor valor de evaluación")
    plt.xlabel("Generación")
    plt.show()

if __name__ == "__main__":
    main()