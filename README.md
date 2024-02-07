# Solar-System
2D Simulation of the Solar System by numerically solving the equations of motion for the planets.

To simulate the planets' motion, we first need to find the equation of motion and solve it.
We could directly use the Keplerian solution of the motion but i'd rather use a numerical method and considering the precession of Mercury's perihelion

The equation of motion is given with Newton's second law : $\displaystyle \sum_{k} \vec{F}_k = m\vec{a}$ where $\displaystyle \sum_{k} \vec{F}_k = G \frac{Mm}{r^3} \vec{r}$.
In cartesian coordinates, the equation becomes 2 equations :

 - $\displaystyle \frac{dv_x}{dt} = -GM \frac{x}{r^3}$ where $\displaystyle \frac{dv_x}{dt} = \frac{d^2x}{dt^2}$
 - $\displaystyle \frac{dv_y}{dt} = -GM \frac{y}{r^3}$ where $\displaystyle \frac{dv_y}{dt} = \frac{d^2y}{dt^2}$

where $r = \sqrt{x^2 + y^2}$ which is the radial distance between the planet and the star.

For Mercury, the precession is $\dot{\phi} =$ 531.7 secondes d'arc/siecle ($\approx 1.5\times 10^(-15) rad/s), the system of equation becomes : 

 - $\displaystyle \frac{dv_x}{dt} = -GM \frac{x}{r^3}$ + \dot{\phi} \frac{dy}{dt}
 - $\displaystyle \frac{dv_y}{dt} = -GM \frac{y}{r^3}$ - \dot{\phi} \frac{dx}{dt}

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

Once the equation system done, I need to choose my initial condition for each planet 

