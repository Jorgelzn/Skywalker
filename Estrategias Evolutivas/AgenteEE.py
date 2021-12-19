import sys
import math

# Leer los checkpoints
numCheckpoints = int(input())
checkpoints = []
for i in range(numCheckpoints):
    checkpoint = [int(j) for j in input().split()]
    checkpoints.append(checkpoint)
    out = open("file.txt", "a")
    print(checkpoint, file=out, flush=True)
    out.close()

# Desnormalizar los parámetros
distanceBonus, speedPenalty, minAcceleration, swerveForce = sys.argv[1:]
distanceBonus = float(distanceBonus) * 20
speedPenalty = float(speedPenalty) * (-20)
minAcceleration = float(minAcceleration) * 200
swerveForce = float(swerveForce)

while True:
    # Leer el input
    checkpoint_index, x, y, vx, vy, angle = [int(i) for i in input().split()]
    
    # Calcular distancias de la vaina al checkpoint
    cx = checkpoints[checkpoint_index][0]
    cy = checkpoints[checkpoint_index][1]
    dx = abs(x - cx)
    dy = abs(y - cy)
    
    distance = math.sqrt((cx - x)**2 + (cy - y)**2)
    bestAngle = math.acos((cx - x) / distance) * 180 / math.pi
    # First quadrant
    if 0 <= bestAngle and bestAngle <= 90 and cy - y < 0:
        bestAngle = 360 - bestAngle
    # Second quadrant
    if 90 < bestAngle and bestAngle <= 180 and cy - y < 0:
        bestAngle = 180 + (180 - bestAngle)

    angleCorrection = bestAngle - angle
    if angleCorrection > 180:
        angleCorrection -= 360
    if angleCorrection < -180:
        angleCorrection += 360
    thrustAngle = angle + swerveForce * (angleCorrection)
    thrustAngle *= math.pi / 180

    acc = distanceBonus * ((180 - abs(angleCorrection)) / 180) * math.sqrt(dx * dx + dy * dy) / 100 + speedPenalty * math.sqrt(vx * vx + vy * vy) / 10
    if acc < minAcceleration:
        acc = minAcceleration
    if acc > 200:
        acc = 200

    print(str(x + int(100 * math.cos(thrustAngle))) + " " + str(y + int(100 * math.sin(thrustAngle))) + " " + str(int(acc)) + " message")