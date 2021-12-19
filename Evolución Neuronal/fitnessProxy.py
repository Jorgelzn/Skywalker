import subprocess
import numpy as np

def getFitness(individual, pomDir="."):
    np.savetxt("individuo.csv",individual, delimiter=",")
    # Run precompiled jar
    jarFile = pomDir + "/target/skeleton-1.0-SNAPSHOT-jar-with-dependencies.jar"
    command = 'java -jar "' + jarFile + '" '
    command += ' 2> nul'
    # Run the simulator
    output = subprocess.check_output(command, shell=True).decode('utf-8')
    # Find the last frame index
    key_frame = output.rfind("KEY_FRAME")
    key_frame += 10
    newline = key_frame
    while output[newline] != "\n":
        newline += 1
    fitness = int(output[key_frame:newline])
    return fitness