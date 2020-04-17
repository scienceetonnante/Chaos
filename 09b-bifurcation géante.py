import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'
FIGSIZE = (16,9)
DPI = 1200   # 240 For 4K, 80 for 720p


def simulogi(x0,N,R):
    f = lambda x: R*x*(1-x)
    x = np.zeros(N)
    x[0] = x0
    for i in range(1,N):
        x[i]=f(x[i-1])
    return x


N = 600
Imin = 200  # plot starting at this iteration
x0= 0.37
rlist = np.arange(1,4,0.0001)

rs = []
xs = []

for r in rlist:
    rs.append([r]*(N-Imin))
    xs.append(simulogi(x0,N,r)[Imin:])


fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
#lines = [plt.plot([r]*(N-Imin),x[Imin:],'.k',markersize=1) for x,r in zip(res,rlist)]
plt.plot(rs,xs,'.k',markersize=0.2)
plt.tight_layout()
plt.savefig("09b-bifurcation_géante.png")

#def init():
#    for line,x in zip(lines,res):
#        line.set_data([],[])
#    return lines
#
#
#def animate(i):
#    print("Computing frame",i)
#    for line,x in zip(lines,res):
#        line.set_data(np.arange(i),x[:i])
#    return lines
#
#ani = animation.FuncAnimation(fig, animate, np.arange(0, N),init_func = init,blit=False)
#writer = animation.FFMpegWriter(fps=5, bitrate=5000)
#ani.save('08-logistique_R3.56o.mp4', writer = writer, dpi=DPI)
#plt.show()