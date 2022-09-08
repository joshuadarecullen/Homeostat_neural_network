import matplotlib.pyplot as plt
import sys
sys.path.insert(1, '../../..')
from situsim_v1_2 import *

m1 = Motor(max_speed=2)
m2 = Motor(max_speed=2, motor_inertia_coeff=100)
m3 = Motor(max_speed=2, motor_inertia_coeff=1000, reversed=True)
m4 = Motor(max_speed=20, motor_inertia_coeff=1000, reversed=True)

motors = [m1, m2, m3, m4]

t = 0
ts = [t]
delta_t = 0.01

speed_command = 1
speed_commands = [speed_command]

while t < 100:

    if t > 10:
        speed_command = 3
    if t > 40:
        speed_command = -1.5
    if t > 70:
        speed_command = -10

    speed_commands.append(speed_command)

    for motor in motors:
        motor.step(speed_command, delta_t)

    t += delta_t
    ts.append(t)

plt.figure()
for i, motor in enumerate(motors):
    plt.plot(ts, motor.speeds,label='m' + str(i+1))
plt.plot(ts, speed_commands, '--', label='speed command')
plt.legend()
plt.show()
