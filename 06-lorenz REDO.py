import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation


plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'

FIGSIZE = (16,9)
DPI = 120   # 240 For 4K, 80 for 720p

T = 200
SUBSAMPLING = 5


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

t2 = np.arange(94.6,T,dt)
state2=[np.round(x[9460],2),np.round(y[9460],2),np.round(z[9460],2)]
res2 = integrate.odeint(derivs, state2, t2)

x2, y2, z2 = np.copy(x), np.copy(y), np.copy(z)

x2[9460:] = res2[:,0]
y2[9460:] = res2[:,1]
z2[9460:] = res2[:,2]


###############################################################################
#SUB = range(9000,12000)
#fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
#fig.add_subplot(311)
#plt.plot(t[SUB],x[SUB], '-k', lw=1)
#plt.plot(t[SUB],x2[SUB], '-r', lw=1)
#fig.add_subplot(312)
#plt.plot(t[SUB],y[SUB], '-k', lw=1)
#plt.plot(t[SUB],y2[SUB], '-r', lw=1)
#fig.add_subplot(313)
#plt.plot(t[SUB],z[SUB], '-k', lw=1)
#plt.plot(t[SUB],z2[SUB], '-r', lw=1)

####################################################################################

SUB = range(9000,11000)
SUB2 = range(9460,11000)
fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
fig.add_subplot(311)
plt.plot(t[SUB],x[SUB], '-', color='darkred', lw=1)
line1, = plt.plot(t[SUB],x2[SUB], '-', color='tomato', lw=1)
ball1, = plt.plot(t[9460],x[9460],'or')
fig.add_subplot(312)
plt.plot(t[SUB],y[SUB], '-', color='darkblue', lw=1)
line2, = plt.plot(t[SUB],y2[SUB], '-', color='dodgerblue', lw=1)
ball2, = plt.plot(t[9460],y[9460],'ob')
fig.add_subplot(313)
plt.plot(t[SUB],z[SUB], '-', color='darkgreen', lw=1)
line3, = plt.plot(t[SUB],z2[SUB], '-', color='limegreen', lw=1)
ball3, = plt.plot(t[9460],z[9460],'og')


def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    return line1, line2, line3


def animate(i):
    print("Computing frame",i)
    line1.set_data(t[SUB2[:i*SUBSAMPLING]],x2[SUB2[:i*SUBSAMPLING]])
    line2.set_data(t[SUB2[:i*SUBSAMPLING]],y2[SUB2[:i*SUBSAMPLING]])
    line3.set_data(t[SUB2[:i*SUBSAMPLING]],z2[SUB2[:i*SUBSAMPLING]])
    ball1.set_data(t[SUB2[i*SUBSAMPLING]],x2[SUB2[i*SUBSAMPLING]])
    ball2.set_data(t[SUB2[i*SUBSAMPLING]],y2[SUB2[i*SUBSAMPLING]])
    ball3.set_data(t[SUB2[i*SUBSAMPLING]],z2[SUB2[i*SUBSAMPLING]])
    return line1, line2, line3, ball1, ball2, ball3

NFRAMES = int(np.floor(len(SUB2)/SUBSAMPLING))

ani = animation.FuncAnimation(fig, animate, np.arange(0, NFRAMES),init_func = init,
                              interval=33, blit=True)
writer = animation.FFMpegWriter(fps=30, bitrate=5000)

ani.save('06-lorenzREDO.mp4', writer = writer, dpi=DPI)
plt.show()
