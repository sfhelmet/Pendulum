from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 2.5  # length of pendulum 1 in m
L2 = 2.5  # length of pendulum 2 in m
M1 = 2  # mass of pendulum 1 in kg
M2 = 2  # mass of pendulum 2 in kg

# Creating a method that returns an array as [w1, a1, w2, a2]
def der_state(state, t):

    der = np.zeros_like(state)
    der[0] = state[1]

    delta = state[2] - state[0]
    den1 = (2*M1+M2) * L1 - M2 * L1 * cos(delta) * cos(delta)
    der[1] = ((2*M2 * L1 * state[1] * state[1] * sin(delta) * cos(delta)
                + M2 * G * sin(state[2]) * cos(delta)
                + M2 * L2 * state[3] * state[3] * sin(delta)
                - (M1+M2) * G * sin(state[0]))
               / den1)

    der[2] = state[3]

    den2 = (L2/L1) * den1
    der[3] = ((- M2 * L2 * state[3] * state[3] * sin(delta) * cos(delta)
                + (M1+M2) * G * sin(state[0]) * cos(delta)
                - (M1+M2) * L1 * state[1] * state[1] * sin(delta)
                - (M1+M2) * G * sin(state[2]))
               / den2)

    return der

# create a time array from 0..100 sampled at dt second steps
dt = 0.025
t = np.arange(0, 100, dt) #Creates array from initial to final (dt = steps)

#in rad and rad/s
th1 = np.pi/2
w1 = 0
th2 = np.pi /4
w2 = 0

# an array of all initial conditions above
state = [th1, w1, th2, w2]

# solving the solution using odeint
y = integrate.odeint(der_state, state, t)

# Finding position coordinates using L and angles
x1 = L1*sin(y[:, 0])
y1 = -L1*cos(y[:, 0])

x2 = L2*sin(y[:, 2]) + x1
y2 = -L2*cos(y[:, 2]) + y1

# Window size set to 10% more than pendulum's length
map_size = 1.1 * (L1 + L2)

fig = plt.figure()
ax = fig.add_subplot(111, xlim=(-(map_size), map_size), ylim=(-(map_size), map_size), ylabel = "y", xlabel = 'x', title = 'Double Pendulum')
ax.set_aspect('equal')


line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.001fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

# Time
def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text

# Animations
def animate(i):
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]

    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
    return line, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
                              interval=dt*500, blit=True, init_func=init)

plt.show()