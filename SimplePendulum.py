from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

G = 9.8  # acceleration due to gravity, in m/s^2
L = 15.0  # length of pendulum in m
U = 0 # air resistance

# Creating a method that returns an array as [w, a]
def der_state(state, t):

    der = np.zeros_like(state)
    der[0] = state[1] # angular velocity

    der[1] = -U*state[1]-G/L *sin(state[0]) # angular acceleration
    return der

# create a time array from 0..100 sampled at dt second steps
dt = 0.025
t = np.arange(0, 100, dt) #Creates array from initial to final (dt = steps)

#in rad and rad/s
th = 0
w = 1.61658 #Critical Value

# an array of all initial conditions above
state = [th, w]

# solving the solution using odeint
y = integrate.odeint(der_state, state, t)

# Finding position coordinates using L and angles
x1 = L*sin(y[:, 0])
y1 = -L*cos(y[:, 0])

# Window size set to 10% more than pendulum's length
map_size = 1.1 * (L)

fig = plt.figure()
ax = fig.add_subplot(111, xlim=(-(map_size), map_size), ylim=(-(map_size), map_size), ylabel = "y", xlabel = 'x', title = 'Pendulum')
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
    thisx = [0, x1[i]]
    thisy = [0, y1[i]]

    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
    return line, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
                              interval=dt*500, blit=True, init_func=init)

plt.show()
