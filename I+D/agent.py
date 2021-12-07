import sys
import math
import numpy as np
import tensorflow as tf

checkpoints = int(input())  #Count of checkpoints to read
for i in range(checkpoints):
    # Checkpoint_x: Position X
    # Checkpoint_y: Position Y
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]


model = tf.keras.models.load_model('model.h5')
#individuo = np.random.rand(403)

#pesos1 = np.reshape(individuo[:140], (7,20))
#pesos2 = individuo[140:160]
#pesos3 = np.reshape(individuo[160:360], (20,10))
#pesos4 = individuo[360:370]
#pesos5 = np.reshape(individuo[370:400], (10,3))
#pesos6 = individuo[400:]
#model.set_weights([pesos1,pesos2,pesos3,pesos4,pesos5,pesos6])

# Game loop
while True:
    # checkpoint_index: Index of the checkpoint to lookup in the checkpoints input, initially 0
    # x: Position X
    # y: Position Y
    # vx: horizontal speed. Positive is right
    # vy: vertical speed. Positive is downwards
    # angle: facing angle of this car
    checkpoint_index, x, y, vx, vy, angle = [int(i) for i in input().split()]

    # Write and action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush = True)

    # X Y THRUST MESSAGE
    check_x = checkpoint_x[checkpoint_index]
    check_y = checkpoint_y[checkpoint_index]
    inputs = [[check_x,check_y,x,y,vx,vy,angle]]
    prediction = model.predict(inputs)[0]
    print(prediction[0],prediction[1],prediction[2],"message")