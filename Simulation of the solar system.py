import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
G, M = 6.67430e-11, 1.989e30  # Gravitational constant and solar mass in kg

# Parameters for planets (semi-major axis, eccentricity, color)
params = {
    'Mercury': (57.91e9, 0.2056, 'gray', 0.13),
    'Venus': (108.2e9, 0.0068, 'yellow', 0.5),
    'Earth': (1.496e11, 0.0167, 'royalblue', 0.5),
    'Mars': (227.9e9, 0.0934, 'red', 0.4),
    'Jupiter': (778.3e9, 0.049, 'orange', 1.5),
    'Saturn': (1.42e12, 0.056, 'gold', 1.3),
    'Uranus': (2.87e12, 0.046, 'lightseagreen', 0.8),
    'Neptune': (4.5e12, 0.010, 'blue', 0.8)
}

# Orbital period for each planet
T = {planet: 2 * np.pi * np.sqrt(a**3 / (G * M)) for planet, (a, _, _, _) in params.items()}

# Function to calculate initial velocity
def v(a, planet):
    return 2 * np.pi * a / T[planet]

# Add this constant for the precession of Mercury's perihelion
precession_mercury = 0.0000001

# Modify the equation function
def equation(r, t, planet):
    x, y, vx, vy = r
    R = np.sqrt(x**2 + y**2)
    dvxdt = -G * M * x / R**3
    dvydt = -G * M * y / R**3

    # Add precession of the perihelion for Mercury
    if planet == 'Mercury':
        dvxdt += precession_mercury * vy
        dvydt += -precession_mercury * vx

    return [vx, vy, dvxdt, dvydt]

# Initial conditions
initial_conditions = {planet: [a * (1 - e), 0, 0, v(a, planet)] for planet, (a, e, _, _) in params.items()}

# Time interval
t_values = np.arange(0, T['Neptune'], 100000)  # One orbital period

# Solve the ODE for each planet
solutions = {planet: odeint(equation, initial_conditions[planet], t_values, args=(planet,)) for planet in params}

# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_xlim(-1.1 * params['Neptune'][0], 1.1 * params['Neptune'][0])
ax.set_ylim(-1.1 * params['Neptune'][0], 1.1 * params['Neptune'][0])

# Represent the Sun as a yellow point and scale it
sun = ax.scatter(0, 0, color='yellow', s=400)

lines, planets, trails = [], [], []

# Create trajectories for each planet
for planet in params:
    size_factor = params[planet][3]
    line, = ax.plot([], [], lw=2, color=params[planet][2])
    planet_point, = ax.plot([], [], 'o', markersize=8 * size_factor, color=params[planet][2])
    trail, = ax.plot([], [], '-', lw=1, alpha=0.3, color=params[planet][2])
    lines.append(line)
    planets.append(planet_point)
    trails.append(trail)

# Add text for the timer
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white')

def init():
    for line, planet_point, trail in zip(lines, planets, trails):
        line.set_data([], [])
        planet_point.set_data([], [])
        trail.set_data([], [])
    time_text.set_text('')
    return lines + planets + trails + [sun, time_text]

def animate(i):
    for (planet, solution, line, planet_point, trail) in zip(params, solutions.values(), lines, planets, trails):
        x = solution[i, 0]
        y = solution[i, 1]
        line.set_data(x, y)
        planet_point.set_data(x, y)
        trail.set_data(solution[:i, 0], solution[:i, 1])
    sun.set_offsets([0, 0])

    # Update time in years
    years_elapsed = t_values[i] / (365.25 * 24 * 60 * 60)  # Convert to years
    time_text.set_text(f'Time elapsed: {years_elapsed:.2f} years')
    
    return lines + planets + trails + [sun, time_text]

# Create the animation
ani = FuncAnimation(fig, animate, init_func=init, frames=len(t_values), blit=True, interval=1)

# Display the animation
plt.title("Planetary Motion around the Sun")
plt.gca().set_aspect('equal', adjustable='box')
ax.set_facecolor('black')
ax.grid(False)
plt.show()
