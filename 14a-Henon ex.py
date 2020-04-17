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

N = 1000
SUBSAMPLING = 1

x0, y0 = -1, 0.1
x, y = simuHenon(x0, y0, N)

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
plt.rc('font', size=20)

ax = fig.add_subplot(111)
ax.set_xlim(-1.5,1.5)
ax.set_ylim(-0.4,0.4)
ax.plot(x0,y0,'o',color='red')
line, = ax.plot(x0,y0,'.',color='red')
plt.tight_layout()

def init():
    line.set_data(x0, y0)
    return line,


def animate(i):
    print("Computing frame",i)
    line.set_data(x[:i*SUBSAMPLING], y[:i*SUBSAMPLING])
    return line,


NFRAMES = int(np.ceil(N/SUBSAMPLING))
ani = animation.FuncAnimation(fig, animate, np.arange(0, NFRAMES),init_func = init,
                              blit=True)
writer = animation.FFMpegWriter(fps=30, bitrate=5000)

ani.save('14a-henon ex1.mp4', writer = writer, dpi=DPI)