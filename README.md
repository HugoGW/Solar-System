# Solar-System
2D Simulation of the Solar System by numerically solving the equations of motion for the planets.

To simulate the planets' motion, we first need to find the equation of motion and solve it.
We could directly use the Keplerian solution of the motion but i'd rather use a numerical method and considering the precession of Mercury's perihelion

The equation of motion is given with Newton's second law : $\displaystyle \sum_{k} \vec{F}_k = m \vec{a}$ where $\displaystyle \sum_{k} \vec{F}_k = G \frac{Mm}{r^3} \vec{r}$.
In cartesian coordinates, the equation becomes 2 equations :

 - $\displaystyle \frac{dv_x}{dt} = -GM \frac{x}{r^3}$ where $\displaystyle \frac{dv_x}{dt} = \frac{d^2x}{dt^2}$
 - $\displaystyle \frac{dv_y}{dt} = -GM \frac{y}{r^3}$ where $\displaystyle \frac{dv_y}{dt} = \frac{d^2y}{dt^2}$

where $r = \sqrt{x^2 + y^2}$ which is the radial distance between the planet and the star.

For Mercury, the precession is $\dot{\phi} =$ 531.7 seconds of arc per century $(\approx 1.5\times 10^{-15} rad/s)$, but we'll arbitrary take $\dot{\phi} = 10^{-7} rad/s$ the system of equation becomes : 

 - $\displaystyle \frac{dv_x}{dt} = -GM \frac{x}{r^3}$ + $\displaystyle \dot{\phi} \frac{dy}{dt}$
 - $\displaystyle \frac{dv_y}{dt} = -GM \frac{y}{r^3}$ - $\displaystyle \dot{\phi} \frac{dx}{dt}$

I first need to give the differents parameters for each planet (Name, distance from the Sun, ellipticity, color and the size) :

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


Once the system of equations is defined, I need to choose the initial conditions for each planet based on the parameters. The initial conditions are determined by the initial distance, which is the semi-major axis $a(1-e)$, and the initial velocity, given by $\displaystyle v = \sqrt{\frac{GM}{a}}$.

    initial_conditions = {planet: [a * (1 - e), 0, 0, v(a, planet)] for planet, (a, e, _, _) in params.items()}

Then, we numerically solve the equations of motion for each planet using odeint from the scipy library. We create a large yellow dot representing the Sun and place it at the center of the plot.

The goal is to generate the motion of the planets and plot their trajectories to clearly observe their orbits. We also include a timer in years (based on Earth's orbit). For each time step, we plot the new position of each planet $(x=$ solution[i, 0], $y=$ solution[i, 1] $)$ and their trajectories by keeping a few points plotted during the animation.

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

We animate the motion using FuncAnimation from the matplotlib.animation library.
Here are screenshots of the simulation

<img width="441" alt="image" src="https://github.com/HugoGW/Solar-System/assets/140922475/1aa5cc5d-84fa-43ad-91c3-39e60f23185c">
<img width="430" alt="image" src="https://github.com/HugoGW/Solar-System/assets/140922475/0e627381-3d16-4abd-bafc-51fdfed01820">
<img width="505" alt="image" src="https://github.com/HugoGW/Solar-System/assets/140922475/8501f7d6-527e-4c95-84e0-b27e7086279f">





