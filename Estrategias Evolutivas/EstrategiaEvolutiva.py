import numpy as np
import math
import pandas as pd
from joblib import Parallel, delayed
from fitnessProxy import getFitness

NJOBS = 1

def evolutionaryStrategyMultiple(agent, solutionSize, populationSize, familySize, lambdaVal, b, numGenerations):
    # Generar una población inicial aleatoria
    solutions = np.random.rand(populationSize, solutionSize)
    variances = np.random.uniform(low=0.1, high=0.5, size=[populationSize, solutionSize])
    fitness = np.zeros(populationSize)
    # Almacenar los datos de cada generación para su posterior análisis
    outputData = []
    # Constante de mutación de las varianzas
    tau = b/math.sqrt(2 * math.sqrt(lambdaVal))
    for generation in range(numGenerations):
        # Guardar la mejor fitness y el mejor individuo
        bestSolution = 0
        # Evaluar la población actual
        fitness = [getFitness(agent, solutions[i]) for i in range(populationSize)]
        for i in range(populationSize):
            if fitness[i] < fitness[bestSolution]:
                bestSolution = i
        # Guardar los datos
        outputData.append({"Generation": generation + 1, "Solution": solutions[bestSolution].copy(), "Variances": variances[bestSolution].copy(), "Fitness": fitness[bestSolution]})
        print(outputData[-1])
        # Generar los pesos para la selección inversamente proporcional al fitness
        weights = [1 / fit for fit in fitness]
        sumWeights = sum(weights)
        weights = [w / sumWeights for w in weights]
        # Generar los descendientes
        descendants = np.zeros([lambdaVal, solutionSize])
        descendantVariances = np.zeros([lambdaVal, solutionSize])
        for i in range(lambdaVal):
            # Seleccionar los individuos que darán lugar al descendiente
            family = [np.random.choice(range(populationSize), p=weights) for p in range(familySize)]
            # Generar la parte funcional como la media aritmética de los progenitores
            for parent in family:
                descendants[i] += solutions[parent]
            descendants[i] /= familySize
            # Generar las varianzas por cruce posicional
            varianceParents = np.random.randint(low=0, high=familySize, size=solutionSize)
            for j in range(solutionSize):
                descendantVariances[i, j] = variances[family[varianceParents[j]], j]
                # Mutar la parte funcional del descendiente
                descendants[i, j] += np.random.normal(0, math.sqrt(descendantVariances[i, j]))
                # Asegurar que el valor se encuentre dentro del rango permitido
                descendants[i, j] %= 360
            # Mutar la varianza del descendiente
            descendantVariances[i] *= np.e ** np.random.normal(0, tau)
        # Generar la nueva población con los mejores individuos entre padres e hijos
        descendantsFitness = [getFitness(agent, descendants[i]) for i in range(lambdaVal)]
        #descendantsFitness = Parallel(n_jobs=NJOBS)(delayed(getFitness)(agent, descendants[i]) for i in range(lambdaVal))
        generatedSolutions = 0
        newSolutions = np.zeros([populationSize, solutionSize])
        newVariances = np.zeros([populationSize, solutionSize])
        addedParents = []
        addedDescendants = []
        bestParent = -1
        bestDescendant = -1
        while generatedSolutions < populationSize:
            # Determinar el mejor individuo de entre los padres
            if bestParent == -1:
                bestParent = 0
                while bestParent in addedParents:
                    bestParent += 1
                for i in range(populationSize):
                    if i not in addedParents and fitness[i] < fitness[bestParent]:
                        bestParent = i
            # Determinar el mejor individuo de entre los descendientes
            if bestDescendant == -1:
                bestDescendant = 0
                while bestDescendant in addedDescendants:
                    bestDescendant += 1
                for i in range(lambdaVal):
                    if i not in addedDescendants and descendantsFitness[i] < descendantsFitness[bestDescendant]:
                        bestDescendant = i
            # Añadir el mejor de ambos
            if bestDescendant >= len(descendantsFitness) or fitness[bestParent] < descendantsFitness[bestDescendant]:
                newSolutions[generatedSolutions] = solutions[bestParent]
                newVariances[generatedSolutions] = variances[bestParent]
                generatedSolutions += 1
                addedParents.append(bestParent)
                bestParent = -1
            else:
                newSolutions[generatedSolutions] = descendants[bestDescendant]
                newVariances[generatedSolutions] = descendantVariances[bestDescendant]
                generatedSolutions += 1
                addedDescendants.append(bestDescendant)
                bestDescendant = -1
        solutions = newSolutions
        variances = newVariances
    return pd.DataFrame(outputData)

if __name__ == "__main__":
    output = evolutionaryStrategyMultiple("AgenteEE.py", 4, 25, 4, 20, 1, 100)
    output.to_csv("salidaEE.csv")