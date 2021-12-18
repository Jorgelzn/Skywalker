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

def mute(poblacion,mutation_factor):
    mutaciones = []
    
    for individuo in range(len(poblacion)):
        mutacion = []

        vectors = rnd.sample([a for a in range(len(poblacion))],3)

        for gen in range(poblacion[individuo].size):
            w = poblacion[vectors[0]][gen]
            y = poblacion[vectors[1]][gen]
            z = poblacion[vectors[2]][gen]
            mutacion.append(w+mutation_factor*(y-z))

        mutaciones.append(np.array(mutacion))

    return mutaciones

def combine(poblacion, mutaciones,combination_factor):
    
    descendientes = []
    
    for j in range(len(poblacion)):

        descendiente = []
        
        for i in range(poblacion[0].size):
            valor = rnd.uniform(0,1)
            if(valor <= combination_factor):
                descendiente.append(mutaciones[j][i])
            else:
                descendiente.append(poblacion[j][i])

        descendientes.append(np.array(descendiente))
        
    return descendientes


if __name__ == "__main__":

    generations = 10
    poblacion = initialize(10)
    fitness_poblacion = get_fitness(poblacion)

    for i in range(generations):
        
        mutaciones = mute(poblacion,0.8)

        descendientes = combine(poblacion,mutaciones,0.5)

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


