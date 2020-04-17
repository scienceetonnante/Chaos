
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'

FIGSIZE = (16,9)
DPI = 120  # 240 For 4K, 120 for 1080p, 80 for 720p

###############################################################################

''' Parameters & Differential equation '''

g = 9.8

def derivs(state, t):
    
    res = np.zeros_like(state) # x vx z vz

    # if above the floor
    if state[2]>=0: 
        res[0] = state[1] 
        res[1] = 0
        res[2] = state[3]
        res[3]= -g

    return res

###############################################################################

# Time range
dt = 0.033
t = np.arange(0.0, 8, dt)
v = 37
a1, a2 = 48,49
# initial state

init_state_list = [[0, v*cos(a1*3.14/180) ,0 , v*sin(a1*3.14/180)],
                   [0, v*cos(a2*3.14/180) ,0 , v*sin(a2*3.14/180)]]

# integration
res_list = [integrate.odeint(derivs, init_state, t) for init_state in init_state_list]

###############################################################################

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
ax = fig.add_subplot(111)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_aspect('equal')
ax.set_xlim(0,140)
ax.set_ylim(0,60)
fig.tight_layout()

#lines = [ax.plot(res[:,0],res[:,2], '-', lw=1)[0] for res in res_list]


lines = [ax.plot(res[:,0],res[:,1], '-', lw=1)[0] for res in res_list]
balls = [ax.plot(res[0:1,0],res[0:1,1], 'o', lw=1)[0] for res in res_list]

#time_template = 't = %.1fs'
#time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    for line in lines:
        line.set_data([], [])
        #time_text.set_text('')
    return lines #, time_text


def animate(i):
    print("Computing frame",i)
    for line,res,ball in zip(lines,res_list,balls):
        x, y = res[:,0], res[:,2]
        line.set_data(x[:i], y[:i])
        ball.set_data(x[i],y[i])
    #time_text.set_text(time_template % (i*dt))
    return lines #, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(res_list[0][:,0])),
                              interval=33, blit=True, init_func=init)
writer = animation.FFMpegWriter(fps=30, bitrate=5000)

ani.save('02-canon_poly.mp4', writer = writer)
plt.show()
