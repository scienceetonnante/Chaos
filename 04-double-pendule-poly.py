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

init_state_list = [np.radians([th1, w1, th2, w2]), 
                   np.radians([th1, w1, th2 + 1, w2])]

# Integration
res_list = [integrate.odeint(derivs, init_state, t) for init_state in init_state_list]



###############################################################################

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
ax = fig.add_subplot(111)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_aspect('equal')
ax.set_xlim(-2.5,2.5)
ax.set_ylim(-2,1)
fig.tight_layout()

lines = [ax.plot(res[:,0],res[:,1], 'o-', lw=3,markersize=20)[0] for res in res_list]

def init():
    for line in lines:
        line.set_data([], [])
    return lines 


def animate(i):
    print("Computing frame",i)
    for line,res in zip(lines,res_list):
        x1, y1 = L1*sin(res[:, 0]), -L1*cos(res[:, 0])
        x2, y2 = L2*sin(res[:, 2]) + x1, -L2*cos(res[:, 2]) + y1
        line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
    return lines

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(res_list[0][:,0])),
                              interval=33, blit=True, init_func=init)
writer = animation.FFMpegWriter(fps=30, bitrate=5000)

ani.save('04-double_pendulum_poly.mp4', writer = writer)
plt.show()
