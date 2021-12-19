from os import system, remove, popen
import subprocess

def getFitness(agent, individual, pomDir="."):
    # Run precompiled jar
    jarFile = pomDir + "/target/skeleton-1.0-SNAPSHOT-jar-with-dependencies.jar"
    command = 'java -jar "' + jarFile + '" '
    commandArgs = agent + ' '
    commandArgs += '2> nul'
    # Run each map once
    testFiles = ["prueba.json", "LosailCircuit.json", "BarcelonaCircuit.json", "DoDaLoop.json", "PyramidScheme.json"]
    fitness = 0
    #Write individuo  en archivo txt/csv
    with open('individuo.txt', 'w') as f:
        f.write(individual)
        f.close()
    for testFile in testFiles:
        # Run the simulator
        output = subprocess.check_output(command + testFile + " " + commandArgs, shell=True).decode('utf-8')
        # Find the last frame index
        key_frame = output.rfind("KEY_FRAME")
        key_frame += 10
        newline = key_frame
        while output[newline] != "\n":
            newline += 1
        newFitness = int(output[key_frame:newline])
        #print("Fitness for map " + testFile, newFitness)
        fitness += newFitness
    return fitness
