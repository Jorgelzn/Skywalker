import sys
import math
import numpy as np
import tensorflow as tf

tf.get_logger().setLevel('ERROR')

model = tf.keras.models.load_model("model.h5")

individuo = np.genfromtxt('individuo.csv', delimiter=',')

pesos1 = np.reshape(individuo[:140], (7,20))
pesos2 = individuo[140:160]
pesos3 = np.reshape(individuo[160:360], (20,10))
pesos4 = individuo[360:370]
pesos5 = np.reshape(individuo[370:400], (10,3))
pesos6 = individuo[400:]
model.set_weights([pesos1,pesos2,pesos3,pesos4,pesos5,pesos6])

numCheckpoints = int(input())
checkpoints = []
for i in range(numCheckpoints):
    checkpoint = [int(j) for j in input().split()]
    checkpoints.append(checkpoint)

while True:
    checkpoint_index, x, y, vx, vy, angle = [int(i) for i in input().split()]
    checkpoint_x = checkpoints[checkpoint_index][0]
    checkpoint_y = checkpoints[checkpoint_index][1]
    prediction= model.predict([[checkpoint_x,checkpoint_y, x, y, vx, vy, angle]])[0]
    if prediction[2]>200:
        prediction[2]=0
    print(int(prediction[0]),int(prediction[1]),int(prediction[2]))