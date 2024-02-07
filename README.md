# Solar-System
2D Simulation of the Solar System by numerically solving the equations of motion for the planets.

To simulate the planets' motion, we first need to find the equation of motion and solve it.
We could directly use the Keplerian solution of the motion but i'd rather use a numerical method and considering the precession of Mercury's perihelion

The equation of motion is given with Newton's second law : $\displaystyle \sum_{k} \vec{F}_k = m\vec{a}$ where $\displaystyle \sum_{k} \vec{F}_k = G \frac{Mm}{r^3} \vec{r}$.
In cartesian coordinates, the equation becomes 2 equations :

 - $\displaystyle \frac{dv_x}{dt} = -GM \frac{x}{r^3}$
 - $\displaystyle \frac{dv_y}{dt} = -GM \frac{y}{r^3}$

where $\displaystyle \frac{dv_x}{dt} = \frac{d^2x}{dt^2}$, $\displaystyle \frac{dv_y}{dt} = \frac{d^2y}{dt^2}$ and $r = \sqrt(x^2 + y^2)$ which is the radial distance between the planet and the star.

