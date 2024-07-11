import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
G, M = 6.67430e-11, 1.989e30  # Gravitational constant and solar mass in kg

# Solar properties
Rs = 696340e3  # in meters
Ts = 6000  # in Kelvin

# Parameters for planets (semi-major axis, eccentricity, color, size factor)
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

# Orbital period for each planet
T = {planet: 2 * np.pi * np.sqrt(a**3 / (G * M)) for planet, (a, _, _, _, _) in params.items()}

# Function to calculate initial velocity
def v(a, planet):
    return 2 * np.pi * a / T[planet]

# Add this constant for the precession of Mercury's perihelion
precession_mercury = 1e-7

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
initial_conditions = {planet: [a * (1 - e), 0, 0, v(a, planet) * np.sqrt((1 + e) / (1 - e))] for planet, (a, e, _, _, _) in params.items()}

# Time interval
t_values = np.arange(0, 2 * T['Neptune'], 100000)  # One orbital period

# Solve the ODE for each planet
solutions = {planet: odeint(equation, initial_conditions[planet], t_values, args=(planet,)) for planet in params}

# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_xlim(-1.1 * params['Neptune'][0] / (1 - params['Neptune'][1]), 1.1 * params['Neptune'][0] / (1 - params['Neptune'][1]))
ax.set_ylim(-1.1 * params['Neptune'][0] / (1 - params['Neptune'][1]), 1.1 * params['Neptune'][0] / (1 - params['Neptune'][1]))

# Represent the Sun as a yellow point and scale it
sun = ax.scatter(0, 0, color='yellow', s=400)

lines, planets, trails = [], [], []

# Create trajectories for each planet
for planet in params:
    size_factor = params[planet][3]
    line, = ax.plot([], [], lw=1, color=params[planet][2])
    planet_point, = ax.plot([], [], 'o', markersize=8 * size_factor, color=params[planet][2])
    trail, = ax.plot([], [], '-', lw=1, alpha=0.3, color=params[planet][2])
    lines.append(line)
    planets.append(planet_point)
    trails.append(trail)

# Add text for the timer
time_text = ax.text(0.73, 0.95, '', transform=ax.transAxes, color='white', fontsize = 11)

# Add text for the period, velocity, and distance display
info_text = ax.text(0.02, 0.82, '', transform=ax.transAxes, color='white', fontsize = 12)

# Add text for the Sun information
sun_info_text = ax.text(0.02, 0.96, '', transform=ax.transAxes, color='white', fontsize = 12)

# Store current hover state
hovered_planet = None

def init():
    for line, planet_point, trail in zip(lines, planets, trails):
        line.set_data([], [])
        planet_point.set_data([], [])
        trail.set_data([], [])
    time_text.set_text('')
    info_text.set_text('')
    sun_info_text.set_text('')
    info_text.set_visible(False)
    sun_info_text.set_visible(False)
    return lines + planets + trails + [sun, time_text, info_text, sun_info_text]

def animate(i):
    global hovered_planet
    
    for (planet, solution, line, planet_point, trail) in zip(params, solutions.values(), lines, planets, trails):
        x = solution[i, 0]
        y = solution[i, 1]
        vx = solution[i, 2]
        vy = solution[i, 3]
        r = np.sqrt(x**2 + y**2)
        v_inst = np.sqrt(vx**2 + vy**2)
        d_UA = r / 150e9
        
        line.set_data(solution[:i, 0], solution[:i, 1])
        planet_point.set_data(x, y)
        trail.set_data(solution[:i, 0], solution[:i, 1])
        
        # Store the current velocity and distance in the planet_point object for hover display
        planet_point.velocity = v_inst
        planet_point.distance = r

        if hovered_planet == planet:
            period_years = T[planet] / (365.25 * 24 * 60 * 60)  # Convert period to years
            period_days = T[planet] / (24 * 60 * 60)  # Convert period to days
            velocity = v_inst / 1000  # Convert velocity to km/s
            BB_TK = np.sqrt(Rs/(2*r))*Ts
            BB_TC = BB_TK-273.15
            Mass = params[planet][-1]
            M_ⴲ = params['Earth'][-1]
            Relative_Mass = Mass/M_ⴲ

            # Convert distance to millions or billions of kilometers
            if r >= 1e12:
                distance = r / 1e12  # Convert distance to billions of kilometers
                distance_unit = '$\\times 10^9$ km'
            else:
                distance = r / 1e9  # Convert distance to millions of kilometers
                distance_unit = '$\\times 10^6$ km'
                
            if 1e23<=Mass and Mass<1e24:
                Mass = Mass/1e23
                Mass_unit = '$\\times 10^{23}$ kg'
                
            elif 1e24<=Mass and Mass<1e25:
                Mass = Mass/1e24
                Mass_unit = '$\\times 10^{24}$ kg'
                
            elif 1e25<=Mass and Mass<1e26:
                Mass = Mass/1e25
                Mass_unit = '$\\times 10^{25}$ kg'
                
            elif 1e26<=Mass and Mass<1e27:
                Mass = Mass/1e26
                Mass_unit = '$\\times 10^{26}$ kg'
                
            elif 1e27<=Mass and Mass<1e28:
                Mass = Mass/1e27
                Mass_unit = '$\\times 10^{27}$ kg'
            
            
            info_text.set_text(f'{planet}\n'
                               f'Orbital period : {period_years:.2f} years ({period_days:.2f} days)\n'
                               f'Orbital velocity : {velocity:.2f} km/s\n'
                               f'Distance : {distance:.2f} {distance_unit} ({d_UA:.2f} UA)\n'
                               f'Black Body Temperature : {BB_TK:.2f} K  ({BB_TC:.2f} °C)\n'
                               f'Mass : {Mass:.2f} {Mass_unit} ({Relative_Mass:.2f} $M_\\oplus$)'
                               )
            info_text.set_visible(True)

    sun.set_offsets([0, 0])

    # Update time in years
    years_elapsed = t_values[i] / (365.25 * 24 * 60 * 60)  # Convert to years
    time_text.set_text(f'Time elapsed: {years_elapsed:.2f} years')
    
    return lines + planets + trails + [sun, time_text, info_text, sun_info_text]

def on_hover(event):
    global hovered_planet
    if event.inaxes == ax:
        for planet, (line, planet_point, _) in zip(params, zip(lines, planets, trails)):
            if line.contains(event)[0] or planet_point.contains(event)[0]:
                hovered_planet = planet
                return
        
        # Check if hovering over the Sun
        if sun.contains(event)[0]:
            Unit = '$\\times 10^{30}$ kg'
            hovered_planet = 'Sun'
            info_text.set_text(f'Sun:\n'
                               f'Radius : {Rs / 1e6:.1f} $\\times 10^3 km$ \n' 
                               f'Temperature : {Ts} K \n'
                               f'Mass : {M / 1e30:.3f} {Unit}')
            info_text.set_visible(True)
            return
        
        hovered_planet = None
        info_text.set_visible(False)  # Hide the info text if not hovering over any planet or line

# Create the animation
ani = FuncAnimation(fig, animate, init_func=init, frames=len(t_values), blit=True, interval=1)

# Connect the hover event
fig.canvas.mpl_connect('motion_notify_event', on_hover)

# Display the animation
plt.title("Planetary Motion around the Sun")
plt.gca().set_aspect('equal', adjustable='box')
ax.set_facecolor('black')
ax.grid(False)
plt.show()
                                                            