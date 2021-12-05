from os import system, remove

def getFitness(pomDir):
    # Run precompiled jar
    jarFile = pomDir + "/target/skeleton-1.0-SNAPSHOT-jar-with-dependencies.jar"
    system('java -jar "' + jarFile + '" > temp.txt 2> nul')
    # Open the output file
    fileContents = None
    with open("temp.txt", "r") as file:
        fileContents = file.readlines()
    # Yeet the temporary file
    remove("temp.txt")
    # Find the last KEY_FRAME line
    fitness = 999
    for i in reversed(range(len(fileContents))):
        if fileContents[i].startswith("KEY_FRAME"):
            fitness = fileContents[i].split(' ')[1]
            break
    return fitness
