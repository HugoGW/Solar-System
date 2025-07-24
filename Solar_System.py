import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import njit

# Constants
G = 6.67430e-11
M_sun = 1.989e30
Rs = 6.96e8
Ts = 5778

# Planets parameters: semi-major axis (m), eccentricity, color, size factor, mass (kg)
params = {
    'Mercury': (57.91e9, 0.2056, 'gray', 0.13, 3.30e23),
    'Venus': (108.2e9, 0.0068, 'yellow', 0.5, 4.87e24),
    'Earth': (1.496e11, 0.0167, 'royalblue', 0.5, 5.972e24),
    'Mars': (227.9e9, 0.0934, 'red', 0.4, 6.42e23),
    'Jupiter': (778.3e9, 0.049, 'orange', 1.5, 1.898e27),
    'Saturn': (1.42e12, 0.056, 'gold', 1.3, 5.68e26),
    'Uranus': (2.87e12, 0.046, 'lightseagreen', 0.8, 8.68e25),
    'Neptune': (4.5e12, 0.010, 'blue', 0.8, 1.02e26)
}

planet_names = list(params.keys())
masses = np.array([params[planet][4] for planet in planet_names])

T = {planet: 2 * np.pi * np.sqrt(params[planet][0]**3 / (G * M_sun)) for planet in planet_names}

def initial_velocity(a, planet):
    return 2 * np.pi * a / T[planet]

initial_conditions = []
for planet in planet_names:
    a, e, _, _, _ = params[planet]
    x0 = a * (1 - e)
    y0 = 0
    vx0 = 0
    vy0 = initial_velocity(a, planet) * np.sqrt((1 + e) / (1 - e))
    initial_conditions.extend([x0, y0, vx0, vy0])
initial_conditions = np.array(initial_conditions)

@njit
def compute_derivatives(w, t, G, M_sun, masses):
    N = len(masses)
    positions = w.reshape((N, 4))[:, :2]
    velocities = w.reshape((N, 4))[:, 2:]
    accelerations = np.zeros_like(positions)
    for i in range(N):
        r_vec = positions[i]
        r = np.linalg.norm(r_vec)
        acc_sun = -G * M_sun * r_vec / (r**3 + 1e-9)
        accelerations[i] += acc_sun
        for j in range(N):
            if i != j:
                r_ij = positions[j] - positions[i]
                dist_ij = np.linalg.norm(r_ij)
                accelerations[i] += G * masses[j] * r_ij / (dist_ij**3 + 1e-9)
    derivatives = np.zeros_like(w)
    for i in range(N):
        derivatives[4*i:4*i+2] = velocities[i]
        derivatives[4*i+2:4*i+4] = accelerations[i]
    return derivatives

def equations(w, t):
    return compute_derivatives(w, t, G, M_sun, masses)

t_values = np.arange(0, 2 * T['Neptune'], 100000)
solution = odeint(equations, initial_conditions, t_values)
positions_over_time = {planet: solution[:, 4 * i: 4 * i + 2] for i, planet in enumerate(planet_names)}
velocities_over_time = {planet: solution[:, 4 * i + 2: 4 * i + 4] for i, planet in enumerate(planet_names)}

fig, ax = plt.subplots(figsize=(12, 12))
ax.set_facecolor('black')
ax.set_aspect('equal')
limit = 1.1 * params['Neptune'][0]
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

sun, = ax.plot(0, 0, 'o', color='yellow', markersize=10)
lines = {}
points = {}
for planet in planet_names:
    color = params[planet][2]
    line, = ax.plot([], [], '-', lw=1, color=color, alpha=0.6, picker=5)
    point, = ax.plot([], [], 'o', color=color, markersize=5, picker=5)
    lines[planet] = line
    points[planet] = point

time_text = ax.text(0.73, 0.95, '', transform=ax.transAxes, color='white', fontsize=11)
info_text = ax.text(0.02, 0.82, '', transform=ax.transAxes, color='white', fontsize=12)
info_text.set_visible(False)
hovered_planet = None

def init():
    for line in lines.values():
        line.set_data([], [])
    for point in points.values():
        point.set_data([], [])
    time_text.set_text('')
    info_text.set_text('')
    info_text.set_visible(False)
    return list(lines.values()) + list(points.values()) + [sun, time_text, info_text]

def animate(i):
    global hovered_planet
    for planet in planet_names:
        pos = positions_over_time[planet]
        vel = velocities_over_time[planet]
        lines[planet].set_data(pos[:i, 0], pos[:i, 1])
        points[planet].set_data([pos[i, 0]], [pos[i, 1]])
        points[planet].velocity = np.linalg.norm(vel[i])
        points[planet].distance = np.linalg.norm(pos[i])
        if hovered_planet == planet:
            r = points[planet].distance
            v_inst = points[planet].velocity
            d_UA = r / 150e9
            period_years = T[planet] / (365.25 * 24 * 60 * 60)
            period_days = T[planet] / (24 * 60 * 60)
            velocity = v_inst / 1000
            BB_TK = np.sqrt(Rs / (2 * r)) * Ts
            BB_TC = BB_TK - 273.15
            Mass = params[planet][-1]
            M_earth = 5.972e24
            Relative_Mass = Mass / M_earth
            if r >= 1e12:
                distance = r / 1e12
                distance_unit = '$\\times 10^9$ km'
            else:
                distance = r / 1e9
                distance_unit = '$\\times 10^6$ km'
            Mass_text = f'{Mass:.2e} kg'
            info_text.set_text(f'{planet}\n'
                               f'Orbital period : {period_years:.2f} years ({period_days:.2f} days)\n'
                               f'Orbital velocity : {velocity:.2f} km/s\n'
                               f'Distance : {distance:.2f} {distance_unit} ({d_UA:.2f} UA)\n'
                               f'Black Body Temperature : {BB_TK:.2f} K ({BB_TC:.2f} °C)\n'
                               f'Mass : {Mass_text} ({Relative_Mass:.2f} $M_\\oplus$)')
            info_text.set_visible(True)
    if hovered_planet == 'Sun':
        info_text.set_visible(True)
    years_elapsed = t_values[i] / (365.25 * 24 * 60 * 60)
    time_text.set_text(f'Time elapsed: {years_elapsed:.2f} years')
    return list(lines.values()) + list(points.values()) + [sun, time_text, info_text]

def on_hover(event):
    global hovered_planet
    if event.inaxes == ax:
        if sun.contains(event)[0]:
            hovered_planet = 'Sun'
            Unit = '$\\times 10^{30}$ kg'
            info_text.set_text(f'Sun:\n'
                               f'Radius : {Rs / 1e6:.1f} $\\times 10^3$ km\n'
                               f'Temperature : {Ts} K\n'
                               f'Mass : {M_sun / 1e30:.3f} {Unit}')
            info_text.set_visible(True)
            return
        for planet in planet_names:
            contains_point, _ = points[planet].contains(event)
            contains_line, _ = lines[planet].contains(event)
            if contains_point or contains_line:
                hovered_planet = planet
                return
        hovered_planet = None
        info_text.set_visible(False)

fig.canvas.mpl_connect('motion_notify_event', on_hover)
ani = FuncAnimation(fig, animate, init_func=init, frames=len(t_values), interval=1, blit=True)
plt.show()

