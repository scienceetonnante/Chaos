import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3

plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'

FIGSIZE = (16,9)
DPI = 120  # 240 For 4K, 60 for 720p

T = 30

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
#init_state_list = []
init_state_list = [[-5, 5, 5],[10, 10, 10],[-10,10,10],[10,-10,-10],[-10,-10,10],
                   [3, 2, 1], [-8,1,-3]]
cols= ['lime','red','dodgerblue','green','darkorange','cyan','yellow']

# integration
res_list = [integrate.odeint(derivs, init_state, t) for init_state in init_state_list]

###############################################################################

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
ax = p3.Axes3D(fig)
ax.set_axis_bgcolor('black')
ax.w_xaxis.set_pane_color((0,0,0,0))
ax.w_yaxis.set_pane_color((0,0,0,0))
ax.w_zaxis.set_pane_color((0,0,0,0))
ax.set_xlim3d([-20, 20])
ax.set_ylim3d([-20, 20])
ax.set_zlim3d([15, 40])
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.grid(True)
ax.view_init(azim=-30,elev=40)

lines = [plt.plot(res[100:,0],res[100:,1],res[100:,2], '-', color=col, lw=1) for (res, col) in zip(res_list,cols)]
plt.savefig("vignette.png")
plt.show()