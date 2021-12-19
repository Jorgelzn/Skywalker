from os import system, remove, popen
import subprocess

def getFitness(agent, individual, pomDir="."):
    # Run precompiled jar
    jarFile = pomDir + "/target/skeleton-1.0-SNAPSHOT-jar-with-dependencies.jar"
    command = 'java -jar "' + jarFile + '" '
    commandArgs = agent + ' '
    for i in individual:
        commandArgs += str(i) + ' '
    commandArgs += '2> nul'
    # Run each map once
    testFiles = ["prueba.json", "LosailCircuit.json", "BarcelonaCircuit.json", "DoDaLoop.json", "PyramidScheme.json"]
    fitness = 0
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
        fitness += newFitness
    return fitness

