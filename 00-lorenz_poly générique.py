import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3

plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'

FIGSIZE = (16,9)
DPI = 120  # 240 For 4K, 60 for 720p

T = 200
SUB_SAMPLING = 10

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
init_state_list = [[-5, 5, 5],[10, 10, 10],[-10,10,10],[10,-10,-10],[-10,-10,10]]

# integration
res_list = [integrate.odeint(derivs, init_state, t) for init_state in init_state_list]

###############################################################################

#fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
#ax = fig.add_subplot(111, projection='3d')
#ax.view_init(elev=None, azim=None)
#ax.set_axis_bgcolor('black')
#ax.w_xaxis.set_pane_color((0,0,0,0))
#ax.w_yaxis.set_pane_color((0,0,0,0))
#ax.w_zaxis.set_pane_color((0,0,0,0))
#ax.set_xlim3d([-30, 30])
#ax.set_ylim3d([-30, 30])
#ax.set_zlim3d([-10, 50])
#
#lines = [plt.plot(res[:,0],res[:,1],res[:,2], '-', lw=1) for res in res_list]

###################################################################################

azim_start = -160.0
azim_end = 160.0

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
ax = p3.Axes3D(fig)
ax.set_axis_bgcolor('black')
ax.w_xaxis.set_pane_color((0,0,0,0))
ax.w_yaxis.set_pane_color((0,0,0,0))
ax.w_zaxis.set_pane_color((0,0,0,0))
ax.set_xlim3d([-30, 30])
ax.set_ylim3d([-30, 30])
ax.set_zlim3d([-10, 50])
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.grid(False)
ax.view_init(azim=azim_start)

lines = [ax.plot(res[:,0],res[:,1],res[:,2], '-', lw=1)[0] for res in res_list]
balls = [ax.plot(res[0:1,0],res[0:1,1],res[0:1,2], 'o', lw=1)[0] for res in res_list]



NB_FRAMES = int(np.floor(len(t)/SUB_SAMPLING))

def init():
    for line, ball, res in zip(lines,balls, res_list):
        x, y, z = res[:,0], res[:,1], res[:,2]
        line.set_data([], [])
        line.set_3d_properties([])
        ball.set_data(x[0],y[0])
        ball.set_3d_properties(z[0])
    return lines, balls #, time_text


def animate(i, res_list, lines):
    print("Computing frame",i)
    ax.view_init(azim=azim_start+(azim_end-azim_start)*i/NB_FRAMES)
    for line,res,ball in zip(lines,res_list,balls):
        x, y, z = res[:,0], res[:,1], res[:,2]
        line.set_data(x[:i*SUB_SAMPLING], y[:i*SUB_SAMPLING])
        line.set_3d_properties(z[:i*SUB_SAMPLING])
        ball.set_data(x[i*SUB_SAMPLING],y[i*SUB_SAMPLING])
        ball.set_3d_properties(z[i*SUB_SAMPLING])
    return lines, balls #, time_text



ani = animation.FuncAnimation(fig, animate, np.arange(1500, 2000), fargs=(res_list, lines), init_func = init,
                              interval=40, blit=False)
writer = animation.FFMpegWriter(fps=30, bitrate=5000)

ani.save('00-lorenz_poly intro.mp4', writer = writer, dpi=DPI)
plt.show()
