
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'
FIGSIZE = (16,9)
DPI = 120   # 240 For 4K, 120 for 1080p, 80 for 720p


###############################################################################

''' Parameters & Differential equation '''

g = 9.8
L = 1

def derivs(state, t):
    
    res = np.zeros_like(state) # theta omega
    
    res[0] = state[1] 
    res[1] = -g/L*sin(state[0])

    return res

###############################################################################

# Time range
dt = 0.033
t = np.arange(0.0, 12, dt)

# initial state
th = 81*3.14/180
omega = 0
state = [th, omega]

# integration
res = integrate.odeint(derivs, state, t)
x, y = L*sin(res[:, 0]), -L*cos(res[:, 0])

###############################################################################

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
ax = fig.add_subplot(111)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_aspect('equal')
ax.set_xlim(-1.5,1.5)
ax.set_ylim(-1.4,0.1)
fig.tight_layout()

###############################################################################

#ax.plot(x,y, '-', lw=1)
#ax.plot([0,x[0]],[0,y[0]],'-o')
#plt.tight_layout()
#plt.savefig("01-pendule_80.png")

###############################################################################

line, = ax.plot([],[], '-', lw=1)
ball, = ax.plot([0,x[0]],[0,y[0]],'-o',lw=3,markersize=20)

time_template = 't = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    time_text.set_text('')
    ball.set_data(x[0],y[0])
    return line, time_text


def animate(i):
    print("Computing frame",i)
    line.set_data(x[:i], y[:i])
    ball.set_data([0,x[i]],[0,y[i]])
    time_text.set_text(time_template % (i*dt))
    return line, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
                              interval=33, blit=True, init_func=init)
writer = animation.FFMpegWriter(fps=30, bitrate=5000)

ani.save('01-pendule_81.mp4', writer = writer)
plt.show()
