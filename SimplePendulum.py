from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

lamb = 10 #The reciprocal of the Poisson rate
num_jolts = 20

#Create random
rg = np.random.default_rng()
jt = rg.exponential(lamb, num_jolts)

G = 9.8  # acceleration due to gravity, in m/s^2
L = 15.0  # length of pendulum in m
U = 0 #air resistance
def der_state(state, t):

    der = np.zeros_like(state)
    der[0] = state[1]

    der[1] = -U*state[1]-G/L *sin(state[0])
    return der

# create a time array from 0..100 sampled at dt second steps
dt = 0.025
t = np.arange(0, 100, dt) #Creates array from initial to final (dt = steps)

th = 0
w = 1.61658 #Critical Value

# initial state (converts degrees to radians)
state = [th, w]

# integrate your ODE using scipy.integrate.
y = integrate.odeint(der_state, state, t)


x1 = L*sin(y[:, 0])
y1 = -L*cos(y[:, 0])

map_size = 1.1 * (L)

fig = plt.figure()
ax = fig.add_subplot(111, xlim=(-(map_size), map_size), ylim=(-(map_size), map_size), ylabel = "y", xlabel = 'x', title = 'Pendulum')
ax.set_aspect('equal')


line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.001fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


def animate(i):
    thisx = [0, x1[i]]
    thisy = [0, y1[i]]

    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
    return line, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
                              interval=dt*500, blit=True, init_func=init)

plt.show()