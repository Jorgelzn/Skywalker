import sys
import math

from numpy import complex128

def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  return m

def binatodeci(binary):
    return sum(val*(2**idx) for idx, val in enumerate(reversed(binary)))
def main():
    numCheckpoints = int(input())
    checkpoints = []
    for i in range(numCheckpoints):
        checkpoint = [int(j) for j in input().split()]
        checkpoints.append(checkpoint)
        out = open("file.txt", "a")
        print(checkpoint, file=out, flush=True)
        out.close()
    #Abrir el archivo y descodificar a las variables por partes 
    with open("individuo.txt") as f:
        content = f.read()
    content1=content[0:5]
    content2=content[5:10]
    content3=content[10:14]
    list1=toBinary(content1)
    list2=toBinary(content2)
    list3=toBinary(content3)
    blind= binatodeci(list1)
    on_sight= binatodeci(list2)
    minAcceleration= binatodeci(list3)

    #distanceBonus, speedPenalty, minAcceleration, swerveForce = sys.argv[1:]
    #distanceBonus = float(distanceBonus) * 20
    #speedPenalty = float(speedPenalty) * (-20)
    #minAcceleration = float(minAcceleration) * 200
    #swerveForce = float(swerveForce)
    while True:
        checkpoint_index, x, y, vx, vy, angle = [int(i) for i in input().split()]
        cx = checkpoints[checkpoint_index][0]
        cy = checkpoints[checkpoint_index][1]
        
        cx2 = checkpoints[checkpoint_index+1][0]
        cy2 = checkpoints[checkpoint_index+1][1]

        dx = abs(x - cx)
        dy = abs(y - cy)
        
        dx2 = abs(x - cx2)
        dy2 = abs(y - cy2)
        #Porcentaje que relacione distancia y frenado

        thrustAngle = 10
        #Miraa el angulo en el que se mueve la nbave y saca el vector velocidad, 
        # luego saca el angulo ideal con el angulo que forma el vector distancia entre el checkpoint y la nave y luego te hace calculo
        distance1 = math.sqrt((cx - x)**2 + (cy - y)**2)
        distance2 = math.sqrt((cx2 - x)**2 + (cy2 - y)**2)
        #El ángulo de giro de golpe que debería dar para estar apuntando al siguiente checkpoint , pasado de radianes a grados
        bestAngle1 = math.acos((cx - x) / distance1) * 180 / math.pi
        bestAngle2 = math.acos((cx2 - x) / distance2) * 180 / math.pi

        # First quadrant
        if 0 <= bestAngle1 and bestAngle1 <= 90 and cy - y < 0:
            bestAngle1 = 360 - bestAngle1
        # Second quadrant
        if 90 < bestAngle1 and bestAngle1 <= 180 and cy - y < 0:
            bestAngle1 = 180 + (180 - bestAngle1)

        # First quadrant
        if 0 <= bestAngle2 and bestAngle2 <= 90 and cy2 - y < 0:
            bestAngle2 = 360 - bestAngle2
        # Second quadrant
        if 90 < bestAngle2 and bestAngle2 <= 180 and cy2 - y < 0:
            bestAngle2 = 180 + (180 - bestAngle2)

        angleCorrection = bestAngle1 - angle
        angleCorrection2 = bestAngle2 - angle
        
        if (angleCorrection <= 18 and angleCorrection >= -18 and angleCorrection2 <= 18 and angleCorrection2 >= -18):
            blind=0
        else:
            on_sight=0
        
        #Ángulo con el que acelera
        thrustAngle =  angle + angleCorrection
        thrustAngle *= math.pi / 180
        #Formula para que acelere según lo alineado que este con el checpoint
        acc =  (((180 - abs(angleCorrection)) / 180) * math.sqrt(dx * dx + dy * dy) / 100 + math.sqrt(vx * vx + vy * vy) / 10 ) +(on_sight)-(blind)

        if acc <minAcceleration:
            acc = minAcceleration
        if acc > 200:
            acc = 200

        print(str(x + int(100 * math.cos(thrustAngle))) + " " + str(y + int(100 * math.sin(thrustAngle))) + " " + str(int(acc)))
if __name__ == "__main__":
    main()