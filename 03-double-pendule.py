from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'
FIGSIZE = (16,9)
DPI = 120   # 240 For 4K, 120 for 1080p, 80 for 720p

G = 9.8  
L1, L2 = 1.0, 0.8
M1, M2 = 1.2, 1.0

def derivs(state, t):
    
    # http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c

    res = np.zeros_like(state)
    res[0] = state[1]

    del_ = state[2] - state[0]
    den1 = (M1 + M2)*L1 - M2*L1*cos(del_)*cos(del_)
    res[1] = (M2*L1*state[1]*state[1]*sin(del_)*cos(del_) +
               M2*G*sin(state[2])*cos(del_) +
               M2*L2*state[3]*state[3]*sin(del_) -
               (M1 + M2)*G*sin(state[0]))/den1

    res[2] = state[3]
    den2 = (L2/L1)*den1
    res[3] = (-M2*L2*state[3]*state[3]*sin(del_)*cos(del_) +
               (M1 + M2)*G*sin(state[0])*cos(del_) -
               (M1 + M2)*L1*state[1]*state[1]*sin(del_) -
               (M1 + M2)*G*sin(state[2]))/den2

    return res

dt = 0.033
t = np.arange(0.0, 20, dt)

# initial state : angles (degrees) and angular velocities (degrees per second)
th1 = 120.0
w1 = 0.0
th2 = -10.0
w2 = 0.0
state = np.radians([th1, w1, th2, w2])

# Integration
res = integrate.odeint(derivs, state, t)
x1, y1 = L1*sin(res[:, 0]), -L1*cos(res[:, 0])
x2, y2 = L2*sin(res[:, 2]) + x1, -L2*cos(res[:, 2]) + y1

###############################################################################

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
ax = fig.add_subplot(111)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_aspect('equal')
ax.set_xlim(-2.5,2.5)
ax.set_ylim(-2,1)
fig.tight_layout()


line, = ax.plot([], [], 'o-', lw=3,markersize=20)


def init():
    line.set_data([], [])
    return line,


def animate(i):
    print("Computing frame",i)
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]

    line.set_data(thisx, thisy)
    return line,

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y1)),
                              interval=33, blit=True, init_func=init)
writer = animation.FFMpegWriter(fps=30, bitrate=5000)

ani.save('03-double_pendulum_120_m10.mp4', writer = writer)
plt.show()
