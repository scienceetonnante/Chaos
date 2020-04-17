import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'
FIGSIZE = (16,9)
DPI = 120   # 240 For 4K, 80 for 720p

# 2 15 2
# 1.6 15 2
# 2.8 25 2


R = 3.5
N = 70
FPS = 5

f = lambda x: R*x*(1-x)

def simulogi(x0,N):
    x = np.zeros(N)
    x[0] = x0
    for i in range(1,N):
        x[i]=f(x[i-1])
    return x




x0list = [0.37,0.55,0.12,0.97,0.04,0.78]
res = [simulogi(x0,N) for x0 in x0list]



fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
lines = [plt.plot(x,'o--')[0] for x in res]
plt.tight_layout()

def init():
    for line,x in zip(lines,res):
        line.set_data([],[])
    return lines


def animate(i):
    print("Computing frame",i)
    for line,x in zip(lines,res):
        line.set_data(np.arange(i),x[:i])
    return lines

ani = animation.FuncAnimation(fig, animate, np.arange(0, N),init_func = init,blit=False)
writer = animation.FFMpegWriter(fps=FPS, bitrate=5000)
ani.save('08-logistique_R3.5.mp4', writer = writer, dpi=DPI)

plt.show()