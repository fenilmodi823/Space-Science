# visualize_orbit.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from predict_orbit import read_tle, propagate_satellite
import numpy as np

def plot_orbit():
    # Read one satellite and predict orbit
    sat = read_tle()
    positions = propagate_satellite(sat)

    # Separate x, y, z
    xs = [pos[0] for pos in positions if pos[0] is not None]
    ys = [pos[1] for pos in positions if pos[1] is not None]
    zs = [pos[2] for pos in positions if pos[2] is not None]

    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(xs, ys, zs, label='Satellite Orbit', linewidth=2)

    # Draw Earth
    _draw_earth(ax)

    # Labels and title
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    ax.legend()
    plt.title("Satellite Orbit Visualization")
    plt.show()

def _draw_earth(ax):
    # Earth as a sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 6371 * np.outer(np.cos(u), np.sin(v))
    y = 6371 * np.outer(np.sin(u), np.sin(v))
    z = 6371 * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='b', alpha=0.3)

if __name__ == "__main__":
    plot_orbit()
