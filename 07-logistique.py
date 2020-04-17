import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'
FIGSIZE = (16,9)
DPI = 120   # 240 For 4K, 80 for 720p


f = lambda x: 4*x*(1-x)

def simulogi(x0,N):
    x = np.zeros(N)
    x[0] = x0
    for i in range(1,N):
        x[i]=f(x[i-1])
    return x



epsilon = 0.000000001
K = 100
N = 40

x0A = 0.37
x0listA = np.linspace(x0A-epsilon,x0A+epsilon,K) 
resA = [simulogi(x0,N) for x0 in x0listA]

x0B = 0.55
x0listB = np.linspace(x0B-epsilon,x0B+epsilon,K) 
resB = [simulogi(x0,N) for x0 in x0listB]

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
linesA = [plt.plot(x,'k')[0] for x in resA]
linesB = [plt.plot(x,'r')[0] for x in resB]
plt.tight_layout()
plt.savefig("07-logistique mixing.png")

#fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
#linesA = [plt.plot(x,'k')[0] for x in resA]
#linesB = [plt.plot(x,'r')[0] for x in resB]
#
#def init():
#    for lineA,xA in zip(linesA,resA):
#        lineA.set_data([],[])
#    for lineB,xB in zip(linesB,resB):
#        lineB.set_data([],[])
#    return linesA, linesB
#
#
#def animate(i):
#    print("Computing frame",i)
#    for lineA,xA in zip(linesA,resA):
#        lineA.set_data(np.arange(i),xA[:i])
#    for lineB,xB in zip(linesB,resB):
#        lineB.set_data(np.arange(i),xB[:i])
#    return linesA, linesB
#
#ani = animation.FuncAnimation(fig, animate, np.arange(0, N),init_func = init,
#                              interval=33, blit=False)
#writer = animation.FFMpegWriter(fps=30, bitrate=5000)
#
#ani.save('07-logistique_mixing.mp4', writer = writer, dpi=DPI)
#plt.show()