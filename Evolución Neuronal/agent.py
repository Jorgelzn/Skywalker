import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model("model.h5")

individuo = np.genfromtxt('individuo.csv', delimiter=',')

pesos1 = np.reshape(individuo[:35], (7,5))
pesos2 = individuo[35:40]
pesos3 = np.reshape(individuo[40:55], (5,3))
pesos4 = individuo[55:]
model.set_weights([pesos1,pesos2,pesos3,pesos4])

numCheckpoints = int(input())
checkpoints = []
for i in range(numCheckpoints):
    checkpoint = [int(j) for j in input().split()]
    checkpoints.append(checkpoint)

while True:
    checkpoint_index, x, y, vx, vy, angle = [int(i) for i in input().split()]
    checkpoint_x = checkpoints[checkpoint_index][0]
    checkpoint_y = checkpoints[checkpoint_index][1]
    data = [[checkpoint_x,checkpoint_y, x, y, vx, vy, angle]]
    data = (data - np.min(data)) / (np.max(data) - np.min(data))
    prediction= model.predict(data)[0]*100

    speed = abs(int(prediction[2]))
    pointx = checkpoint_x+int(prediction[0])
    pointy = checkpoint_y+int(prediction[1])


    print(pointx,pointy,speed)