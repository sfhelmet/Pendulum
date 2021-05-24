from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

U = 0.1
G = 9.8
L = 15
    
def der_state(state, t):
    der = np.zeros_like(state)
    der[0] = state[1]

    der[1] = -U*state[1]-G/L * sin(state[0])
    return der


y1 = np.linspace(-3.0, 9.0, 20)
y2 = np.linspace(-2.0, 2.5, 40)

Y1, Y2 = np.meshgrid(y1, y2)

t = 0

u, v = np.zeros(Y1.shape), np.zeros(Y2.shape)

NI, NJ = Y1.shape

for i in range(NI):
    for j in range(NJ):
        x = Y1[i, j]
        y = Y2[i, j]
        yprime = der_state([x, y], t)
        u[i, j] = yprime[0]
        v[i, j] = yprime[1]

Q = plt.quiver(Y1, Y2, u, v, color='g')

plt.xlabel('$θ$ (rad)')
plt.ylabel("$θ'$ (rad/s)")
plt.xlim([-3, 9])
plt.ylim([-2, 2.5])

#Initial values
y10 = np.arange(0,2.5,0.5)
for y20 in y10:
    tspan = np.linspace(0, 100, 2000)
    y0 = [0.0, y20]
    ys = odeint(der_state, y0, tspan)
    plt.plot(ys[:, 0], ys[:, 1], 'b-')  # path
    plt.plot([ys[0, 0]], [ys[0, 1]], 'o')  # start

plt.title("Pendulum Phase portrait of  θ' vs  θ (with air resistance)")
plt.savefig('Phase Portrait + Air')
plt.show()
