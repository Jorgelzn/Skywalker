from numpy.core.fromnumeric import argmin
from fitnessProxy import getFitness
import numpy as np
import random as rnd
from tqdm import tqdm

def initialize(num_poblacion):
    poblacion=[]
    for i in range(num_poblacion):
        poblacion.append(np.random.uniform(-1,1,58))
    return poblacion

def get_fitness(poblacion):
    fitness=[]
    for i in tqdm (range(len(poblacion)), desc="Loading..."):
        value = getFitness(poblacion[i])
        if value <= 130:
            value=370
        fitness.append(value)
    return fitness

def mute(poblacion,factor_mutacion):
    mutaciones = []
    vectors = rnd.sample([a for a in range(len(poblacion))],3)
    valor_w = vectors[0]
    valor_y = vectors[1]
    valor_z = vectors[2]
    
    for individuo in range(len(poblacion)):
        mutacion = []
        for gen in range(poblacion[individuo].size):
            w = poblacion[valor_w][gen]
            y = poblacion[valor_y][gen]
            z = poblacion[valor_z][gen]
            mutacion.append(w+factor_mutacion*(y-z))
        mutaciones.append(np.array(mutacion))

    return mutaciones

def combine(poblacion, mutaciones):
    
    descendientes = []
    
    for j in range(len(poblacion)):

        descendiente = []
        
        for i in range(poblacion[0].size):
            valor = rnd.randint(0,1)
            if(valor == 0):
                descendiente.append(poblacion[j][i])
            else:
                descendiente.append(mutaciones[j][i])

        descendientes.append(np.array(descendiente))
        
    return descendientes


if __name__ == "__main__":

    generations = 10
    poblacion = initialize(10)
    fitness_poblacion = get_fitness(poblacion)

    for i in range(generations):
        
        mutaciones = mute(poblacion,0.8)

        descendientes = combine(poblacion,mutaciones)

        fitness_descendientes = get_fitness(descendientes)

        for individuo in range(len(poblacion)):
            if fitness_descendientes[individuo] < fitness_poblacion[individuo]:
                poblacion[individuo] = descendientes[individuo]
                fitness_poblacion[individuo] = fitness_descendientes[individuo]
        print("Generation",i+1)
        print("fitness population:",fitness_poblacion)
        print("Best fitness of generation:",min(fitness_poblacion))

    best = poblacion[argmin(fitness_poblacion)]
    print("Best model weights:",best)
    np.savetxt("individuo.csv",best, delimiter=",")


