import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation


plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'

FIGSIZE = (16,9)
DPI = 120   # 240 For 4K, 80 for 720p

T = 200
SUBSAMPLING = 50


###############################################################################

''' Parameters & Differential equation '''

sigma = 10
rho = 28
beta = 8/3

def derivs(state, t):
    
    x, y, z = state[0], state[1], state[2]
    res = np.zeros_like(state)
    
    res[0] = sigma * (y - x)
    res[1] = x * (rho - z) - y
    res[2] = x * y - beta * z

    return res

###############################################################################

# Time range
dt = 0.01
t = np.arange(0.0, T, dt)

# initial state
state = [0, 0.1, 0]

# integration
res = integrate.odeint(derivs, state, t)
x, y, z = res[:,0], res[:,1], res[:,2]

###############################################################################

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
fig.add_subplot(311)
plt.plot(t,x, '-r', lw=1)
fig.add_subplot(312)
plt.plot(t,y, '-b', lw=1)
fig.add_subplot(313)
plt.plot(t,z, '-g', lw=1)

###################################################################################

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
fig.add_subplot(311)
line1, = plt.plot(t,x, '-r', lw=1)
fig.add_subplot(312)
line2, = plt.plot(t,y, '-b', lw=1)
fig.add_subplot(313)
line3, = plt.plot(t,z, '-g', lw=1)


def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    return line1, line2, line3


def animate(i):
    print("Computing frame",i)
    line1.set_data(t[:i*SUBSAMPLING],x[:i*SUBSAMPLING])
    line2.set_data(t[:i*SUBSAMPLING],y[:i*SUBSAMPLING])
    line3.set_data(t[:i*SUBSAMPLING],z[:i*SUBSAMPLING])
    return line1, line2, line3

NFRAMES = int(np.floor(len(t)/SUBSAMPLING))

ani = animation.FuncAnimation(fig, animate, np.arange(1, NFRAMES),init_func = init,
                              interval=33, blit=True)
writer = animation.FFMpegWriter(fps=30, bitrate=5000)

ani.save('05-lorenzTS.mp4', writer = writer, dpi=DPI)
plt.show()
