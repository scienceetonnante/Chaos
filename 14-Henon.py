import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'
FIGSIZE = (16,9)
DPI = 120   # 240 For 4K, 80 for 720p

a, b = 1.4, 0.3

def simuHenon(x0,y0,N):
    f = lambda x,y: (1-a*x**2+y, b*x)
    x,y = np.zeros(N), np.zeros(N)
    x[0], y[0] = x0, y0
    for i in range(1,N):
        x[i], y[i] = f(x[i-1], y[i-1])
    return x,y

N = 10000000

x0, y0 = 0.2, 0.2
x, y = simuHenon(x0,y0, N)

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
ax = fig.add_subplot(111)
plt.rc('font',size=20)
plt.tight_layout()
ax.plot(x,y,'.',markersize=1)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

xc1, yc1 = 0, 0
xc2, yc2 = 0.5, 0.2089
s1 = 0.8
s2 = 0.0001

#ax.set_xlim([xc2-(16/9)*s2,xc2+(16/9)*s2])
#ax.set_ylim([yc2-s2,yc2+s2])
#plt.show()






NSTEP = 1000


def init():
    return

def animate(i):
    print("Computing frame",i)
    
    alpha = (i/(NSTEP-1))**0.05
    
    xc = xc1 + alpha*(xc2-xc1)
    yc = yc1 + alpha*(yc2-yc1)
    s = s1 + alpha*(s2-s1)
    xmin, xmax = xc - (16/9)*s, xc + (16./9.)*s
    ymin, ymax = yc - s, yc + s
    
    print(xmin,xmax,ymin,ymax)
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    
    return


ani = animation.FuncAnimation(fig, animate, np.arange(0, NSTEP),blit=False)
writer = animation.FFMpegWriter(fps=30, bitrate=5000)

ani.save('14-henon zoom.mp4', writer = writer, dpi=DPI)